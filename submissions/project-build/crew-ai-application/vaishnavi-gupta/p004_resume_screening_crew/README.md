# RESUME SCREENING PROJECT

## Description
- This project focuses on the hiring process of candidates for a particular role.
- Multiple agents are made that are assigned multiple tasks as per their specialization.
- Designed specially for Hiring Managers and people involved in hiring processes.

## Business Use Case
- Hiring process is usually a hectic and very time taking process.
- To ease up this process, this system is designed.
- It consists of multiple agents that can automate the hiring workflow.
- Can make the procees very easy and automatic.

## Folder structure
p004_resume_screening_crew/
│
├── README.md
├── .env.example
├── requirements.txt
│
├── data/
│ └── p004_resume_screening_crew_dataset/
│
├── src/
│ ├── config.py
│ ├── main.py
│ ├── crew.py
│ ├── agents.py
│ ├── tasks.py
│ ├── tools.py
│ ├── schemas.py
│ ├── scoring.py
│ └── output_writer.py
│
├── tests/
│ ├── test_tools.py
│ ├── test_scoring.py
│ ├── test_output_schema.py
│ └── test_crew_flow.py
│
├── evals/
│ ├── test_report_evals.py
│ └── evaluation_prompts.md
│
└── outputs/
 ├── CAND-001_screening_report.json
 ├── CAND-002_screening_report.json
 ├── CAND-003_screening_report.json
 └── execution_log.txt

## Workflow
- Sequential
- This means tasks will be executed one by one in an sequential manner.

## Folders/files description

### .venv
- Virtual environment
command - python -m venv .venv
- To activate .venv
command - .venv\Scripts\activate

### .env
- Stores secret variables.
- Like api_keys, models, tokens.

### data folder
- This folder conatains the whole data on which this project is based.
- Multiple resumes of candidates.
- MD files for information along with a .csv file also.

### requirements.txt
- Consists of all the required frameworks and packages with suitable versions
- Command - pip install -r requirements.txt
- These are the requirements:
crewai==0.177.0
crewai-tools==0.76.0
python-dotenv==1.1.1
langchain-groq==0.3.8
pydantic>=2.13.4
pytest>=9.1.1
pandas>=3.0.3
rich>=15.0.0
deepeval>=4.0.7
requests

### tests folder
- Very important as it can test things before running the whole project.
- Consists of files:
test_crew_flow.py - test the flow of crew
test_output_schema.py - test the format of output
test_scoring.py - test the scoring of candidates
test_tools.py - test the working of tools

### src foler
- Contains all the impotant files that contains all the working code, i.e,

### agents.py
- Contains all the 7 agents as per requirements.

### config.py
- Contains the code for all the configuration like api_key and model.

### crew.py
- Contains code of crew that combines all the agents and tasks.

### main.py
- Main working file of the project

### output_writer.py
- Contains the code for output parsing.

### scoring.py
- Contains the code to define how to score candidates.

### tasks.py
- Contains the code for defining all the tasks performed by agents.

### tools.py
- Contains all the tools as mentioned in the PRD.

### README.md
- Documentation file.
- Contains the procedure and all the details of the whole project.

### evals folder
- evaluation_prompts.md
Contains the prompts on the basis of which evaluation is done.

- test_report_evals.py
Contains the test report of the candidate.

### outputs folder
- Contains .json file for multiple resumes report generated after evaluation.
- Contains a file "execution_log.txt" which contains information of the json outputs stored.

## How to run the project
- Save all the files and folders.
- Then, run the command in the terminal : python main.py
## Author
- Vaishnavi Gupta