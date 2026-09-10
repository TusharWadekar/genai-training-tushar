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

## PII Masking - Verified Working

Tested with a message containing account info + a fake Aadhaar number.
Log file (capstone/logs/conversation.log) confirms the real Aadhaar number 
was masked to XXXX-XXXX-XXXX BEFORE being written to disk - the raw PII 
never touched the log file.

## Minor Observation
The combined message ("account is X and Aadhaar is Y") was classified as 
out_of_scope and escalated, rather than being treated as an account-update 
message. This is a minor classifier limitation (mixed-intent messages), 
noted but not fixed in this pass - the important security property (PII 
never logged in plaintext) held regardless of this routing behavior.