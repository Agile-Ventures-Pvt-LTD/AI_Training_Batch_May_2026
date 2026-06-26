# AI RESUME SCREENING

# Participant Name

**Mohd Zaid Ansari**

## Project Overview
This project is an automated, multi-agent recruitment pipeline built with CrewAI and Groq. It eliminates manual recruitment workloads by automatically reading job requirements, parsing candidate resumes, calculating algorithmic fitment scores against an evaluation rubric, and compiling candidate-specific interview playbooks.

## Technology Stack
- CrewAI 
- Groq 
- Pytest

## Dataset Description
The system expects an extraction folder setup following this strict layout:
```text
data/p004_resume_screening_crew_dataset/
├── job_description/
│   └── jd_ai_engineer.md           
├── resumes/
│   ├── candidate_001_rohan_mehta.md 
└── metadata/
    ├── candidate_index.csv        
    ├── screening_rubric.json       
    └── skill_synonyms.json         
```

## Setup Instructions
Activate your project virtual environment:
   ```.venv\Scripts\activate
   ```

Download the requirements.txt file
```uv add -r requirements.txt
```

# Environment Variables
Create a file named `.env` inside the root directory and paste your configuration keys:
```text
GROQ_API_KEY=gsk_your_actual_groq_api_key_string
MODEL=groqmodel
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs
```

## How to Run Candidate Screening
To trigger the sequential batch processing loop across all active candidates (`CAND-001`, `CAND-002`, `CAND-003`), run this command from the root folder:
```
python src/main.py
```
## How to Run Pytest Tests
The workspace features an internal verification layer of **6 testing test cases** checking data-types, logic math limits, file writers, and path lookups. Run the test suite using:
```
python -m pytest tests/test_tools.py
```

## Agent Used 
- Job Description Analyst Agent**: Ingests raw markdown files to extract structured required/preferred skills and role responsibilities.
- Resume Extraction Agent**: Extracts personal details, experience timelines, projects, and certifications directly from resume files.
- Skill and Experience Matching Agent**: Cross-references profiles using synonyms and calculates strict rubric scores from 0 to 5 across 8 core categories.
- Agent 4: Interview Planning Agent**: Reviews candidate skill gaps to generate technical, situational, and project deep-dive questions.
- Final Recommendation Agent**: Consolidates all data into a definitive executive screening report and assigns the final recommendation match tier.

## Tools Used 
- read_job_description : Opens local job markdown files safely using system encoding guards.
- read_resume_tool : Ingests unstructured candidate text files from storage folders.
- candidate_index_lookup_tool : Searches CSV files to find matching candidate names and paths from an ID.
- load_screening_rubric_tool : Pulls the evaluation criteria rules from the metadata directory.
- score_calculator_tool : Sums category metrics, derives percentages, and assigns recommendation match bands.
- save_report_tool : Safely writes structured output files directly into the outputs repository folder.

## Known Limitations
- Groq Rate Limits
- Context Window Constraints

## Future Improvements
- Async Multi-Threading
- Vector DB Embedding Search

# Author

**Mohd Zaid Ansari**