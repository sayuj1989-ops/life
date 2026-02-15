
import os
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

async def test_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found.")
        return

    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='gemini-2.0-flash',
            contents='Hello, world!'
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_genai())
