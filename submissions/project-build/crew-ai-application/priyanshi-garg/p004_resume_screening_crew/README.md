The README must include:

#  AI Resume Screening and Interview Planning Crew Using CrewAI

## 1. Project overview.
Recruiters and hiring managers often review multiple resumes manually for a 
single open role. This process can be time-consuming and inconsistent, especially 
when the role requires a mix of technical skills, project experience, and 
communication ability.
The goal of this project is to build a CrewAI-based multi-agent system where 
multiple specialized agents work together in a sequential workflow.
The system should:
1. Read a job description.
2. Read candidate resumes.
3. Extract structured candidate details.
4. Match candidate skills against job requirements.
5. Score candidate fit using a defined rubric.
6. Identify gaps and areas to probe.
7. Generate interview questions.
8. Produce a final screening report for human review.
This project is intended to demonstrate multi-agent orchestration, sequential 
task execution, tool integration, testing, and LLM output evaluation.


## Business use case.
Hiring teams often face the following challenges:
1. Reviewing resumes manually takes time.
2. Screening criteria may vary between reviewers.
3. Interview questions are not always aligned with role requirements.
4. Candidate strengths and gaps are not always documented clearly.
5. Resume claims may not be linked back to evidence.
6. Recruiters need a structured first-level screening report for discussion with 
hiring managers.
The proposed system should assist the screening process by generating a 
structured report based only on the provided job description and resume content

## Technology stack.
Python
CrewAI
LLM provider such as Groq or OpenAI
python-dotenv
pydantic
pytest
crewai-tool

## Dataset description.
### Job Description
File:
*job_description/jd_ai_engineer.md*
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
10.Communication and problem-solving skills

### Candidate Resumes
The dataset includes five synthetic candidate resumes.

### Candidate Index
File:
*metadata/candidate_index.csv*

Expected columns:
candidate_id,candidate_name,resume_file,years_experience,current_role,
primary_skills

Purpose:
The candidate index helps the system locate the correct resume file for a given 
candidate ID.
### Screening Rubric
File:
*metadata/screening_rubric.json*
The scoring rubric contains exactly 8 scoring categories.
Each category should be scored from 0 to 5.
Category
Score Range - 0-5
python_programming - 0-5
sql_database_skills - 0-5
api_integration - 0-5
llm_application_development - 0-5
agent_frameworks - 0-5
rag_understanding - 0-5
testing_and_quality - 0-5
communication - 0-5


## Setup instructions.
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

## Environment variables
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs

## How to run candidate screening.

## How to run sample screening.
run - python -m pytest tests/test_report_evals.py -v

## How to run pytest tests.
run - python -m pytest tests/test_recruitment_pipeline.py -v

## How to run evaluation checks.
run - python -m pytest evals/test_batch_evaluations.py -v

## Agent list and responsibilities.
1. Job Description Analyst Agent
Responsibility: Understand the job description

2. Resume Extraction Agent
Responsibility: Extract structured candidate information from the resume

3. Skill and Experience Matching Agent
Responsibility: Compare JD requirements with the candidate profile.

4. Interview Planning Agent
Responsibility: Generate candidate-specific interview questions.

5. Final Recommendation Agent
Responsibility: Produce the final screening report.

6. Gap Analysis Agent
Responsibility: Identify missing or weak areas separately.

7. Report Review Agent
Responsibility: Review final report for completeness, schema consistency, and 
evidence quality.

## Tool list and responsibilities.
1. read_job_description_tool
Purpose:
Reads the job description file.

2. read_resume_tool
Purpose:
Reads a candidate resume file

3. candidate_index_lookup_tool
Purpose:
Finds the resume file for a candidate ID.

4. load_screening_rubric_tool
Purpose:
Loads the scoring rubric from metadata/screening_rubric.json

5. score_calculator_tool
Purpose:
Calculates total score, percentage, and recommendation band

6. save_report_tool
Purpose:
Saves the final report to the outputs/ folder

7. skill_matcher_tool
Purpose:
Compares JD skills with candidate resume skills

8. validate_report_schema_tool
Purpose:
Validates that the final report contains all required fields

## Sequential orchestration explanation.
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

## Output report format.
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
Required human_review_note:
This is an AI-assisted screening report based on the provided resume 
and job description. A human reviewer should validate the 
recommendation before making any recruitment decision.

## Known limitations
API key rate limit error

## Future improvements
Impelement more custom tools and agent for the better screening and flow. 
Can add the concept of ATS score for resume screening

