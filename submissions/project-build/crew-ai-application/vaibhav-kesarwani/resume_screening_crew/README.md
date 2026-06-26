# Project Build - AI Resume Screening and Interview Planning Crew Using CrewAI

## Participant Name

**Vaibhav Kesarwani**

## Assignment Title

### AI Resume Screening and Interview Planning Crew Using CrewAI

## Project Overview

This is the Multi AI Agent which can use to evaluate the multiple resume at the same time and according to the job role which will help the hr and the hiring manager to make there task easier to todo but at the end ther will the detailed report created by the agent for the candidate so that can be reviewed by the hiring managers / recrutier.

---

## Business Use Case

Recruiters and hiring managers often review multiple resumes manually for a 
single open role. This process can be time-consuming and inconsistent, especially 
when the role requires a mix of technical skills, project experience, and 
communication ability.
The goal of this project is to build a CrewAI-based multi-agent system where 
multiple specialized agents work together in a sequential workflow.

### Business Problem

Hiring teams often face the following challenges:

1. Reviewing resumes manually takes time.
2. Screening criteria may vary between reviewers.
3. Interview questions are not always aligned with role requirements.
4. Candidate strengths and gaps are not always documented clearly.
5. Resume claims may not be linked back to evidence.
6. Recruiters need a structured first-level screening report for discussion with hiring managers.

The proposed system should assist the screening process by generating a structured report based only on the provided job description and resume content.

---

## Technology Stack

| Component              | Technology            |
| ---------------------- | --------------------- |
| Language               | Python 3.11+          |
| Framework              | Crew ai               |
| LLM Provider           | GROQ API              |
| Evaluation             | DeepEval              |
| Testing                | PyTest                |

---


## Dataset Description

Dataset consist the `job description` and the candidates `resumes` in the seprate folder and also ther is the `.csv` which contains all the information about the candidates which is actually parsed through the resume and stored in the .csv format.

#### Dataset Structure

```bash
data/p004_resume_screening_crew_dataset/
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
```

---

## Setup Instructions

### 1. Create Virtual Environment

```bash
uv venv
```

Activate the environment:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt #
```

---

## Environment Variables Required

Create a `.env` file:

```env
GROQ_API_KEY="..."
GROQ_MODEL=groq/llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs
CONFIDENT_API_KEY=...
```

---

## How to Run

It is bases on the user question which is asked by the agenet 

```bash
python -m src.main.py
```
---

if you really wanted to run the whole agent all together you can make the samll change in the main.py

```py
from src.crew import resume_screening_crew

while True: 
    question = input("\nAsk: ") 
    if question.lower() in ["quit", "exit", "stop"]: 
        break 
    
    result = resume_screening_crew.kickoff({"user_query" : question})

    print(result)
```

instead of this use this code in your main.py

```py
from src.crew import resume_screening_crew
    
result = resume_screening_crew.kickoff()

print(result)
```

### How to run pytest tests.

All the pytest files are present inside the `test/` folder which you can access to to run the test files like:

- test_tools.py
- test_crew_flow.py
- test_output_schema.py
- test_scoring.py

```bash
pytest tests/
```
To run the test file inside the `test/` folder

```py
def test_read_job_description():
    result = read_job_description()

    assert isinstance(result, JobDescriptionOutput)

    assert result.content != "" or result.error != ""
