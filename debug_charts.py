import sys
import os
import base64

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from chart_generator import ChartGenerator

def test_charts():
    print("--- Testing Chart Generation ---")
    
    # 1. Pie Chart
    print("\n1. Testing Pie Chart...")
    try:
        data = [30, 25, 20, 15, 10]
        labels = ['A', 'B', 'C', 'D', 'E']
        img, desc = ChartGenerator.create_pie_chart(labels, data, title="Test Pie")
        if img:
             print("Pie Chart: SUCCESS (Base64 length: {})".format(len(img)))
        else:
             print("Pie Chart: FAILED (None returned)")
    except Exception as e:
        print(f"Pie Chart Error: {e}")

    # 2. Bar Chart
    print("\n2. Testing Bar Chart...")
    try:
        data = [10, 20, 30, 40, 50]
        categories = ['Cat1', 'Cat2', 'Cat3', 'Cat4', 'Cat5']
        img, desc = ChartGenerator.create_bar_chart(categories, data, title="Test Bar")
        if img:
             print("Bar Chart: SUCCESS (Base64 length: {})".format(len(img)))
        else:
             print("Bar Chart: FAILED (None returned)")
    except Exception as e:
        print(f"Bar Chart Error: {e}")

    # 3. Line Chart
    print("\n3. Testing Line Chart...")
    try:
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        img = ChartGenerator.create_line_chart(x, y, title="Test Line") # Note: returns just img
        if img:
             print("Line Chart: SUCCESS (Base64 length: {})".format(len(img)))
        else:
             print("Line Chart: FAILED (None returned)")
    except Exception as e:
        print(f"Line Chart Error: {e}")

    # 4. Histogram
    print("\n4. Testing Histogram...")
    try:
        data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
        img = ChartGenerator.create_histogram(data, title="Test Histogram") # Note: returns just img
        if img:
             print("Histogram: SUCCESS (Base64 length: {})".format(len(img)))
        else:
             print("Histogram: FAILED (None returned)")
    except Exception as e:
        print(f"Histogram Error: {e}")

if __name__ == "__main__":
    test_charts()
