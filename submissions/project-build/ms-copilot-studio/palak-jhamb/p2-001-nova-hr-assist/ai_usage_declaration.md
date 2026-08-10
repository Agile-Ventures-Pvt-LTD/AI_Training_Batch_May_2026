# AI Usage Declaration

## AI Tool Used

**ChatGPT** was used as a supporting tool during the development of the NovaHR Assist solution.

## How AI Assisted the Development

ChatGPT was mainly used to support the planning and development process.
It helped with:

-   Improving and refining prompts and agent instructions.
-   Structuring guardrails for scope, tone, grounding, source
    precedence, privacy, escalation, and employee-specific decisions.
-   Improving the wording and clarity of chatbot responses and project documentation.
-   Providing suggestions while troubleshooting and refining the chatbot behaviour.

AI was used as an **assistive tool**, while the final implementation and decisions were reviewed and completed manually.

## Manual Validation of Outputs

All important chatbot behaviours and test cases were manually tested and validated.

This included checking:

-   Responses against the approved HR knowledge sources.
-   Correct handling of conflicting information using source precedence.
-   Leave and other HR policy queries.
-   Workplace concerns and escalation scenarios.
-   Sensitive-information handling.
-   Out-of-scope questions.
-   Unknown or unsupported questions.
-   Employee-specific requests.
-   Prompt-injection and attempts to reveal hidden instructions.

The outputs were reviewed to make sure the chatbot responded accurately, safely, and according to the defined requirements.

## Corrections Made to AI-Generated Suggestions

AI-generated suggestions were not used without review. They were manually checked and modified where needed.

Key corrections included:

-   Rewording prompts and instructions to better match the project requirements.
-   Removing unnecessary or unsupported information suggested by AI.
-   Strengthening privacy, escalation, refusal, and prompt-injection rules.



All final content, instructions, test results, and chatbot behaviour were manually reviewed before being included in the solution.
