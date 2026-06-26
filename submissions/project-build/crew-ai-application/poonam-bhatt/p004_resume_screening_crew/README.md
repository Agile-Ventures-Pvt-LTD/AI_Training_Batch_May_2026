# 🤖 AI RESUME SCREENING AND INTERVIEW PLANNING

Recruiters and hiring managers often review multiple resumes manually for a 
single open role. This process can be time-consuming and inconsistent, especially 
when the role requires a mix of technical skills, project experience, and 
communication ability.
The goal of this project is to build a CrewAI-based multi-agent system where 
multiple specialized agents work together in a sequential workflow.
The system should:
1. Read a job description.
2. Read candidate resumes.
3. Extract structured candidate details.
4. Match candidate skills against job requirements.
5. Score candidate fit using a defined rubric.
6. Identify gaps and areas to probe.
7. Generate interview questions.
8. Produce a final screening report for human review.
This project is intended to demonstrate multi-agent orchestration, sequential 
task execution, tool integration, testing, and LLM output evaluation.

## ✨ Features

Build a CrewAI-based resume screening crew that can:
1. Analyze a job description.
2. Analyze candidate resumes.
3. Extract candidate skills, projects, experience, education, and certifications.
4. Compare resume content with job requirements.
5. Calculate a fitment score using a fixed scoring rubric.
6. Identify candidate strengths and gaps.
7. Generate role-specific interview questions.
8. Produce a structured JSON screening report.
9. Save the final report to the outputs/ folder.
10.Provide pytest tests for tools, scoring, schema, and crew execution.
11.Provide DeepEval-style or equivalent evaluation checks for generated 
reports.


## Target Users
1. Primary User
Recruiter / Talent Acquisition Associate
Uses the system to generate a first-level screening report.
2. Secondary User
Hiring Manager
Uses the report to understand candidate fit, gaps, and interview focus areas.
3. Optional User
Technical Interview Panel
Uses the generated questions to conduct a structured interview


## 🛠️ Tech Stack

- **[CrewAI](https://github.com/joaomdmoura/crewAI)**: Multi-agent orchestration framework
- **[Groq](https://groq.com/)**: Ultra-fast LLM inference (llama-3.3-70b-versatile)
- **[HuggingFace](https://huggingface.co/)**: Local embeddings (sentence-transformers)
- **[Embedchain](https://embedchain.ai/)**: Vector database and RAG framework
- **Python 3.11+**: Core programming language

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.10 or higher installed
- A Groq API key (free tier available)
- Git for version control

## 🚀 Installation


### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Get your free Groq API key:**
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key

## 📁 Project Structure

004_resume_screening_crew/
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


## Resume Screening Crew Dataset

This is a synthetic dataset for **P004: AI Resume Screening and Interview Planning Crew Using CrewAI**.

The dataset is aligned with the revised PRD and contains only the participant-facing files required by the project.

## Folder Structure

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
│
└── README_dataset.md
```

## Candidate IDs

| Candidate ID | Candidate Name | Resume File |
|---|---|---|
| CAND-001 | Rohan Mehta | candidate_001_rohan_mehta.md |
| CAND-002 | Priya Sharma | candidate_002_priya_sharma.md |
| CAND-003 | Neha Gupta | candidate_003_neha_gupta.md |
| CAND-004 | Arjun Nair | candidate_004_arjun_nair.md |
| CAND-005 | Sara Khan | candidate_005_sara_khan.md |

## Required Candidate Screenings

Participants must generate JSON screening reports for at least:

```text
CAND-001
CAND-002
CAND-003
```

Strong submissions may screen all five candidates.

## Scoring Rubric

The rubric has exactly 8 categories. Each category must be scored from 0 to 5.

Maximum score: 40

Categories:

```text
python_programming
sql_database_skills
api_integration
llm_application_development
agent_frameworks
rag_understanding
testing_and_quality
communication
```

## Recommendation Bands

| Percentage | Recommendation |
|---:|---|
| 80–100 | STRONG_MATCH |
| 60–79 | MODERATE_MATCH |
| 40–59 | WEAK_MATCH |
| Below 40 | NEEDS_MANUAL_REVIEW |


## 🎯 Usage

### Basic Usage

Run the resume screening crew

```bash
python crew.py
```

This will:
1. Process tools,task and agents from the crew file


## 🔧 Configuration

### Agent Configuration (`agents.py`)

- **Model Selection**: Change the LLM model in the `llm` configuration
- **Agent Behavior**: Modify `role`, `goal`, and `backstory` for different writing styles
- **Memory**: Currently disabled to avoid OpenAI dependency (can be re-enabled with custom embeddings)

### Task Configuration (`tasks.py`)

- **Research Depth**: Adjust `expected_output` for more/less detailed research
- **Output Format**: Customize the blog post structure and length

### Tool Configuration (`tools.py`)

- **Embedding Model**: Change the HuggingFace model for different performance/quality trade-offs
- **YouTube Channel**: Target different content sources

## 🤔 How It Works

### Step 1: Job Description


### Step 2: resume extraction


### Step 3: skill and experience matching


### Step 4: Interview planning 


### Step 5: Recommendation


### Step 6: Gap analysis


### Step 7: Report Review



## ⚠️ Troubleshooting

### Rate Limit Errors (Groq)

**Error**: `RateLimitError: Request too large for model`

**Solution**: 
- Switch to `llama-3.1-8b-instant` for higher rate limits (30K TPM)
- Reduce output length in `tasks.py`
- Make task descriptions more specific



### Import Errors

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```


## 🔐 Security

- ✅ `.env` file excluded from Git
- ✅ API keys never committed to repository
- ✅ Database cached locally (not shared)
- ✅ All processing happens on your machine

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent framework
- [Groq](https://groq.com/) - Lightning-fast LLM inference
- [HuggingFace](https://huggingface.co/) - Open-source embeddings
- [Embedchain](https://embedchain.ai/) - RAG framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing GitHub Issues
3. Create a new issue with detailed information

---

**Built with ❤️ using CrewAI and Groq**

*Happy Screening! 📝✨*