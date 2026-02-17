#!/usr/bin/env python3
"""
MAXY Chat Diagnostic Tool
Checks if everything is configured correctly
"""

import os
import sys
import subprocess
import json
import http.client
from pathlib import Path

def check_python():
    """Check Python version"""
    print("✓ Python version:", sys.version.split()[0])
    if sys.version_info < (3, 8):
        print("✗ ERROR: Python 3.8+ required")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = ['fastapi', 'uvicorn', 'pydantic', 'python-dotenv']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"✗ Missing packages: {', '.join(missing)}")
        print("  Run: pip install -r backend/requirements.txt")
        return False
    else:
        print("✓ All required packages installed")
        return True

def check_files():
    """Check if required files exist"""
    base = Path(__file__).parent
    required_files = [
        'backend/server.py',
        'backend/models.py',
        'backend/schemas.py',
        'backend/config.py',
        'backend/requirements.txt',
        'frontend/chat.html',
        'frontend/chat.js'
    ]
    
    missing = []
    for file in required_files:
        if not (base / file).exists():
            missing.append(file)
    
    if missing:
        print(f"✗ Missing files: {', '.join(missing)}")
        return False
    else:
        print("✓ All required files present")
        return True

def check_server_running():
    """Check if server is already running"""
    try:
        conn = http.client.HTTPConnection("localhost", 8000, timeout=2)
        conn.request("GET", "/health")
        response = conn.getresponse()
        conn.close()
        
        if response.status == 200:
            print("✓ Backend server is running on port 8000")
            data = json.loads(response.read().decode())
            print(f"  Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"✗ Server responded with status {response.status}")
            return False
    except:
        print("✗ Backend server is NOT running")
        print("  Run: START_SERVER.bat (Windows) or python backend/server.py")
        return False

def main():
    print("="*60)
    print("MAXY Chat Diagnostic Tool")
    print("="*60)
    print()
    
    checks = [
        ("Python", check_python),
        ("Dependencies", check_dependencies),
        ("Files", check_files),
        ("Server", check_server_running),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        results.append((name, check_func()))
    
    print()
    print("="*60)
    print("Summary")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 Everything looks good!")
        print("🌐 Open http://localhost:8000 in your browser")
    else:
        print("❌ Some checks failed. See above for details.")
        print()
        print("Quick fixes:")
        print("1. Install dependencies: pip install -r backend/requirements.txt")
        print("2. Start server: START_SERVER.bat")
        print("3. Open: http://localhost:8000")
    
    print("="*60)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
