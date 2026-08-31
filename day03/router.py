import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "day02"))

from intent_classifier import classify


def route(intent_result: dict) -> str:
    """Takes the intent classification result and decides what action to take."""
    intent = intent_result["intent"]
    entities = intent_result.get("entities", {})

    if intent == "balance_enquiry":
        return "ACTION: Fetch balance from mock account database"

    elif intent == "card_hotlist":
        card_info = entities.get("card_last4", "unknown")
        return f"ACTION: Block card (last4={card_info}) immediately + notify security team"

    elif intent == "statement_request":
        period = entities.get("period", "unspecified period")
        return f"ACTION: Generate and email statement for {period}"

    elif intent == "upi_issue":
        return "ACTION: Escalate to UPI support team for investigation"

    elif intent == "small_talk":
        return "ACTION: Respond politely, no backend action needed"

    else:  # out_of_scope
        return "ACTION: Escalate to human agent"


if __name__ == "__main__":
    test_messages = [
        "What's my account balance?",
        "Someone stole my card ending 4412",
        "Email me my statement for July",
        "My UPI payment failed but money was deducted",
        "Hi, good morning!",
        "Which mutual fund should I invest in?",
    ]

    for msg in test_messages:
        result = classify(msg)
        action = route(result)
        print(f"Message: {msg}")
        print(f"Intent: {result['intent']} | Confidence: {result['confidence']}")
        print(f"Router Decision: {action}")
        print("---")