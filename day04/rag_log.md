# Task 4 - Mini RAG Bot Results

## Test 1: In-scope question (card blocking)
Q: How do I block my debit card if it's stolen?
A: To block a stolen debit card, you can call the 24x7 helpline at 1800-123-4567, 
or use the mobile app's "Block Card" feature under Card Services.
Source: faq1.txt
Correct: Yes - accurately grounded in the document

## Test 2: In-scope question (FD rates)
Q: What is the FD interest rate for 3 years?
A: 7.0% per annum, with an additional 0.5% for senior citizens.
Source: faq4.txt
Correct: Yes - accurately grounded in the document

## Test 3: Out-of-scope question (not in any document)
Q: What is the loan interest rate for home loans?
A: "I don't have that information, please contact our support team."
Correct: Yes - correctly refused instead of hallucinating, since no document 
covers home loans

## Conclusion
Unlike the ungrounded model in Day 1's Hallucination Hunt (which sometimes gave 
confident-but-uncertain answers), this RAG-based bot only answers from retrieved 
documents and cleanly refuses when the answer isn't present - this is the core 
value RAG adds for a real banking bot.