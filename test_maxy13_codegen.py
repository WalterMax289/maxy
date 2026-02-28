import sys
import os
import asyncio
import json

# Add the backend and parent directories to sys.path
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

async def run_test(name, query):
    print(f"\n[TEST: {name}]")
    print(f"QUERY: {query}")
    print("-" * 30)
    
    result = MAXY1_3.process_message(query, include_thinking=True)
    
    if result.get('thinking'):
        # Just show the last step for brevity
        thinking_lines = result['thinking'].split('\n')
        last_step = [l for l in thinking_lines if l.strip() and l[0].isdigit()][-1:]
        print(f"THINKING (Last Step): {last_step[0] if last_step else 'N/A'}")
        
    print(f"MODEL: {result.get('model')}")
    
    response = result.get('response', '')
    # Truncate long responses for easier reading
    display_response = response[:200] + "..." if len(response) > 200 else response
    print(f"RESPONSE PREVIEW: {display_response}")
    
    # Check for specific indicators
    is_code = "```" in response
    is_research = "VERIFIED RESEARCH REPORT" in response or "Deep Research" in response
    
    print(f"CONTAINS CODE BLOCK: {is_code}")
    print(f"CONTAINS RESEARCH HEADER: {is_research}")
    print("=" * 50)
    return result

async def main():
    print("MAXY 1.3 CODE GENERATION & INTENT VERIFICATION")
    print("=" * 50)
    
    tests = [
        ("Portfolio Website", "create a dark theme portfolio website with inter font"),
        ("Python Function", "write a python function to scrape a news website using beautifulsoup"),
        ("React Component", "generate a react functional component for a login form"),
        ("Disambiguation (Info)", "explain how react hooks work in depth"),
        ("Disambiguation (Code)", "implement a simple useFetch react hook snippet"),
        ("Framework Logic", "give me a boilerplate for a django rest api project")
    ]
    
    results = []
    for name, query in tests:
        res = await run_test(name, query)
        results.append(res)
        await asyncio.sleep(1) # Small delay for readable output

if __name__ == "__main__":
    asyncio.run(main())
