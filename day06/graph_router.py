import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "day02"))

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from intent_classifier import classify


class RouterState(TypedDict):
    user_input: str
    intent: str
    confidence: float
    response: str
    handover: Optional[dict]


def classify_node(state: RouterState) -> RouterState:
    result = classify(state["user_input"])
    state["intent"] = result["intent"]
    state["confidence"] = result["confidence"]
    return state


def mock_api_node(state: RouterState) -> RouterState:
    state["response"] = f"[Mock API] Processed '{state['intent']}' request successfully."
    return state


def faq_node(state: RouterState) -> RouterState:
    state["response"] = f"[FAQ] Here's some general info about '{state['intent']}'."
    return state


def escalate_node(state: RouterState) -> RouterState:
    state["response"] = "Escalating to a human agent."
    state["handover"] = {"reason": "low_confidence_or_out_of_scope", "intent": state["intent"]}
    return state


def route_decision(state: RouterState) -> str:
    if state["confidence"] < 0.6 or state["intent"] == "out_of_scope":
        return "escalate"
    elif state["intent"] in ["balance_enquiry", "card_hotlist", "statement_request"]:
        return "mock_api"
    elif state["intent"] == "upi_issue":
        return "faq"
    else:
        return "escalate"


builder = StateGraph(RouterState)

builder.add_node("classify", classify_node)
builder.add_node("mock_api", mock_api_node)
builder.add_node("faq", faq_node)
builder.add_node("escalate", escalate_node)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route_decision,
    {
        "mock_api": "mock_api",
        "faq": "faq",
        "escalate": "escalate",
    }
)
builder.add_edge("mock_api", END)
builder.add_edge("faq", END)
builder.add_edge("escalate", END)

app = builder.compile()


if __name__ == "__main__":
    test_utterances = [
        "What's my account balance?",
        "I lost my debit card, block it now!",
        "My UPI payment failed but money was deducted",
        "Which mutual fund should I invest in?",
    ]

    for u in test_utterances:
        result = app.invoke({"user_input": u, "intent": "", "confidence": 0.0, "response": "", "handover": None})
        print(f"Input: {u}")
        print(f"Intent: {result['intent']} (confidence: {result['confidence']})")
        print(f"Response: {result['response']}")
        print("---")