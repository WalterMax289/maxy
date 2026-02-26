import subprocess
import sys
import time
import os
import webbrowser
import threading
import http.client
SERVER_PORT = 8000
SERVER_HOST = "127.0.0.1"
STATUS_URL = f"http://{SERVER_HOST}:{SERVER_PORT}/server-status"
CHAT_URL = f"http://{SERVER_HOST}:{SERVER_PORT}/"
MAX_WAIT_TIME = 30  

def check_server_running():
    
    try:
        conn = http.client.HTTPConnection(SERVER_HOST, SERVER_PORT, timeout=2)
        conn.request("GET", "/health")
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except:
        return False

def wait_for_server():
    
    print("⏳ Waiting for server to start...")
    start_time = time.time()
    
    while time.time() - start_time < MAX_WAIT_TIME:
        if check_server_running():
            return True
        time.sleep(0.5)
    
    return False

def open_browser():
    time.sleep(2)  
    
    if check_server_running():
        print("\n🌐 Opening browser...")
        webbrowser.open(STATUS_URL)
        print(f"✅ Status page opened: {STATUS_URL}")
        print(f"📱 Chat URL: {CHAT_URL}")
    else:
        print("\n⚠️  Could not verify server status, but server should be running.")
        print(f"🌐 Please manually open: {CHAT_URL}")

def main():
    """Main function to start server and open browser"""
    print("=" * 60)
    print("🚀 MAXY Server Startup")
    print("=" * 60)
    
    # Check if server is already running
    if check_server_running():
        print("\n✅ Server is already running!")
        print(f"🌐 Opening browser...")
        webbrowser.open(STATUS_URL)
        print(f"📱 Chat available at: {CHAT_URL}")
        return
    
    # Start browser opener in background thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print(f"\n📡 Starting server on {SERVER_HOST}:{SERVER_PORT}...")
    print("📝 Server logs will appear below:\n")
    print("-" * 60)
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    try:
        # Start the server using uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "server:app",
            "--host", SERVER_HOST,
            "--port", str(SERVER_PORT),
            "--reload"  # Enable auto-reload for development
        ]
        
        # Run server (this will block until server stops)
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n💡 Try running manually:")
        print("   cd backend")
        print("   python server.py")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
