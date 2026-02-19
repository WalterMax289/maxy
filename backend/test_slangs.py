import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import MAXY1_1, MAXY1_2, MAXY1_3
from slang_manager import SlangManager

def test_slangs():
    print("Testing Bangalore Slangs Integration...\n")
    
    # Test SlangManager directly
    sm = SlangManager()
    print(f"Loaded {len(sm.slangs)} slangs.")
    print(f"Random Slang: {sm.get_random_slang()}")
    print(f"Enhanced Text: {sm.enhance_text('This is a test message')}")
    
    print("\n--- Model Tests ---")
    
    # Test MAXY 1.1 Greeting
    res1 = MAXY1_1.process_message("hello")
    print(f"\nMAXY 1.1 Greeting:\n{res1['response']}")
    
    # Test MAXY 1.2 Greeting
    res2 = MAXY1_2.process_message("hello")
    print(f"\nMAXY 1.2 Greeting:\n{res2['response']}")
    
    # Test MAXY 1.3 Greeting
    res3 = MAXY1_3.process_message("hello")
    print(f"\nMAXY 1.3 Greeting:\n{res3['response']}")
    
    # Test MAXY 1.1 Response Injection
    res4 = MAXY1_1.process_message("tell me a joke")
    print(f"\nMAXY 1.1 Joke:\n{res4['response']}")

if __name__ == "__main__":
    test_slangs()
