from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from config import GROQ_API_KEY, GROQ_MODEL
from tools import TOOLS
from memory import save_conversation_memory

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)

from langchain.agents import initialize_agent, AgentType

agent_executor = initialize_agent(
    tools=TOOLS,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
    

def health_check():

    try:

        response = llm.invoke("Reply with OK")

        return {
            "status": "healthy",
            "response": response.content
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }    

def run_agent(user_query: str):

    try:

        result = agent_executor.invoke(
            {"input": user_query}
        )

        print("\nRAW RESULT:\n")
        print(result)

        answer = result.get(
            "output",
            str(result)
        )

        save_conversation_memory(
            user_message=user_query,
            agent_response=answer,
            tools_used=""
        )

        return {
            "user_request": user_query,
            "plan_summary": "Agent selected tools automatically.",
            "tools_used": [],
            "reflection_summary": "Execution completed.",
            "final_answer": answer,
            "memory_saved": True
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        return {
            "error": str(e),
            "memory_saved": False
        }
