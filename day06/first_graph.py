from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    account_type: str
    message: str


def greet(state: State) -> State:
    state["message"] = f"Hello {state['name']}, welcome to ACC Bank!"
    return state


def set_account_type(state: State) -> State:
    state["account_type"] = "savings"
    return state


def compose(state: State) -> State:
    state["message"] = f"{state['message']} Your account type is: {state['account_type']}."
    return state


builder = StateGraph(State)

builder.add_node("greet", greet)
builder.add_node("set_account_type", set_account_type)
builder.add_node("compose", compose)

builder.add_edge(START, "greet")
builder.add_edge("greet", "set_account_type")
builder.add_edge("set_account_type", "compose")
builder.add_edge("compose", END)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"name": "Asha", "account_type": "", "message": ""})
    print(result)