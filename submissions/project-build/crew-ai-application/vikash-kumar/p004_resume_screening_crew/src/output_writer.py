from crew import screening_crew
from crewai import LLM, Agent, Task, Crew, Process


user_input = "Screen CAND-001 for the AI Engineer role.",
" Screen CAND-002 for the AI Engineer role",
" Screen CAND-003 for the AI Engineer role",
" Screen all candidates.",
" Compare CAND-001 and CAND-005.",
" Identify top gaps across all candidates"


inputs = {'customer_query': user_input}

# Start the crew's work
result = screening_crew.kickoff(inputs=inputs)