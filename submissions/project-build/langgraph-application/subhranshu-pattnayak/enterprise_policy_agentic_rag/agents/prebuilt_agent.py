from utils.gClient import get_client
from tools.retrieval_tools import tools

llm = get_client()

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt
)