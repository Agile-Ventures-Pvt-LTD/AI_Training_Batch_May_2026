# Project-04 Case-1
## Project Title
### P004: AI Resume Screening and Interview Planning Crew Using CrewAI
### Submitted By: Palak
### 1. Project overview:
The goal of this project is to build a CrewAI-based multi-agent system where 
multiple specialized agents work together in a sequential workflow.

The proposed system should assist the screening process by generating a 
structured report based only on the provided job description and resume content.


### 2. Requirements
crewai>=0.114.0
crewai[tools]>=0.186.1
python-dotenv>=1.2.1
pytest
langchain-community==0.3.19
markdown
crewai[litellm]

### 3.Setup instructions

Steps for set-up are as follows:
1. initialize uv
```bash
uv init
```

2. create Environment 
```bash
uv venv
```
3. install requirements
```bash
uv add -r requirements.txt
```

**set-up part is completed!!!**

---


### 4.Environment variable setup

To set any Environment variable, do the following:
1. first create Environment file named **.env**
2. add your api key here 
```python
API_KEY=zwxx2.....
```
3. Load the api in any folder or file with the help of os
```bash
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['API_KEY'] = os.getenv("API_KEY")
```

---

### 5. Folder structure
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

### 6. Components in Crew
### Tools 

1. **read_job_description_tool** - use to read job discription
2. **read_resume_tool** - use to read resume
3. **candidate_index_lookup_tool** - used to find candidate
4. **load_screening_rubric_tool** - used to load rubric.json
5. **score_calculator_tool** - use to find score
6. **save_report_tool** - use to save final report


### Agents

1. **job_review** - this agent is used to analyze JD
2. **resume_extraction** -this agent is used to analyze candidate
3. **Skill_and_Experience_Matching_Agent** - This is used to compare candidate against rubric
4. **Interview_Planning_Agent** - this agent is developed to plan for interview
5. **Final_Recommendation_Agent**  - This agent is final decision maker


### task 
1. job_review_task
2. resume_review_task
3. matching_task
4. planner_task
5. final_task


### 7.Sequence

Input: Job Description + Candidate Resume
   ↓
Job Description Analyst Agent
   ↓
Resume Extraction Agent
   ↓
Skill and Experience Matching Agent
   ↓
Interview Planning Agent
   ↓
Final Recommendation Agent
   ↓
Output: Candidate Screening Report

### 8. How to run Crew

To run the crew run file named as main.py
```bash
uv run src/main.py
```
This will run the main application.

---

### 8. How to run test

To run the test cases
```bash
uv run test/test_tool.py
```

---

### dataset details
This data set contain resumes, evaluation rubric and job discription
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

