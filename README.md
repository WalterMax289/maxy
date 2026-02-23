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

## 📁 Project Structure

```
maxy/
├── backend/
│   ├── server.py         # Main FastAPI application
│   ├── models.py         # AI model implementations
│   ├── config.py         # Configuration management
│   ├── schemas.py        # Pydantic models
│   ├── database.py       # Database operations
│   ├── news_updater.py   # News fetching service
│   └── updates.json      # Dynamic updates data
├── frontend/
│   ├── chat.html         # Main chat interface
│   ├── chat.css         # Styling
│   ├── chat.js          # Frontend logic
│   └── assets/          # Images and assets
├── logs/                # Application logs
├── .env.example         # Environment template
└── start_backend.bat    # Windows startup script
```

---

## 🔧 Configuration

Key environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection | SQLite |
| `SECRET_KEY` | JWT secret | Generated |
| `DEBUG` | Debug mode | False |
| `PORT` | Server port | 8000 |
| `MAX_CREDITS_PER_USER` | Message credits | 30 |

---

## 📖 Documentation

- [Detailed Documentation](./DOCUMENTATION.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Render Deployment](./RENDER_DEPLOY.md)
- [Vercel Deployment](./VERCEL_DEPLOY.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - feel free to use this project for any purpose.

---

## 👤 Author

**WalterMax289**
- GitHub: [@WalterMax289](https://github.com/WalterMax289)

---

<div align="center">
  <sub>Built with ❤️ using FastAPI</sub>
</div>
