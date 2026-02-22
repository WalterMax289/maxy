import sys
import os

# Add the current directory to path
sys.path.append(os.getcwd())

from backend.models import MAXY1_3

def test_model():
    test_cases = [
        "What is the weather in Paris?",
        "Tell me a joke",
        "Who is Marie Curie?",
        "What time is it?",
        "Write a python script to hello world",
        "Create a bar chart for sales: 10, 20, 30",
        "What is the meaning of life?",
        "Hello MAXY!",
    ]
    
    for query in test_cases:
        print(f"\n--- Testing Query: '{query}' ---")
        result = MAXY1_3.process_message(query, include_thinking=False)
        print(f"Response: {result['response'][:200]}...")
        if 'charts' in result:
             print(f"Chart generated: {result['charts'][0]['type']}")

if __name__ == "__main__":
    test_model()
