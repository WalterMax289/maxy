# 🤖 MAXY - Multi-Model AI Chatbot

A powerful multi-tier AI chatbot built with Python FastAPI and vanilla HTML/CSS/JS. MAXY adapts to your needs—from casual conversations to technical coding assistance.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### Multi-Model Intelligence
- **MAXY 1.1** - Conversational specialist with multi-lingual slang support (including Bangalore slang)
- **MAXY 1.2** - Research maven with Wikipedia integration and real-time web search
- **MAXY 1.3** - Technical architect with code generation, file analysis, and data processing

### Core Capabilities
- 💬 Smart conversation management with context awareness
- 📁 File processing (CSV analysis, document reading)
- 📊 Data analysis and chart generation
- 💻 Code generation and debugging assistance
- 🌐 Real-time web research with source verification
- 📖 Wikipedia integration for factual queries
- 🔍 Intent detection and intelligent routing

### User Experience
- Credit-based usage system
- Thinking process display
- Confidence scores
- Dark mode UI
- Responsive design

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or uv

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/WalterMax289/maxy.git
cd maxy
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run the backend**
```bash
# Windows
start_backend.bat
# or
python -m uvicorn backend.server:app --reload --host 0.0.0.0 --port 8000
```

6. **Open the frontend**
Navigate to `frontend/chat.html` in your browser, or serve it:
```bash
python -m http.server 5500 --directory frontend
```

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (default) / Supabase |
| Search | Wikipedia API, DuckDuckGo |
| Auth | JWT tokens |

---

## 📂 Project Roadmap

- [x] **v2.0**: Bangalore Slang Integration
- [x] **v2.0**: Real-time Daily Updates popover
- [x] **v2.0**: Advanced File Intelligence (PDF/CSV)
- [ ] **v2.1**: Multi-lingual slang expansion (Planned)
- [ ] **v2.1**: Image generation integration (Planned)

---

## 📖 Useful Links
*   [Full Documentation](./DOCUMENTATION.md)
*   [Vercel + Render Deployment Guide](./DEPLOYMENT_GUIDE.md)

---

<div align="center">
  <sub>Built with ❤️ using FastAPI</sub>
</div>
