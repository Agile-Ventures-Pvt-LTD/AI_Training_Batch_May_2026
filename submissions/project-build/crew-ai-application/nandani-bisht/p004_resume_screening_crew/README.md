# P004: AI Resume Screening and Interview Planning Crew

## 1. Project Overview

A multi-agent system built using CrewAI that automates the initial screening of candidate resumes against a specific job description. The system extracts structured data, calculates fitment scores using a deterministic rubric, identifies skill gaps, and generates targeted interview questions.


## Participant Name

Nandani Bisht

## 2. Business Use Case

Recruiters spend excessive time manually reviewing resumes. This system provides a structured, consistent, and evidence-backed first-level screening report, allowing hiring managers to focus on qualified candidates and conduct more effective interviews.

## 3. Technology Stack
```
- Python 3.10+
- CrewAI (Multi-agent orchestration)
- Groq (LLM inference via Llama 3.3)
- Pydantic (Schema validation)
- Pytest (Automated testing and evaluation)
```

## 4. Dataset Description

The system utilizes the `p004_resume_screening_crew_dataset` containing:
- 1 Job Description (AI Engineer)
- 5 Candidate Resumes
- Metadata: Candidate index, screening rubric, skill synonyms.

## 5. Setup Instructions

1. Create a virtual environment:
 `uv init`
 `uv venv`
 `.venv\Scripts\activate`

2. Install dependencies:
 `uv add -r requirements.txt`

3. Extract the dataset into `data/p004_resume_screening_crew_dataset/`.

## 6. Environment Variables

Copy `.env.example` to `.env` and populate the required keys:
```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs
```


## 7.How to run candidate Screening

```
uv run python src/main.py --candidate-id CAND-001
```
## 8. How to run the sample screening
```
uv run python src/main.py --run-sample-screening | Tee-Object -FilePath execution_log.txt
```

## 9. How to run pytest tests
```
# Run deterministic tests (Tools, Scoring, Schema)
uv run pytest tests/test_tools.py tests/test_scoring.py tests/test_output_schema.py -v

# Run integration tests (Full Crew Flow)
uv run pytest tests/test_crew_flow.py -v -m integration
```


## 10. How to run evaluation checks
```
uv run pytest evals/test_report_evals.py -v
```


## 11. Agent list and responsibilities

1. Job Description Analyst: Parses the JD into structured requirements, skills, and evaluation criteria.
2. Resume Extraction Specialist: Extracts candidate profile data (skills, experience, projects) without hallucinating.
3. Skill and Experience Matcher: Uses deterministic tools to calculate scores, match skills using synonyms, and determine the recommendation band.
4. Gap Analysis Expert: Identifies critical and moderate skill gaps and areas requiring interview probing.
5. Interview Planning Strategist: Generates targeted technical, project, scenario, and gap-validation interview questions.
6. Final Recommendation Synthesizer: Compiles all previous analyses into a comprehensive, evidence-backed final JSON report.
7. Report Quality Reviewer: Validates the final report for schema compliance, completeness, and evidence quality before saving.


## 12. Tool List and Responsibilities

1. The system implements 8 deterministic tools to ensure reliability:
2. read_job_description_tool: Reads and returns the JD file content.
3. read_resume_tool: Reads and returns a specific candidate's resume content.
4. candidate_index_lookup_tool: Maps a candidate ID to their specific resume file path.
5. load_screening_rubric_tool: Loads the 8-category scoring rubric from metadata.
6. skill_matcher_tool: Compares JD skills with resume skills using the synonym mapping.
7. score_calculator_tool: Calculates the overall score, percentage, and recommendation band.
8. validate_report_schema_tool: Validates the final JSON report against the required schema.
9. save_report_tool: Persists the final JSON report to the outputs/ directory.


## 13. Sequential Orchestration Explanation

1. The crew utilizes Process.sequential to ensure a strict, logical flow of data. Context is passed from one agent to the next:
2. JD Analyst reads the JD and outputs structured requirements.
3. Resume Extractor reads the resume and outputs the candidate profile.
4. Skill Matcher takes the JD and Profile, uses tools to calculate the match_score.
5. Gap Analyst analyzes the match_score to identify specific weaknesses.
6. Interview Planner uses the JD, Profile, and Gaps to generate the interview_plan.
7. Final Recommender synthesizes all 5 previous outputs into the final report and saves it.
8. Report Reviewer validates the saved report to ensure no data was lost or malformed.

