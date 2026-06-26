# AI Resume Screening and Interview Planning Crew Using CrewAI

# Overview
We are going to create the Resume Screening Crew who is going to analyse the Job Description and candidate resume.

Then the job description analyst agent will analyse the job description.

Then Resume Extraction Agent will come into the picture which extracts the candidate resume.

Then Skill and Experience Matching Agent will analyse the skills and experience

Then Interview Planning Agent will plan the questions accordingly.

The Final Recommendation Agent is going to give the final recommendation about the candidate according to the job descriptions.

#  Project Context
Recruiters and hiring managers often review multiple resumes manually for a 
single open role. This process can be time-consuming and inconsistent, especially 
when the role requires a mix of technical skills, project experience, and 
communication ability.

The goal of this project is to build a CrewAI-based multi-agent system where 
multiple specialized agents work together in a sequential workflow.

# Business Problem
Hiring teams often face the following challenges:
1. Reviewing resumes manually takes time.
2. Screening criteria may vary between reviewers.
3. Interview questions are not always aligned with role requirements.
4. Candidate strengths and gaps are not always documented clearly.
5. Resume claims may not be linked back to evidence.
6. Recruiters need a structured first-level screening report for discussion with 
hiring managers.
The proposed system should assist the screening process by generating a 
structured report based only on the provided job description and resume content.

# Product Goal
Build a CrewAI-based resume screening crew that can:
1. Analyze a job description.
2. Analyze candidate resumes.
3. Extract candidate skills, projects, experience, education, and certifications.
4. Compare resume content with job requirements.
5. Calculate a fitment score using a fixed scoring rubric.
6. Identify candidate strengths and gaps.
7. Generate role-specific interview questions.
8. Produce a structured JSON screening report.
9. Save the final report to the outputs/ folder.
10. Provide pytest tests for tools, scoring, schema, and crew execution
11. Provide DeepEval-style or equivalent evaluation checks for generated 
reports.

# Target Users
Primary User: Recruiter / Talent Acquisition Associate

Uses the system to generate a first-level screening report.


Secondary User: Hiring Manager

Uses the report to understand candidate fit, gaps, and interview focus areas.


Optional User:Technical Interview Panel

Uses the generated questions to conduct a structured interview.


# Scope Boundary
This system is a screening-support assistant.
It should not be presented as a final hiring decision system.
The final report should use one of the approved recommendation labels:
STRONG_MATCH
MODERATE_MATCH
WEAK_MATCH
NEEDS_MANUAL_REVIEW

These labels should be treated as screening support indicators only. A human 
reviewer must make the final recruitment decision.


# Dataset Folder Structure
After extraction, the dataset should follow this structure:
p004_resume_screening_crew_dataset/
│
├── job_description/
│   └── jd_ai_engineer.md
│
├── resumes/
│   ├── candidate_001_rohan_mehta.md
│   ├── candidate_002_priya_sharma.md
│   ├── candidate_003_neha_gupta.md
│   ├── candidate_004_arjun_nair.md
│   └── candidate_005_sara_khan.md
│
├── metadata/
│   ├── candidate_index.csv
│   ├── screening_rubric.json
│   └── skill_synonyms.json
│
└── README_dataset.md


# Dataset Description
## 10.1 Job Description
File:
job_description/jd_ai_engineer.md
The job description is for an AI Engineer role.
It includes requirements around:
1. Python programming
2. SQL and database basics
3. API integration
4. LLM application development
5. LangChain or agent framework exposure
6. RAG fundamentals
7. Vector database awareness
8. Testing practices
9. Git/GitHub familiarity
10. Communication and problem-solving skills

## 10.2 Candidate Resumes
The dataset includes five synthetic candidate resumes.
Candidate ID
Candidate Name
Resume File
CAND-001
CAND-002
CAND-003
CAND-004
CAND-005
Rohan Mehta
Priya Sharma
Neha Gupta
Arjun Nair
Sara Khan
Participants must screen at least:
CAND-001
CAND-002
CAND-003
candidate_001_roha
n_mehta.md
candidate_002_priy
a_sharma.md
candidate_003_neha
_gupta.md
candidate_004_arju
n_nair.md
candidate_005_sara
_khan.md
Strong submissions may screen all five candidates.

## 10.3 Candidate Index
File:
metadata/candidate_index.csv

Expected columns:
candidate_id,candidate_name,resume_file,years_experience,current_role,
primary_skills

Purpose:
The candidate index helps the system locate the correct resume file for a given 
candidate ID.

## 10.5 Skill Synonyms
File:
metadata/skill_synonyms.json
This file helps participants normalize similar terms.
Example:

