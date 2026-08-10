# Resume Screening Crew

## Overview

Resume Screening Crew is a multi-agent AI system built using **CrewAI** and **Groq LLM** to automate candidate screening against a job description. The system extracts information from resumes, evaluates candidate-job fit, identifies skill gaps, generates interview questions, and produces a structured hiring recommendation.

The project follows a modular architecture with dedicated agents, reusable tools, structured outputs using Pydantic, and configurable execution through environment variables.

---

# Features

* Multi-agent workflow using CrewAI
* Automated Job Description analysis
* Resume information extraction
* Skill matching
* Candidate scoring
* Gap analysis
* Interview question generation
* Hiring recommendation
* Structured JSON reports
* Report validation
* Configurable environment
* Modular tool-based architecture

---

# Architecture

```
Job Description
        │
        ▼
JD Analyst Agent
        │
        ▼
Resume Extractor Agent
        │
        ▼
Skill Matching Agent
        │
        ▼
Gap Analysis Agent
        │
        ▼
Interview Planning Agent
        │
        ▼
Recommendation Agent
        │
        ▼
Report Review Agent
        │
        ▼
JSON Report
```

---

# Project Structure

```
PB4/

├── data/
│
├── logs/
│
├── outputs/
│   ├── reports/
│   ├── benchmark_results.json
│   ├── sample_output.json
│   └── sample_run.txt
│
├── src/
│   ├── prompts/
│   ├── tools/
│   ├── agents.py
│   ├── config.py
│   ├── crew.py
│   ├── logger.py
│   ├── main.py
│   ├── output_writer.py
│   ├── schemas.py
│   ├── scoring.py
│   └── tasks.py
│
├── tests/
│
├── requirements.txt
├── README.md
└── .env.example
```

---

# Agents

| Agent                   | Responsibility                        |
| ----------------------- | ------------------------------------- |
| Job Description Analyst | Extract job requirements              |
| Resume Extractor        | Extract structured resume information |
| Skill Matcher           | Compare candidate against JD          |
| Gap Analyst             | Identify missing skills               |
| Interview Planner       | Generate interview questions          |
| Recommendation Agent    | Produce final recommendation          |
| Report Reviewer         | Validate final report                 |

---

# Tools

* read_job_description_tool
* read_resume_tool
* candidate_index_lookup_tool
* batch_candidate_loader_tool
* skill_matcher_tool
* load_screening_rubric_tool
* score_calculator_tool
* save_report_tool
* validate_report_schema_tool

---

# Technologies

* Python 3.13
* CrewAI 0.114.0
* LangChain
* Groq
* Pydantic
* Pandas
* Rich
* Pytest

---

# Installation

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```text
GROQ_API_KEY=YOUR_API_KEY

GROQ_MODEL=llama-3.3-70b-versatile

TEMPERATURE=0

DATASET_PATH=data/p004_resume_screening_crew_dataset

OUTPUT_PATH=outputs

LOG_PATH=logs/app.log
```

---

# Running the Project

Run a candidate screening.

```bash
python src/main.py --candidate-id CAND-001
```

---

# Running Tests

Execute all tests.

```bash
pytest
```

---

# Workflow

1. Load Job Description
2. Load Resume
3. Extract Candidate Information
4. Match Skills
5. Calculate Candidate Score
6. Analyze Skill Gaps
7. Generate Interview Questions
8. Produce Hiring Recommendation
9. Validate Report
10. Save Final Report

---

# Outputs

Generated reports are saved in:

```
outputs/reports/
```

Additional files:

```
benchmark_results.json

sample_output.json

sample_run.txt
```

---

# Configuration

All configurable values are stored outside the source code.

Examples include:

* Groq API Key
* Model Name
* Dataset Location
* Output Folder
* Log File

---

# Testing

The project includes tests for:

* Reader Tools
* Matching Tools
* Scoring Tools
* Report Tools
* Agents
* Tasks
* Crew
* Main Execution

---

# Assumptions

* Dataset follows the expected directory structure.
* Candidate IDs are unique.
* Job description is available before execution.
* Groq API key is configured.
* Resume files are in Markdown format.

---

# Limitations

* Supports one job description per execution.
* Scoring is rule-based.
* Resume parsing assumes a consistent document format.
* LLM output quality depends on the selected model.

---

# Future Improvements

* Parallel agent execution
* Vector database retrieval
* Resume PDF parsing
* Web dashboard
* Human review interface
* Multiple job descriptions
* Historical candidate tracking
* Recruiter feedback loop

---

## Participant

Mohammad Anas
