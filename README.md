# 🤖 AI Powered QA Test Case Generator

An intelligent QA automation tool that **scrapes any website** and generates **professional test cases** using state-of-the-art AI models — built with Python, Streamlit, and Playwright.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green?style=flat-square&logo=openai)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🚀 Live Demo

🔗 **[Try it Live →](https://your-app-name.streamlit.app)**

---

## ✨ Features

- 🌐 **Scrapes any website** using Playwright (handles JavaScript-rendered pages)
- 🧠 **3 AI Models supported:** OpenAI GPT-4, Google Gemini, Local Ollama (Mistral)
- 📋 **Structured test cases** with: ID, Scenario, Preconditions, Steps, Expected Result, Priority, Type
- 📊 **Export to Excel (.xlsx)** and plain text (.txt)
- ⚡ **Real-time progress** tracking with response time display
- 🎨 **Beautiful dark UI** with gradient design
- 🔒 **Secure API key** handling via Streamlit Secrets

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web UI framework |
| Playwright | Website scraping (JS support) |
| BeautifulSoup4 | HTML parsing |
| OpenAI SDK | GPT-4 integration |
| Google GenAI SDK | Gemini integration |
| Ollama | Local LLM (Mistral) |
| Pandas + openpyxl | Excel export |

---

## ⚙️ Installation & Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-qa-agent.git
cd ai-qa-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Set up API keys
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-your-key-here"
GEMINI_API_KEY = "your-gemini-key-here"
```

Or export as environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="AI..."
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file:** `app.py`
5. Add secrets in **App Settings → Secrets**:
   ```
   OPENAI_API_KEY = "sk-..."
   GEMINI_API_KEY = "AI..."
   ```
6. Click **Deploy** 🎉

---

## 📸 Screenshots

> Add screenshots of your app here after deploying!

---

## 📁 Project Structure

```
ai-qa-agent/
├── app.py                  # Streamlit UI
├── agent.py                # AI model logic + web scraper
├── requirements.txt        # Python dependencies
├── packages.txt            # System packages for Playwright
├── setup.sh                # Playwright browser installer
├── .streamlit/
│   ├── config.toml         # Streamlit theme config
│   └── secrets.toml        # API keys (local only, not committed)
└── README.md
```

---

## 🔐 Security

- API keys are **never hardcoded** in source code
- Keys are loaded from `st.secrets` (cloud) or environment variables (local)
- Users can optionally enter API keys directly in the sidebar

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues for bugs or feature requests.

---

## 👨‍💻 Author

**Subham Sahu**
🔗 [LinkedIn](https://www.linkedin.com/in/subham-sahu-15549824a/)
📦 [GitHub](https://github.com/YOUR_USERNAME)

---

## 📄 License

MIT License — free to use and modify.
