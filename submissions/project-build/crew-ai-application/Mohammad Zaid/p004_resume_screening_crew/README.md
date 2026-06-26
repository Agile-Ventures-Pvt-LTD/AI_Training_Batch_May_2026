<!-- 1. Project overview.
2. Business use case.
3. Technology stack.
4. Dataset description.
5. Setup instructions.
6. Environment variables.
7. How to run candidate screening.
8. How to run sample screening.
9. How to run pytest tests.
10. How to run evaluation checks.
11. Agent list and responsibilities.
12. Tool list and responsibilities.
13. Sequential orchestration explanation.
14. Output report format.
15. Known limitations.
16. Future improvements. -->


# Output
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

# P004 Resume Screening Crew Dataset

This is a synthetic dataset for **P004: AI Resume Screening and Interview Planning Crew Using CrewAI**.

The dataset is aligned with the revised PRD and contains only the participant-facing files required by the project.

## Folder Structure for dataset

```text
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
```
### Folder Structure

```text

p004_resume_screening_crew/
│
├── README.md
├── .env.example
├── requirements.txt
│
├── data/
│ └── p004_resume_screening_crew_dataset/
│
├── src/
│ ├── config.py
| |- all_crew.py
│ ├── main.py
│ ├── crew.py
│ ├── agents.py
│ ├── tasks.py
│ ├── tools.py
│ └── output_writer.py
│
├── tests/
│ ├── test_tools.py
│ ├── test_scoring.py
│ ├── test_output_schema.py
│ └── test_crew_flow.py
│
│
└── outputs/
 ├── CAND-001_screening_report.json
 ├── CAND-002_screening_report.json
 ├── CAND-003_screening_report.json
 └── execution_log.txt

```
## Candidate IDs

| Candidate ID | Candidate Name | Resume File |
|---|---|---|
| CAND-001 | Rohan Mehta | candidate_001_rohan_mehta.md |
| CAND-002 | Priya Sharma | candidate_002_priya_sharma.md |
| CAND-003 | Neha Gupta | candidate_003_neha_gupta.md |
| CAND-004 | Arjun Nair | candidate_004_arjun_nair.md |
| CAND-005 | Sara Khan | candidate_005_sara_khan.md |

## Required Candidate Screenings

```text
CAND-001
CAND-002
CAND-003
```

Strong submissions may screen all five candidates.

## Scoring Rubric

The rubric has exactly 8 categories. Each category must be scored from 0 to 5.

Maximum score: 40

Categories:

```text
python_programming
sql_database_skills
api_integration
llm_application_development
agent_frameworks
rag_understanding
testing_and_quality
communication
```

## Bands

| Percentage | Recommendation |
|---:|---|
| 80–100 | STRONG_MATCH |
| 60–79 | MODERATE_MATCH |
| 40–59 | WEAK_MATCH |
| Below 40 | NEEDS_MANUAL_REVIEW |

## Requirements

```text
langchain>=1.3.6
langchain_community>=0.4.2
langchain_groq==1.1.3
python-dotenv>=1.2.2
ipykernel>=7.3.0
groq>=0.30.0,<1.0.0
crewai
crewai[tools]

```
