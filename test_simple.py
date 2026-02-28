import sys
import os
import asyncio

# Add the backend and parent directories to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.models import MAXY1_3

async def main():
    query = "create a portfolio website"
    result = MAXY1_3.process_message(query)
    print("FULL RESPONSE:")
    print(result['response'])

if __name__ == "__main__":
    asyncio.run(main())
