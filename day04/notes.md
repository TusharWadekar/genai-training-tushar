# Task 4.1 - Chunk Size Experiment

## Results
- chunk_size=500, chunk_overlap=50 -> 19 chunks from 10 documents
- chunk_size=100, chunk_overlap=50 -> 72 chunks from 10 documents

## What happened and why

Reducing chunk_size from 500 to 100 nearly quadrupled the number of chunks 
(19 -> 72). This makes sense because each document now has to be split into 
many more, smaller pieces to stay under the 100-character limit, and the 
overlap (50 characters) becomes a much larger proportion of each small chunk, 
causing even more overlap-driven duplication of content across chunks.

## Why chunk size is a design decision, not a default

1. **Too large a chunk** (e.g., 500+) risks mixing multiple unrelated facts 
   into one chunk (e.g., a document covering both hotlisting AND replacement 
   fees in one chunk) — when retrieved, the model gets extra irrelevant 
   context along with the answer, which can dilute precision.

2. **Too small a chunk** (e.g., 100) risks cutting a single fact or sentence 
   in half across two chunks (e.g., "the interest rate is 7.25%" might get 
   split from "for 5+ year tenures"), so the retriever might fetch an 
   incomplete piece of information that doesn't make sense on its own.

3. The "right" chunk size depends on how self-contained each fact in the 
   source documents naturally is — for short, fact-dense FAQ-style content 
   like ours, a medium chunk size (e.g., 300-500) is likely better than either 
   extreme, since each chunk can hold one complete fact/rule without pulling 
   in unrelated ones.