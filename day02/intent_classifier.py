import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an intent classifier for a bank's customer support chatbot.
Given a customer message, respond ONLY with a JSON object in this exact format:
{
  "intent": "<one of: check_balance, block_card, loan_inquiry, complaint, other>",
  "reason": "<short reason extracted from the message, or null>",
  "confidence": "<high, medium, or low>"
}
Do not include any text outside the JSON object."""

test_messages = [
    "Mera card kho gaya hai, please block karo",
    "What's my current account balance?",
    "I want to know about personal loan interest rates",
    "Your app keeps crashing, this is very frustrating",
    "Kal mausam kaisa rahega?",  # unrelated message - to test "other"
]

for msg in test_messages:
    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=msg,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    print(f"Message: {msg}")
    print(f"Response: {resp.text}")
    print("---")