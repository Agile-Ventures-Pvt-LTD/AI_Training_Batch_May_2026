import os
import sys
import re
import json
import pandas as pd
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools import find_resume, calculate_score

def analyze_resume_profile(candidate_id: str) -> Dict[str, Any]:
    csv_path = "data/p004_resume_screening_crew_dataset/metadata/candidate_index.csv"
    if not os.path.exists(csv_path):
        for root, _, files in os.walk("."):
            if "candidate_index.csv" in files:
                csv_path = os.path.join(root, "candidate_index.csv")
                break

    if not os.path.exists(csv_path):
        raise FileNotFoundError("candidate_index.csv not found")

    df = pd.read_csv(csv_path)
    row = df[df["candidate_id"] == candidate_id]
    if row.empty:
        return {
            "candidate_id": candidate_id,
            "candidate_name": f"Candidate {candidate_id}",
            "role_title": "AI Engineer",
            "overall_score": 0,
            "max_score": 40,
            "percentage": 0.0,
            "recommendation": "NEEDS_MANUAL_REVIEW",
            "executive_summary": "Candidate profile not found in index.",
            "strengths": ["None identified"],
            "gaps": ["Missing candidate profile"],
            "interview_focus_areas": ["General programming foundations"],
            "interview_questions": {
                "technical_questions": ["What is your background in software engineering?"],
                "project_deep_dive_questions": ["Can you describe a key project you worked on?"],
                "scenario_questions": ["Describe a challenge you faced and how you solved it."],
                "gap_validation_questions": ["Could you explain the gaps in your experience?"]
            },
            "evidence": ["Candidate profile was missing from the candidate index."],
            "human_review_note": "Profile missing. Needs manual verification."
        }

    cand_info = row.iloc[0].to_dict()
    cand_name = cand_info["candidate_name"]
    resume_file = cand_info["resume_file"]
    exp_years = float(cand_info["years_experience"])

    resume_paths = find_resume(candidate_id) or find_resume(resume_file)
    if not resume_paths:
        raise FileNotFoundError(f"Resume file for {candidate_id} not found")

    with open(resume_paths[0], "r", encoding="utf-8") as f:
        resume_text = f.read()

    synonyms_path = "data/p004_resume_screening_crew_dataset/metadata/skill_synonyms.json"
    if not os.path.exists(synonyms_path):
        for root, _, files in os.walk("."):
            if "skill_synonyms.json" in files:
                synonyms_path = os.path.join(root, "skill_synonyms.json")
                break

    with open(synonyms_path, "r", encoding="utf-8") as f:
        synonyms = json.load(f)

    scores = {}
    resume_lower = resume_text.lower()

    for category, keywords in synonyms.items():
        matches = sum(1 for kw in keywords if kw.lower() in resume_lower)
        
        if matches == 0:
            base = 0
        elif matches == 1:
            base = 2
        elif matches == 2:
            base = 3
        elif matches == 3:
            base = 4
        else:
            base = 5

        if category in ["agent_frameworks", "rag_understanding"]:
            if exp_years < 2.0:
                base = min(base, 2)
            elif exp_years < 4.0:
                base = min(base, 4)
        elif category in ["python_programming", "sql_database_skills"]:
            if exp_years >= 3.0:
                base = max(base, 3)

        scores[category] = min(max(base, 0), 5)

    scoring_res = calculate_score(scores)

    category_labels = {
        "python_programming": "Python Programming",
        "sql_database_skills": "SQL and Database Skills",
        "api_integration": "REST API Integration",
        "llm_application_development": "LLM Application Development",
        "agent_frameworks": "Agentic Frameworks",
        "rag_understanding": "RAG Understanding",
        "testing_and_quality": "Testing and Quality Assurance",
        "communication": "Technical Communication"
    }

    strengths = []
    gaps = []

    for cat, val in scores.items():
        label = category_labels.get(cat, cat.replace("_", " ").title())
        if val >= 4:
            strengths.append(label)
        elif val <= 2:
            gaps.append(label)

    if not strengths:
        strengths.append("General Python programming basics")
    if not gaps:
        gaps.append("Production-grade scaling")

    focus_areas = gaps[:3]
    project_names = []
    project_section = re.search(r"## Projects(.*?)(?:##|$)", resume_text, re.DOTALL | re.IGNORECASE)
    
    if project_section:
        project_content = project_section.group(1)
        headers = re.findall(r"###\s*(.*)", project_content)
        for h in headers:
            project_names.append(h.strip())
        if not project_names:
            bold_lines = re.findall(r"\*\*(.*?)\*\*", project_content)
            for b in bold_lines:
                if 5 < len(b) < 50:
                    project_names.append(b.strip())

    if not project_names:
        project_names = ["Candidate Portfolio Projects"]

    question_pool = {
        "python_programming": "How do you optimize memory consumption when processing large datasets in Python?",
        "sql_database_skills": "Can you explain the differences between indexing strategies in SQL databases?",
        "api_integration": "How do you handle API rate limiting and transient connection errors in a backend service?",
        "llm_application_development": "What strategies do you use for prompt optimization and managing model context windows?",
        "agent_frameworks": "How do you manage state and handle routing loops in complex agentic workflows?",
        "rag_understanding": "Describe how you optimize chunking strategies and embedding retrievals for domain-specific RAG applications.",
        "testing_and_quality": "How do you structure unit tests and mock external API dependencies using pytest?",
        "communication": "How do you document technical trade-offs and communicate application limitations to non-technical stakeholders?"
    }

    tech_questions = []
    for cat in focus_areas:
        cat_key = next((k for k, v in category_labels.items() if v == cat), None)
        if cat_key and cat_key in question_pool:
            tech_questions.append(question_pool[cat_key])

    if not tech_questions:
        tech_questions = [
            "What is your approach to handling exceptions in third-party API clients?",
            "How do you ensure code readability and maintainability across a shared codebase?"
        ]

    project_questions = []
    for proj in project_names[:2]:
        project_questions.append(f"In your project '{proj}', what were the main technical challenges you faced, and how did you resolve them?")
        project_questions.append(f"Could you explain the system architecture design decisions you made for '{proj}'?")

    scenario_questions = [
        "Describe a situation where you had to work with a team member who had a very different technical approach. How did you align?",
        "How do you handle unexpected shifts in project requirements or priorities under tight deadlines?"
    ]

    gap_questions = []
    for cat in focus_areas:
        gap_questions.append(f"Your profile indicates less hands-on experience in '{cat}'. How would you plan to bridge this gap if selected?")

    if not gap_questions:
        gap_questions = ["What new technologies or frameworks are you currently learning to expand your engineering skills?"]

    report = {
        "candidate_id": candidate_id,
        "candidate_name": cand_name,
        "role_title": "AI Engineer",
        "overall_score": scoring_res["overall_score"],
        "max_score": 40,
        "percentage": scoring_res["percentage"],
        "recommendation": scoring_res["recommendation"],
        "executive_summary": f"{cand_name} is currently working as a {cand_info['current_role']} with {exp_years} years of experience. The evaluation indicates key competencies in {', '.join(strengths[:3])}. The candidate is recommended as a {scoring_res['recommendation']} for the AI Engineer role.",
        "strengths": strengths,
        "gaps": gaps,
        "interview_focus_areas": focus_areas,
        "interview_questions": {
            "technical_questions": tech_questions[:3],
            "project_deep_dive_questions": project_questions[:2],
            "scenario_questions": scenario_questions,
            "gap_validation_questions": gap_questions[:2]
        },
        "evidence": [
            f"Evaluated skills against synonyms: python_programming ({scores['python_programming']}/5), sql_database_skills ({scores['sql_database_skills']}/5), api_integration ({scores['api_integration']}/5), llm_application_development ({scores['llm_application_development']}/5), agent_frameworks ({scores['agent_frameworks']}/5), rag_understanding ({scores['rag_understanding']}/5), testing_and_quality ({scores['testing_and_quality']}/5), communication ({scores['communication']}/5).",
            f"Primary skills listed: {cand_info['primary_skills']}",
            f"Analyzed projects: {', '.join(project_names)}"
        ],
        "human_review_note": "Automated screening evaluation. Please verify findings during the technical interview phase."
    }

    return report

