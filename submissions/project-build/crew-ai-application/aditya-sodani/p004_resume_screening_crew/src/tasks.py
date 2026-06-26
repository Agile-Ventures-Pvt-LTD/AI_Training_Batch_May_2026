from crewai import Task


def get_tasks(agents, jd_text, resume_text):

    
    jd_agent = agents[0]
    resume_agent = agents[1]
    match_agent = agents[2]
    interview_agent = agents[3]
    final_agent = agents[4]


    jd_task = Task(
        description=f"""
Return STRICT JSON only.

Extract:
- role_title
- required_skills (list)
- responsibilities (list)

JD:
{jd_text}
""",
        expected_output="Valid JSON only",
        agent=jd_agent
        # agent=agents[0]

    )

    resume_task = Task(
        description=f"""
Return STRICT JSON only.

Extract:
- candidate_name
- skills (list)
- projects (list)
- experience_summary (list)

Resume:
{resume_text}
""",
        expected_output="Valid JSON only",
        agent=resume_agent,
    )

    match_task = Task(
        description="""
Return STRICT JSON only.

Compare skills and return:
- matched_skills (list)
- missing_skills (list)

Do NOT guess anything not present.
""",
        expected_output="Valid JSON only",
        agent=match_agent,
    )

    interview_task = Task(
        description="""
Return STRICT JSON only with:

- technical_questions (3)
- project_deep_dive_questions (2)
- scenario_questions (2)
- gap_validation_questions (2)

Questions must match JD + candidate gaps.
""",
        expected_output="Valid JSON only",
        agent=interview_agent,
    )

    final_summary_task = Task(
        description="""
Return STRICT JSON only:

- strengths (list)
- gaps (list)
- executive_summary (short paragraph)

Use only previous outputs.
""",
        expected_output="Valid JSON only",
        agent=final_agent,
    )

    return [jd_task, resume_task, match_task, interview_task, final_summary_task]
