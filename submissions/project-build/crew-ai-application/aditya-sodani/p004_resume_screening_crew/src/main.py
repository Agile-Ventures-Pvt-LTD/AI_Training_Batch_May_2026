import argparse
from config import get_llm, DATASET_PATH, OUTPUT_PATH
from tools import *
from agents import get_agents
from tasks import get_tasks
from crew import build_crew
import json
import os
os.environ["CREWAI_DISABLE_MEMORY"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"


from scoring import default_category_scores, calculate_final_score
from output_writer import write_json_report

def run(candidate_id):
    
    index_path = f"{DATASET_PATH}/metadata/candidate_index.csv"
    

    candidate = candidate_index_lookup_tool(candidate_id, index_path)
    if not candidate["found"]:
        print("Candidate not found")
        return

    jd_path = f"{DATASET_PATH}/job_description/jd_ai_engineer.md"
    resume_path = f"{DATASET_PATH}/resumes/{candidate['resume_file']}"

    jd = read_job_description_tool(jd_path)
    resume = read_resume_tool(resume_path)

    llm = get_llm()
    agents = get_agents(llm)
    tasks = get_tasks(agents, jd["content"], resume["content"])

    crew = build_crew(agents, tasks)
    result = crew.kickoff(inputs={})


    outputs = [t.output.raw for t in crew.tasks]

    jd_data = safe_json_parse(outputs[0])
    resume_data = safe_json_parse(outputs[1])
    match_data = safe_json_parse(outputs[2])
    interview_data = safe_json_parse(outputs[3])
    summary_data = safe_json_parse(outputs[4])

    matched_skills = match_data.get("matched_skills", [])
    missing_skills = match_data.get("missing_skills", [])


    category_scores = default_category_scores(
        matched_skills, missing_skills
    )
    score = calculate_final_score(category_scores)

    report = {
        "candidate_id": candidate_id,
        "candidate_name": candidate["candidate_name"],
        "role_title": jd_data.get("role_title", "AI Engineer"),

        "overall_score": score["overall_score"],
        "max_score": score["max_score"],
        "percentage": score["percentage"],
        "recommendation": score["recommendation_band"],

        "executive_summary": summary_data.get("executive_summary", ""),

        "strengths": summary_data.get("strengths", matched_skills),
        "gaps": summary_data.get("gaps", missing_skills),

        "interview_focus_areas": jd_data.get("required_skills", [])[:5],

        "interview_questions": {
            "technical_questions": interview_data.get("technical_questions", []),
            "project_deep_dive_questions": interview_data.get("project_deep_dive_questions", []),
            "scenario_questions": interview_data.get("scenario_questions", []),
            "gap_validation_questions": interview_data.get("gap_validation_questions", []),
        },

        "evidence": [
            f"Matched skills: {matched_skills}",
            f"Missing skills: {missing_skills}"
        ],

        "human_review_note": "This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."
    }

    write_json_report(report, OUTPUT_PATH, candidate_id)

    print(f"Report generated for {candidate_id}")



def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        return {}



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-id", required=True)
    args = parser.parse_args()

    run(args.candidate_id)