"""
Quick test to verify backend is working
"""
import urllib.request
import json

def test_connection():
    urls = [
        "http://localhost:8000/health",
        "http://127.0.0.1:8000/health",
        "http://localhost:8000/api",
        "http://127.0.0.1:8000/api"
    ]
    
    for url in urls:
        try:
            print(f"\nTesting: {url}")
            req = urllib.request.Request(url, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = response.read().decode('utf-8')
                print(f"✅ SUCCESS - Status: {response.status}")
                print(f"Response: {data[:200]}...")
                return True
        except Exception as e:
            print(f"❌ FAILED: {e}")
    
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Backend Connection")
    print("=" * 60)
    success = test_connection()
    print("\n" + "=" * 60)
    if success:
        print("✅ Backend is running and accessible!")
    else:
        print("❌ Backend is not responding")
        print("\nTroubleshooting:")
        print("1. Make sure server is running: python server.py")
        print("2. Check port 8000 is not blocked")
        print("3. Try refreshing the browser page")
    print("=" * 60)
