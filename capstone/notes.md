## Fix Applied: Added "product_info" Intent

Added a new "product_info" intent to Day 2's classifier for general FAQ/product 
questions (savings accounts, fees, policies) that don't fit the transactional 
intents. Updated bot.py's INFORMATIONAL_INTENTS to route this to the rag node.

## Re-test Result: ALL 3 TURNS PASSED
1. "My account is ACC1001" -> tools node -> correct balance
2. "What savings accounts do you offer?" -> rag node (FIXED) -> correct FAQ 
   answer with citation
3. "And what's my balance?" -> tools node -> correctly remembered ACC1001 
   from turn 1, gave correct balance

This confirms: (a) memory works correctly across turns, (b) the routing gap 
found earlier is now fixed, (c) the full pipeline (classify -> route -> 
RAG/tools -> memory) works end-to-end for a realistic mixed conversation.