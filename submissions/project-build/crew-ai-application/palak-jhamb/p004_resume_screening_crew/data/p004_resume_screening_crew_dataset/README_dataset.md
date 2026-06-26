# P004 Resume Screening Crew Dataset

This is a synthetic dataset for **P004: AI Resume Screening and Interview Planning Crew Using CrewAI**.

The dataset is aligned with the revised PRD and contains only the participant-facing files required by the project.

## Folder Structure

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

## Candidate IDs

| Candidate ID | Candidate Name | Resume File |
|---|---|---|
| CAND-001 | Rohan Mehta | candidate_001_rohan_mehta.md |
| CAND-002 | Priya Sharma | candidate_002_priya_sharma.md |
| CAND-003 | Neha Gupta | candidate_003_neha_gupta.md |
| CAND-004 | Arjun Nair | candidate_004_arjun_nair.md |
| CAND-005 | Sara Khan | candidate_005_sara_khan.md |

## Required Candidate Screenings

Participants must generate JSON screening reports for at least:

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

## Recommendation Bands

| Percentage | Recommendation |
|---:|---|
| 80–100 | STRONG_MATCH |
| 60–79 | MODERATE_MATCH |
| 40–59 | WEAK_MATCH |
| Below 40 | NEEDS_MANUAL_REVIEW |

## Important Notes

- This is synthetic training data.
- Do not rename candidate IDs or files.
- Do not hard-code scores or recommendations.
- Final reports should be based on the job description, resume content, rubric, and tool outputs.
- The final report is a screening-support artifact for human review.
