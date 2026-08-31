import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("day02/complaint.txt", "r", encoding="utf-8") as f:
    complaint_text = f.read()

# Prompt A - Bad/simple prompt
resp_a = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=f"Summarize this email\n\n{complaint_text}"
)

# Prompt B - Good/structured prompt
system_b = """You are a complaints triage assistant for a bank.
Respond with exactly three fields:
issue: <one line describing the core issue>
severity: <low|medium|high>
requested_action: <what the customer wants done>
Only use information from the email; do not invent details."""

resp_b = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=complaint_text,
    config=types.GenerateContentConfig(system_instruction=system_b)
)

print("=== PROMPT A (bad/simple) ===")
print(resp_a.text)
print("\n=== PROMPT B (good/structured) ===")
print(resp_b.text)