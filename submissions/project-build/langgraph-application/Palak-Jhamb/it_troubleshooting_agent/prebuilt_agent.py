from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from config import get_api_key
from tools import tools
from prompts import SYSTEM_PROMPT

#defining the llm
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=get_api_key(),
)
# defining the agent using prebuild react agents method
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)
#this function is defined to get response from llm
def invoke(user_input):
    messages_input = [HumanMessage(content=user_input)]
    response = agent.invoke({"messages": messages_input})
    final_ai_message = response['messages'][-1].content
    return final_ai_message