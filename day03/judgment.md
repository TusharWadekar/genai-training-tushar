# Task 3.1 - Workflow or Agent?

## 1. Classify incoming customer emails into five categories.
Decision: Workflow
Reasoning: This is a repetitive, well-defined task with fixed categories, so a 
predictable workflow is sufficient and cheaper to run. If the classifier makes 
an error, it's low-cost — the email can be easily re-routed or manually 
reviewed, so we don't need the flexibility (and unpredictability) of a full agent.

## 2. Resolve a customer's failed UPI transaction end-to-end across three internal systems, deciding the path as it goes.
Decision: Agent
Reasoning: The exact sequence of checks needed depends on what's found at each 
step (e.g., which system shows the failure first), so a fixed workflow can't 
anticipate every path in advance. The cost of a wrong or incomplete resolution 
is high (customer's money is stuck), but the task is inherently non-linear, so 
an agent that can adapt its investigation is more appropriate than a rigid script.

## 3. Generate a monthly account-summary paragraph from a fixed data table.
Decision: Workflow
Reasoning: The input data is already structured and the output format is fixed, 
so there's no real decision-making involved — just formatting/summarizing known 
values. A workflow is more predictable and cheaper here, and if there's an error 
it's easy to spot and fix since the data source itself is well-defined.

## 4. Answer product FAQs from a knowledge base.
Decision: Workflow
Reasoning: This is essentially a lookup-and-respond task (RAG) with a bounded, 
known set of possible questions and answers, so a predictable retrieval workflow 
works well. An agent's extra flexibility isn't needed since there's no multi-step 
investigation required — the answer either exists in the knowledge base or it doesn't.

## 5. Research and compile a comparison of competitor credit-card offerings.
Decision: Agent
Reasoning: This requires open-ended exploration — deciding which sources to check, 
how many competitors to include, and how to structure the comparison — which can't 
be fully predetermined. The cost of a slightly incomplete or imperfect research 
pass is relatively low (it can be reviewed and refined by a human), so the 
flexibility of an agent is worth the reduced predictability here.

## 6. Route an incoming call to the right department.
Decision: Workflow
Reasoning: This is a simple, fixed-category classification task similar to email 
routing — the set of departments and routing rules are known in advance. Errors 
are low-cost and easily correctable (the call can be transferred again), so a 
predictable workflow is more efficient than an agent for this repetitive task.