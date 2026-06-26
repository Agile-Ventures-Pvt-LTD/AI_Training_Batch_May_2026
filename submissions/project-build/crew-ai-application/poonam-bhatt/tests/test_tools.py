from tools import read_job_description_tool,read_resume_tool,skill_matcher, find_resume,calculate_score,LoadScreeningRubric,validate_report,save_report_tool

config = {
    'embedder': {
        'provider': 'huggingface',
        'config': {
            'model': 'sentence-transformers/all-MiniLM-L6-v2'
        }
    }
}

read_job_description_tool("job_description")
read_resume_tool("resume")
candidate_skills=["python","llm","rag","api"]
skill_matcher(job_skills=["python","django","api","rag","llm"],candidate_skills=["python","llm","rag","api"],data)
find_resume("candidate_id":"candidate_001")


calculate_score({
    "python_programming": "0-5",
    "sql_database_skills": "0-5",
"api_integration": "0-5",
"llm_application_development": "0-5",
"agent_frameworks" :"0-5",
"rag_understanding" :"0-5",
"testing_and_quality":"0-5",
"communication": "0-5"
})


validate_report("outputs/")
save_report_tool("outputs/CAND-001_screening_report.json")