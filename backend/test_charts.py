#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MAXY 1.3 Chart Generation
Verifies all chart types generate actual images
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from models import MAXY1_3

def test_chart_generation():
    """Test that MAXY 1.3 generates actual chart images"""
    
    print("="*60)
    print("MAXY 1.3 Chart Generation Tests")
    print("="*60)
    print()
    
    chart_tests = [
        {
            'name': 'Pie Chart',
            'message': 'create a pie chart with data 10 20 30 40',
            'expected_type': 'pie'
        },
        {
            'name': 'Bar Chart', 
            'message': 'make a bar chart showing sales 100 200 150 300',
            'expected_type': 'bar'
        },
        {
            'name': 'Line Chart',
            'message': 'plot a line chart with values 5 10 15 20 25',
            'expected_type': 'line'
        },
        {
            'name': 'Scatter Plot',
            'message': 'create scatter plot of 10 20 30 40 50',
            'expected_type': 'scatter'
        },
        {
            'name': 'Histogram',
            'message': 'make histogram of data 10 15 20 25 30 35 40',
            'expected_type': 'histogram'
        }
    ]
    
    all_passed = True
    
    for test in chart_tests:
        print(f"Testing {test['name']}...")
        result = MAXY1_3.process_message(test['message'])
        
        # Check if chart was generated
        if 'charts' not in result:
            print(f"  ❌ FAIL: No charts in response")
            all_passed = False
            continue
        
        chart = result['charts'][0]
        
        # Check chart type
        if chart['type'] != test['expected_type']:
            print(f"  ❌ FAIL: Wrong type. Expected {test['expected_type']}, got {chart['type']}")
            all_passed = False
            continue
        
        # Check if image exists
        if not chart['base64_image']:
            print(f"  ❌ FAIL: No base64 image generated")
            all_passed = False
            continue
        
        # Check image size (should be substantial)
        image_size = len(chart['base64_image'])
        if image_size < 1000:
            print(f"  ❌ FAIL: Image too small ({image_size} bytes)")
            all_passed = False
            continue
        
        print(f"  ✅ PASS: {test['name']} generated ({image_size} bytes)")
    
    print()
    print("="*60)
    if all_passed:
        print("✅ ALL CHART TESTS PASSED!")
        print("MAXY 1.3 now generates actual chart images!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = test_chart_generation()
    sys.exit(0 if success else 1)
