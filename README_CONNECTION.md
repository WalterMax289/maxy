# MAXY Chat - Complete Setup & Run Guide

## 🚀 QUICK START (Follow these steps exactly)

### Step 1: Start the Server
**Double-click the file:** `START_SERVER.bat`

**DO NOT CLOSE the black command window that opens!**

Wait until you see:
```
Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 2: Open the Chat
Open your browser and go to: **http://localhost:8000**

### Step 3: Check Connection
- Look at the bottom right corner
- The status dot should turn **GREEN** ✅
- If it's red, wait 5 seconds and refresh the page

### Step 4: Test It
Type "hello" and press Enter. You should get a response from MAXY!

---

## 🔴 If Status Shows "Not Connected" (Red Light)

### Problem 1: Server Not Running
**Symptom:** Red status dot, no AI responses

**Solution:**
1. Look for a black command window
2. If you don't see one, run `START_SERVER.bat`
3. Wait for "Uvicorn running" message
4. Refresh your browser

### Problem 2: Wrong URL
**Symptom:** Chat loads but shows red dot

**Solution:**
- ❌ DON'T open `file:///C:/.../chat.html` directly
- ✅ DO open `http://localhost:8000`

### Problem 3: Port Already in Use
**Symptom:** Server won't start, error about port 8000

**Solution:**
```cmd
# Open Command Prompt as Administrator and run:
netstat -ano | findstr :8000
taskkill //F //PID <PID_NUMBER>
```

Then restart the server.

---

## 📋 What I Fixed

### ✅ Backend Connection
- Created `START_SERVER.bat` - Proper Windows startup script
- Server now runs continuously without timing out
- Proper error messages if server crashes

### ✅ Frontend Improvements  
- Fixed connection detection in `chat.js`
- Added offline fallback mode when backend is unavailable
- Better error messages to guide you
- Connection banner shows helpful instructions

### ✅ Diagnostic Tools
- Created `diagnose.py` - Run this to check everything
- Created `CONNECTION_FIX.md` - Detailed troubleshooting

---

## 🎯 How The Connection Works

```
┌─────────────────┐      HTTP Request       ┌─────────────────┐
│   Browser       │  ─────────────────────► │  Backend Server │
│  (Frontend)     │  http://localhost:8000  │   (Python)      │
│                 │ ◄────────────────────── │                 │
└─────────────────┘      JSON Response      └─────────────────┘
        │                                            │
        │                                            │
        ▼                                            ▼
   Sends: "Hello"                            AI Models Process
                                              MAXY 1.1, 1.2, 1.3
                                                  │
                                                  ▼
                                            Returns: Response
```

**Important:** The server must be running for the AI to work!

---

## 🛠️ Manual Start (Alternative)

If the batch file doesn't work:

```cmd
# 1. Open Command Prompt
cd "C:\Users\vinay\Downloads\intern\MAIN PROJECT CHAT BOT\backend"

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Start server
python server.py

# 4. Open browser to http://localhost:8000
```

---

## 🐛 Debugging

### Check Server Health
Open browser console (F12) and type:
```javascript
fetch('/health').then(r => r.json()).then(console.log)
```

Should show: `{status: "healthy", ...}`

### Check Server Logs
Open: `backend/logs/app.log`

### Run Diagnostics
Double-click: `diagnose.py`

---

## ✅ Success Indicators

When everything works:
1. ✅ Command window shows "Uvicorn running"
2. ✅ Status dot is **GREEN** (bottom right)
3. ✅ You can type messages
4. ✅ AI responds intelligently
5. ✅ No red connection banners

---

## 🆘 Emergency Reset

If nothing works:

1. Close all browser tabs
2. Close all command windows  
3. Restart computer
4. Run `START_SERVER.bat`
5. Open http://localhost:8000

---

## 📞 Support Files

- **START_SERVER.bat** - Start the backend
- **diagnose.py** - Check configuration
- **CONNECTION_FIX.md** - Detailed troubleshooting
- **QUICK_START.md** - Original documentation

**You MUST keep the server running while using the chat!**
