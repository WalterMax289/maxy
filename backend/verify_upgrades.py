import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models import MAXY1_1, MAXY1_2, MAXY1_3
except ImportError:
    # Try alternate import if needed
    try:
        from backend.models import MAXY1_1, MAXY1_2, MAXY1_3
    except ImportError:
        print("Could not import models. Check path.")
        sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_maxy1_1():
    print("\n--- Testing MAXY 1.1 (Context) ---")
    history = [{'role': 'assistant', 'content': 'Hello! How are you?'}]
    
    # Test 1: Continue conversation
    msg = "I'm fine, thanks."
    print(f"User: {msg}")
    try:
        response = MAXY1_1.process_message(msg, include_thinking=False, conversation_history=history)
        print(f"MAXY 1.1: {response.get('response')}")
    except Exception as e:
        print(f"MAXY 1.1 Error: {e}")
    
    # Test 2: New greeting (should normally trigger greeting, but context might change it)
    history = []
    msg = "Hello there"
    print(f"\nUser (No history): {msg}")
    try:
        response = MAXY1_1.process_message(msg, include_thinking=False, conversation_history=history)
        print(f"MAXY 1.1: {response.get('response')}")
    except Exception as e:
        print(f"MAXY 1.1 Error: {e}")

def test_maxy1_2():
    print("\n--- Testing MAXY 1.2 (Research) ---")
    msg = "Tell me about Python programming"
    print(f"User: {msg}")
    try:
        response = MAXY1_2.process_message(msg, include_thinking=False)
        print(f"MAXY 1.2 Response length: {len(response.get('response', ''))}")
        
        # Check for related topics
        if "Related Topics" in response.get('response', ''):
            print("SUCCESS: Related Topics found.")
        else:
            print("WARNING: Related Topics NOT found (this might be due to mocked or real wiki failing or no results).")
            
    except Exception as e:
        print(f"MAXY 1.2 Error: {e}")

def test_maxy1_3():
    print("\n--- Testing MAXY 1.3 (Data Analysis) ---")
    msg = "Please analyze these test scores: 85, 90, 78, 92, 88, 76, 95, 89"
    print(f"User: {msg}")
    try:
        response = MAXY1_3.process_message(msg, include_thinking=False)
        output = response.get('response', '')
        print(f"MAXY 1.3 Response snippet:\n{output[:200]}...")
        
        # Check if analysis was triggered
        if "Statistical Analysis" in output:
            print("SUCCESS: Data analysis triggered.")
        else:
            print("FAILURE: Data analysis NOT triggered.")
    except Exception as e:
        print(f"MAXY 1.3 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_maxy1_1()
    test_maxy1_2()
    test_maxy1_3()
