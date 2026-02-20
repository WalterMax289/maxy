import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from models import MAXY1_3

def test_model_chart():
    print("--- Testing MAXY1_3 Chart Processing ---")
    
    # Test case 1: Line chart with "data" keyword (likely to trigger conflict)
    msg1 = "Create a line chart with this data: 10, 20, 30, 40, 50"
    print(f"\nQuery: '{msg1}'")
    result1 = MAXY1_3.process_message(msg1, include_thinking=False)
    
    if 'charts' in result1:
        print("Result: Generated CHART")
        print(f"Type: {result1['charts'][0]['type']}")
    else:
        print("Result: NO CHART generated")
        print(f"Response starts with: {result1['response'][:50]}...")

    # Test case 2: Histogram (simple)
    msg2 = "histogram of 1 2 3 4 5"
    print(f"\nQuery: '{msg2}'")
    result2 = MAXY1_3.process_message(msg2, include_thinking=False)
    
    if 'charts' in result2:
        print("Result: Generated CHART")
        print(f"Type: {result2['charts'][0]['type']}")
    else:
        print("Result: NO CHART generated")
        print(f"Response starts with: {result2['response'][:50]}...")

if __name__ == "__main__":
    test_model_chart()
