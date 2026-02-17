# Vercel Deployment Configuration

This guide shows you how to deploy MAXY Chat on **Vercel**.

## ⚠️ IMPORTANT: Vercel Limitations

Vercel has ** limitations for Python backends**:
- ❌ No SQLite persistence (filesystem is read-only)
- ❌ Serverless functions have 10s timeout (can be increased to 60s on Pro)
- ❌ Cold starts on free tier
- ✅ Great for frontend, okay for simple backend

**Recommended**: Use Vercel for frontend + Railway for backend (see Option B below)

---

## Option A: Full Deployment on Vercel (Frontend + Backend)

### Step 1: Update Backend for Vercel

Edit `backend/config.py` line 21:
```python
# Change to allow Vercel domains
ALLOWED_ORIGINS = [
    "https://your-project.vercel.app",
    "http://localhost:3000"
]
```

### Step 2: Update Database for Vercel

Since Vercel doesn't support SQLite, you need PostgreSQL:

Edit `backend/.env`:
```env
DATABASE_URL=postgresql://user:pass@your-db-url.com/dbname
```

**Get free PostgreSQL from:**
- [Supabase](https://supabase.com) (recommended - 500MB free)
- [Neon](https://neon.tech) (free tier)
- [ElephantSQL](https://elephantsql.com)

### Step 3: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 4: Deploy

```bash
# From project root
cd "C:\Users\vinay\Downloads\intern\MAIN PROJECT CHAT BOT"

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? [Y/n] → Y
# - Which scope? → Your account
# - Link to existing project? [y/N] → N
# - What's your project name? → maxy-chat
# - In which directory is your code located? → ./
```

### Step 5: Add Environment Variables

```bash
vercel env add SECRET_KEY
# Enter: your-secure-random-key

vercel env add DATABASE_URL
# Enter: postgresql://...

vercel env add ALLOWED_ORIGINS
# Enter: https://your-project.vercel.app
```

Then redeploy:
```bash
vercel --prod
```

---

## Option B: Vercel Frontend + Railway Backend (RECOMMENDED) ⭐

This is the **best approach** for production.

### Backend on Railway

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Go to backend folder
cd backend

# 4. Initialize project
railway init

# 5. Add PostgreSQL database
railway add --database postgresql

# 6. Deploy
railway up

# 7. Get your backend URL
railway domain
# Copy the URL (e.g., https://maxy-chat-backend.up.railway.app)
```

### Frontend on Vercel

```bash
# 1. Go to frontend folder
cd frontend

# 2. Create vercel.json
echo '{"version": 2}' > vercel.json

# 3. Update chat.js line 8
# Change: const BACKEND_URL = 'http://127.0.0.1:8000';
# To: const BACKEND_URL = 'https://your-railway-url.up.railway.app';

# 4. Deploy
vercel

# 5. Set environment variable
vercel env add BACKEND_URL
# Enter: https://your-railway-url.up.railway.app

# 6. Deploy to production
vercel --prod
```

---

## Option C: Quick Test (Without Database)

If you just want to test quickly without setting up PostgreSQL:

### 1. Create Simple Backend

Create `api/index.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MAXY Chat API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Import your server logic
from backend.server import app as main_app

# Merge routes
for route in main_app.routes:
    if hasattr(route, 'methods'):
        app.add_api_route(
            route.path,
            route.endpoint,
            methods=route.methods
        )
```

### 2. Update vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### 3. Deploy

```bash
vercel --prod
```

---

## 🎯 QUICK START (Option B - Recommended)

**I recommend Option B** - it's easier and more reliable.

```bash
# Terminal 1 - Backend
cd backend
pip install railway
railway login
railway init
railway add --database postgresql
railway up

# Copy the URL from output

# Terminal 2 - Frontend
cd frontend
# Edit chat.js and update BACKEND_URL to your Railway URL
vercel
vercel --prod
```

---

## 🚨 Common Issues

### Issue 1: CORS Errors
**Fix**: Update `ALLOWED_ORIGINS` in backend `.env` with your exact Vercel domain

### Issue 2: Database Not Working
**Fix**: Vercel doesn't support SQLite. Use PostgreSQL (Supabase, Neon, etc.)

### Issue 3: Timeout Errors
**Fix**: Vercel has 10s timeout on free tier. Upgrade to Pro for 60s or optimize code.

### Issue 4: "Module not found"
**Fix**: Add `requirements.txt` to root folder (copy from backend/)

---

## 💰 Costs

**Option A (Full Vercel)**:
- Vercel: Free (up to 100GB bandwidth)
- PostgreSQL: $5-15/month

**Option B (Vercel + Railway)**:
- Vercel Frontend: Free
- Railway Backend: $5/month (includes PostgreSQL)

---

## ✅ VERCEL DEPLOYMENT CHECKLIST

- [ ] Created Vercel account
- [ ] Installed Vercel CLI
- [ ] Set up PostgreSQL database (if using Option A)
- [ ] Updated `ALLOWED_ORIGINS` in backend
- [ ] Updated `BACKEND_URL` in frontend chat.js
- [ ] Added all environment variables
- [ ] Tested locally before deploying
- [ ] Deployed successfully

---

## 🎉 YOU'RE READY!

**Which option do you want to use?**

- **Option A**: Everything on Vercel (simpler but limited)
- **Option B**: Vercel frontend + Railway backend (recommended ⭐)

**Option B is strongly recommended** for better performance and reliability.

Need help with any step?
