import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slang_manager import SlangManager
from models import ModelRouter

def test_slang_toggle():
    print("Testing Slang Toggle...")
    
    # Singleton check
    sm = SlangManager()
    
    # 1. Default State (Should be Disabled)
    print(f"Initial Enabled State: {sm.enabled}")
    if sm.enabled:
        print("FAIL: Slangs should be disabled by default.")
    
    # Verify fallback
    slang = sm.get_random_slang()
    print(f"Fallback Slang: {slang}")
    if slang != "friend":
        print(f"FAIL: Expected 'friend' when disabled, got '{slang}'")
        
    enhanced = sm.enhance_text("Hello world.")
    print(f"Enhanced (Disabled): {enhanced}")
    if enhanced != "Hello world.":
        print("FAIL: Enhanced text should match input when disabled.")

    # 2. Enable Slangs
    print("\nEnabling Slangs via ModelRouter...")
    response = ModelRouter.process("maxy1.1", "enable slangs")
    print(f"Response: {response['response']}")
    
    if not sm.enabled:
        print("FAIL: SlangManager should be enabled after command.")
        
    # Verify slang usage
    slang = sm.get_random_slang()
    print(f"Active Slang: {slang}")
    if slang == "friend":
        print("FAIL: Should return actual slang when enabled.")
        
    enhanced = sm.enhance_text("Hello world.")
    print(f"Enhanced (Enabled): {enhanced}")
    # Enhance text is random (30%), so we might need multiple tries to see it change
    # But checking if it *can* change is enough or we rely on the flag check.
    
    # 3. Disable Slangs
    print("\nDisabling Slangs via ModelRouter...")
    response = ModelRouter.process("maxy1.1", "disable slangs")
    print(f"Response: {response['response']}")
    
    if sm.enabled:
        print("FAIL: SlangManager should be disabled after command.")

    print("\nTest Complete.")

if __name__ == "__main__":
    test_slang_toggle()
