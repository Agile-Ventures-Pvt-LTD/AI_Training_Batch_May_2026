# Agentic Resume Screening Architecture

It is multi-agent screening framework built on CrewAI and Groq. The system automatically processes, scores, and creates targeted interview plans for technical candidate pipelines without manual HR intervention.

## 1. Project Overview
This project delivers a deterministic, production-ready pipelines workflow using a serial execution group of 5 specialized AI agents. It reads a pool of unstructured markdown candidate profiles, runs synonyms-matched technical matrix scoring against fixed rubrics, plans deep-dive validation interview focus vectors, and persists structured audit-compliant evaluation data logs.

## 2. Business Use Case
Manual evaluation of high-volume technical resumes for niche engineering pipelines leads to inconsistent scoring, long turnaround times, and severe human cognitive fatigue. This automated framework addresses these issues by:
* **Standardizing Evaluations:** Eliminating subjective human bias by grading candidate capabilities against explicit rubric constraints.
* **Saving Technical Hours:** Offloading initial technical screening checks from senior engineering team leaders.
* **Providing Target Discovery High-Signals:** Generating candidates-specific deep-dive questions targeting identified resume text anomalies and missing skills.

## 3. Technology Stack
python-dotenv
langchain-groq
langchain
langchain-community
langgraph
pillow
crewai    
pydantic-ai
requests

## 4. Dataset Description
The underlying processing ecosystem mirrors the following isolated file hierarchy layout structure:
* `job_description/`: Holds the targeted benchmark markdown role parameters (`jd_ai_engineer.md`).
* `resumes/`: Plain text markdown source documents containing candidates' technical histories.
* `metadata/`: 
  * `candidate_index.csv`: Central routing matrix linking string Candidate IDs to source filenames.
  * `screening_rubric.json`: Configuration tracking the exact 8 validation capability parameters.
  * `skill_synonyms.json`: Standardized lexicon translating technical variations.

## 5. Setup Instructions
Initialize your localized runtime environment quickly using the following command sequentials:

# 1. Folder Creation
Made a folder p004_resume_screening_crew

# 2. Initialize uv
uv venv

# 3. Activate the virtual runtime package environment
.venv\Scripts\Activate.ps1


# 4. Install Dependencies
```
uv pip install -r requirements.txt
```

# 6. Environment Variables
Create a .env file in the project's root directory containing the parameters below:

GROQ_API_KEY=....
GROQ_MODEL=llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs

## 7. How to Run Project
```bash
python src/main.py
```

## 7. How to Run Pytest Tests


```bash
pytest -v
```

## 8. How to Run Evaluation Checks
```bash
pytest evals/test_report_evals.py -v
```

## 9. Agent List and Responsibilities
1. **Job Description Analyst:** Parses roles parameters; isolates core hard skills from preferred requirements.
2. **Resume Extraction Agent:** Locates records via index; pulls explicit history metadata strings into context.
3. **Skill and Experience Matching Agent:** Compares background structures against rubrics; manages calculators.
4. **Interview Planning Agent:** Reviews profile gaps; designs investigative technical questions and core discovery intents.
5. **Final Recommendation Agent:** Compiles executive summaries and human review notes; handles serialization.

## 10. Tool List and Responsibilities
* `read_job_description_tool`: Reads raw text role files safely from disk.
* `read_resume_tool`: Performs text collection file extraction from target candidate markdown files.
* `candidate_index_lookup_tool`: Maps candidate IDs to corresponding resume files inside the CSV index.
* `load_screening_rubric_tool`: Loads the standardized scoring criteria configuration.
* `score_calculator_tool`: Runs arithmetic logic to calculate matching percentages and performance bands.
* `save_report_tool`: Exports the completed report payload to disk as a JSON file.

## 11. Sequential Orchestration Explanation
```text
[JD Analyst] ──> [Resume Extractor] ──> [Matching Agent] ──> [Interview Planner] ──> [Recommendation Agent]
```

## 12. Output Report Format
The final reports are exported as a validated JSON document matching the following schema:

```json
{
    "candidate_id": "CAND_001",
    "candidate_name": "Rohan Mehta",
    "role_title": "AI Engineer",
    "overall_score": 35,
    "max_score": 40,
    "percentage": 87,
    "recommendation": "STRONG_MATCH",
    "executive_summary": "Extensive LLM application deployment background...",
    "strengths": ["Python Expert", "Advanced RAG Pipelines"],
    "gaps": ["No production experience with multi-agent orchestration frameworks"],
    "interview_focus_areas": ["Validate autonomous state recovery tracking mechanisms"],
    "interview_questions": [
        {
            "question": "How do you handle cyclic graph dependencies in custom agent networks?",
            "intent": "Verify production readiness for multi-agent systems"
        }
    ],
    "evidence": {
        "python_programming": "Maintained core enterprise frameworks for 4 years."
    },
    "human_review_note": "Excellent technical fit; baseline compensation requirements match senior banding limits."
}
```

## 13. Future Improvements
* In future, we can perform parallel Processing (process.hierarchical).
