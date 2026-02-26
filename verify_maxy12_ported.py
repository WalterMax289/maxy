import sys
import os
import asyncio

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

def count_sentences(text):
    return len([s for s in text.split('. ') if len(s.strip()) > 5])

async def test_ported_features():
    test_cases = [
        {"name": "Weather Query", "query": "what is the weather in Bangalore?"},
        {"name": "Time Query", "query": "what time is it right now?"},
        {"name": "Date Query", "query": "what is today's date?"},
        {"name": "Calculation", "query": "can you calculate 256 times 4?"},
        {"name": "Deep Research (Stability Check)", "query": "comprehensive research on the history of AI"},
    ]

    print("\n" + "="*50)
    print("MAXY 1.2 PORTED FEATURES VERIFICATION")
    print("="*50 + "\n")

    for case in test_cases:
        print(f"Testing: {case['name']}")
        print(f"Query: {case['query']}")
        
        result = MAXY1_2.process_message(case['query'], include_thinking=False)
        response = result['response']
        sentence_count = count_sentences(response)
        
        print(f"Response Preview: {response[:150]}...")
        print(f"Sentence Count: {sentence_count}")
        
        # Validation Logic
        if "VERIFIED RESEARCH REPORT" in response:
            status = "✅ PASS (Research Mode)"
        elif 7 <= sentence_count <= 15:
            status = "✅ PASS (Detailed Convo Mode)"
        else:
            status = f"❌ FAIL (Sentences: {sentence_count})"
            
        print(f"Result: {status}")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(test_ported_features())
