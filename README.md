# 🧬 MediSimplify

> Upload a medical test PDF and get a plain-English explanation — powered by a local AI model. Your data **never leaves your computer**.

![MediSimplify Screenshot](https://img.shields.io/badge/Status-Active-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue) ![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-purple)

---

## ✨ Features

- 📄 **PDF Upload** — Drag & drop or browse for your medical test results
- 🤖 **Local AI** — Uses [Ollama](https://ollama.com) to run a private LLM on your machine
- 🔒 **100% Private** — No data is sent to any server or third party
- ⚡ **Streaming Output** — Results appear token-by-token in real time
- 💬 **Follow-up Questions** — Ask anything about your results in plain English
- 🌐 **No Backend Needed** — Pure HTML/JS frontend, calls Ollama's local API directly

---

## 🚀 Getting Started

### 1. Install Ollama

Download and install from [ollama.com](https://ollama.com), then pull a model:

```bash
ollama pull llama3.2
```

### 2. Clone the repo

```bash
git clone https://github.com/Krishp1244/medical_simplifer.git
cd medical_simplifer
```

### 3. Open the app

Just open `index.html` in your browser — no server required!

> **If you see a CORS error**, start Ollama with origins enabled:
> ```powershell
> # Windows PowerShell
> $env:OLLAMA_ORIGINS="*"; ollama serve
> ```

### 4. (Optional) Run the CLI version

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run on a PDF:

```bash
python main.py your_results.pdf
python main.py your_results.pdf --model mistral --save
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Vanilla JS |
| PDF Parsing | [PDF.js](https://mozilla.github.io/pdf.js/) (in-browser) |
| AI Model | [Ollama](https://ollama.com) (local LLM) |
| CLI Backend | Python + PyMuPDF |
| Hosting | GitHub Pages |

---

## 🔧 Configuration

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API endpoint |
| `DEFAULT_MODEL` | `llama3.2` | Default model to use |

---

## 📁 Project Structure

```
medical_simplifer/
├── index.html        # Frontend app (login + dashboard)
├── main.py           # Python CLI backend
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

---

## ⚠️ Disclaimer

MediSimplify is for **informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider with questions about your medical results.

---

## 📄 License

MIT License — free to use and modify.