def run_screening_crew(candidate_id: str) -> Dict[str, Any]:
    print(f"Running screening process for: {candidate_id}")
    
    groq_key = os.getenv("GROQ_API_KEY")
    is_valid_key = groq_key and groq_key != "..." and len(groq_key) > 10
    
    if is_valid_key:
        try:
            from crewai import Crew, Process
            from src.agents import (
                job_description_agent,
                Resume_Extraction_Agent,
                Skill_Experience_Matching_Agent,
                Interview_Planning_Agent,
                Final_Recommendation_Agent,
                Gap_Analysis_Agent,
                Report_Review_Agent,
                save_report_Agent
            )
            from src.tasks import (
                job_description_task,
                resume_extraction_task,
                skill_experience_matching_task,
                interview_planning_task,
                gap_analysis_task,
                recommendation_task,
                report_review_task,
                save_report_task
            )
            
            jd_path = "data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"
            resume_files = find_resume(candidate_id)
            resume_path = resume_files[0] if resume_files else f"data/p004_resume_screening_crew_dataset/resumes/candidate_{candidate_id[-3:]}_unknown.md"
            
            job_description_task.description = job_description_task.description.format(job_description_path=jd_path)
            resume_extraction_task.description = resume_extraction_task.description.format(resume_path=resume_path)
            save_report_task.description = save_report_task.description.format(candidate_id=candidate_id)
            
            crew = Crew(
                agents=[
                    job_description_agent,
                    Resume_Extraction_Agent,
                    Skill_Experience_Matching_Agent,
                    Interview_Planning_Agent,
                    Gap_Analysis_Agent,
                    Final_Recommendation_Agent,
                    Report_Review_Agent,
                    save_report_Agent
                ],
                tasks=[
                    job_description_task,
                    resume_extraction_task,
                    skill_experience_matching_task,
                    interview_planning_task,
                    gap_analysis_task,
                    recommendation_task,
                    report_review_task,
                    save_report_task
                ],
                process=Process.sequential,
                memory=False,
                cache=False,
                verbose=True
            )
            
            result = crew.kickoff(inputs={
                "job_description_path": jd_path,
                "resume_path": resume_path,
                "candidate_id": candidate_id
            })
            
            output_file = os.path.join("outputs", f"{candidate_id}_screening_report.json")
            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                try:
                    return json.loads(str(result))
                except Exception:
                    pass
        except Exception as e:
            print(f"CrewAI execution failed: {e}. Falling back to dynamic parsing engine.")
            
    report_data = analyze_resume_profile(candidate_id)
    
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{candidate_id}_screening_report.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    print(f"Report saved to: {file_path}")
    return report_data

if __name__ == "__main__":
    candidates = ["CAND-001", "CAND-002", "CAND-003", "CAND-004", "CAND-005"]
    for cid in candidates:
        try:
            run_screening_crew(cid)
        except Exception as err:
            print(f"Error screening {cid}: {err}")