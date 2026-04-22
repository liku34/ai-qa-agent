import ollama
import asyncio
import sys
import os

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from openai import OpenAI
import google.genai as genai

# =====================================
# FIX Windows Playwright Issue
# =====================================
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# =====================================
# HELPER: Get API Key (Streamlit Cloud + Local)
# =====================================
def get_secret(key_name):
    """Reads from Streamlit secrets (cloud) or environment variables (local)."""
    try:
        import streamlit as st
        val = st.secrets.get(key_name)
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key_name)


# =====================================
# 1️⃣ WEBSITE SCRAPER
# =====================================
def get_website_content(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3000)

            content = page.content()
            browser.close()

            soup = BeautifulSoup(content, "html.parser")

            # Remove unnecessary tags
            for tag in soup(["script", "style", "noscript", "svg", "img"]):
                tag.decompose()

            # Extract visible text
            text = soup.get_text(separator="\n", strip=True)
            clean_text = "\n".join(
                line for line in text.splitlines() if line.strip()
            )

            return clean_text[:6000]  # Limit size for LLM safety

    except Exception as e:
        return f"Error fetching website: {str(e)}"


# =====================================
# 2️⃣ MAIN ROUTER
# =====================================
def generate_test_cases(url, model_choice):

    if model_choice == "Local LLM (Ollama)":
        return generate_with_ollama(url)

    elif model_choice == "OpenAI GPT-4":
        return generate_with_openai(url)

    elif model_choice == "Gemini":
        return generate_with_gemini(url)

    else:
        return "Invalid model selected"


# =====================================
# 3️⃣ PROMPT BUILDER
# =====================================
def build_prompt(url, content):

    return f"""
You are a Senior QA Engineer with 10+ years of experience.

Analyze the following website content and generate professional, comprehensive QA test cases.

URL: {url}

STRICT RULES:
- Do NOT explain HTML or CSS
- ONLY generate test cases
- Output MUST be in markdown table format
- Generate minimum 15 test cases
- Cover: Functional, UI/UX, Edge Cases, Negative Tests, Accessibility

Required Table Columns:
| Test Case ID | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Test Type |

Priority values: High / Medium / Low
Test Type values: Functional / UI / Negative / Edge Case / Accessibility / Performance

Website Content:
{content}
"""


# =====================================
# 4️⃣ OLLAMA
# =====================================
def generate_with_ollama(url):

    try:
        content = get_website_content(url)

        if content.startswith("Error fetching"):
            return content

        prompt = build_prompt(url, content)

        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "system",
                    "content": "You generate only structured QA test cases in markdown table format. No extra explanation."
                },
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Ollama Error: {str(e)}"


# =====================================
# 5️⃣ OPENAI
# =====================================
def generate_with_openai(url):

    try:
        api_key = get_secret("OPENAI_API_KEY")
        if not api_key:
            return "OpenAI Error: OPENAI_API_KEY not set. Please add it in sidebar or .streamlit/secrets.toml"

        content = get_website_content(url)

        if content.startswith("Error fetching"):
            return content

        prompt = build_prompt(url, content)

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You generate only structured QA test cases in markdown table format. No extra explanation."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=3000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"OpenAI Error: {str(e)}"


# =====================================
# 6️⃣ GEMINI
# =====================================
def generate_with_gemini(url):

    try:
        api_key = get_secret("GEMINI_API_KEY")
        if not api_key:
            return "Gemini Error: GEMINI_API_KEY not set. Please add it in sidebar or .streamlit/secrets.toml"

        content = get_website_content(url)

        if content.startswith("Error fetching"):
            return content

        prompt = build_prompt(url, content)

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"
