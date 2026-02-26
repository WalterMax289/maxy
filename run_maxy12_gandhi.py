import sys
import os
import asyncio
import json

# Add the backend and parent directories to sys.path to import modules correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

try:
    from backend.models import MAXY1_2
except ImportError:
    try:
        from models import MAXY1_2
    except ImportError as e:
        print(f"Import Error: {e}")
        sys.exit(1)

async def run_query(query):
    print(f"\nQUERY: {query}")
    print("="*50)
    
    # Run the model
    result = MAXY1_2.process_message(query, include_thinking=True)
    
    if result.get('thinking'):
        print("\n[THINKING PROCESS]")
        print(result['thinking'])
        print("-" * 30)
        
    print("\n[MAXY 1.2 RESPONSE]")
    print(result['response'])
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(run_query("who is mahatma gandhi?"))
