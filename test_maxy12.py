import requests
import re
import json
import time
import os

BASE_URL = "http://localhost:8000"
QUESTIONS_FILE = "Deep Research Questions.txt"
RESULTS_FILE = "test_results_maxy12.json"

def parse_questions(filepath):
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find questions like "1. Question?" followed by indented answer
    # Note: The format is "N. Question" then a newline with the answer
    matches = re.finditer(r'(\d+)\.\s*(.*?)\n\s+(.*?)(?=\n\d+\.|\n\n|\Z)', content, re.DOTALL)
    
    for match in matches:
        q_num = match.group(1)
        question = match.group(2).strip()
        answer = match.group(3).strip().replace('\n', ' ')
        
        questions.append({
            "id": int(q_num),
            "question": question,
            "expected": answer
        })
            
    return questions

def run_tests(user_id="maxy12_test_unique"):
    print(f"Loading deep research questions from {QUESTIONS_FILE}...")
    test_cases = parse_questions(QUESTIONS_FILE)
    print(f"Found {len(test_cases)} test cases.")
    
    results = []
    success_count = 0
    
    print(f"\nStarting tests against {BASE_URL}/chat using model maxy1.2 (User: {user_id})...")
    
    for i, test in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Testing Q{test['id']}: {test['question'][:60]}...")
        
        payload = {
            "message": test['question'],
            "model": "maxy1.2",
            "include_thinking": True
        }
        
        headers = {
            "X-User-ID": user_id
        }
        
        start_time = time.time()
        try:
            response = requests.post(f"{BASE_URL}/chat", json=payload, headers=headers, timeout=120)
            duration = round(time.time() - start_time, 2)
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response")
                thinking = data.get("thinking", {}).get("reasoning", "No thinking") if isinstance(data.get("thinking"), dict) else data.get("thinking")
                
                results.append({
                    "id": test['id'],
                    "question": test['question'],
                    "expected": test['expected'],
                    "ai_response": ai_response,
                    "thinking": thinking,
                    "time_taken": duration,
                    "status": "Success"
                })
                success_count += 1
            else:
                results.append({
                    "id": test['id'],
                    "question": test['question'],
                    "status": "Error",
                    "error_code": response.status_code,
                    "error_text": response.text
                })
                print(f"  Error: {response.status_code}")
        except Exception as e:
            results.append({
                "id": test['id'],
                "question": test['question'],
                "status": "Failed",
                "error": str(e)
            })
            print(f"  Failed: {str(e)}")
            
        time.sleep(1) # Research mode takes more processing
        
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"\nTest complete! Results saved to {RESULTS_FILE}")
    print(f"Summary: {success_count}/{len(test_cases)} successful requests.")

if __name__ == "__main__":
    run_tests()
