from crewai import Agent


def get_agents(llm):
    jd_agent = Agent(
        role="JD Analyst",
        goal="Understand job requirements and extract key details",
        backstory="You read job descriptions and summarize them in structured form.",
        llm=llm
    )

    resume_agent = Agent(
        role="Resume Extractor",
        goal="Extract structured candidate information",
        backstory="You convert resumes into clean structured data.",
        llm=llm
    )

    matcher_agent = Agent(
        role="Matcher",
        goal="Compare candidate with job requirements and score",
        backstory="You evaluate skill fit and assign scores carefully.",
        llm=llm
    )

    interview_agent = Agent(
        role="Interview Planner",
        goal="Create interview questions based on candidate gaps",
        backstory="Technical interviewer who creates structured interview plans.",
        llm=llm
    )

    final_agent = Agent(
        role="Report Generator",
        goal="Generate final structured hiring report",
        backstory="Senior recruiter summarizing candidate evaluation.",
        llm=llm
    )

    return [jd_agent, resume_agent, matcher_agent, interview_agent, final_agent]