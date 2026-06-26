jd_schema_analyst_output_schema="""
"role_title": "",
"required_skills": [],
"preferred_skills": [],
"responsibilities": [],
"experience_expectation": "",
"evaluation_criteria": []"""

resume_extraction_output_schema="""{"candidate_id": "",
"candidate_name": "",
"current_role": "",
"years_experience": "",
"skills": [],
"projects": [],
"experience_summary": [],
"education": [],
"certifications": []}"""

skill_matching_output_schmea="""{
"matched_skills": [],
"partial_matches": [],
"missing_skills": [],
"category_scores": {
"python_programming": 0,
"sql_database_skills": 0,
"api_integration": 0,
"llm_application_development": 0,
"agent_frameworks": 0,
"rag_understanding": 0,
"testing_and_quality": 0,
"communication": 0
},
"overall_score": 0,
"max_score": 40,
"percentage": 0,
"recommendation_band": ""}"""

interview_planning_output_schmea="""{
"interview_focus_areas": [],
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []}"""

final_recommendation_output_schema="""{
"candidate_id": "",
"candidate_name": "",
"role_title": "",
"overall_score": 0,
"max_score": 40,
"percentage": 0,
"recommendation": "STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | 
NEEDS_MANUAL_REVIEW",
"executive_summary": "",
"strengths": [],
"gaps": [],
"interview_focus_areas": [],
"interview_questions": {
"technical_questions": [],
"project_deep_dive_questions": [],
"scenario_questions": [],
"gap_validation_questions": []
},
"evidence": [],
"human_review_note": ""}"""

gap_analysis_output_schema="""
{
"critical_gaps": [],
"moderate_gaps": [],
"areas_to_probe": []}"""

agent_review_output_schmea="""
{
"report_complete": true,
"missing_sections": [],
"schema_valid": true,
"review_notes": []}"""

valid_lookup_output_schema={"found": True,"candidate_id": "",
            "candidate_name": "Rohan Mehta","resume_file": "*.md"}


