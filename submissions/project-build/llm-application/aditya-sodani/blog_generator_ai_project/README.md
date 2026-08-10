# AI Blog Generator

## Overview

AI Blog Generator is an LLM-powered application that generates high-quality blog content from user inputs. The system analyzes the user's requirements, identifies the blog intent, creates a structured outline, generates the complete blog, and performs an automated quality review.

The project demonstrates prompt engineering, structured JSON outputs, multi-step content generation, and automated content evaluation using Large Language Models (LLMs).

---

## Features

* Intent analysis from user requirements
* Audience and content-angle identification
* Blog outline generation
* Full blog generation
* Automated quality review
* Structured JSON outputs
* Modular prompt design
* Groq API integration

---

## Project Workflow

### Step 1: Intent Analysis

The user's blog requirements are analyzed to determine:

* Blog intent
* Target reader maturity
* Recommended content angle
* Reasoning summary

### Step 2: Blog Outline Generation

Based on the identified intent, the system creates:

* Title suggestions
* Section structure
* Key discussion points
* Content flow

### Step 3: Blog Generation

The complete blog is generated using:

* User input
* Blog intent
* Generated outline

### Step 4: Quality Review

The generated blog is evaluated on:

* Relevance
* Clarity
* Structure
* Tone alignment
* SEO usage
* Hallucination risk
* CTA effectiveness

The reviewer also provides:

* Strengths
* Improvement areas
* Final quality summary

---

## Project Structure

```text
blog_generator_ai_project/
│
├── app.py
├── prompts.py
├── output_parser.py
├── groq_client.py
├── requirements.txt
├── .env
└── README.md
```

### Files Description

#### app.py

Main application entry point.

Responsibilities:

* Collect user input
* Execute blog generation pipeline
* Parse outputs
* Display final results

#### prompts.py

Contains all prompt templates used in the workflow.

Examples:

* Intent Prompt
* Outline Prompt
* Blog Generation Prompt
* Quality Review Prompt

#### groq_client.py

Handles communication with the Groq API.

Responsibilities:

* API initialization
* Sending prompts
* Receiving model responses

#### output_parser.py

Converts model responses into Python dictionaries using JSON parsing.

Responsibilities:

* Validate model output
* Handle parsing errors
* Return structured data

---



### Create Virtual Environment

```bash
uv venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```


### Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=model
```

---

## Running the Project

```bash
python app.py
```

---

## Sample Input

```text
Topic: AI in Customer Support

Target Audience: Customer Support Managers

Key Points:
- Faster response times
- Reduced operational costs
- 24/7 availability

Call To Action:
Book a demo
```

---

## Sample Output

### Intent Analysis

```json
{
  "blog_intent": "Educational/Informative",
  "target_reader_maturity": "Intermediate",
  "recommended_content_angle": "Problem-Agitate-Solve",
  "reasoning_summary": "Focuses on educating customer support leaders about AI benefits."
}
```

### Quality Review

```json
{
  "scores": {
    "relevance": 9,
    "clarity": 8,
    "structure": 9,
    "tone_alignment": 8,
    "seo_usage": 7,
    "hallucination_risk": 2,
    "cta_effectiveness": 8
  }
}
```

---

## Technologies Used

* Python
* Groq API
* Large Language Models (LLMs)
* Prompt Engineering
* JSON Parsing
* Environment Variables

---

## Challenges Faced

* Ensuring valid JSON outputs from the LLM
* Handling markdown-wrapped responses
* Managing parsing failures
* Designing structured prompts
* Maintaining consistency across generation stages

---
