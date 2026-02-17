# MAXY Chat Deployment Configuration

## 🚀 Production Deployment Guide

### 1. Current Architecture

**Frontend (Static Websites):**
- `maxy.html` - Landing page (pure static HTML/CSS/JS)
- `chat.html` - Chat interface (static SPA that calls backend API)
- Both are static files that can be served by any web server or by the FastAPI backend

**Backend (Dynamic API):**
- `server.py` - FastAPI application with CORS, static file serving, and REST API endpoints
- Auto-serves frontend files when running (lines 67-83 in server.py)
- Endpoints: `/chat`, `/health`, `/credits`, `/conversations`, `/models`, `/analyze`, `/charts`

### 2. Update Backend Configuration

Edit `backend/config.py` (line 24):
```python
# Current (development - allows all):
ALLOWED_ORIGINS_STR = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000,...")

# For production, set environment variable:
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

### 3. Environment Variables

Create `.env` file in `backend/` folder:
```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Security (CHANGE THESE!)
SECRET_KEY=your-super-secret-key-here-change-this

# CORS (comma-separated, no spaces)
ALLOWED_ORIGINS=https://your-frontend.com

# Database
DATABASE_URL=postgresql://user:password@localhost/maxy_chat

# Features
ENABLE_CREDITS=True
MAX_CREDITS_PER_USER=30
CREDIT_REFRESH_HOURS=3
MAX_FILE_SIZE=10485760

# Logging
LOG_LEVEL=WARNING
```

### 4. Frontend URL Configuration (chat.js)

The frontend auto-detects the backend URL (line 17-20 in chat.js):
- If served by backend on port 8000: Uses relative URLs (`/chat`, `/health`)
- If opened directly (e.g., file:// or Live Server): Uses `http://127.0.0.1:8000`
- Can override via browser console: `localStorage.setItem('maxyBackendUrl', 'https://your-api.com')`

For production deployment, you can either:

**Option A: Set custom backend URL (recommended for separate hosting)**
```javascript
// In browser console before loading chat:
localStorage.setItem('maxyBackendUrl', 'https://api.yourdomain.com');
```

**Option B: Modify chat.js line 17 temporarily**
```javascript
const BACKEND_URL = 'https://api.yourdomain.com';
```

### 5. Static File Serving (Already Configured)

Your `server.py` already includes static file serving (lines 67-83):
```python
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(static_dir, "chat.html"))
```

This means:
- Access chat at: `http://localhost:8000/` (serves chat.html)
- Access frontend files at: `http://localhost:8000/static/...`
- API endpoints at: `http://localhost:8000/chat`, `/health`, etc.

### 6. Deployment Options

#### Option A: Backend Serves Everything (Simplest)
```bash
cd backend
pip install -r requirements.txt
python server.py
# Frontend available at http://localhost:8000/
# API available at http://localhost:8000/chat
```

#### Option B: Separate Frontend + Backend (Production)

**Frontend → Vercel/Netlify:**
```bash
# 1. Push frontend folder to GitHub
# 2. Connect to Vercel
# 3. Set environment variable in browser localStorage or modify chat.js:
#    localStorage.setItem('maxyBackendUrl', 'https://api.yourdomain.com')
```

**Backend → Railway/Render/AWS:**
```bash
# 1. Push backend folder to GitHub
# 2. Connect to Railway/Render
# 3. Add PostgreSQL database
# 4. Set environment variables from .env file
# 5. Deploy
```

#### Option C: Single VPS (DigitalOcean, AWS EC2, etc.)
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run with Gunicorn (production WSGI)
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# Or use systemd service for auto-start
# Use Nginx as reverse proxy with SSL
```

### 7. Local Development Workflow

**Method 1: Backend serves frontend (recommended)**
```bash
cd backend
python server.py
# Open http://localhost:8000/ in browser
```

**Method 2: Separate development servers**
```bash
# Terminal 1: Backend
cd backend
python server.py

# Terminal 2: Frontend (using Live Server or similar)
cd frontend
# Open chat.html with Live Server on port 5500
# Backend auto-detected at localhost:8000
```

### 8. Required Changes Checklist

- [ ] Update `ALLOWED_ORIGINS` in config.py or .env for production domains
- [ ] Change `SECRET_KEY` from default value
- [ ] Set `DEBUG=False` in production
- [ ] Configure PostgreSQL database (not SQLite)
- [ ] Set up SSL/HTTPS
- [ ] Add authentication system (currently credit-based only)
- [ ] Configure proper logging
- [ ] Test file upload limits
- [ ] Add error monitoring (Sentry, etc.)

### 9. Security Checklist

- [ ] Change default `SECRET_KEY` in production
- [ ] Set `DEBUG=False`
- [ ] Remove `*` from `ALLOWED_ORIGINS` in production
- [ ] Add user authentication
- [ ] Set up HTTPS/SSL
- [ ] Add rate limiting per user
- [ ] Validate file uploads (type, size)
- [ ] Add security headers
- [ ] Remove test endpoints before production

### 10. Website Types Explained

**maxy.html - Static Website:**
- Pure HTML/CSS/JavaScript
- No server-side processing
- Can be hosted on any static hosting (GitHub Pages, Netlify, Vercel)

**chat.html - Static SPA (Single Page Application):**
- Static frontend that makes dynamic API calls
- JavaScript fetches data from backend in real-time
- Requires backend server to function fully
- Same hosting options as maxy.html, but needs backend API

**Backend (server.py) - Dynamic Application:**
- FastAPI server processing requests
- Handles AI responses, file processing, data analysis
- Requires Python server environment
- Must be hosted on platform supporting Python (Railway, Render, VPS)

### 11. Troubleshooting

**Frontend can't connect to backend:**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check browser console for CORS errors
3. Verify `ALLOWED_ORIGINS` includes your frontend domain
4. Try setting backend URL manually: `localStorage.setItem('maxyBackendUrl', 'http://localhost:8000')`

**CORS errors:**
1. Update `ALLOWED_ORIGINS` in backend/config.py
2. Add your frontend domain to the list
3. Restart backend server

**File uploads not working:**
1. Check `MAX_FILE_SIZE` in config
2. Verify `ENABLE_FILE_PROCESSING=True`
3. Check file type is supported

## 📊 Estimated Costs

- **Vercel/Netlify (Frontend)**: Free tier (100GB bandwidth)
- **Railway/Render (Backend)**: $5-20/month
- **PostgreSQL**: $5-15/month
- **Domain**: $10-15/year
- **Total**: ~$20-50/month for small app

## 🎯 Quick Testing with ngrok

For temporary public access during development:
```bash
# Install ngrok: https://ngrok.com/

# Start backend
cd backend
python server.py

# In another terminal, expose backend
ngrok http 8000

# Update frontend to use ngrok URL
localStorage.setItem('maxyBackendUrl', 'https://your-ngrok-url.ngrok.io');
```

## 🔧 Development Commands

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server (with auto-reload)
python server.py

# Run production server
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# View logs
tail -f backend/logs/app.log
```

---

**Note:** This guide is accurate as of the current codebase. The frontend auto-detects backend URLs and the backend already serves static files when running.
