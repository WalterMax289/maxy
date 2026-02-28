import sys
import os
import asyncio

# Add the backend and parent directories to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.models import MAXY1_3

async def test_chart():
    query = "create a bar chart for sales: 100, 200, 300"
    print(f"QUERY: {query}")
    
    analysis = MAXY1_3.analyze_user_intent(query)
    print(f"IS_CHART (Analysis): {analysis['is_chart']}")
    print(f"IS_RESEARCH (Analysis): {analysis['is_research']}")
    print(f"DEPTH: {analysis['depth']}")
    
    result = MAXY1_3.process_message(query)
    print(f"MODEL: {result.get('model')}")
    print(f"CHARTS IN RESPONSE: {'charts' in result}")
    print(f"RESPONSE PREVIEW: {result.get('response', '')[:200]}...")

if __name__ == "__main__":
    asyncio.run(test_chart())
