import json
import os
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "mock_data.json")


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


# ---- Manual tool test (sanity check before wiring up the agent) ----
def manual_tool_test():
    print("=== Manual Tool Tests ===")
    print(get_balance.invoke({"account_id": "ACC1001"}))
    print(get_balance.invoke({"account_id": "ACC9999"}))
    print(hotlist_card.invoke({"card_last4": "4412", "reason": "lost"}))
    print(hotlist_card.invoke({"card_last4": "0000", "reason": "stolen"}))
    print()


# ---- LangGraph prebuilt ReAct agent ----
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """You are a banking assistant. Use the available tools when needed
to answer account balance or card-blocking questions. Never invent balances or
reference numbers — only report what the tools actually return. If a tool returns
an error, report that error honestly to the customer."""

agent = create_react_agent(llm, [get_balance, hotlist_card], prompt=SYSTEM_PROMPT)


def run_conversation(message: str):
    result = agent.invoke({"messages": [{"role": "user", "content": message}]})
    print(f"User: {message}")
    for msg in result["messages"]:
        role = getattr(msg, "type", "unknown")
        content = getattr(msg, "content", "")
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            print(f"  [{role}] tool_calls: {tool_calls}")
        elif content:
            print(f"  [{role}] {content}")
    print("---")
    return result


if __name__ == "__main__":
    # Step 1: sanity-check the tools directly
    manual_tool_test()

    # Step 2: run the 4 required conversations one at a time
    # (comment/uncomment as needed to manage API quota)
    conversations = [
        "What's the balance of ACC1001?",
         "Block my card ending 4412, I lost it.",
         "I lost my card ending 4412 — block it and then tell me my remaining balance in ACC1001.",
         "What's the balance of ACC9999?",
    ]

    for conv in conversations:
        run_conversation(conv)