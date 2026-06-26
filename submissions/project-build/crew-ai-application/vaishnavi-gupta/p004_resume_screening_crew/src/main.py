from src.crew import ai_resume_screening_and_interview_planning

def main():
    project_name = """
    Hiring Management System

    Features:
    - Read job description 
    - Read candidate resumes
    - Extract structured candidate details
    - Match candidate skills against job requirements
    - Score candidate fit using a defined rubric
    - Identify gaps and areas to probe
    - Generate interview questions
    - Produce a final screening report for human review

    """

    crew = ai_resume_screening_and_interview_planning(
    
    project_name
)

    result = crew.kickoff()

    print("\n")
    print("=" * 100)
    print("FINAL OUTPUT")
    print("=" * 100)
    print(result)


if __name__ == "__main__":
    main()
