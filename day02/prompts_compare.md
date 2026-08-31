# Task 2.1 - Bad Prompt vs Good Prompt

## Prompt A (Simple: "Summarize this email")
This is the sender's third complaint (Ref: CMP-88213) regarding two unsuccessful visits to
the MG Road branch to update their mobile number. During the first visit on Tuesday, they
waited 45 minutes before being informed the system was down. Upon returning on Thursday,
they were told a required form was missing, which had not been provided to them earlier.
As a result of the un-updated number, the sender's UPI has been failing since the 3rd,
posing an issue for an upcoming EMI payment due on the 10th.

## Prompt B (Structured: role + explicit format + constraint)
issue: Delay and poor service in updating mobile number at MG Road branch, leading to UPI
failures and risk to an upcoming EMI payment (Ref CMP-88213).
severity: high
requested_action: Update mobile number

## Observation (what did structure buy you?)
1. Prompt B's output is immediately machine-readable — my code can directly read
   `severity: high` and auto-route this to a priority queue, whereas Prompt A's paragraph
   would need additional parsing/another AI call just to figure out how urgent it is.
2. Prompt B forced the model to commit to one clear requested_action instead of leaving it
   buried in a narrative — this is exactly what a triage system or support agent needs to
   act quickly, not a full story.
3. Prompt A is more "human-readable" as a summary, but Prompt B is more useful for building
   an actual bot workflow, since a real system needs structured signals (severity, action)
   to decide what happens next, not free text to re-read every time.