{
"llm": ["large language model", "genai", "generative ai"],
"rag": ["retrieval augmented generation", "retrieval-augmented 
generation"],
"api": ["rest api", "fastapi", "flask api"],
"agent_frameworks": ["langchain", "langgraph", "crewai", "agents"]
}

Participants may use this file in the skill matching tool.

# Technology Stack

Minimum required:
Python
CrewAI
LLM provider such as Groq or OpenAI
python-dotenv
pydantic
pytest

Recommended:
crewai-tools
pandas
rich
deepeval

Optional:
streamlit
gradio
jinja2

#  Environment Variables
```python
Expected .env.example:
GROQ_API_KEY=""
GROQ_MODEL=llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs

```

# Recommended Project Structure
p004_resume_screening_crew/
│
├── README.md
├── .env.example
├── requirements.txt
│
├── data/
│   └── p004_resume_screening_crew_dataset/
│
├── src/
│   ├── config.py
│   ├── main.py
│   ├── crew.py
│   ├── agents.py
│   ├── tasks.py
│   ├── tools.py
│   ├── schemas.py
│   ├── scoring.py
│   └── output_writer.py
│
├── tests/
│   ├── test_tools.py
│   ├── test_scoring.py
│   ├── test_output_schema.py
│   └── test_crew_flow.py
│
├── evals/
│   ├── test_report_evals.py
│   └── evaluation_prompts.md
│
└── outputs/
    ├── CAND-001_screening_report.json
    ├── CAND-002_screening_report.json
    ├── CAND-003_screening_report.json
    └── execution_log.txt

# 15. Required Sequential Workflow
The workflow must run in sequence.
Minimum required sequence:
Input: Job Description + Candidate Resume
   ↓
Job Description Analyst Agent
   ↓
Resume Extraction Agent
   ↓
Skill and Experience Matching Agent
   ↓
Interview Planning Agent
   ↓
Final Recommendation Agent
   ↓
Output: Candidate Screening Report
The final report must depend on the outputs of the earlier agents.

# Required Multi-Agent Design

## Agent 1: Job Description Analyst Agent
Responsibility: Understand the job description.
Inputs:
jd_ai_engineer.md
Expected output file/object:
jd_analysis.json
Expected output structure:
```python
{
"role_title": "",
"required_skills": [],
"preferred_skills": [],
"responsibilities": [],
"experience_expectation": "",
"evaluation_criteria": []}
```

## Agent 2: Resume Extraction Agent
Responsibility: Extract structured candidate information from the resume.
Inputs:
candidate resume file
Expected output file/object:
resume_profile.json
Expected output structure:
```python
{
"candidate_id": "",
"candidate_name": "",
"current_role": "",
"years_experience": "",
"skills": [],
"projects": [],
"experience_summary": [],
"education": [],
"certifications": []}
```

## Agent 3: Skill and Experience Matching Agent
Responsibility: Compare JD requirements with the candidate profile.
Inputs:
jd_analysis.json
resume_profile.json
screening_rubric.json
skill_synonyms.json
Expected output file/object:
match_score.json
Expected output structure:
```python
{
"matched_skills": [],
"partial_matches": [],
"missing_skills": [],
"category_scores": {
"python_programming": 0,
"sql_database_skills": 0,
"api_integration": 0,
"llm_application_development": 0,
"agent_frameworks": 0,
"rag_understanding": 0,
"testing_and_quality": 0,
"communication": 0
},
"overall_score": 0,
"max_score": 40,
"percentage": 0,
"recommendation_band": ""}


## Agent 4: Interview Planning Agent
Responsibility: Generate candidate-specific interview questions.
Inputs:
jd_analysis.json
resume_profile.json
match_score.json
Expected output file/object:
interview_plan.json
Expected output structure:

```python
{
"interview_focus_areas": [],
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []}
```

## Agent 5: Final Recommendation Agent
Responsibility: Produce the final screening report.
Inputs:
jd_analysis.json
resume_profile.json
match_score.json
interview_plan.json
Expected output file/object:
candidate_screening_report.json
Expected output structure:
```python
{
"candidate_id": "",
"candidate_name": "",
"role_title": "",
"overall_score": 0,
"max_score": 40,
"percentage": 0,
"recommendation": "STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | 
NEEDS_MANUAL_REVIEW",
"executive_summary": "",
"strengths": [],
"gaps": [],
"interview_focus_areas": [],
"interview_questions": {
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []
},
"evidence": [],
"human_review_note": ""}
```

# Tool Descriptions
1. read_job_description_tool
2.  read_resume_tool
3.  candidate_index_lookup_tool
4. load_screening_rubric_tool
5. score_calculator_tool
6.  save_report_tool
7. validate_report_schema_tool
8. skill_matcher_tool

# Final Report Schema
Every final report must contain:

```python
{
"candidate_id": "",
"candidate_name": "",
"role_title": "",
"overall_score": 0,
"max_score": 40,
"percentage": 0,
"recommendation": "",
"executive_summary": "",
"strengths": [],
"gaps": [],
"interview_focus_areas": [],
"interview_questions": {
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []
},
"evidence": [],
"human_review_note": ""
}
```

Required human_review_note:
This is an AI-assisted screening report based on the provided resume 
and job description. A human reviewer should validate the 
recommendation before making any recruitment decision.

# Required Commands

## Setup
```python
uv venv
.venv\Scripts\activate
```

```python
uv pip install -r requirements.txt

python src/main.py --candidate-id CAND-001

python src/main.py --run-sample-screening

pytest tests/

pytest -m integration

deepeval test run evals/
```

# Example Evaluation Fallback Using pytest
```python
def test_report_recommendation_matches_score_band():
    report = load_report("outputs/CAND-001_screening_report.json")
    percentage = report["percentage"]
    recommendation = report["recommendation"]
if percentage >= 80:
assert recommendation == "STRONG_MATCH"
elif percentage >= 60:
assert recommendation == "MODERATE_MATCH"
elif percentage >= 40:
assert recommendation == "WEAK_MATCH"
else:
assert recommendation == "NEEDS_MANUAL_REVIEW"
```

