import sys
import os
import json
import asyncio

# Add the project root and backend to sys.path
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
sys.path.append(os.path.join(root, "backend"))

from backend.models import MAXY1_2

async def test_maxy12_capabilities():
    print("=== Testing MAXY 1.2 Enhanced Capabilities ===\n")
    
    test_cases = [
        {
            "name": "Deep Technical Research",
            "query": "comprehensive research on the history and science of quantum computing",
            "expect_research": True
        },
        {
            "name": "Natural Conversation (Greeting)",
            "query": "hello there maxy, how's it going today?",
            "expect_research": False
        },
        {
            "name": "Tonal Diversity (Slang/Informal)",
            "query": "yo maxy, what's up with space exploration?",
            "expect_research": True
        },
        {
            "name": "Complex Follow-up (Digging Deeper)",
            "query": "tell me more about the technical challenges of quantum error correction",
            "expect_research": True
        }
    ]
    
    # Mock history for follow-up test
    history = [{"role": "user", "content": "tell me about quantum computing"}, {"role": "assistant", "content": "**VERIFIED RESEARCH REPORT"}]
    
    for case in test_cases:
        print(f"Test Case: {case['name']}")
        print(f"Query: {case['query']}")
        
        if case['name'] == "Complex Follow-up (Digging Deeper)":
            result = MAXY1_2.process_message(case['query'], conversation_history=history)
        else:
            result = MAXY1_2.process_message(case['query'])
            
        response = result['response']
        is_research = "**VERIFIED RESEARCH REPORT" in response
        
        print(f"Detected as Research: {is_research}")
        print(f"Response Length (sentences): {len([s for s in response.split('. ') if s.strip()])}")
        print("\n--- Response Sample ---")
        print(response[:800] + "...")
        print("--- End Sample ---\n")
        
        if case['expect_research'] and not is_research:
            print("❌ FAILURE: Expected research report but got conversation.")
        elif not case['expect_research'] and is_research:
            print("❌ FAILURE: Expected conversation but got research report.")
        else:
            print("✅ SUCCESS: Logic trigger working as expected.")
        
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_maxy12_capabilities())
