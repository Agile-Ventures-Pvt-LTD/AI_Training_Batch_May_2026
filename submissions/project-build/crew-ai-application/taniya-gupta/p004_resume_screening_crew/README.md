# P004: AI Resume Screening and Interview Planning Using CrewAI

A system built using CrewAI that does screening candidate resumes against a job description, calculates scores based on 8-categories, performs gap analysis and prepares personalized interview questions.
---

## 1. Project Overview

Recruiters and hiring managers often review multiple resumes manually for a
single open role. This process can be time-consuming and inconsistent, especially
when the role requires a mix of technical skills, project experience, and
communication ability.
The goal of this project is to build a CrewAI-based multi-agent system where
multiple specialized agents work together in a sequential workflow.

---

## 2. Environment Variables

Create a `.env` file using the `.env.example` template:

```env
GROQ_API_KEY=your-api-key
GROQ_MODEL=llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs
```

---

## 3. Required Multi-Agent Design

It uses **7 specialized agents** executing in a sequential process:

| Agent | Assigned Tools |
|---|---|
| **Job Description Analyst** | `read_job_description_tool` |
| **Resume Information Extractor** | `read_resume_tool` |
| **Skill and Experience Matcher** | `load_screening_rubric_tool`, `score_calculator_tool`, `skill_matcher_tool` |
| **Gap Analyst** | `skill_matcher_tool` |
| **Technical Interview Planner** | None (Uses LLM) |
| **Quality Assurance Reviewer** | `validate_report_schema_tool` |
| **Final Recommendation Specialist** | `save_report_tool`, `validate_report_schema_tool` |

---


## 4. Output Report Format

The final JSON output format conforms to the following schema:
```json
{
  "candidate_id": "CAND-001",
  "candidate_name": "Rohan Mehta",
  "role_title": "AI Engineer",
  "overall_score": 32,
  "max_score": 40,
  "percentage": 80.0,
  "recommendation": "STRONG_MATCH",
  "executive_summary": "...",
  "strengths": [
    "..."
  ],
  "gaps": [
    "..."
  ],
  "interview_focus_areas": [
    "..."
  ],
  "interview_questions": {
    "technical_questions": [
      "..."
    ],
    "project_deep_dive_questions": [
      "..."
    ],
    "scenario_questions": [
      "..."
    ],
    "gap_validation_questions": [
      "..."
    ]
  },
  "evidence": [
    "..."
  ],
  "human_review_note": ""
}
```

---

## 5. Setup 

Create the venv:
```bash
uv venv
```

Activate the virtual environment

Install dependencies:
```bash
uv pip install -r requirements.txt
```

### Running Screening
Run screening for one candidate:
```bash
python -m src.main --candidate-id CAND-001
```

Run sample screening for required candidates [CAND-001,CAND-002,CAND-003]:
```bash
python -m src.main --run-sample-screening
```

### Running Tests
Run pytest tests:
```bash
pytest tests/
```

Run evaluation tests:
```bash
pytest evals/
```

---

## 6. Crew AI workflow
The process workflow implemented is sequential, that means the agents will run in a sequential manner.
```bash
jd_analyst -> resume_extractor -> skill_matcher -> gap_analyst -> interview_planner -> reviewer ->  final_recommender
```

## 6.Challenges, Limitations & Future Improvements

### Challenges faced during building
- Schema generation, implementation and testing was time taking but achieveable
- Groq rate limit error and endpoint error (I had tried using litellm)

### Limitations
- Depend on Groq API limits.

### Future Improvements
- To implement sztreamlit for better UI integration.
- Report generation as .md

---
To note: 
- Python version that was tested with this project is 3.13
- Percentage score is rounded off by 2
- I have also enabled tracing as true in crew ai
- All test cases have been passed successfully
- The deepeval tests implemented for this project are AnswerRelevancyMetric, FaithfulnessMetric, ToolCorrectnessMetric
- I have also implemented Logger in this project


# Author
Taniya Gupta