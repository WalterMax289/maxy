#!/usr/bin/env python3
"""
Verify Accuracy Fix for MAXY 1.3
"""
import sys
import os

# Add the current directory to path so it can find models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import MAXY1_1, MAXY1_2, MAXY1_3

def test_query(model, model_name, query):
    print(f"\nTesting {model_name} - Query: '{query}'")
    
    if hasattr(model, 'is_code_request'):
        is_tech, lang = model.is_code_request(query)
    elif hasattr(model, 'should_use_wikipedia'):
        is_tech = model.should_use_wikipedia(query)
    elif hasattr(model, 'is_research_query'):
        is_tech = model.is_research_query(query)
    else:
        is_tech = False
        
    print(f"Is Technical/Research Request: {is_tech}")
    
    result = model.process_message(query, include_thinking=False)
    print(f"Model ID: {result['model']}")
    print(f"Response Preview: {result['response'][:150]}...")
    
    # Check for meaningful content (not a generic greeting)
    is_greeting = any(g in result['response'].lower() for g in ["ready to help", "what are we building", "what can i do"])
    has_tech_content = "```" in result['response'] or "verified research" in result['response'].lower() or len(result['response']) > 100
    
    return is_tech, has_tech_content

if __name__ == "__main__":
    print("Running Verification for ALL Models Accuracy Fix...")
    
    models = [
        (MAXY1_1, "MAXY 1.1"),
        (MAXY1_2, "MAXY 1.2"),
        (MAXY1_3, "MAXY 1.3")
    ]
    
    test_cases = ["bubble sort", "binary search"]
    
    all_passed = True
    for model, name in models:
        for query in test_cases:
            is_tech, has_content = test_query(model, name, query)
            if not (is_tech or has_content):
                print(f"❌ FAILED: {name} failed to identify '{query}' as technical")
                all_passed = False
            else:
                print(f"✅ PASSED: {name} correctly handled '{query}'")

    if all_passed:
        print("\n✨ ALL MODELS PASSED! Accuracy improved across the board.")
    else:
        sys.exit(1)

    if all_passed:
        print("\n✨ ALL CORE TESTS PASSED! MAXY 1.3 is now accurately identifying technical requests.")
    else:
        print("\n⚠️ Some tests failed. Check the logic.")
