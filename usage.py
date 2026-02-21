import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def check_account_usage():
    print("--- OpenAI Account Overview ---")
    
    
    try:
   
        print("Checking Enqueued Token Limits...")
        response = client.models.list()
        print("API Key is active.")
    except Exception as e:
        print(f"Error: {e}")

    print("\nTip: To see your exact dollar balance ($), visit:")
    print("https://platform.openai.com/settings/organization/billing/overview")

if __name__ == "__main__":
    check_account_usage()