from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import TOOLS
import prompts
import config

def get_prebuilt_agent():
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not loaded.")
        
    primary_llm = ChatGroq(
        groq_api_key=config.GROQ_API_KEY,
        model_name=config.GROQ_MODEL,
        temperature=0.0
    )
    
    fallback_llm = ChatGroq(
        groq_api_key=config.GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.0
    )
    
    llm = primary_llm.with_fallbacks([fallback_llm])
    
    agent = create_react_agent(
        llm, 
        tools=TOOLS, 
        messages_modifier=prompts.SYSTEM_PROMPT
    )
    return agent

def run_prebuilt_agent(query):
    try:
        agent = get_prebuilt_agent()
        inputs = {"messages": [("user", query)]}
        response = agent.invoke(inputs)
    except Exception as e:
        if "429" in str(e) or "rate" in str(e).lower() or "limit" in str(e).lower():
            print(f"Primary model rate limited. Re-trying with fallback model llama-3.1-8b-instant. Error: {e}")
            from langchain_groq import ChatGroq
            from langgraph.prebuilt import create_react_agent
            from tools import TOOLS
            
            fallback_llm = ChatGroq(
                groq_api_key=config.GROQ_API_KEY,
                model_name="llama-3.1-8b-instant",
                temperature=0.0)
            fallback_agent = create_react_agent(
                fallback_llm, 
                tools=TOOLS, 
                messages_modifier=prompts.SYSTEM_PROMPT)
            inputs = {"messages": [("user", query)]}
            response = fallback_agent.invoke(inputs)
        else:
            raise e
            
    last_msg = response["messages"][-1]
    
    return {
        "messages": response["messages"],
        "final_response": last_msg.content
    }
