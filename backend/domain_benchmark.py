import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

from backend.models import MAXY1_1, MAXY1_2, MAXY1_3

def benchmark():
    test_queries = {
        "Technical": "Latest trends in Quantum Computing 2024",
        "Educational": "Explain the process of photosynthesis for a 10th grade student",
        "Health": "Common symptoms of seasonal flu and best prevention methods",
        "News": "What happened in the world today? Give me top headlines",
        "Daily Updates": "Current status of technology industry in India"
    }
    
    models = [
        ("MAXY 1.1", MAXY1_1),
        ("MAXY 1.2", MAXY1_2),
        ("MAXY 1.3", MAXY1_3)
    ]
    
    results = {}
    
    for model_name, model_class in models:
        print(f"\n Benchmarking {model_name}...")
        results[model_name] = {}
        for category, query in test_queries.items():
            print(f"  - Testing {category}...")
            try:
                res = model_class.process_message(query, include_thinking=False)
                
                results[model_name][category] = {
                    "query": query,
                    "response": res.get('response', ''),
                    "length": len(res.get('response', '')),
                    "preview": res.get('response', '')[:150] + "..."
                }
            except Exception as e:
                results[model_name][category] = {"query": query, "error": str(e)}

    # Output results for analysis
    with open('domain_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("\nDomain benchmark completed. Results saved to domain_results.json")

if __name__ == "__main__":
    benchmark()
