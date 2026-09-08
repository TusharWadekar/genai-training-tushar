# Task 7.1 - ReAct Agent with Banking Tools

## Tools Built
1. get_balance(account_id) - looks up account balance from mock_data.json
2. hotlist_card(card_last4, reason) - finds account by card number, blocks it, returns a reference number

## Manual Tool Tests (sanity check)
- Valid account, invalid account, valid card, invalid card - all 4 handled 
  correctly with no crashes (errors returned as clean strings)

## Agent Test Results (using LangGraph's create_react_agent)

| Test | Tool(s) Called | Result |
|---|---|---|
| "What's the balance of ACC1001?" | get_balance | Correct: Rs. 42,500.50 |
| "Block my card ending 4412, I lost it." | hotlist_card | Correct: hotlisted, ref number given |
| "I lost my card ending 4412 — block it and then tell me my remaining balance in ACC1001." | hotlist_card + get_balance (both, in correct order) | Correct: both actions completed, combined into one natural response |
| "What's the balance of ACC9999?" | get_balance | Correct: honestly reported "not found" - did not invent a balance |

## Key Learning
The most significant result is the chained test: the agent correctly parsed 
a single message containing two distinct requests, called both tools in the 
right order, and combined both real results into one coherent reply - without 
being explicitly told how to handle multi-part requests. This is the core 
value of the ReAct (Reasoning + Acting) pattern over a single-tool-call design.

The invalid-account test also confirms the agent stays grounded in real tool 
output rather than fabricating data when a tool fails - consistent with the 
RAG refusal behavior seen in Day 4.