# MAXY Chat - Quick Vercel Deployment
# Option B Recommended: Frontend on Vercel + Backend on Railway

## STEP 1: Deploy Backend on Railway
```bash
cd backend
pip install railway
railway login
railway init
railway add --database postgresql
railway up
# Copy the URL shown (e.g., https://maxy-chat.up.railway.app)
```

## STEP 2: Update Frontend
Edit `frontend/chat.js` line 8:
```javascript
const BACKEND_URL = 'https://your-railway-url.up.railway.app';
```

## STEP 3: Deploy Frontend on Vercel
```bash
cd frontend
npm install -g vercel
vercel
vercel --prod
```

## DONE! 🎉
Your app will be live at: https://your-project.vercel.app
