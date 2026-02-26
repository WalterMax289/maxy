import requests
import re
import json
import time
import os

BASE_URL = "http://localhost:8000"
QUESTIONS_FILE = "test_questions.txt"
RESULTS_FILE = "test_results_maxy11.json"

def parse_questions(filepath):
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into blocks by Q[0-9]+
    blocks = re.split(r'\n(?=Q\d+\.)', '\n' + content)
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        lines = block.split('\n')
        question = ""
        answer = ""
        
        q_match = re.match(r'Q\d+\.\s*(.*)', lines[0])
        if q_match:
            question = q_match.group(1).strip()
            
            # Find the answer line
            for line in lines[1:]:
                a_match = re.match(r'A\d+\.\s*(.*)', line)
                if a_match:
                    answer = a_match.group(1).strip()
                elif answer: # Handle multi-line answers if any
                    answer += " " + line.strip()
        
        if question and answer:
            questions.append({
                "question": question,
                "expected": answer
            })
            
    return questions

def run_tests(offset=0, user_id="test_user_2"):
    print(f"Loading questions from {QUESTIONS_FILE}...")
    test_cases = parse_questions(QUESTIONS_FILE)
    print(f"Found {len(test_cases)} test cases.")
    
    # Load existing results if any
    results = []
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                results = json.load(f)
        except:
            results = []
            
    success_count = sum(1 for r in results if r.get('status') == 'Success')
    
    print(f"\nResuming tests from index {offset+1} against {BASE_URL}/chat using model maxy1.1 (User: {user_id})...")
    
    for i in range(offset, len(test_cases)):
        test = test_cases[i]
        curr_id = i + 1
        print(f"[{curr_id}/{len(test_cases)}] Testing: {test['question'][:50]}...")
        
        payload = {
            "message": test['question'],
            "model": "maxy1.1",
            "include_thinking": True
        }
        
        headers = {
            "X-User-ID": user_id
        }
        
        start_time = time.time()
        try:
            response = requests.post(f"{BASE_URL}/chat", json=payload, headers=headers, timeout=60)
            duration = round(time.time() - start_time, 2)
            
            # Remove any existing error entry for this ID
            results = [r for r in results if r.get('id') != curr_id]
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response")
                thinking = data.get("thinking", {}).get("reasoning", "No thinking") if isinstance(data.get("thinking"), dict) else data.get("thinking")
                
                results.append({
                    "id": curr_id,
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
                    "id": curr_id,
                    "question": test['question'],
                    "status": "Error",
                    "error_code": response.status_code,
                    "error_text": response.text
                })
                print(f"  Error: {response.status_code}")
        except Exception as e:
            results.append({
                "id": curr_id,
                "question": test['question'],
                "status": "Failed",
                "error": str(e)
            })
            print(f"  Failed: {str(e)}")
            
        time.sleep(0.5)
        
    # Sort results by ID
    results.sort(key=lambda x: x.get('id', 0))
    
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"\nTest complete! Results saved to {RESULTS_FILE}")
    print(f"Summary: {success_count}/{len(test_cases)} successful requests.")

if __name__ == "__main__":
    # Resume from 30 (0-indexed 30 is the 31st question)
    run_tests(offset=30, user_id="test_user_finish")

if __name__ == "__main__":
    run_tests()
