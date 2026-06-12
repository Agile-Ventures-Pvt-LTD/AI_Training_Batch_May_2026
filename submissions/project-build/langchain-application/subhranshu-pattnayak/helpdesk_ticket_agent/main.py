from dotenv import load_dotenv
from langchain_groq import ChatGroq
from agent.helpdesk_agent import build_agent
from tools.init import *

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

tools = [
    get_ticket_details,
    get_ticket_comments,
    get_overdue_tickets,
    get_work_queue,
    update_ticket_status,
    add_ticket_comment,
    save_conversation,
    recall_conversation,
    save_archival_memory,
    recall_archival_memory,
    summarize_conversation
]

agent_executor = build_agent(
    llm,
    tools
)


while True:
    query = input("User (Enter 'exit' to quit): ")
    if query == 'exit':
        break
    response = agent_executor.invoke(
        {
            "input": query
        }
    )

    print(response["output"])