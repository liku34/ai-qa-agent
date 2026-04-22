import pandas as pd
import io
import streamlit as st
import time
from agent import generate_test_cases

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="AI QA Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS — Better UI
# =====================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* Title style */
    h1 {
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 16px;
        backdrop-filter: blur(8px);
    }

    /* Input box */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(167,139,250,0.5);
        border-radius: 10px;
        color: white;
        font-size: 1rem;
        padding: 12px;
    }

    /* Generate button */
    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 40px;
        font-size: 1.1rem;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #6d28d9, #1d4ed8);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124,58,237,0.4);
    }

    /* Download button */
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(90deg, #059669, #0891b2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(90deg, #047857, #0e7490);
        transform: translateY(-2px);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15,12,41,0.95);
        border-right: 1px solid rgba(167,139,250,0.2);
    }

    /* Text area */
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: monospace;
    }

    /* Divider */
    hr {
        border-color: rgba(167,139,250,0.2) !important;
    }

    /* Success / Info / Warning / Error boxes */
    .stAlert {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)


# =====================================
# HEADER
# =====================================
st.title("🤖 AI Powered QA Test Case Generator")
st.markdown("##### Generate professional QA test cases from any website using Multiple LLMs")
st.markdown("---")

# Stats Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧠 AI Models", "3")
col2.metric("📋 Output", "Table Format")
col3.metric("📥 Export", "Excel / Copy")
col4.metric("🌐 Input", "Any Website URL")
st.markdown("---")


# =====================================
# SIDEBAR SETTINGS
# =====================================
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("---")

model_choice = st.sidebar.selectbox(
    "🧠 Select AI Model",
    ["OpenAI GPT-4", "Gemini", "Local LLM (Ollama)"]
)

st.sidebar.success(f"✅ Active: {model_choice}")
st.sidebar.markdown("---")

# Optional: In-sidebar API key inputs (for local/demo use)
if model_choice == "OpenAI GPT-4":
    st.sidebar.info("🔑 Requires: OPENAI_API_KEY")
    user_openai_key = st.sidebar.text_input(
        "Enter OpenAI API Key (optional)",
        type="password",
        placeholder="sk-..."
    )
    if user_openai_key:
        import os
        os.environ["OPENAI_API_KEY"] = user_openai_key

elif model_choice == "Gemini":
    st.sidebar.info("🔑 Requires: GEMINI_API_KEY")
    user_gemini_key = st.sidebar.text_input(
        "Enter Gemini API Key (optional)",
        type="password",
        placeholder="AI..."
    )
    if user_gemini_key:
        import os
        os.environ["GEMINI_API_KEY"] = user_gemini_key

elif model_choice == "Local LLM (Ollama)":
    st.sidebar.warning("⚠️ Requires Ollama running locally with Mistral model.")

st.sidebar.markdown("---")
st.sidebar.markdown("**How to use:**")
st.sidebar.markdown("1. Select an AI model\n2. Enter any website URL\n3. Click Generate\n4. Download as Excel")
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Subham Sahu** 🚀")


# =====================================
# MAIN INPUT SECTION
# =====================================
st.subheader("🌐 Enter Website URL")

url = st.text_input(
    "",
    placeholder="https://example.com",
    label_visibility="collapsed"
)

# URL Validation
if url and not url.startswith(("http://", "https://")):
    st.error("❌ Please enter a valid URL starting with http:// or https://")
    st.stop()

st.markdown("")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generate_btn = st.button("🚀 Generate Test Cases", use_container_width=True)


# =====================================
# GENERATE TEST CASES
# =====================================
if generate_btn:

    if not url:
        st.warning("⚠️ Please enter a website URL first.")
        st.stop()

    # Progress bar + spinner
    progress = st.progress(0, text="🔍 Starting analysis...")
    with st.spinner(""):

        progress.progress(20, text="🌐 Fetching website content...")
        time.sleep(0.5)

        progress.progress(50, text=f"🤖 Sending to {model_choice}...")
        start_time = time.time()
        result = generate_test_cases(url, model_choice)
        end_time = time.time()

        progress.progress(90, text="📋 Formatting results...")
        time.sleep(0.3)

        progress.progress(100, text="✅ Done!")
        time.sleep(0.3)

    progress.empty()

    response_time = round(end_time - start_time, 2)

    # =====================================
    # ERROR DISPLAY
    # =====================================
    if any(result.startswith(prefix) for prefix in [
        "OpenAI Error", "Gemini Error", "Ollama Error", "Error fetching"
    ]):
        st.error(f"❌ {result}")
        st.stop()

    # =====================================
    # SUCCESS DISPLAY
    # =====================================
    st.markdown("---")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.success("✅ Generated Successfully!")
    res_col2.info(f"⏱️ Time: {response_time}s")
    res_col3.info(f"🤖 Model: {model_choice}")

    st.markdown("---")
    st.subheader("📋 Generated Test Cases")

    # Display result as markdown (renders table properly)
    st.markdown(result)

    st.markdown("---")
    st.subheader("📥 Export Options")

    export_col1, export_col2 = st.columns(2)

    # =====================================
    # EXCEL EXPORT
    # =====================================
    with export_col1:
        lines = result.split("\n")
        table_lines = [line for line in lines if "|" in line and line.strip()]

        if len(table_lines) > 2:
            headers = [h.strip() for h in table_lines[0].split("|") if h.strip()]
            data = []

            for row in table_lines[2:]:  # Skip header + separator
                cols = [c.strip() for c in row.split("|") if c.strip()]
                if len(cols) == len(headers):
                    data.append(cols)

            if data:
                df = pd.DataFrame(data, columns=headers)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="TestCases")

                excel_data = output.getvalue()

                st.download_button(
                    label="📊 Download as Excel (.xlsx)",
                    data=excel_data,
                    file_name="AI_Generated_Test_Cases.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Could not parse table for Excel export.")
        else:
            st.warning("⚠️ Output not recognized as a table.")

    # =====================================
    # RAW TEXT DOWNLOAD
    # =====================================
    with export_col2:
        st.download_button(
            label="📄 Download as Text (.txt)",
            data=result,
            file_name="AI_Generated_Test_Cases.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Copyable raw output (collapsed)
    with st.expander("📝 View Raw Output (for copy-paste)"):
        st.text_area("Raw Output", result, height=400)
