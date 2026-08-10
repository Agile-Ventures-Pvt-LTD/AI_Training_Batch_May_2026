# AI-Powered Blog Generator using Groq and Python

## Overview

This project is an AI-powered blog generation application built using Python and the Groq API. It generates a complete blog package from structured marketing inputs.

The application performs:

1. Blog Intent Classification
2. Input Summarization
3. Blog Outline Generation
4. Full Blog Generation
5. SEO Metadata Generation
6. LinkedIn Post Generation
7. Quality Review
8. Hallucination Check
9. JSON Export

---

## Project Structure

```text
project/
│
├── app.py
├── config.py
├── groq_client.py
├── prompts.py
├── validators.py
├── output_parser.py
│
├── outputs/
│   └── sample_blog_output.json
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Create a `.env` file

```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

3. Run the application

```bash
python app.py
```

---

## Prompt Engineering Techniques Used

* Role Prompting
* Zero-Shot Prompting
* One-Shot Prompting
* Few-Shot Prompting
* Structured JSON Output
* Reasoning Summary
* Hallucination Control Instructions

---

## Hallucination Control

The application reduces hallucinations by:

* Using only user-provided information
* Preventing invented facts and statistics
* Avoiding unsupported claims
* Running a hallucination checklist on the final blog
* Flagging claims requiring verification

---

## Output

The final output contains:

* Blog Intent Analysis
* Input Summary
* Blog Outline
* Full Blog
* SEO Metadata
* LinkedIn Post
* Quality Review
* Hallucination Check
* Generation Metadata

The output is saved as:

```text
outputs/sample_blog_output.json
```

---

## Known Limitations

* Output quality depends on user input quality.
* Generated content should be reviewed before publishing.
* The application does not use external knowledge sources or RAG.

---

## Future Improvements

* Streamlit UI
* Blog regeneration with feedback
* Markdown export
* Additional quality metrics

