import sys
import os
import asyncio
import json

# Add the backend and parent directories to sys.path to import modules correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

try:
    from backend.models import MAXY1_3
except ImportError:
    try:
        from models import MAXY1_3
    except ImportError as e:
        print(f"Import Error: {e}")
        sys.exit(1)

async def test_maxy13_website():
    query = "create a portfolio website"
    print(f"\nQUERY: {query}")
    print("="*50)
    
    # Run the model
    result = MAXY1_3.process_message(query, include_thinking=True)
    
    if result.get('thinking'):
        print("\n[THINKING PROCESS]")
        print(result['thinking'])
        print("-" * 30)
        
    print("\n[MAXY 1.3 RESPONSE]")
    print(result['response'])
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(test_maxy13_website())
