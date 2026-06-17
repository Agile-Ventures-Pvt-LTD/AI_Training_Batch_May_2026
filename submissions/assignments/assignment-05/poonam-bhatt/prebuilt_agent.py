from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import find_customer_by_name

from config import GROQ_API_KEY
from config import GROQ_MODEL

from prompts import SYSTEM_PROMPT

from tools import tools
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)
print("\n===== TOOLS =====")

for t in tools:
    print("\n", t.name)
    print(t.args)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)