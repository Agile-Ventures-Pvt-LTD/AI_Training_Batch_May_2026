from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import tools
from prompts import SYSTEM_PROMPT
from config import config
llm = ChatGroq(
    model=config.GROQ_MODEL,
    temperature=0,
    api_key=config.GROQ_API_KEY
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
agent_executor = create_react_agent(llm, tools, prompt=prompt)