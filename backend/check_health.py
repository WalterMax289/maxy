import urllib.request
import json
import sys

def check_health():
    url = "http://127.0.0.1:8000/health"
    try:
        print(f"Checking {url}...")
        with urllib.request.urlopen(url, timeout=5) as response:
            status_code = response.getcode()
            data = json.loads(response.read().decode())
            print(f"Status Code: {status_code}")
            print(f"Response: {json.dumps(data, indent=2)}")
            if status_code == 200 and data.get("status") == "healthy":
                print("Backend is HEALTHY and CONNECTED.")
                return True
            else:
                print("Backend responded but status is not healthy.")
                return False
    except Exception as e:
        print(f"Failed to connect to backend: {e}")
        return False

if __name__ == "__main__":
    success = check_health()
    sys.exit(0 if success else 1)
