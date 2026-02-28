import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.models import MAXY1_1, MAXY1_2, MAXY1_3, MAXYThinkingEngine

async def test_all_models():
    test_queries = [
        ("What is 2+2?", "Basic math - should give answer 4"),
        ("What is the capital of France?", "Geography - should give Paris"),
        ("Hello!", "Greeting - should respond with greeting"),
        ("Who are you?", "Identity - should identify as MAXY"),
    ]
    
    models = [
        ("MAXY1_1", MAXY1_1),
        ("MAXY1_2", MAXY1_2),
        ("MAXY1_3", MAXY1_3),
    ]
    
    for model_name, model in models:
        print(f"\n{'='*50}")
        print(f"Testing {model_name}")
        print('='*50)
        
        for query, expected in test_queries:
            print(f"\nQuery: {query}")
            print(f"Expected: {expected}")
            try:
                result = await model.process_message(query)
                response = result.get('response', 'No response')
                print(f"Response: {response[:200]}..." if len(response) > 200 else f"Response: {response}")
            except Exception as e:
                print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_all_models())
