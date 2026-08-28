# Task 1.1 - Answers

## (a) Why did the Hindi sentence produce more tokens than the English one?

Tokenizers are built (trained) mostly on English/Latin-script text, so common English words
and sub-words already exist as single tokens in the vocabulary. Devanagari script (Hindi)
is far less represented in that vocabulary, so the tokenizer often has to break Hindi words
into smaller pieces (sometimes individual characters or byte-level fragments) to represent
them. More "splitting" = more tokens for the same meaning, even though the Hindi sentence
was not semantically longer than the English one.

## (b) What does that imply for the cost and latency of a multilingual bot?

Since API pricing and processing time are both based on the number of tokens (not words or
characters), a bot that serves Hindi/Hinglish-speaking customers will cost more and respond
slightly slower than one that only serves English speakers, even for equivalent sentences.
For a bank bot expecting mixed-language input (English, Hindi, Hinglish), this must be
budgeted for up front — the same conversation volume will consume noticeably more tokens
(and therefore more cost) than an English-only estimate would suggest.

## (c) What happened to the account number — why did it split the way it did?

The account number ("3021 4456 8890 1123") produced the most tokens (14) of all samples,
even though it's visually short. Tokenizers do not treat digit sequences as single units;
long numbers are usually broken into groups of 2-3 digits per token (since numbers weren't
common "whole words" in the training data). This means numeric identifiers like account
numbers, card numbers, and OTPs are token-expensive, and a bot handling many customers who
share account/card numbers in chat will use up tokens quickly on this alone.

## Cost Calculation

Using the average token count observed in this exercise (~9-10 tokens per customer message):

- 50,000 customer utterances/day x ~10 tokens/message = 500,000 input tokens/day
- 500,000 tokens/day x 30 days = 15,000,000 input tokens/month (15M tokens)

To get an actual monthly cost, look up the **current** per-million-token input price for the
assigned model on the provider's official pricing page (e.g., Google AI pricing for Gemini,
or OpenAI's pricing page), since prices change over time and should never be hardcoded.

Example formula once you have the price:
  Monthly input cost = (15,000,000 / 1,000,000) x price_per_million_input_tokens

Note: this is *input* cost only — output tokens (the bot's replies) are billed separately
and usually at a different (often higher) rate, so the real monthly cost would be higher
once output tokens are included.
