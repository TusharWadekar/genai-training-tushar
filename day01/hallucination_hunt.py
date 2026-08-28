import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

questions = [
    "What is the capital of Maharashtra?",
    "Who wrote the Ramayana?",
    "What are the annual charges of the Platinum Sapphire Credit Card from SuryaFirst Bank?",
    "What are the current RBI repo rate and today's date?",
    "What is the customer-care number of SuryaFirst Bank?",
]

for q in questions:
    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=q,
        config=types.GenerateContentConfig(
            system_instruction="If you are not certain or the information may be out of date, say 'I don't know' instead of guessing."
        )
    )
    print(f"Q: {q}")
    print(f"A: {resp.text}")
    print("---")