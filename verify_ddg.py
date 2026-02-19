from ddgs import DDGS

try:
    print("Attempting search...")
    with DDGS() as ddgs:
        results = list(ddgs.text("python programming", max_results=3))
    print(f"Results found: {len(results)}")
    for r in results:
        print(r)
except Exception as e:
    print(f"Error: {e}")
