# MAXY Chat - Quick Start Guide

## 🚀 How to Start the Backend

### Option 1: Double-Click (Easiest)
Double-click `start_backend.bat` in the main folder

### Option 2: Command Line
```bash
cd backend
python server.py
```

### Option 3: Using start_server.py (with auto browser open)
```bash
cd backend
python start_server.py
```

## 🌐 How to Access

Once the server is running:
- **Chat Interface:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/health

## ⚠️ Connection Issues?

### Red Light / "Not Connected"
**Problem:** The frontend can't connect to the backend

**Solutions:**
1. **Make sure the server is running** - You should see "Uvicorn running on http://0.0.0.0:8000" in the terminal
2. **Click the status dot** (bottom right corner) to retry connection
3. **Refresh the browser page** (F5)
4. **Check if port 8000 is blocked** by another application

### Port Already in Use
**Problem:** "error while attempting to bind on address ('0.0.0.0', 8000)"

**Solutions:**
1. Kill the process using port 8000:
   ```cmd
   netstat -ano | findstr :8000
   taskkill //F //PID <PID>
   ```
2. Or change the port in `backend/.env`:
   ```env
   PORT=8001
   ```

## 🔧 Common Commands

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Check Server Status
```bash
curl http://localhost:8000/health
```

### Stop Server
Press **Ctrl+C** in the terminal where server is running

## 📁 File Structure

```
MAIN PROJECT CHAT BOT/
├── start_backend.bat      # Windows startup script
├── backend/
│   ├── server.py          # Main server file
│   ├── requirements.txt   # Python dependencies
│   ├── .env              # Configuration
│   └── ...
├── frontend/
│   ├── chat.html         # Main chat interface
│   ├── chat.js           # Frontend logic
│   └── ...
```

## ✅ Verification Checklist

- [ ] Server terminal shows "Uvicorn running on http://0.0.0.0:8000"
- [ ] Opening http://localhost:8000 shows the chat interface
- [ ] Status dot turns green (click it to test)
- [ ] You can send a test message

## 🆘 Still Not Working?

1. Check the server logs in `backend/logs/app.log`
2. Try opening http://localhost:8000/api/docs in your browser
3. Make sure Python 3.8+ is installed
4. Try a different browser or clear cache (Ctrl+Shift+R)

## 💡 Tips

- Keep the server terminal window open while using the chat
- The server must be running for the chat to work
- If you close the terminal, the server stops
- Use `start_server.py` to auto-open your browser
