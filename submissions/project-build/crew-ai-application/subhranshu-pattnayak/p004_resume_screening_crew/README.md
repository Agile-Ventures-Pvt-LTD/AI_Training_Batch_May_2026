# AI Resume Screening and Interview Planning Crew

This project is a CrewAI-based multi-agent application that screens a candidate's resume against a job description and generates a structured screening report along with interview questions.

The application follows a sequential workflow where different agents perform specific responsibilities such as analyzing the job description, extracting resume information, matching candidate skills, planning interview questions, and generating the final report.

---

## Tech Stack

- Python
- CrewAI
- Groq LLM
- Pydantic
- python-dotenv

---

## Project Structure

```
p004_resume_screening_crew/

├── agents/
├── tasks/
├── tools/
├── data/
├── outputs/
├── utils/
├── tests/
├── schemas.py
├── config.py
├── crew.py
├── main.py
└── README.md
```

---

## Agents

- Job Description Analyst
- Resume Extraction Specialist
- Skill and Experience Matching Specialist
- Technical Interview Planner
- Candidate Screening Report Specialist

---

## Tools

- Read Job Description
- Read Resume
- Candidate Lookup
- Load Screening Rubric
- Skill Matcher
- Score Calculator
- Save Report
- Report Schema Validation

---

## Setup

Clone the repository

```bash
git clone <repository-url>
cd p004_resume_screening_crew
```

Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
uv sync
```

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DATASET_PATH=data/p004_resume_screening_crew_dataset
OUTPUT_PATH=outputs
```

---

## Running the Project

Run the application

```bash
python main.py
```

The application will prompt for a Candidate ID.

Example:

```
Enter Candidate ID: CAND-001
```

The generated screening report will be saved in the `outputs/` directory.

---

## Workflow

The project executes the following sequence:

```
Job Description
JD Analysis Agent
Resume Extraction Agent
Skill Matching Agent
Interview Planning Agent
Final Report Agent
JSON Screening Report
```

---

## Output

The final report includes:

- Candidate Information
- Overall Score
- Recommendation
- Executive Summary
- Strengths
- Gaps
- Interview Focus Areas
- Interview Questions
- Supporting Evidence
- Human Review Note

---

## Notes

Due to the limited time available for the assignment, the primary focus was on implementing the complete multi-agent workflow, deterministic tools, schema validation, and report generation.

The `tests/` directory has been created as part of the project structure, but comprehensive unit tests and evaluation checks were not completed within the allotted time.

---

## Future Improvements

- Complete pytest test suite
- Add DeepEval evaluation checks
- Batch candidate screening
- Candidate comparison report
- Streamlit interface
- Markdown report generation
- Improved skill synonym matching