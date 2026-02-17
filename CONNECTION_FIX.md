# 🔧 Connection Troubleshooting Guide

## Problem: Frontend shows "Not Connected" (Red Light)

### Quick Fix (90% of cases)

**Step 1:** Close any existing command windows

**Step 2:** Double-click **`START_SERVER.bat`** in the main folder

**Step 3:** Wait until you see:
```
Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Step 4:** Open http://localhost:8000 in your browser

**Step 5:** The status dot should turn **GREEN**

---

## If Still Not Working

### Check 1: Is the server actually running?

Open Command Prompt and run:
```cmd
curl http://localhost:8000/health
```

You should see a JSON response like:
```json
{"status": "healthy", "version": "2.0.0"}
```

**If you get "Connection refused"** → Server is not running. Run START_SERVER.bat

### Check 2: Port conflicts

Run this to check if port 8000 is in use:
```cmd
netstat -ano | findstr :8000
```

If you see results, the port is taken. Either:
- Kill the process using it
- Change port in `backend/.env` file to 8001

### Check 3: Firewall/Antivirus

Some antivirus software blocks localhost connections:
- Add exception for Python
- Or temporarily disable antivirus to test

---

## Common Issues

### Issue: Server starts but stops immediately

**Cause:** Dependencies not installed or Python not in PATH

**Fix:**
```cmd
cd backend
pip install -r requirements.txt
```

### Issue: Frontend works but models don't respond

**Cause:** Backend models not loading properly

**Fix:** 
1. Restart the server
2. Check browser console (F12 → Console) for errors
3. Try a simple message like "hello"

### Issue: Chat interface loads but status is red

**Cause:** Frontend can't reach backend

**Fix:**
1. Make sure you're accessing via http://localhost:8000
2. Not by opening chat.html directly
3. Clear browser cache (Ctrl+Shift+R)

---

## 🔍 Debug Information

To see what's happening:

1. **Browser Console:** Press F12 → Console tab
2. **Server Logs:** Check `backend/logs/app.log`
3. **Network Tab:** F12 → Network tab → Look for failed requests

---

## ✅ Verification Checklist

- [ ] START_SERVER.bat is running (don't close the window!)
- [ ] You see "Uvicorn running on http://0.0.0.0:8000"
- [ ] You're accessing http://localhost:8000 (not file://)
- [ ] Status dot turns green within 5 seconds
- [ ] You can type and send a message
- [ ] AI responds (even if in offline mode)

---

## 🆘 Emergency Fix

If nothing works:

1. Restart your computer
2. Delete `backend/__pycache__` folder
3. Run START_SERVER.bat
4. Wait 10 seconds
5. Open http://localhost:8000

---

## 📞 Need More Help?

Check these files:
- `backend/logs/app.log` - Server errors
- Browser console (F12) - Frontend errors
- Windows Event Viewer - System errors
