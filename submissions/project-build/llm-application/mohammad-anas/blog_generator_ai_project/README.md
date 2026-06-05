# AI-Powered Blog Generator

## How to Run
1. Create a virtual environment: `python -m venv venv` and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and add your `GROQ_API_KEY`.
4. Run the pipeline: `python app.py`

## Prompt Engineering Techniques Used
- **Role Prompting**: Every step assigns a specific role (e.g., "B2B content strategist", "Fact-checking assistant").
- **Zero-Shot Prompting**: Used for Intent Classification and Summarization to enforce strict JSON schemas without bias.
- **One-Shot Prompting**: Used for SEO & Social post generation to show the exact key structure required.
- **Few-Shot Prompting**: Used in Outline generation to demonstrate the difference between GOOD (safe) and BAD (hallucinated) claims.

## Hallucination Control
- **Prompt Constraints**: The `BLOG_WRITER` prompt explicitly forbids inventing statistics, names, and guaranteed outcomes.
- **Post-Generation Verification**: A dedicated step (`HALLUCINATION_SYSTEM_PROMPT`) scans the final text specifically to extract and flag numerical claims or competitor mentions for human review.

## Known Limitations & Future Improvements
- **Limitation**: Strict JSON parsing can sometimes fail if the model adds conversational text. `output_parser.py` mitigates this, but an improvement would be using native JSON-mode API features if supported.
- **Future**: Add a Streamlit UI for non-technical marketing teams to input parameters easily.