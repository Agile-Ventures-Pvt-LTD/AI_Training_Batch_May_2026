from crewai import Crew,Process


def build_crew(agents, tasks):
    return Crew(
        agents=list(agents),
        tasks=tasks,
        process=Process.sequential,
        memory=False,  
        cache=False,   
        max_rpm=100,
        share_crew=True
    )