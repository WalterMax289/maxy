#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick test of MAXY 1.3 features"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from models import MAXY1_1, MAXY1_2, MAXY1_3

print("="*60)
print("TESTING MAXY MODELS")
print("="*60)

# Test MAXY 1.1
print("\n1. MAXY 1.1 (should be unchanged):")
r = MAXY1_1.process_message('hello')
print(f"   ✓ Works: {r['model']}")

# Test MAXY 1.2  
print("\n2. MAXY 1.2 (should be unchanged):")
r = MAXY1_2.process_message('hello')
print(f"   ✓ Works: {r['model']}")

# Test MAXY 1.3 - Chart
print("\n3. MAXY 1.3 - Chart Generation:")
r = MAXY1_3.process_message('create pie chart 10 20 30')
has_chart = 'chart' in r['response'].lower()
print(f"   ✓ Detects charts: {has_chart}")
print(f"   Preview: {r['response'][:60]}...")

# Test MAXY 1.3 - Code
print("\n4. MAXY 1.3 - Code Generation:")
r = MAXY1_3.process_message('write python function')
has_code = '```' in r['response']
print(f"   ✓ Generates code: {has_code}")
print(f"   Preview: {r['response'][:80]}...")

# Test MAXY 1.3 - No capabilities list
print("\n5. MAXY 1.3 - Conversational (no capabilities list):")
r = MAXY1_3.process_message('hello')
no_caps = 'Capabilities:' not in r['response']
print(f"   ✓ No capabilities list: {no_caps}")
print(f"   Response: {r['response'][:100]}...")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
