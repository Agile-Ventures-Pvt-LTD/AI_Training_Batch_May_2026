
# Project Build -  AI Resume Screening and Interview Planning Crew Using CrewAI

## Participant Name

Simran Kaur

## Project Title
 AI Resume Screening and Interview Planning Crew Using CrewAI
## Description

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
10. Provide pytest tests for tools, scoring, schema, and crew execution.
11. Provide DeepEval-style or equivalent evaluation checks for generated reports.



## 
## How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
cd credit-card-agent-assignment
```

### 2. Create Virtual Environment


```bash
uv venv 
```

Activate:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```


### 3. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the Application

```bash
python -m app
```

### 5. Run Tests


```bash
pytest tests/test_tools.py

```

## Libraries / Packages Required


```text

ipykernel>=7.3.0
python-dotenv>=1.2.2
langchain-groq==0.3.8
langchain==0.3.20
langchain-community==0.3.19
langgraph==0.3.21
mermaid-python==0.1
chromadb>=0.5.0
langchain-chroma==0.1.4
sentence-transformers>=5.1.2
crewai>=0.114.0
pandas
```

 

## Output Explanation

### Example User Query


```

### Example Output

```text
The final answer should include:
Expected answer:
```text
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