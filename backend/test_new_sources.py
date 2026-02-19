import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import MAXY1_1, MAXY1_2, MAXY1_3

def test_weather():
    print("Testing Weather (MAXY 1.1)...")
    res = MAXY1_1.get_weather("London")
    if res and "Temp:" in res:
        print(f"✅ Weather Success: {res}")
    else:
        print(f"❌ Weather Failed: {res}")

def test_web_search():
    print("\nTesting Web Search (MAXY 1.2)...")
    res = MAXY1_2.perform_web_search("latest AI news")
    if res['success'] and len(res['sources']) > 0:
        print(f"✅ Web Search Success: Found {len(res['sources'])} sources.")
        print(f"Sample: {res['response'][:100]}...")
    else:
        print(f"❌ Web Search Failed: {res}")

def test_stock():
    print("\nTesting Stock Analysis (MAXY 1.3)...")
    res = MAXY1_3.analyze_stock("AAPL")
    if res and "Current Price:" in res:
        print(f"✅ Stock Analysis Success.")
        print(f"Sample: {res[:100]}...")
    else:
        print(f"❌ Stock Analysis Failed: {res}")

if __name__ == "__main__":
    test_weather()
    test_web_search()
    test_stock()
