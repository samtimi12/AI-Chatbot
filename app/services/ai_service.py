import os
from dotenv import load_dotenv
from openai import OpenAI

# load .env once
load_dotenv()

# get API key from env
API_KEY = os.getenv("OPENAI_API_KEY")   # <-- this is the correct way
if not API_KEY:
    raise ValueError("No API key found. Set OPENAI_API_KEY in .env")

# initialize client
client = OpenAI(api_key=API_KEY)

def get_ai_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4o" if you want
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error] {str(e)}"
