from tools import (retrieve_ai_usage_policy,retrieve_hr_policy,retrieve_it_security_policy,
                   retrieve_reimbursement_policy,retrieve_travel_policy,rewrite_query,
                   generate_grounded_answer,grade_context)

from config import (GROQ_API_KEY, GROQ_MODEL)

from prompt import system_prompt

from langgraph.prebuilt import create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_groq import ChatGroq

agent_tools = [retrieve_ai_usage_policy,retrieve_hr_policy,retrieve_it_security_policy,
        retrieve_reimbursement_policy,retrieve_travel_policy,rewrite_query,
        generate_grounded_answer,grade_context]

llm = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY)

agent_prompt = ChatPromptTemplate.from_messages([("system",system_prompt)])

agent = create_react_agent(
    model=llm,
    tools=agent_tools,
    prompt=agent_prompt
)

def prebuilt_agent(user_input):
    try: 
        message_input = [HumanMessage(content=user_input)]
        response = agent.invoke({"messages": message_input})
        return response["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}"
