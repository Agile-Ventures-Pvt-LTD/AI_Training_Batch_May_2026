from prebuilt_agent import agent
from prompts import system_prompt
from output_formatter import output_formatter
from custom_react_agent import agent_workflow
from langchain_core.messages import HumanMessage, SystemMessage

while True: 
    question = input("\nAsk: ") 
    if question.lower() in ["quit", "exit", "stop"]: 
        break 

    prebuilt_message_input = [HumanMessage(content=question)]
    custom_message_input = [SystemMessage(content=system_prompt), HumanMessage(content=question)]
    
    try:
        # This is for the Prebuit agent in the LangGraph
        prebuilt_response = agent.invoke({"messages" : prebuilt_message_input})
        final_prebuilt_response = prebuilt_response["messages"][-1].content

        # This is for the Custom LangGraph Agent
        custom_response = agent_workflow.invoke({"messages" : custom_message_input})
        final_custom_response = custom_response["messages"][-1].content

        # Saving the Output in the output folder in .txt format    
        output_formatter(prebuilt_response["messages"], "sample_prebuilt_agent_run.txt")
        output_formatter(custom_response["messages"], "sample_custom_agent_run.txt")
       
        print("\nAnswer:") 
        print(final_prebuilt_response) # Just Change the varaible from final_prebuilt_response to final_custom_response for the custom made agent.
    
    except Exception as e:
        print(e)