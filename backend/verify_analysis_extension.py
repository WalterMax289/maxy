#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')

from models import MAXY1_3

def test_document_intelligence():
    print("\n--- Testing Document Intelligence ---")
    file_data = {
        'name': 'test_article.txt',
        'type': 'text/plain',
        'content': """
        Innovation in AI is reaching great heights! We are happy to announce our success in Bangalore. 
        Our team at team@maxy.ai has developed amazing tools. 
        Visit our website at https://maxy.ai for more details. 
        The launch event is scheduled for October 15, 2026.
        However, some legacy problems still cause errors in slow systems.
        """
    }
    
    result = MAXY1_3.process_message("Analyze this file", include_thinking=False, file_data=file_data)
    print(f"Response:\n{result['response']}")
    
    # Simple checks
    success = "Document Intelligence" in result['response'] and "positive" in result['response'].lower()
    if success:
        print("✅ SUCCESS: Document intelligence correctly identified sentiment and file type.")
    else:
        print("❌ FAILURE: Document intelligence check failed.")

def test_data_intelligence():
    print("\n--- Testing Data Intelligence (CSV) ---")
    csv_content = """Date,Sales,Revenue,Expenses
2023-01-01,100,5000,2000
2023-01-02,120,6000,2200
2023-01-03,110,5500,2100
2023-01-04,150,7500,2500
2023-01-05,200,10000,3000
2023-01-06,180,9000,2800
2023-01-07,220,11000,3200
"""
    file_data = {
        'name': 'sales_data.csv',
        'type': 'text/csv',
        'content': csv_content
    }
    
    result = MAXY1_3.process_message("What can you tell me about this data?", include_thinking=False, file_data=file_data)
    print(f"Response:\n{result['response']}")
    
    # Simple checks
    success = "Data Intelligence" in result['response'] and "Sales" in result['response'] and "correlation" in result['response'].lower()
    if success:
        print("✅ SUCCESS: Data intelligence correctly parsed CSV and generated correlation insights.")
    else:
        print("❌ FAILURE: Data intelligence check failed.")

if __name__ == "__main__":
    print("="*60)
    print("VERIFYING MAXY 1.3 ANALYTICAL EXTENSIONS")
    print("="*60)
    
    test_document_intelligence()
    test_data_intelligence()
    
    print("\n" + "="*60)
