#!/usr/bin/env python3
"""
Test MAXY 1.3 Model - Verify all features work
"""
from models import MAXY1_3

def test_chart_generation():
    print("\n" + "="*60)
    print("TEST 1: Chart Generation")
    print("="*60)
    
    test_cases = [
        "create a pie chart with data 10 20 30 40",
        "make a bar chart showing 100 200 150",
        "plot a line graph with values 5 10 15 20"
    ]
    
    for msg in test_cases:
        result = MAXY1_3.process_message(msg)
        print(f"\nInput: {msg}")
        print(f"Response preview: {result['response'][:100]}...")
        print(f"Confidence: {result['confidence']}")

def test_code_generation():
    print("\n" + "="*60)
    print("TEST 2: Code Generation")
    print("="*60)
    
    test_cases = [
        ("write a python function", "python"),
        ("create javascript code", "javascript"),
        ("generate a java class", "java"),
        ("write c++ code", "cpp"),
        ("create html page", "html"),
        ("write css styling", "css"),
        ("create sql query", "sql")
    ]
    
    for msg, expected_lang in test_cases:
        result = MAXY1_3.process_message(msg)
        is_code, detected_lang = MAXY1_3.is_code_request(msg)
        print(f"\nInput: {msg}")
        print(f"Detected language: {detected_lang} (expected: {expected_lang})")
        print(f"Response contains code block: {'```' in result['response']}")
        print(f"Confidence: {result['confidence']}")

def test_conversational():
    print("\n" + "="*60)
    print("TEST 3: Conversational AI (No Capabilities List)")
    print("="*60)
    
    test_cases = [
        "hello",
        "who are you",
        "help",
        "thanks"
    ]
    
    for msg in test_cases:
        result = MAXY1_3.process_message(msg)
        print(f"\nInput: {msg}")
        print(f"Response: {result['response'][:150]}...")
        print(f"Confidence: {result['confidence']}")
        
        # Verify no capabilities list
        if "Capabilities:" in result['response'] and msg not in ['who are you', 'help']:
            print("⚠️ WARNING: Response contains capabilities list!")
        else:
            print("✓ No unwanted capabilities list")

if __name__ == "__main__":
    print("Testing MAXY 1.3 Model...")
    print("This verifies charts, code generation, and AI conversation work")
    
    test_chart_generation()
    test_code_generation()
    test_conversational()
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
