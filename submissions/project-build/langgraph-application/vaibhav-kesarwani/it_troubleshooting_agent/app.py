from graph import graph
from prebuilt_agent import agent
from output_parser import output_parser
from langchain_core.messages import HumanMessage

while True: 
    question = input("\nAsk: ") 
    if question.lower() in ["quit", "exit", "stop"]: 
        break 
    
    prebuilt_agent_input = [HumanMessage(content=question)]
    
    try:
        prebuilt_agent_response = agent.invoke({"messages" : prebuilt_agent_input})
        final_prebuilt_agent_response = prebuilt_agent_response["messages"][-1].content

        # custom_agent_response = graph.invoke({"user_question" : question})
        # final_custom_agent_response = custom_agent_response["messages"][-1].content

        output_parser(prebuilt_agent_response["messages"], "sample_prebuilt_agent_run.txt")
        # output_parser(custom_agent_response["messages"], "sample_custom_agent_run.txt")

        print("\nAnswer:") 
        print(final_prebuilt_agent_response) 
    except Exception as e:
        print(e)