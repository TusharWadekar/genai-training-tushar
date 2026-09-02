# Task 4.2 - RAG Results (with citations & refusal)

| Question | Sources Retrieved | Answer OK? | Refused Correctly? |
|---|---|---|---|
| How do I hotlist my debit card if it's stolen? | debit_card_hotlisting_process.txt | Yes - all 3 options (helpline, app, branch) correctly cited | N/A |
| What is the daily UPI transaction limit? | upi_limits_and_failures.txt | Yes - Rs. 1,00,000 correctly cited | N/A |
| What documents do I need for KYC? | kyc_requirements.txt | Yes - all 4 documents correctly cited | N/A |
| What is today's USD-INR exchange rate? | (unrelated docs retrieved: hotlisting, savings, charges) | N/A | Yes - exact refusal line given, no invented rate |
| What are the charges for the Platinum Sapphire card? | credit_card_types.txt, charges_schedule.txt | N/A | Yes - exact refusal line given; correctly did not confuse with the real Platinum card |

## Observations
1. All three answerable questions were answered accurately with correct source 
   citations, with no invented information.
2. Both unanswerable questions produced the exact required refusal sentence, 
   even though the retriever fetched semantically related (but not actually 
   matching) documents in both cases - the model correctly distinguished 
   between "similar topic" and "actual answer present."
3. Compared to Task 1.2's Hallucination Hunt (where the ungrounded model 
   sometimes gave uncertain/outdated answers), this RAG-grounded bot never 
   guessed - it either cited a real fact from the knowledge base or refused 
   cleanly. This is the concrete value retrieval adds over relying on the 
   model's own training data.