#!/usr/bin/env python3
"""Test enhanced MAXY 1.1 and 1.2 models"""
from models import MAXY1_1, MAXY1_2

def count_sentences(text):
    """Count actual sentences"""
    sentences = [s.strip() for s in text.replace('! ', '. ').replace('? ', '. ').split('. ') if s.strip()]
    return len(sentences)

def test_models():
    test_cases = [
        "hello",
        "who are you",
        "what is machine learning",
        "thank you",
        "bye",
        "how are you",
        "tell me a joke"
    ]
    
    print("="*80)
    print("ENHANCED MODELS TEST - Response Length Check")
    print("="*80)
    print()
    
    for test in test_cases:
        print(f"\nInput: '{test}'")
        print("-"*80)
        
        # MAXY 1.1
        result1 = MAXY1_1.process_message(test)
        sentences1 = count_sentences(result1['response'])
        print(f"\nMAXY 1.1 (Expected: 3-4 sentences) -> Got: {sentences1} sentences")
        print(f"Response: {result1['response'][:150]}...")
        
        # MAXY 1.2
        result2 = MAXY1_2.process_message(test)
        sentences2 = count_sentences(result2['response'])
        print(f"\nMAXY 1.2 (Expected: 5-10 sentences) -> Got: {sentences2} sentences")
        print(f"Response: {result2['response'][:200]}...")
    
    print("\n" + "="*80)
    print("✅ All tests completed!")
    print("="*80)

if __name__ == "__main__":
    test_models()
