# P004: AI Resume Screening and Interview Planning Crew Using CrewAI

## Project Overview

A Participants are expected to build a working CrewAI-based multi-agent system that screens candidate resumes against a job description, 
generates a structured fitment report, 
and prepares candidate-specific interview questions.

## Bussiness Use Case 
  Recruiters spend hours manually reviewing resumes for each open role.This multi-agent system automates first-level screening using CrewAI:it reads job descriptions, extracts candidate details, matches skills, scores fitment, and generates interview questions. Output is a structured JSON report for human review.


## Tech Stack

- Python 3.11+
- CrewAI -
- LangChain Groq
- python-dotenv
- Pydantic
- pytest
- pandas
- rich 

## Dataset Description

The dataset is provided in `data/p004_resume_screening_crew_dataset/` with the following structure:

```
p004_resume_screening_crew_dataset/
├── job_description/
│   └── jd_ai_engineer.md
├── resumes/
│   ├── candidate_001_rohan_mehta.md
│   ├── candidate_002_priya_sharma.md
│   ├── candidate_003_neha_gupta.md
│   ├── candidate_004_arjun_nair.md
│   └── candidate_005_sara_khan.md
├── metadata/
│   ├── candidate_index.csv
│   ├── screening_rubric.json
│   └── skill_synonyms.json
└── README_dataset.md
```

Five synthetic candidates are provided:
- CAND-001: Rohan Mehta 
- CAND-002: Priya Sharma 
- CAND-003: Neha Gupta 
- CAND-004: Arjun Nair 
- CAND-005: Sara Khan 

## Setup Instructions
*** Folder Structure ***
```
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

1. Create a virtual environment:
```
.venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
```
 .env.example .env
```

5.  `.env` with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs
```

## How to Run Candidate Screening

Run screening for a single candidate:
```
python src/main.py --candidate-id CAND-001
```

Run sample screening for required candidates (CAND-001, CAND-002, CAND-003):
```
python src/main.py --run-sample-screening
```

Run screening for all 5 candidates:
```
python src/main.py --run-all
```

## How to Run pytest Tests

Run all tests:
```
pytest tests/

```

## Agent List and Responsibilities

1. Job Description Analyst : Analyzes the job description and extracts structured requirements 
2. Resume Extraction Specialist : Extracts structured candidate information including skills, experience, projects, education, and certifications 
3. Skill and Experience Matcher : Compares JD requirements with candidate profile, identifies matches and gaps, calculates fitment scores 
4. Interview Planning Agent :  Generates candidate-specific interview questions
5. Final Recommendation Agent : Produces final screening report 
6. Gap Analysis Agent : Identifies missing or weak areas and categorizes them 
7. Report Review Agent : Reviews the final report 

## Tool List and Responsibilities

 1. read_job_description_tool : Reads the job description file from the dataset 
 2. read_resume_tool : Finds the resume file path for a given candidate ID 
 4. load_screening_rubric_tool  Loads the scoring rubric with 8 categories 
 3. candidate_index_lookup_tool | Finds the resume file path for a given candidate ID
 5. score_calculator_tool  Calculates total score, percentage, and recommendation band 
 6. save_report_tool  Saves the final report to outputs/ folder 
 7. skill_matcher_tool Compares JD skills with candidate resume skills 
 8. validate_report_schema_tool  Validates that the final report contains all required fields 
 9. batch_candidate_loader_tool  Loads all candidates from the index file

## Sequential Orchestration Explanation

The workflow runs in a sequential order where each agent depends on the output of the previous agent:

1. **Job Description Analyst Agent** reads and analyzes the JD
2. **Resume Extraction Agent** extracts candidate profile from the resume
3. **Skill and Experience Matcher Agent** compares JD with profile using rubric and synonyms
4. **Interview Planning Agent** generates questions based on gaps
5. **Final Recommendation Agent** produces the screening report
6. **Gap Analysis Agent** identifies critical and moderate gaps
7. **Report Review Agent** validates the final report quality

Each agent's output is passed as context to the next agent, ensuring the final report is comprehensive and grounded in earlier analysis.

## Output Report Format

Reports are saved as JSON files in the `outputs/` folder:
```
outputs/CAND-001_screening_report.json
outputs/CAND-002_screening_report.json
outputs/CAND-003_screening_report.json
```

Each report contains:
- candidate_id, candidate_name, role_title
- overall_score, max_score, percentage
- recommendation (STRONG_MATCH / MODERATE_MATCH / WEAK_MATCH / NEEDS_MANUAL_REVIEW)
- executive_summary
- strengths and gaps
- interview_focus_areas
- interview_questions (technical, project deep-dive, scenario, gap-validation)
- evidence
- human_review_note

## Scoring Rubric

8 categories scored from 0-5 (max 40 points):
- python_programming
- sql_database_skills
- api_integration
- llm_application_development
- agent_frameworks
- rag_understanding
- testing_and_quality
- communication

Recommendation bands:
- 80-100%: STRONG_MATCH
- 60-79%: MODERATE_MATCH
- 40-59%: WEAK_MATCH
- Below 40%: NEEDS_MANUAL_REVIEW

## Known Limitations


1. The scoring is based on keyword matching in the current deterministic implementation
2. The system requires a valid Groq API key for LLM-powered agents
3. Markdown report export is a secondary format; JSON is the primary structured output

## Future Improvements

1. Add support for PDF and DOCX resume parsing
2. Implement batch comparison reports across candidates
3. Add Streamlit or Gradio web interface
4. Implement candidate ranking across multiple roles
5. Add export to ATS-compatible formats
