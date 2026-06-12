from langchain.agents import create_agent
from langchain_groq import ChatGroq
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
load_dotenv()
from config import GROQ_API_KEY, GROQ_MODEL






from tools import (
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
)

llm = ChatGroq(
    model=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0,
)

tools = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
]

agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)



from evaluation.evaluation_logger import logger





def run_agent(user_query, agent, memory_used=False):

    response = None  

    logger.set_user_request(user_query)
    logger.data["tools_used"] = []
    logger.data["final_answer"] = ""

    try:
        response = agent.invoke({"input": user_query})

        output = response.get("output", "")
        logger.set_final_answer(output)

    except Exception as e:
        error_msg = str(e)
        logger.set_final_answer(f"ERROR: {error_msg}")

        response = {
            "output": f"Error occurred: {error_msg}"
        }

    finally:
        logger.set_memory_used(memory_used)
        logger.set_write_action(False)

        logger.save()

    return response




