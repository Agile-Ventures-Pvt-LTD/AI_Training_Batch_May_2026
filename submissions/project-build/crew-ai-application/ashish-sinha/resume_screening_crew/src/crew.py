import os
import json
import re
from dotenv import load_dotenv
from crewai import Crew, Process

from agents import ResumeScreeningAgents
from tasks import ResumeScreeningTasks
from tools import candidate_index_lookup_tool, score_calculator_tool, save_report_tool

load_dotenv()

class ResumeScreeningCrew:
    def __init__(self):
        self.agents_factory = ResumeScreeningAgents()
        self.tasks_factory = ResumeScreeningTasks()

    def kickoff(self, candidate_id: str) -> dict:
        lookup_res = candidate_index_lookup_tool._run(candidate_id=candidate_id)
        if not lookup_res.get("found"):
            raise ValueError(f"Aborting Pipeline: {lookup_res.get('message')}")
        
        base_path = os.getenv("DATASET_PATH", "data/p004_resume_screening_crew_dataset")
        jd_path = os.path.join(base_path, "job_description/jd_ai_engineer.md")
        resume_path = os.path.join(base_path, f"resumes/{lookup_res['resume_file']}")

        # Instantiate agents
        jd_analyst_agent = self.agents_factory.jd_analyst()
        resume_extractor_agent = self.agents_factory.resume_extractor()
        skill_matcher_agent = self.agents_factory.skill_matcher()
        gap_analyst_agent = self.agents_factory.gap_analyst()
        interview_planner_agent = self.agents_factory.interview_planner()
        rec_specialist_agent = self.agents_factory.recommendation_specialist()
        qa_agent = self.agents_factory.quality_controller()

        # Instantiate tasks
        task_jd = self.tasks_factory.jd_analysis_task(jd_analyst_agent, jd_path)
        task_resume = self.tasks_factory.resume_extraction_task(resume_extractor_agent, resume_path, candidate_id)
        task_match = self.tasks_factory.skill_matching_task(skill_matcher_agent, [task_jd, task_resume])
        task_gap = self.tasks_factory.gap_analysis_task(gap_analyst_agent, [task_jd, task_resume, task_match])
        task_interview = self.tasks_factory.interview_planning_task(interview_planner_agent, [task_jd, task_resume, task_match, task_gap])
        task_rec = self.tasks_factory.final_recommendation_task(rec_specialist_agent, [task_jd, task_resume, task_match, task_gap, task_interview])
        task_qa = self.tasks_factory.quality_control_task(qa_agent, [task_rec])

        # FIX: Added max_rpm=2 to restrict the crew to a maximum of 2 requests per minute.
        # This keeps token volume under Groq's 12,000 TPM limit.
        crew = Crew(
            agents=[
                jd_analyst_agent, resume_extractor_agent, skill_matcher_agent, 
                gap_analyst_agent, interview_planner_agent, rec_specialist_agent, qa_agent
            ],
            tasks=[task_jd, task_resume, task_match, task_gap, task_interview, task_rec, task_qa],
            process=Process.sequential,
            max_rpm=2, 
            verbose=True
        )

        # Execute multi-agent loop with active rate exception intercepting
        try:
            crew.kickoff()
        except Exception as e:
            print(f"[Warning] Crew execution encountered a rate limit or API block: {e}")

        # Extract whatever valid text data was compiled before hitting the limit
        final_report_data = {}
        raw_output_text = ""

        if hasattr(task_rec, 'output') and task_rec.output:
            raw_output_text = task_rec.output.raw
            final_report_data = task_rec.output.json_dict or {}
        elif hasattr(task_qa, 'output') and task_qa.output:
            raw_output_text = task_qa.output.raw
            final_report_data = task_qa.output.json_dict or {}

        # Fallback Substring RegEx Capture if Pydantic model output was interrupted
        if not final_report_data and raw_output_text:
            print("[System] Attempting partial text recovery from truncated text block...")
            try:
                json_match = re.search(r'\{.*\}', raw_output_text, re.DOTALL)
                if json_match:
                    final_report_data = json.loads(json_match.group(0))
            except Exception:
                pass

        # If data is completely empty due to a premature crash, populate mandatory fields
        if not final_report_data:
            final_report_data = {
                "status": "PARTIAL_OUTPUT_DUE_TO_RATE_LIMIT",
                "executive_summary": "Pipeline execution was interrupted by API limits. Review raw logs.",
                "strengths": [],
                "gaps": ["Unable to fully analyze profile due to token constraints."]
            }

        # Handle score calculations safely
        scores = final_report_data.get("category_scores", {})
        if not scores and hasattr(task_match, 'output') and task_match.output and task_match.output.json_dict:
            scores = task_match.output.json_dict.get("category_scores", {})
            
        if scores:
            calc_res = score_calculator_tool._run(category_scores=scores)
            final_report_data["overall_score"] = calc_res.get("overall_score", 0)
            final_report_data["percentage"] = calc_res.get("percentage", 0.0)
            final_report_data["recommendation"] = calc_res.get("recommendation_band", "NEEDS_MANUAL_REVIEW")
        else:
            final_report_data.setdefault("overall_score", 0)
            final_report_data.setdefault("percentage", 0.0)
            final_report_data.setdefault("recommendation", "NEEDS_MANUAL_REVIEW")

        # Injects compliance disclaimer note text
        final_report_data["human_review_note"] = (
            "This is an AI-assisted screening report based on the provided resume and job description. "
            "A human reviewer should validate the recommendation before making any recruitment decision."
        )
        
        final_report_data["candidate_id"] = final_report_data.get("candidate_id", candidate_id)
        final_report_data["candidate_name"] = final_report_data.get("candidate_name", lookup_res.get("candidate_name", "Unknown"))

        return final_report_data
