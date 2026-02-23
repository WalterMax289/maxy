import requests
import json
import time

BASE_URL = "http://localhost:8000"

def run_benchmark():
    scenarios = [
        {
            "category": "Identity (Concise)",
            "query": "Who is the Prime Minister of India?",
            "expected": "Should be concise and mention Narendra Modi."
        },
        {
            "category": "Technical (Research)",
            "query": "How does the transformer architecture work in LLMs?",
            "expected": "Detailed technical explanation of attention mechanisms."
        },
        {
            "category": "Educational",
            "query": "Explain the Pythagorean theorem with a real-world example.",
            "expected": "Clear mathematical explanation with a practical application."
        },
        {
            "category": "Current Events (News)",
            "query": "What are the latest developments in space exploration this month?",
            "expected": "Recent news citations and external source references."
        },
        {
            "category": "Finance/Data",
            "query": "What is the current market trend for NVIDIA stock?",
            "expected": "Financial data points (via yfinance)."
        },
        {
            "category": "Slang Handling",
            "query": "Semma work design guru!",
            "expected": "Friendly response acknowledging the slang."
        }
    ]

    models = ["maxy1.1", "maxy1.2", "maxy1.3"]
    all_results = {}

    print(f"Starting Benchmark at {BASE_URL}...")

    for model in models:
        print(f"\nEvaluating Model: {model}")
        all_results[model] = []
        
        for scenario in scenarios:
            print(f"  Testing {scenario['category']}...")
            payload = {
                "message": scenario["query"],
                "model": model,
                "include_thinking": True
            }
            
            start_time = time.time()
            try:
                response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=60)
                end_time = time.time()
                
                if response.status_code == 200:
                    data = response.json()
                    thinking_data = data.get("thinking")
                    reasoning = "No thinking provided"
                    if isinstance(thinking_data, dict):
                        reasoning = thinking_data.get("reasoning", "No reasoning content")
                    elif isinstance(thinking_data, str):
                        reasoning = thinking_data
                        
                    result = {
                        "category": scenario["category"],
                        "query": scenario["query"],
                        "response": data.get("response"),
                        "thinking": reasoning,
                        "time_taken": round(end_time - start_time, 2),
                        "status": "Success"
                    }
                else:
                    result = {
                        "category": scenario["category"],
                        "status": "Error",
                        "error_code": response.status_code,
                        "error_text": response.text
                    }
            except Exception as e:
                result = {
                    "category": scenario["category"],
                    "status": "Failed",
                    "error": str(e)
                }
            
            all_results[model].append(result)
            time.sleep(1) # Be gentle

    with open("benchmark_report.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    
    print("\nBenchmark complete! Results saved to benchmark_report.json")

if __name__ == "__main__":
    run_benchmark()
