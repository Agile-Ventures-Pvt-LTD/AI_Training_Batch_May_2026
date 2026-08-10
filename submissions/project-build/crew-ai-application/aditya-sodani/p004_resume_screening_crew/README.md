# AI Resume Screening and Interview Planning System (CrewAI)

## Overview

This project implements a multi-agent resume screening system using CrewAI. It automates the initial screening of candidates by comparing resumes against a job description, assigning a score based on a defined rubric, identifying strengths and gaps, and generating interview questions.

The output is a structured screening report that helps recruiters and hiring managers quickly understand candidate fit.

---

## Business Problem

Resume screening is often manual, time-consuming, and inconsistent. Different reviewers may evaluate candidates differently, and interview preparation is not always aligned with role requirements.

This system aims to make the process more structured, consistent, and efficient by generating a standardized report based on the job description and resume content.

---

## Features

- Multi-agent workflow using CrewAI
- Resume and job description analysis
- Skill matching and gap identification
- Scoring using an 8-category rubric
- Candidate-specific interview question generation
- Structured JSON output reports
- Pytest-based testing
- Evaluation checks (DeepEval-style)

---

## Project Structure

```
p004_resume_screening_crew/
│
├── data/
│   ├── metadata/
│   ├── resumes/
│   └── job_description/
│
├── src/
│   ├── config.py
│   ├── main.py
│   ├── crew.py
│   ├── agents.py
│   ├── tasks.py
│   ├── tools.py
│   ├── scoring.py
│   ├── schemas.py
│   └── output_writer.py
│
├── tests/
├── evals/
├── outputs/
├── requirements.txt
└── README.md
```

---

## Setup

Create and activate a virtual environment:

```
uv venv
.venv\Scripts\activate
```

Install dependencies:

```
uv pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=
DATASET_PATH=data
OUTPUT_PATH=outputs
```

---

## Running the Project

Run screening for a candidate:

```
python src/main.py --candidate-id CAND-001
```


## Running Tests

Run all tests:

```
pytest tests/
```

Run integration tests:

```
pytest -m integration
```

---

## Running Evaluation

```
pytest evals/
```

Evaluation covers:
- recommendation consistency
- report structure validity
- interview question quality
- basic groundedness checks

---

## Agents

- Job Description Analyst: extracts key requirements from the JD  
- Resume Extraction Agent: structures candidate profile  
- Skill Matching Agent: compares candidate with JD  
- Interview Planning Agent: generates interview questions  
- Final Recommendation Agent: compiles final report  

---

## Tools

- read_job_description_tool  
- read_resume_tool  
- candidate_index_lookup_tool  
- load_screening_rubric_tool  
- score_calculator_tool  
- save_report_tool  

---

## Output

Each run generates a report:

```
outputs/CAND-001_screening_report.json
```

The report includes:
- score and recommendation
- strengths and gaps
- interview focus areas
- interview questions
- supporting evidence

---

## Limitations

- LLM outputs may vary slightly
- Rate limits may affect runtime
- Skill matching is rule-based
- The system should not be used as a final hiring decision tool

---

## Future Improvements

- semantic skill matching
- batch candidate comparison
- UI dashboard
- improved evaluation metrics
- candidate ranking system

