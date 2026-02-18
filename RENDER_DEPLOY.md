# MAXY Backend - Render.com Deployment Guide

Follow these steps to deploy your backend to Render. This will host your AI logic, data analysis, and file processing capabilities.

## 1. Preparation
Ensure your latest code is pushed to your GitHub repository:
`https://github.com/WalterMax289/maxy`

## 2. Create a Web Service on Render
1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository (`maxy`).
4. **Configure the Service:**
   - **Name**: `maxy-backend` (or any unique name)
   - **Region**: **Singapore (Asia)**  <-- **BEST for India (Lowest Latency)**
   - **Branch**: `main`
   - **Root Directory**: `backend`  <-- **IMPORTANT: This must be set to 'backend'**
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

## 3. Environment Variables
In the **Environment** tab of your Render service, click **Add Environment Variable** for each of these:

| Key | Value | Notes |
|-----|-------|-------|
| `PORT` | `10000` | Render's default port |
| `DATABASE_URL` | `sqlite:///./maxy_chat.db` | Or your PostgreSQL connection string |
| `SUPABASE_URL` | `your-supabase-url` | From your Supabase project settings |
| `SUPABASE_ANON_KEY` | `your-anon-key` | From your Supabase project settings |
| `SECRET_KEY` | `your-random-generated-key` | A long secure string |
| `ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` | **CRITICAL: Replace with your actual frontend URL** |
| `DEBUG` | `False` | Recommended for production |

## 4. Finalizing Deployment
1. Click **Create Web Service**.
2. Wait for the build and deployment to finish (Success logs will show "Uvicorn running on http://0.0.0.0:10000").
3. Copy your live backend URL (e.g., `https://maxy-backend.onrender.com`).

## 5. Connecting Frontend
Now that your backend is live, update your frontend to talk to it:
1. Open `frontend/chat.js`.
2. Update the `PRODUCTION_BACKEND_URL` at line 20:
   ```javascript
   const PRODUCTION_BACKEND_URL = 'https://maxy-backend.onrender.com';
   ```
3. Push this change to GitHub so your live site (on Vercel or elsewhere) connects to the new Render backend.

---
> [!TIP]
> **Free Tier Sleep**: Note that on Render's free tier, the backend will spin down after inactivity. The first request after a break might take 30-60 seconds to respond.
