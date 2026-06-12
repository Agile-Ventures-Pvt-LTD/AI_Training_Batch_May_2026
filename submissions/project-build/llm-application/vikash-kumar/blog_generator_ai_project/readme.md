# AI-Powered Blog Generator

## Overview

This project builds an end-to-end Blog Generator using:

- Groq API
- Python
- Prompt Engineering
- Structured JSON Outputs

No RAG, vector databases, embeddings, web search, or external retrieval systems are used.

---

## Features

1. Blog Intent Classification
2. Input Summarization
3. Blog Outline Generation
4. Full Blog Creation
5. SEO Metadata Generation
6. LinkedIn Post Generation
7. Quality Review
8. Hallucination Detection
9. JSON Export
10. Input Validation

---

## Prompt Engineering Techniques

### Role Prompting

- Content Strategist
- Business Analyst
- Content Architect
- SEO Writer
- Editorial Reviewer
- Fact Checking Assistant

### Zero Shot

- Intent Classification
- Quality Review
- Hallucination Analysis

### One Shot

- SEO Metadata
- LinkedIn Post

### Reasoning Summary

Model is instructed to think carefully and return concise reasoning summaries.

### Hallucination Control

The model is explicitly instructed:

- Not to invent facts
- Not to invent statistics
- Not to invent customer names
- Not to invent certifications
- Not to invent awards

---

## Setup

Create virtual environment:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create .env:

```text
GROQ_API_KEY=your_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Run:

```bash
python app.py
```

---

## Output

Generated output is saved to:

```text
outputs/sample_blog_output.json
```

---

## Known Limitations

- Depends on model quality
- Long inputs may increase latency
- Hallucination detection is heuristic

---

## Future Improvements

- Streamlit UI
- Markdown export
- Multi-title generation
- Regeneration workflow
- Token usage tracking
- User feedback loop