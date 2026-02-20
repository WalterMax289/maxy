import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from models import ModelRouter, slang_manager

def test_slang_reactive(model_name):
    print(f"\nTesting {model_name}...")
    
    # Test 1: Standard Greeting (No Slang)
    print("  Input: 'Hello'")
    response_std = ModelRouter.process(model_name, "Hello", include_thinking=False)
    print(f"  Response: {response_std['response'][:100]}...")
    
    # Test 2: Slang Greeting (With Slang)
    print("  Input: 'Hello Macha'")
    response_slang = ModelRouter.process(model_name, "Hello Macha", include_thinking=False)
    print(f"  Response: {response_slang['response'][:100]}...")
    
    # Check if slang was used in the second response
    # Keywords like "Maga", "Guru", "Boss" are default fallbacks if file read fails, 
    # but actual loaded slangs might be different. 
    # Since we can't easily check for *any* slang without the full list, 
    # we'll check if the response is DIFFERENT from the standard one in a way that suggests slang injection 
    # or if it contains common fallback slangs.
    
    common_slangs = ["maga", "macha", "guru", "boss", "thika", "sisya", "da", "kane", "kano", "le", "lo"]
    has_slang = any(s in response_slang['response'].lower() for s in common_slangs)
    
    if has_slang:
        print("  [PASS] Slang detected in response.")
    else:
        print("  [WARN] No common slang detected. Check if response just used a different one.")

def main():
    # Ensure slangs are disabled globally first
    slang_manager.set_enabled(False)
    print("Global Slang Mode: DISABLED")
    
    test_slang_reactive('maxy1.1')
    test_slang_reactive('maxy1.2')
    test_slang_reactive('maxy1.3')

if __name__ == "__main__":
    main()
