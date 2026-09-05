# Task 6.2 - Router Rebuilt as a Graph

## Test Results (Same 4 test utterances as before)
| Input | Intent | Confidence | Routed To |
|---|---|---|---|
| "What's my account balance?" | balance_enquiry | 0.99 | mock_api |
| "I lost my debit card, block it now!" | card_hotlist | 0.98 | mock_api |
| "My UPI payment failed but money was deducted" | upi_issue | 0.98 | faq |
| "Which mutual fund should I invest in?" | out_of_scope | 0.99 | escalate |

## Comparison to Day 3 (Plain Python Router)
Behavior is identical to the Day 3 if/else router - same intents map to the 
same actions. The routing LOGIC didn't change; what changed is HOW that logic 
is expressed and executed - as a declared graph (nodes + conditional edges) 
instead of nested if/else statements.

## Why This Matters in a Bank (2 lines)
1. The graph structure is drawable and auditable - a compliance reviewer can 
   see exactly which path a customer's request took (classify -> faq -> END), 
   which is harder to demonstrate from scattered if/else logic buried in code.
2. Adding a new intent/action later (e.g., "loan_inquiry") means adding one 
   node and one new conditional-edge mapping, without touching or risking the 
   existing routing logic for other intents - safer to extend in a regulated, 
   audited environment.