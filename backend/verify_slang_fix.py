#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')

from models import MAXY1_1

test_queries = [
    "yen guru",
    "yen samachara",
    "kya haal hai",
    "eppadi irukkenga",
    "ela unnavu"
]

print("="*60)
print("VERIFYING SLANG GREETINGS FIX")
print("="*60)

for query in test_queries:
    print(f"\nQuery: '{query}'")
    try:
        result = MAXY1_1.process_message(query, include_thinking=False)
        print(f"   Response: {result['response']}")
        
        # Check if it's a slang response (contains specific keywords from our map)
        success = False
        if "yen guru" in query and "helu guru" in result['response'].lower(): success = True
        elif "yen samachara" in query and "super guru" in result['response'].lower(): success = True
        elif "kya haal hai" in query and "ekdum mast" in result['response'].lower(): success = True
        elif "eppadi irukkenga" in query and "nanba" in result['response'].lower(): success = True
        elif "ela unnavu" in query and "anna" in result['response'].lower(): success = True
        
        if success:
            print(f"   ✅ SUCCESS: Correct slang response detected.")
        else:
            print(f"   ❌ FAILURE: Unexpected response (might still be research or default).")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")

print("\n" + "="*60)
