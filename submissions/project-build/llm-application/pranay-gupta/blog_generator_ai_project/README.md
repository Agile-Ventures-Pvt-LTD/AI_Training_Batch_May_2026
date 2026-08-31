# Blog Generator AI Project

A Python-based AI blog generator that uses Groq and a structured prompt template to create complete blog packages, including intent analysis, outlines, SEO metadata, blog content, and quality review output.

## Project Overview

This project is designed to generate long-form blogs from a marketing brief. It includes:
- Prompt templates for intent classification, outline creation, SEO metadata, blog drafting, and review
- Groq API integration via `groq_client.py`
- A notebook workflow in `app.ipynb` for interactive generation and experimentation
- A sample output file in `Outputs/sample_blog_output.json`

## Key Files

- `app.ipynb` - Notebook containing prompt setup and model call flow
- `prompts.py` - Prompt text templates used to structure AI output
- `groq_client.py` - Groq client initialization with environment variable support
- `validator.py` - Validation helper for environment variables and generated JSON output
- `main.py` - Entrypoint demonstrating validation and error handling
- `requirements.txt` - Python dependency list
- `pyproject.toml` - Project metadata and dependency declarations

## Requirements

- Python 3.11 or newer
- `groq` library
- `python-dotenv`
- `ipykernel` (for notebook support)


## Environment Setup

This project requires a Groq API key stored in a `.env` file at the project root.

Create a `.env` file with:

```text
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Run the notebook

Open `app.ipynb` in Jupyter or VS Code and execute the cells to:
1. load prompts
2. configure the Groq client
3. call the model
4. review generated blog output

### Run the Python entrypoint

Run `main.py` to verify environment setup and validate the sample output JSON:

```powershell
python main.py
```

### Validation and Error Handling

This project includes `validator.py` for:
- checking required environment variables before starting the Groq client
- parsing and validating AI-generated JSON output
- raising clear errors for missing keys, invalid JSON, or invalid field types

`groq_client.py` now verifies `GROQ_API_KEY` before creating the client.
`main.py` demonstrates safe startup and sample output validation.

## Notes

- The notebook stores reusable prompt templates such as `assistant_message_role`, `assistant_message_zero_shot`, `assistant_message_one_shot`, `assistant_message_few_shot`, and `assistant_message_self_consistency`.
- The prompt flow is designed to produce structured JSON output for blog intent, outline, SEO metadata, final blog content, quality review, and hallucination checks.
- If the Groq client fails to initialize, verify the `.env` file and the `GROQ_API_KEY` value.

## Improvements

To make this project production-ready, consider adding:
- A command-line interface for marketing briefs
- Validation of generated JSON output
- Error handling for API calls
- Unit tests for prompt formatting and output parsing
- A proper Python package entrypoint instead of the placeholder `main.py`
