# Task 5 - Multi-Query RAG Results

## Test Question (deliberately combines 2 sub-topics)
"What happens if my card is lost and I also want to know about replacement fees?"

## Query Variations Generated
1. Original: "What happens if my card is lost and I also want to know about replacement fees?"
2. "How do I report a lost card, and how much will I be charged for a replacement?"
3. "What steps should I take if my card is lost, and what are the replacement card fees?"
4. "If my card goes missing, what is the procedure and does it cost anything to get a new one?"

## Result
All 4 query variations retrieved the same single source document 
(debit_card_hotlisting_process.txt), since this document happens to cover 
both the hotlisting process AND replacement fees together. The final answer 
correctly covered both parts of the original question with full citations.

## Observation
In this case, multi-query didn't surface additional documents (since one 
document already answered both parts of the question), but it did increase 
confidence that the retrieval was correct - 4 different phrasings of the 
question all converged on the same source, which is a strong signal that 
this is genuinely the right document rather than a coincidental keyword match.

Multi-query would show more visible benefit on a question whose sub-parts are 
split across different documents (e.g., a question combining "UPI limits" and 
"KYC requirements" - two separate documents) - each variation could then pull 
in the specific document relevant to that phrasing, and the deduplication step 
would combine both sources instead of just the single best-match document 
a single query might have retrieved.

---------------------------------------------------------------------------------------------------------------
## Test 2: Multi-Topic Question (UPI + KYC)

Question: "I need to know my UPI daily limit and also what documents are 
required for KYC"

Result: All 4 query variations retrieved ONLY upi_limits_and_failures.txt 
chunks (3 chunks, all from the same document) — kyc_requirements.txt was 
never retrieved, despite being a clearly separate, relevant document.

Final answer: Full refusal ("I don't have that information..."), even though 
the UPI part of the question WAS answerable from the retrieved context.

## Why This Happened (Failure Analysis)
With k=3 (top 3 chunks per query), if the UPI-related chunks scored higher 
similarity across all 4 phrasings, they filled all 3 slots each time, leaving 
no room for KYC-related chunks to surface — even though KYC is clearly 
relevant to the question. This is a real limitation of naive multi-query 
RAG: combining "OR the union of separately retrieved chunks" doesn't guarantee 
balanced coverage when multiple sub-topics compete for the same top-k slots per query.

## What This Reveals
1. The system correctly avoided inventing a KYC answer (still didn't 
   hallucinate) - but it also failed to give the customer the UPI answer 
   they could have received, because the prompt design forces an all-or-nothing 
   refusal rather than a partial answer.
2. Fixes for a production system: (a) increase k, (b) split multi-part 
   questions into sub-questions and retrieve+answer each separately, or 
   (c) allow the model to answer partially and flag which part it couldn't 
   find, instead of refusing the entire response.

-------------------------------------------------------------------------------------------------
## Follow-up: Increasing k from 3 to 5

Repeated the same UPI+KYC question with k=5 instead of k=3.
Result: STILL only retrieved upi_limits_and_failures.txt chunks (same 3 
unique chunks - this document likely only has 3 total chunks, so increasing 
k found no new chunks from it, and kyc_requirements.txt still ranked too low 
to appear even in the top 5 for any of the 4 query phrasings).

## Real Root Cause
Increasing k alone did not fix the issue - this confirms the problem is 
about embedding similarity ranking, not just a cutoff limit. The KYC 
document's content is semantically "further" from the phrasing used in 
this combined question than the UPI document is, regardless of how the 
question is rephrased.

## Better Fix (identified but not implemented here)
The most reliable fix would be to detect that this is a multi-part question 
and split it into independent sub-questions ("What is my UPI daily limit?" 
and "What documents are needed for KYC?"), retrieve separately for each 
sub-question with its own top-k, then combine both answers. This guarantees 
each sub-topic gets its own retrieval budget instead of competing for the 
same top-k slots.