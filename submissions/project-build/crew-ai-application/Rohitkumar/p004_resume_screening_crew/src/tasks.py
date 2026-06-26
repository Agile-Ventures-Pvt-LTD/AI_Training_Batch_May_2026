from crewai import Task


def create_jd_analysis_task(agent, jd_text):
    return Task(
        description=f"""Analyze the following job description and extract structured information.

Job Description:
{jd_text}

Extract the following fields:
1. role_title: The title of the role
2. required_skills: List of required skills from the job description
3. preferred_skills: List of preferred/nice-to-have skills
4. responsibilities: List of key responsibilities
5. experience_expectation: Experience range expected
6. evaluation_criteria: List of evaluation criteria mentioned

Return your output as a valid JSON object with exactly these fields.""",
        agent=agent,
        expected_output="A JSON object with role_title, required_skills (list), preferred_skills (list), responsibilities (list), experience_expectation (string), evaluation_criteria (list).",
        output_file=None
    )


def create_resume_extraction_task(agent, resume_text, candidate_id, candidate_name):
    return Task(
        description=f"""Extract structured information from the following resume.

Candidate ID: {candidate_id}
Candidate Name: {candidate_name}

Resume:
{resume_text}

Extract the following fields:
1. candidate_id: The candidate's ID
2. candidate_name: The candidate's full name
3. current_role: Their current job title
4. years_experience: Total years of experience
5. skills: List of all technical and professional skills mentioned
6. projects: List of projects mentioned
7. experience_summary: List of experience entries
8. education: List of education entries
9. certifications: List of certifications

Return your output as a valid JSON object with exactly these fields.""",
        agent=agent,
        expected_output="A JSON object with candidate_id, candidate_name, current_role, years_experience, skills (list), projects (list), experience_summary (list), education (list), certifications (list).",
        output_file=None
    )


def create_skill_matching_task(agent, jd_analysis, resume_profile, rubric_text):
    return Task(
        description=f"""Compare the job description requirements with the candidate profile and calculate fitment scores.

Job Analysis:
{jd_analysis}

Candidate Profile:
{resume_profile}

Screening Rubric:
{rubric_text}

Score each of these 8 categories from 0 to 5:
- python_programming
- sql_database_skills
- api_integration
- llm_application_development
- agent_frameworks
- rag_understanding
- testing_and_quality
- communication

Also identify:
1. matched_skills: Skills from JD that appear in the resume
2. partial_matches: Skills that partially match
3. missing_skills: Required skills not found in resume
4. category_scores: Object with all 8 category scores
5. overall_score: Sum of all category scores
6. max_score: 40
7. percentage: (overall_score / 40) * 100
8. recommendation_band: STRONG_MATCH (80-100), MODERATE_MATCH (60-79), WEAK_MATCH (40-59), NEEDS_MANUAL_REVIEW (below 40)

Return your output as a valid JSON object.""",
        agent=agent,
        expected_output="A JSON object with matched_skills (list), partial_matches (list), missing_skills (list), category_scores (object), overall_score (int), max_score (int), percentage (float), recommendation_band (string).",
        output_file=None
    )


def create_interview_planning_task(agent, jd_analysis, resume_profile, match_score):
    return Task(
        description=f"""Generate candidate-specific interview questions based on the job requirements, candidate profile, and gap analysis.

Job Analysis:
{jd_analysis}

Candidate Profile:
{resume_profile}

Match Score:
{match_score}

Generate at least:
- 3 technical questions to assess core skills
- 2 project deep-dive questions based on candidate's projects
- 2 scenario questions relevant to the role
- 2 gap-validation questions targeting missing or weak areas

Also identify interview_focus_areas based on gaps and role requirements.

Return your output as a valid JSON object with these fields:
- interview_focus_areas (list of strings)
- technical_questions (list of strings)
- project_deep_dive_questions (list of strings)
- scenario_questions (list of strings)
- gap_validation_questions (list of strings)""",
        agent=agent,
        expected_output="A JSON object with interview_focus_areas, technical_questions, project_deep_dive_questions, scenario_questions, gap_validation_questions (all lists of strings).",
        output_file=None
    )


def create_final_recommendation_task(agent, jd_analysis, resume_profile, match_score, interview_plan):
    return Task(
        description=f"""Produce the final screening report by consolidating all analysis results.

Job Analysis:
{jd_analysis}

Candidate Profile:
{resume_profile}

Match Score:
{match_score}

Interview Plan:
{interview_plan}

Generate a comprehensive final report with these fields:
1. candidate_id: From candidate profile
2. candidate_name: From candidate profile
3. role_title: From job analysis
4. overall_score: From match score
5. max_score: 40
6. percentage: From match score
7. recommendation: From match score recommendation_band
8. executive_summary: A 2-3 sentence summary of the candidate's fit
9. strengths: List of candidate's strong areas (use matched_skills)
10. gaps: List of candidate's weak areas (use missing_skills)
11. interview_focus_areas: From interview plan
12. interview_questions: Object containing technical_questions, project_deep_dive_questions, scenario_questions, gap_validation_questions
13. evidence: List of evidence points supporting the assessment
14. human_review_note: "This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."

Return your output as a valid JSON object.""",
        agent=agent,
        expected_output="A complete JSON report object with all required fields for the candidate screening report.",
        output_file=None
    )


def create_gap_analysis_task(agent, jd_analysis, resume_profile, match_score):
    return Task(
        description=f"""Analyze gaps in the candidate profile against job requirements.

Job Analysis:
{jd_analysis}

Candidate Profile:
{resume_profile}

Match Score:
{match_score}

Categorize gaps into:
1. critical_gaps: Skills absolutely required that are missing
2. moderate_gaps: Skills that would be useful but candidate has partial exposure
3. areas_to_probe: Topics to explore further during interview

Return as a valid JSON object.""",
        agent=agent,
        expected_output="A JSON object with critical_gaps (list), moderate_gaps (list), areas_to_probe (list).",
        output_file=None
    )


def create_report_review_task(agent, final_report):
    return Task(
        description=f"""Review the final screening report for completeness and quality.

Final Report:
{final_report}

Check:
1. All required fields are present (candidate_id, candidate_name, role_title, overall_score, max_score, percentage, recommendation, executive_summary, strengths, gaps, interview_focus_areas, interview_questions, evidence, human_review_note)
2. All scores are within valid ranges
3. Recommendation matches the score band
4. Interview questions are relevant
5. Evidence supports the conclusions

Return as a valid JSON object:
- report_complete (bool)
- missing_sections (list)
- schema_valid (bool)
- review_notes (list of strings)""",
        agent=agent,
        expected_output="A JSON object with report_complete (bool), missing_sections (list), schema_valid (bool), review_notes (list).",
        output_file=None
    )