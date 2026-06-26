# AI Resume Screening and Interview Planning Crew Using CrewAI

## Overview
The goal of this project is to build a CrewAI-based multi-agent system where 
multiple specialized agents work together in a sequential workflow

# Project Structure
```text
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
```
---
# 9. Dataset Structure
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
└── README_dataset.md
```
---

# Environment Variables
Create `.env`
```env
GROQ_API_KEY=your_groq_api_key
```
---
 Activate Environment
   ```bash
    source .venv/Scripts/activate
    uv pip install -r requirements.txt
```
---
# run this
```bash
 python src/main.py --candidate-id CAND-001 ## for user 1
 python src/main.py --candidate-id CAND-002 ## for user 2
 python src/main.py --candidate-id CAND-003 ## for user 3
 python src/main.py --candidate-id CAND-004 ## for user 4
 python src/main.py --candidate-id CAND-005 ## for user 5

 ```
---

## outputs folder 
``` bash
store the output of the the user data
```
---
