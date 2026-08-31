#  AI Resume Screening and Interview Planning Agent


## Project Context
Recruiters and hiring managers often review multiple resumes manually for a 
single open role. This process can be time-consuming and inconsistent, especially 
when the role requires a mix of technical skills, project experience, and 
communication ability.
The goal of this project is to build a CrewAI-based multi-agent system where 
multiple specialized agents work together in a sequential workflow.

## Business Problem

Hiring teams often face the following challenges:
1. Reviewing resumes manually takes time.
2. Screening criteria may vary between reviewers.
3. Interview questions are not always aligned with role requirements.
4. Candidate strengths and gaps are not always documented clearly.
5. Resume claims may not be linked back to evidence.
6. Recruiters need a structured first-level screening report for discussion with 
hiring managers.
The proposed system should assist the screening process by generating a 
structured report based only on the provided job description and resume content.

## Overview
This project is an automated recruitment screening pipeline built using CrewAI. It utilizes a team of 7 specialized agents to read a candidate's resume, compare their skills against a target Job Description using an 8-category grading rubric, perform gap analysis, and generate a tailored technical interview plan.

The final evaluation is exported directly as a structured JSON snapshot inside the local file system.


---

## Tech Stack
* **Language**: Python 3.12+
* **Frameworks**: CrewAI,Pydattic
* **Inference API**: Groq API
* **Testing**: deepeval,pytest
* **Environment Management**: python-dotenv

---

## Project Structure
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

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repository-url>
cd resume_screening_crew
```

### 2. Create Virtual Environment
```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install -r requirements.txt
```

---

## Environment Variables
Create a `.env` file in the root directory matching this schema:

```env
GROQ_API_KEY= your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile 
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs

```

---

## Running the Application
Execute the primary runtime block wrapper:

```bash
python main.py
```


---

## Available Tools

1. read_job_description_tool
2. read_resume_tool
3. candidate_index_lookup_tool
4. load_screening_rubric_tool
5. score_calculator_tool
6. save_report_tool
7. validate_report_schema_tool


---

## Availale Agents
1. Job desciption Analyst Agent
2. Resume Extraction Agent
3. Skill and Experience Matching Agent
4. Interview Planning Agent
5. Final Recommendation Agent
6. Gap Analysis Agent
7.  Report Review Agent

##  Required Commands
```
Run screening for one candidate:
python src/main.py --candidate-id CAND-001

Run sample screening for required candidates:
python src/main.py --run-sample-screening

Run pytest tests:
pytest tests/

Run integration tests:
pytest -m integration

Run evaluation tests:
deepeval test run evals/

```
---

## 🔮 Future Enhancements

Here are a few features and improvements planned for upcoming versions of the platform:

### 1. Hybrid LLM Routing (Cost Optimization)
* Currently, all tasks run on a large 70B model, which strains rate limits. 
* Future updates will route lightweight parsing tasks (like reading raw text or extracting contact info) to faster, cheaper models (like Llama-3-8B), reserving the 70B model strictly for final grading and interview planning.

### 2. Live Resume File Format Parsing (.pdf & .docx)
* Expand the ingestion tools to support native PDF and Word Document processing using libraries like `pypdf` or `docx2txt`.
* This removes the requirement of converting candidate profiles into Markdown files before running the pipeline.

### 3. Interactive Web Dashboard (Streamlit / FastAPI)
* Build a clean browser interface to replace the command-line execution.
* Recruiters will be able to upload a resume file directly, view progress indicators for each agent, and visually compare score matrices across candidates.

### 4. Custom Rubric Configuration Profiles
* Create a configuration layer to support different screening rubrics based on seniority levels (e.g., Intern vs. Principal Engineer).
* This will allow teams to change category weights and scoring constraints dynamically using simple external YAML configuration files.

### 5. Vector Database Memory (RAG) Integration
* Integrate a local vector instance (such as ChromaDB or FAISS) to cache and store previous evaluations.
* This will enable semantic search functionality across the entire candidate pool, allowing recruiters to look up profiles using semantic prompts like "Find candidates with strong multi-agent deployment experience."


---

## Author
**Ashish Sinha**