```

PyTest for the Validating the job description.


### How to run evaluation checks

---


## Agent list and responsibilities.

#### Agent 1: Job Description Analyst Agent

**Responsibility:** Understand the job description.

**Inputs**: `jd_ai_engineer.md`

**Expected output file:** `jd_analysis.json`

Expected output structure:
```json
{
    "role_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "experience_expectation": "",
    "evaluation_criteria": []
}
```

#### Agent 2: Resume Extraction Agent

**Responsibility:** Extract structured candidate information from the resume.

**Inputs:** candidate resume file

**Expected output file:** resume_profile.json

Expected output structure:

```json
{
"candidate_id": "",
"candidate_name": "",
"current_role": "",
"years_experience": "",
"skills": [],
"projects": [],
"experience_summary": [],
"education": [],
"certifications": []
}
```

#### Agent 3: Skill and Experience Matching Agent

**Responsibility:** Compare JD requirements with the candidate profile.

**Inputs:** 
- `jd_analysis.json`
- `resume_profile.json`
- `screening_rubric.json`
- `skill_synonyms.json`

**Expected output file:** `match_score.json`

Expected output structure:

```json
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
"recommendation_band": ""
```

#### Agent 4: Interview Planning Agent

**Responsibility:** Generate candidate-specific interview questions.

**Inputs:**

- `jd_analysis.json`
- `resume_profile.json`
- `match_score.json`

**Expected output file:** `interview_plan.json`

Expected output structure:

```json
{
"interview_focus_areas": [],
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []
}
```

Minimum required questions:

- 3 technical questions
- 2 project deep-dive questions
- 2 scenario questions
- 2 gap-validation questions


#### Agent 5: Final Recommendation Agent
**Responsibility:** Produce the final screening report.

**Inputs:**
- `jd_analysis.json`
- `resume_profile.json`
- `match_score.json`
- `interview_plan.json`

**Expected output file:** `candidate_screening_report.json`

Expected output structure:

```json
{
"candidate_id": "",
"candidate_name": "",
"role_title": "",
"overall_score": 0,
"max_score": 40,
"percentage": 0,
"recommendation": "STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | NEEDS_MANUAL_REVIEW",
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

#### Agent 6: Gap Analysis Agent
**Responsibility:** Identify missing or weak areas separately.

Expected output:

```json
{
"critical_gaps": [],
"moderate_gaps": [],
"areas_to_probe": []
}
```

#### Agent 7: Report Review Agent

**Responsibility:** Review final report for completeness, schema consistency, and  evidence quality.

Expected output:

```json
{
"report_complete": true,
"missing_sections": [],
"schema_valid": true,
"review_notes": []
}
```

---


## Tool list and responsibilities

Implemented tools are:

1. read_job_description_tool
2. read_resume_tool
3. candidate_index_lookup_tool
4. load_screening_rubric_tool
5. score_calculator_tool
6. save_report_tool
7. skill_matcher_tool
8. validate_report_schema_tool

---

## Task Reasoning

All the agents are making the `.md` files for there required task to do and with the proper outputs of ther e task.

Which can be notice inside the `task_reasoning/` folder which will give the better understanding about what agent is doing which task what are the outputs generated by them

```json
{
    "role_title": "AI Engineer",
    "required_skills": [
        "Python programming",
        "SQL and database basics",
        "REST API integration",
        "LLM application development",
        "Prompt engineering",
        "LangChain, LangGraph, CrewAI, or another agent framework",
        "RAG fundamentals",
        "Embeddings and vector database concepts",
        "Basic testing using pytest or equivalent",
        "Git and GitHub",
        "Clear technical communication"
    ],
    "preferred_skills": [
        "FastAPI or Flask",
        "Streamlit or Gradio",
        "Cloud deployment basics",
        "Docker basics",
        "MLOps or model monitoring awareness",
        "Evaluation frameworks for LLM applications",
        "Experience building internal automation tools"
    ],
    "responsibilities": [
        "Build Python-based AI applications using LLM APIs.",
        "Design and implement prompt-driven workflows for business use cases.",
        "Build retrieval-augmented generation prototypes using documents, embeddings, and vector databases.",
        "Integrate APIs and external tools into AI applications.",
        "Work with SQL databases for data retrieval and analysis.",
        "Build simple agentic workflows using frameworks such as LangChain, LangGraph, CrewAI, or similar tools.",
        "Write modular, readable, and testable Python code.",
        "Create unit tests and basic evaluation checks for AI application behavior.",
        "Use Git and GitHub for version control and collaboration.",
        "Communicate solution design, assumptions, limitations, and next steps clearly."
    ],
    "experience_expectation": "2 to 5 years",
    "evaluation_criteria": [
        "Ability to build working Python applications",
        "Practical LLM and GenAI application experience",
        "Understanding of RAG and retrieval workflows",
        "Experience with APIs, SQL, and integration",
        "Familiarity with agent frameworks",
        "Testing mindset and code quality",
        "Ability to explain technical decisions clearly"
    ]
}
```

Above is the JSON response of the agent which is generated using the job_description.md file inside the data folder.

---

## Future improvements.

The Future Improvements can be done to this project are:

1. Giving it the Proper UI which will also help the non coder people to use easily the streamlit tool can be used to make the UI.

2. Using the MCP server for the tools which will helps us to limit the token usage.

3. And, For to save more tokens we can also implement the code execution MCP technique which also help to reduce the token usage and calling the specific tool which is actually needed to do that task.