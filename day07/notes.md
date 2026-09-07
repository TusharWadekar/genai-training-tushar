# Task 7.1 - ReAct Agent with Banking Tools

## Tools Built
1. get_balance(account_id) - looks up account balance from mock_data.json
2. hotlist_card(card_last4, reason) - finds account by card number, blocks it, 
   returns a reference number

## Manual Tool Tests (before agent integration)
- Valid account (ACC1001): correctly returned balance
- Invalid account (ACC9999): correctly returned error, no crash
- Valid card (4412): correctly hotlisted with reference number
- Invalid card (0000): correctly returned error, no crash

## Agent Test Results
| Message | Tool Called | Arguments | Result |
|---|---|---|---|
| "What's the balance on account ACC1002?" | get_balance | {account_id: ACC1002} | Correct - Rs. 128900.00 |
| "I lost my card ending in 4412, please block it" | hotlist_card | {card_last4: 4412, reason: lost} | Correct - hotlisted, ref HTL-6427 |

## Key Learning
This is the first time the bot moved from just generating text to actually 
taking real actions (calling functions that read/modify data). The agent 
correctly inferred both WHICH tool to call and WHAT arguments to extract 
from natural, casual customer phrasing - without being told explicitly which 
tool matches which message.