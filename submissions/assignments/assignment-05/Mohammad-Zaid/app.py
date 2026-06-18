# app.py 

from output_formatter import save_output

from prebuilt_agent import prebuilt_langgraph_agent

print("\nCCMS AI Agent - LangGraph")

u_question = input("Please Enter Your Question: ")

result = prebuilt_langgraph_agent(u_question)

print("\nResponse:")
print(result)

save_output(
    "sample_prebuilt_agent_run.txt",
    u_question,
    result
    )
