import sys
import os

# Add the current directory to sys.path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import MAXY1_3

def verify_fix():
    print("Testing MAXY 1.3 with 'hi'...")
    try:
        result = MAXY1_3.process_message("hi", include_thinking=False)
        print("Success!")
        print(f"Response: {result['response']}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    verify_fix()
