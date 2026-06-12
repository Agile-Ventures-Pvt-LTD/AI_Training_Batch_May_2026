# AI-Powered Blog Generator for Marketing Teams

 application that generates a complete blog package from structured marketing inputs using the Groq API.

## What this project does
- Validates user input for blog generation
- Classifies blog intent
- Summarizes user-provided notes
- Generates a structured blog outline
- Produces a polished blog draft
- Generates SEO metadata and a LinkedIn post
- Reviews blog quality and flags hallucination risk
- Saves the final package as JSON

## Install
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
 pip install -r requirements.txt
```

##
```

```bash
python main.py sample_input.json
```

## Files
- `app.py` - 
- `groq_client.py` - 
- `prompt.py` - 
- `validators.py` - 
- `output_parser.py` - 
- `

## Prompt engineering used
  Role prompting for each task
- Zero-shot prompting for quality review and hallucination check
- Few-shot prompting for blog outline generation
- One-shot prompting for SEO + LinkedIn output
- Structured JSON output schemas for easy parsing
- Explicit hallucination control rules in prompts

## Hallucination control
- Prompts instruct the model not to invent facts, statistics, awards, or customer names
- The model is asked to use only user-provided input
- A hallucination checklist step flags unsupported claims and verification needs

