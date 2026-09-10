import os
import sys
import json

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "day02"))

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from google import genai
from google.genai import types

from intent_classifier import classify
from banking_tools import get_balance, hotlist_card, get_statement

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "capstone_chroma_db")
db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

tools_agent = create_react_agent(
    llm,
    [get_balance, hotlist_card, get_statement],
    prompt="""You are a banking assistant. Use the available tools when needed.
Never invent balances, reference numbers, or transactions — only report what
the tools actually return. If a tool returns an error, report it honestly."""
)


class BotState(TypedDict):
    messages: List[dict]      # conversation history: [{"role": "user"/"assistant", "content": "..."}]
    user_input: str
    intent: str
    confidence: float
    response: str


INFORMATIONAL_INTENTS = {"statement_request", "small_talk", "product_info"}
TRANSACTIONAL_INTENTS = {"balance_enquiry", "card_hotlist"}


def classify_node(state: BotState) -> BotState:
    result = classify(state["user_input"])
    state["intent"] = result["intent"]
    state["confidence"] = result["confidence"]
    return state


def rag_node(state: BotState) -> BotState:
    docs = retriever.invoke(state["user_input"])
    context = "\n\n".join(
        f"[{d.metadata.get('source', 'unknown')}]\n{d.page_content}" for d in docs
    )
    history_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in state["messages"][-6:]
    )
    system_prompt = f"""You are a customer support assistant for ACC Bank.
Answer using ONLY the context below. Cite sources in [brackets].
If not answerable, say: "I don't have that information in my knowledge base — let me connect you to a human agent."

Recent conversation:
{history_text}

Context:
{context}
"""
    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=state["user_input"],
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    state["response"] = resp.text
    return state


def tools_node(state: BotState) -> BotState:
    history_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in state["messages"][-6:]
    )
    combined_input = f"Conversation so far:\n{history_text}\n\nLatest message: {state['user_input']}"
    result = tools_agent.invoke({"messages": [{"role": "user", "content": combined_input}]})
    final_msg = result["messages"][-1]
    content = getattr(final_msg, "content", "")
    if isinstance(content, list):
        content = " ".join(c.get("text", "") for c in content if isinstance(c, dict))
    state["response"] = content
    return state


def escalate_node(state: BotState) -> BotState:
    state["response"] = "I'm not fully sure how to help with that — let me connect you to a human agent."
    return state


def route_decision(state: BotState) -> str:
    if state["confidence"] < 0.6 or state["intent"] == "out_of_scope":
        return "escalate"
    elif state["intent"] in TRANSACTIONAL_INTENTS:
        return "tools"
    elif state["intent"] in INFORMATIONAL_INTENTS or state["intent"] == "upi_issue":
        return "rag"
    else:
        return "escalate"


builder = StateGraph(BotState)
builder.add_node("classify", classify_node)
builder.add_node("rag", rag_node)
builder.add_node("tools", tools_node)
builder.add_node("escalate", escalate_node)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route_decision,
    {"rag": "rag", "tools": "tools", "escalate": "escalate"}
)
builder.add_edge("rag", END)
builder.add_edge("tools", END)
builder.add_edge("escalate", END)

app = builder.compile()


def chat(user_input: str, messages: List[dict]) -> tuple:
    """Run one turn. Returns (response, updated_messages)."""
    state: BotState = {
        "messages": messages,
        "user_input": user_input,
        "intent": "",
        "confidence": 0.0,
        "response": "",
    }
    result = app.invoke(state)
    messages.append({"role": "user", "content": user_input})
    messages.append({"role": "assistant", "content": result["response"]})
    return result["response"], messages


if __name__ == "__main__":
    messages = []
    turns = [
        "My account is ACC1001",
        "What savings accounts do you offer?",
        "And what's my balance?",
    ]
    for turn in turns:
        response, messages = chat(turn, messages)
        print(f"User: {turn}")
        print(f"Bot: {response}")
        print(f"Intent: {messages}")
        print("---")