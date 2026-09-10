# ACC Bank Customer Service Bot (Capstone Project)

A BFSI-style customer service bot built during the GenAI & Agentic AI training 
program. It answers general banking questions from a knowledge base (RAG), 
performs real account actions via tools (mock APIs), remembers context across 
a conversation, and includes basic security guardrails.

## What It Does

- **Classifies** each customer message into an intent (balance check, card 
  block, statement request, UPI issue, general product/FAQ question, or 
  out-of-scope) using an LLM-based classifier with strict JSON output.
- **Routes** the message to the right handler using a LangGraph state graph:
  - Transactional intents (balance, card block) -> a ReAct tool-calling agent
  - Informational intents (FAQs, product info) -> a RAG pipeline grounded in 
    a 10-document knowledge base, with citations
  - Low-confidence or unrecognized intents -> escalation to a human agent
- **Remembers** the conversation: a customer can say "my account is ACC1001" 
  in one turn and ask "what's my balance?" in a later turn without repeating 
  the account number.
- **Takes real actions** via mock tools: check balance, hotlist (block) a 
  card, and retrieve a statement — all against a local mock JSON "database."
- **Protects customer data**: Aadhaar, PAN, and card numbers are masked 
  before being written to any log file.
- **Resists a known prompt-injection attack**: the bot will not act on an 
  account ID other than the one the current customer has established as 
  their own, even if the message claims "admin mode" or special authority.

## Architecture

```
Customer message
      |
      v
 [classify] -- LLM intent classifier (Day 2)
      |
      v
 route_decision (confidence + intent based)
      |
      +-- balance_enquiry / card_hotlist -----> [tools]  -- ReAct agent + mock APIs (Day 7)
      |                                              |
      +-- product_info / statement_request /         |
      |   upi_issue --------------------------> [rag] -- Chroma vector DB + Gemini (Day 4/5)
      |                                              |
      +-- out_of_scope / low confidence ------> [escalate]
                                                       |
                                                       v
                                                  Final response
                                            (conversation history updated,
                                             PII masked before logging)
```

## How to Run

1. Create and activate a virtual environment, install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Add a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your_key_here
   ```
3. Build the knowledge base index (one-time, or after changing kb/ docs):
   ```
   python capstone/graph/build_kb_index.py
   ```
4. Run the bot's built-in demo conversation:
   ```
   python capstone/graph/bot.py
   ```
5. Run the automated tests:
   ```
   pytest capstone/evals/test_bot.py -v
   ```

## Test Results

12/12 automated tests passing, covering:
- Intent classification (4 tests)
- Tool correctness, including error handling for invalid accounts/cards (3 tests)
- PII masking correctness (2 tests)
- End-to-end bot behavior: memory across turns, RAG citation, and the 
  account-isolation security fix (3 tests)

## Known Limitations (Honest Disclosure)

- **No persistent memory**: conversation history exists only in-process for 
  the duration of a script run. There is no database backing it, so history 
  is lost when the program exits.
- **No multi-user session isolation**: the current design assumes a single 
  conversation at a time. A real deployment would need to keep each 
  customer's session (including their account identity) properly isolated.
- **Multi-topic questions can fail silently**: during Day 5 testing, a 
  question combining two unrelated topics (UPI limits + KYC documents) only 
  retrieved chunks for one topic even after increasing top-k, causing the 
  bot to refuse the whole answer instead of partially answering. This was 
  documented but not fixed — a proper fix would split multi-part questions 
  into sub-questions before retrieval.
- **No hard limit on tool-call loops**: the ReAct agent can call multiple 
  tools per turn (this works correctly for the tested chained-request case), 
  but there is no explicit maximum-iteration safety cap in case of unexpected 
  model behavior.
- **Account identity comes from chat text, not authentication**: the 
  account-isolation security fix (Day 8) is a prompt-level guardrail. In a 
  real production system, the account ID should come from an authenticated 
  session/token, not be typed freely by the user in chat — relying on the 
  LLM alone to enforce this is a mitigation, not a complete fix.
- **Free-tier API rate limits**: development was frequently interrupted by 
  Gemini's free-tier daily quota (20 requests/day on some days) and 
  occasional 503 "server busy" errors, both documented in day-level notes. 
  A production deployment would need a paid tier and proper retry/backoff 
  and request-queuing logic.

## Project History

Built incrementally over Days 1-8 of the training:
- Day 1: LLM fundamentals, tokenization, hallucination behavior
- Day 2: Structured intent classification with defensive JSON parsing
- Day 3: Workflow-vs-agent judgment, plain-Python router
- Day 4-5: RAG knowledge base, chunking, multi-query retrieval + failure analysis
- Day 6: Router rebuilt as a LangGraph state graph
- Day 7: ReAct agent with real (mocked) banking tools; capstone scaffold
- Day 8: Harness mapping, red-teaming (found + fixed a real security bug), 
  PII masking, 12-test eval suite