# Evaluation System Prompts

## 1. Rubric Score Alignment Guidelines
Verify that the matching scores (0 to 5) given by the agent completely match the text justification.
- **5 (Expert):** Clear evidence of managing production architectures at scale.
- **0 (No Match):** Absolutely no mention of the technology skill or concept.

## 2. Hallucination Guardrails
Compare the generated screening report parameters strictly against the candidate's original raw text resume.
- Any technical tool, professional certification, or career project length mentioned in the report that does **not** exist in the resume must fail evaluation instantly.
