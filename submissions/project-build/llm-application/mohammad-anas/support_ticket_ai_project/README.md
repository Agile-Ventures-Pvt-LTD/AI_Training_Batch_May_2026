# AI-Powered Customer Support Ticket Intelligence System

## Participant Name

Mohammad Aans

## Setup and Execution
1. Create a virtual environment: `python -m venv venv`
2. Activate it and install requirements: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and insert your `GROQ_API_KEY`.
4. Run the orchestration pipeline: `python main.py`

## Prompt Engineering Techniques Applied
- **Role Prompting:** Every API call assumes a strict persona (e.g., `Escalation manager`, `Support QA reviewer`) to tailor the perspective of the analysis.
- **Zero-Shot Prompting:** Used for Summarization, Sensitive Info Detection, and QA Review.
- **Few-Shot Prompting:** Used in Classification to explicitly teach the model that an angry tone does not inherently mean a technical bug.
- **Reasoning Summaries:** Used instead of full Chain-of-Thought to ensure high accuracy without exhausting tokens (e.g., `category_reasoning_summary`).

## Risk, Safety & Hallucination Control
- **Policy Enforcement:** The `DRAFT_RESPONSE` prompt strictly forbids the AI from confirming cancellations or promising refunds without verification, completely eliminating the risk of costly AI hallucinations.
- **Data Privacy Check:** A dedicated LLM pass is made *before* the response is drafted to flag and handle sensitive PCI/PII data.
- **QA Guardrail:** The final step runs an LLM-as-a-Judge protocol to verify that the drafted response adhered to empathy and policy safety constraints.

## Known Limitations & Future Enhancements
- **Limitations:** Strict JSON reliance means if Groq hallucinates a malformed markdown block, the fallback parses it as raw text.
- **Future:** Integrate a Pydantic validation layer or use Groq's native JSON mode for 100% deterministic schema enforcement. 