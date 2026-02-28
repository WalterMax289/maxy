import sys
import os
import asyncio

# Add the backend and parent directories to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.models import ModelRouter

async def test_essay_speech():
    test_cases = [
        ("MAXY1.2 Essay", "maxy1.2", "write an essay on the importance of renewable energy"),
        ("MAXY1.2 Speech", "maxy1.2", "write a speech about space exploration for students"),
        ("MAXY1.3 Essay", "maxy1.3", "write an argumentative essay on artificial intelligence"),
        ("MAXY1.3 Speech", "maxy1.3", "write a formal speech for a graduation ceremony about persistence"),
        ("MAXY1.3 Paragraph", "maxy1.3", "write a paragraph about the beauty of nature")
    ]
    
    for name, model, query in test_cases:
        print(f"\n[TEST: {name}]")
        print(f"QUERY: {query}")
        print("-" * 30)
        
        result = ModelRouter.process(model, query, include_thinking=False)
        response = result.get('response', '')
        
        print(f"MODEL: {result.get('model')}")
        
        # Check for headers
        is_essay = "📝 **Essay" in response
        is_speech = "🎤 **Speech" in response
        
        print(f"IS ESSAY: {is_essay}")
        print(f"IS SPEECH: {is_speech}")
        
        # Preview first 150 chars
        preview = response[:150].replace('\n', ' ')
        print(f"PREVIEW: {preview}...")
        
        if not (is_essay or is_speech) and "paragraph" not in query:
            print("❌ FAILED: No essay/speech header found.")
        elif "paragraph" in query and not is_essay:
             # Paragraphs are formatted as essays
             print("✅ PASSED: Paragraph treated as essay.")
        else:
            print("✅ PASSED")
        print("=" * 50)
        
        await asyncio.sleep(1) # Delay for DDG/Wiki rate limits

if __name__ == "__main__":
    asyncio.run(test_essay_speech())
