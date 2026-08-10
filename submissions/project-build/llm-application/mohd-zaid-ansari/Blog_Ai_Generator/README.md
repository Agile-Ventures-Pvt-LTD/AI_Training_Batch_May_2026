# Blog Generator AI Project

## Participant Name

Mohd Zaid Ansari

## Description

This project is an end-to-end blog generation application built using Python and the Groq API. It accepts business-related inputs from users and generates:

* Blog Intent Analysis
* Input Summary
* Blog Outline
* Full Blog Draft
* SEO Metadata
* LinkedIn Post
* Quality Review
* Hallucination Check

The project demonstrates multiple prompt engineering techniques including Role Prompting, Zero-Shot, One-Shot, Few-Shot Prompting, Reasoning Summaries, and Hallucination Control.

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

3. Run the application:

```bash
python app.py
```

## Required Libraries

* groq
* python-dotenv
* json
* pathlib
* re

Install using:

```bash
pip install -r requirements.txt
```

## Assumptions

* User provides at least 3 key points.
* User provides at least 2 SEO keywords.
* No external knowledge or RAG is used.
* Content is generated only from user-provided information.

## Output

The application generates a structured JSON output containing:

* Blog Intent Analysis
* Input Summary
* Blog Outline
* Final Blog
* SEO Metadata
* LinkedIn Post
* Quality Review
* Hallucination Check

Sample output:

```text
outputs/sample_blog_output.json
```

## Model Used

* llama-3.3-70b-versatile
* Groq API
