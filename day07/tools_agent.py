import json
import os
from langchain_core.tools import tool
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "mock_data.json")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def load_data():
    with open(MOCK_DATA_PATH, "r") as f:
        return json.load(f)


@tool
def get_balance(account_id: str) -> str:
    """Return the current balance for an account id like ACC1001."""
    data = load_data()
    account = data.get(account_id)
    if account is None:
        return f"Error: Account {account_id} not found."
    return f"Account {account_id} ({account['name']}) balance: Rs. {account['balance']:.2f}"


@tool
def hotlist_card(card_last4: str, reason: str) -> str:
    """Block a card by its last 4 digits and return a reference number."""
    data = load_data()
    found_account = None
    for acc_id, acc_info in data.items():
        if card_last4 in acc_info.get("cards", []):
            found_account = acc_id
            break

    if found_account is None:
        return f"Error: No card ending in {card_last4} found in our records."

    ref_number = f"HTL-{hash(card_last4 + reason) % 10000:04d}"
    return f"Card **{card_last4} hotlisted successfully. Reason: {reason}. Ref: {ref_number}"


TOOLS_SYSTEM_PROMPT = """You are a banking assistant with access to two tools:
1. get_balance(account_id) - use when customer asks about their balance
2. hotlist_card(card_last4, reason) - use when customer wants to block a lost/stolen card

When you need to use a tool, respond ONLY with JSON in this format:
{"tool": "<tool_name>", "args": {...}}

If no tool is needed, respond normally with a plain text answer."""


def run_agent(user_message: str):
    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=TOOLS_SYSTEM_PROMPT,
            response_mime_type="application/json"
        )
    )

    try:
        decision = json.loads(resp.text)
        tool_name = decision.get("tool")
        args = decision.get("args", {})

        if tool_name == "get_balance":
            result = get_balance.invoke(args)
        elif tool_name == "hotlist_card":
            result = hotlist_card.invoke(args)
        else:
            result = "I'm not sure how to help with that."

        print(f"User: {user_message}")
        print(f"Agent decided to call: {tool_name}({args})")
        print(f"Tool result: {result}")
        print("---")

    except (json.JSONDecodeError, TypeError):
        print(f"User: {user_message}")
        print(f"Agent response: {resp.text}")
        print("---")


if __name__ == "__main__":
    test_messages = [
        "What's the balance on account ACC1002?",
        "I lost my card ending in 4412, please block it",
    ]
    for msg in test_messages:
        run_agent(msg)  