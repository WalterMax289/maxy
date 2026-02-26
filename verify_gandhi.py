import requests
import json

BASE_URL = "http://localhost:8000"

def verify():
    payload = {
        "message": "who is mahatma gandhi",
        "model": "maxy1.2",
        "include_thinking": True
    }
    
    print("Sending request: who is mahatma gandhi...")
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=60)
    except Exception as e:
        print(f"Request failed: {e}")
        return
    
    if response.status_code == 200:
        data = response.json()
        print("\nResponse Received:")
        print("="*40)
        print(data['response'])
        print("="*40)
        
        if "MAHATMA GANDHI" in data['response'] and "ASSASSINATION" not in data['response'].split('\n')[0]:
            print("\n✅ Verification SUCCESS: Proper title found.")
        else:
            print("\n❌ Verification FAILED: Check result title.")
            
        print(f"\nConfidence: {data['confidence']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def verify_conversation():
    payload = {
        "message": "Hi, I'm Vinay. What do you think about the future of AI and how it will impact creative work?",
        "model": "maxy1.2",
        "include_thinking": False
    }
    
    print("\nSending conversation request...")
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("\nConversation Response:")
            print("-" * 20)
            print(data['response'])
            print("-" * 20)
            sentences = [s for s in data['response'].split('. ') if s.strip()]
            print(f"Sentence count: {len(sentences)}")
            if 7 <= len(sentences) <= 12:
                print("✅ Depth Verification SUCCESS: 7-12 sentences found.")
            else:
                print(f"❌ Depth Verification FAILED: Found {len(sentences)} sentences.")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    verify()
    verify_conversation()
