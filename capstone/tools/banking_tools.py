import json
import os
from langchain_core.tools import tool

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


@tool
def get_statement(account_id: str, period: str) -> str:
    """Return recent transactions for an account. Period can be 'last month' or similar."""
    data = load_data()
    account = data.get(account_id)
    if account is None:
        return f"Error: Account {account_id} not found."

    transactions = account.get("transactions", [])
    if not transactions:
        return f"No transactions found for account {account_id}."

    lines = "\n".join(transactions)
    return f"Statement for {account_id} ({account['name']}), period: {period}:\n{lines}"


if __name__ == "__main__":
    print(get_balance.invoke({"account_id": "ACC1001"}))
    print(hotlist_card.invoke({"card_last4": "4412", "reason": "lost"}))
    print(get_statement.invoke({"account_id": "ACC1001", "period": "last month"}))
    print(get_statement.invoke({"account_id": "ACC9999", "period": "last month"}))