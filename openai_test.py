import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

def test_openai_connection():
    print("--- OpenAI Connection Check ---")
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return

    # Initialize the client
    client = OpenAI(api_key=api_key)

    try:
        # Simple test: List models to verify authentication
        print("Verifying API Key...")
        client.models.list()
        print("Success: API Key is valid and connected!")
        
        # Optional: Test a small chat completion
        print("Testing small completion...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Connection Verified'"}],
            max_tokens=5
        )
        print(f"AI Response: {response.choices[0].message.content.strip()}")
        
    except Exception as e:
        print(f"Error: OpenAI Test Failed: {e}")

if __name__ == "__main__":
    test_openai_connection()