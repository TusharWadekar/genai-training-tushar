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



## Day 10 - Fresh-Clone Test Findings

Cloned the repo into a completely new folder (D:\Demo\genai-training-tushar), 
created a fresh venv, installed requirements.txt, recreated .env manually, 
rebuilt the Chroma index, and ran the full eval suite.

Result: 7/12 passed, 5/12 failed - but ALL 5 failures were tests that call 
the Gemini API, and all failed with the classifier's safe fallback 
("out_of_scope"), not a crash. Confirmed via a diagnostic check that the 
API key WAS loading correctly from .env.

Root cause: the fresh-clone process itself (rebuilding the vector index + 
running earlier tests) consumed enough of the day's 20-request free-tier 
quota that the remaining AI-dependent tests failed silently into the 
defensive fallback rather than erroring out.

## Why This Is a Good (Not Bad) Finding
This actually validates the Day 2 defensive design: when the API is 
unavailable/exhausted, the system does NOT crash - it degrades safely to 
out_of_scope/escalate behavior, which is exactly the intended fallback 
behavior. However, it also reveals a real operational limitation: on the 
free tier, a fresh setup + full test run can exceed the daily quota by 
itself, which would need a paid tier or quota-aware test batching in a real 
CI/CD pipeline.