# AI-Powered Blog Generator

This project is a Groq + Python prototype that generates a complete marketing blog package from structured business inputs.

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file using `.env.example`:

```bash
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=you_model_name
```

3. Update `prompts.json` with the blog requirements.

4. Run:

```bash
python app.py
```

The generated package is saved to `outputs/sample_blog_output.json`.

## Prompt Engineering Techniques Used

- Role prompting: each step uses a specific role such as B2B content strategist, business analyst, SEO specialist, or fact-checker.
- Zero-shot prompting: quality review and hallucination checking use direct task instructions.
- One-shot prompting: SEO metadata and LinkedIn generation include sample input-output examples.
- Structured Inputs: JSON schemas are provided for classification, summary, outline, SEO, review, and hallucination checks.
- Reasoning summaries: analytical steps ask for concise reasoning summaries without long hidden chain-of-thought.

## Hallucination Control

The prompts instruct the model to use only user-provided inputs and avoid invented facts, statistics, customer names, awards, certifications, legal claims, financial results, guarantees, and case studies. A separate hallucination checklist flags claims requiring verification and recommends edits.

## Known Limitations

- The blog still requires human editorial review before publishing.
- JSON repair retries once, but badly malformed model responses can still fail.
- The app is terminal/file based and does not include a UI.

## Future Improvements

- Add a Streamlit or Gradio interface.
- Add Markdown export.