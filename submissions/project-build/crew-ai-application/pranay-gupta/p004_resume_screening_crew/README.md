# P004: AI Resume Screening and Interview Planning Crew Using CrewAI

An advanced, production-ready multi-agent orchestration intelligence system engineered with **CrewAI** to automate first-level candidate fitment screening. This application sequentially cross-references unstructured applicant resume data against core role requirements parameters, runs numerical rating diagnostics across an 8-tier category grading framework, and prepares candidate-tailored behavioral and technical interview questions loops.

---

##  Objective
Hiring teams manually filtering high volumes of application resumes deal with parsing inconsistencies, human bias variations, and loose documentation alignments. This system acts as a **screening-support assistant**, transforming unstructured text inputs into deterministic, structured JSON evaluation indices. This data enables talent management specialists to gain clear, automated summaries while retaining human control over the final recruitment decisions.

---

##  Core Features
- **Deterministic Multi-Agent Pipeline**: 5 highly specialized autonomous agents executing step-by-step logic workflows.
- **8-Category Grading Matrix**: Strict scoring evaluation mapping from 0 to 5 per core skill segment for a maximum score threshold of 40 points.
- **Synonym-Aware Cross-Referencing**: Built-in normalization parsing maps varying acronym descriptors (e.g., *GenAI*, *RAG*) smoothly using explicit configuration keys.
- **Targeted Question Stream Blueprinting**: Dynamically maps discovered profile gaps into precise tactical validation interview prompts.
- **Automated Validation & Evaluation Suite**: Pre-integrated test suites that continuously evaluate schema compliance, mathematical consistency, and parameter limits.

---

##  Project Structure
```text
p004_resume_screening_crew/
│
├── .env.example                       
├── requirements.txt                   
├── README.md                          
│
├── data/
│   └── p004_resume_screening_crew_dataset/
│       ├── job_description/           
│       ├── resumes/                   
│       └── metadata/                  
│
├── src/
│   ├── __init__.py
│   ├── main.py                        
│   ├── crew.py                        
│   ├── agents.py                      
│   ├── tasks.py                       
│   ├── tools.py                       
│   └── schemas.py                     
│
├── tests/
│   └── test_deterministic.py          
│
└── evals/
    └── test_report_evals.py           
```

---

##  Tech Stack
- **Core Framework**: Python 3.10+
- **Agent Orchestrator**: CrewAI
- **LLM Gateway Engine**: OpenAI / Groq API Interfacing
- **Data Validation Layer**: Pydantic v2
- **Testing Engine**: Pytest

---

##  Environment Variables & Setup

1. Clone the project repository code into your local development space.
2. Initialize and activate an isolated virtual workspace environment:
   ```bash
   python -o -m venv .venv
   On Windows use: .venv\Scripts\activate
   ```
3. Install the application dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure a `.env` instance referencing the keys inside `.env.example`:
   ```env
   GROQ_API_KEY=your_groq_api_credential_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   DATASET_PATH=data/p004_resume_screening_crew_dataset
   OUTPUT_PATH=outputs
   ```

---

##  Execution Manual

### Screen a Single Candidate
Run the orchestration crew pipeline against an individual ID record via the command line interface:
```bash
python src/main.py --candidate-id CAND-001
```

### Run Batch Sample Screening
Run evaluation processes across the required base criteria profiles group sequentially (`CAND-001`, `CAND-002`, and `CAND-003`):
```bash
python src/main.py --run-sample-screening
```
*Generated file outputs are securely written inside the `/outputs` project folder.*

---

##  Workforce Crew Specification

### 1. Principal Job Description Analyst
- **Goal**: Extracts raw textual constraints from role descriptions into clean competency configurations.
- **Tools**: `read_job_description_tool`

### 2. Expert Talent Profile Extractor
- **Goal**: Converts unstructured resume profiles into standardized candidate data fields.
- **Tools**: `candidate_index_lookup_tool`, `read_resume_tool`

### 3. Senior Technical Fitment Evaluator
- **Goal**: Calculates objective profile fitment across the 8-category scoring rubric.
- **Tools**: `load_screening_rubric_tool`, `skill_matcher_tool`, `score_calculator_tool`

### 4. Lead Technical Interview Architect
- **Goal**: Creates targeted technical, project-based, and gap-validation interview questions.
- **Tools**: *Autonomous logical inference parsing based on computed metric differentials.*

### 5. Chief Talent Acquisition Officer
- **Goal**: Audits data formatting outputs, confirms structural validity, and generates the final JSON screening report.
- **Tools**: `validate_report_schema_tool`, `save_report_tool`

---

##  System Tools Blueprint

- **`read_job_description_tool`**: Safely opens, reads, and processes raw markdown files containing role criteria text.
- **`read_resume_tool`**: Extracts candidate-specific data points from raw submission files.
- **`candidate_index_lookup_tool`**: Maps target `candidate_id` entries to the correct local resume filenames using an index spreadsheet.
- **`load_screening_rubric_tool`**: Reads the structured score evaluation categories directly from the metadata configuration file.
- **`score_calculator_tool`**: Sums category marks, calculates percentage metrics, and maps candidates to the correct matching band (`STRONG_MATCH`, `MODERATE_MATCH`, `WEAK_MATCH`, or `NEEDS_MANUAL_REVIEW`).
- **`skill_matcher_tool`**: Cross-references application documents with requirement vectors while accounting for domain synonyms.
- **`validate_report_schema_tool`**: Validates generated outputs against the required report structure parameters before saving.
- **`save_report_tool`**: Writes final candidate structural screening files out onto storage media blocks cleanly.

---

##  Quality Testing & Evaluation Matrix

The pipeline splits testing into deterministic tool verifications and automated output validation routines:

### 1. Testing 
Verifies local parsing tools and mathematical calculations without calling LLM endpoints:
```bash
pytest tests/ -v
```
Expected Output:
25 passed, 116 warnings in 11.49s

### 2. Automated Report Evaluations
Evaluates the consistency of generated reports against original document contexts to check relevance, groundedness, and question metrics parameters:
```bash
pytest evals/ -v
```


---
##  Author
**Pranay Gupta**  
