from uuid import uuid4

from agent import agent_executor
from memory import save_conversation
from evaluation.evaluation_logger import logger
from agent import run_agent



session_id = str(uuid4())

print("=" * 60)
print("AI HELPDESK TICKET OPERATIONS AGENT")
print("=" * 60)
answer=""

while True:

    user_query = input("\nAsk Question: ")

    if user_query.lower() == "exit":
        break

    try:

        response = agent_executor.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query
                    }
                ]
            }
        )

        print("\nAnswer:")
        answer=response["messages"][-1].content

        print(
            answer
        )

    except Exception as e:
        print("Error:", e)

    


    

    save_conversation(
        session_id=session_id,
        user_message=user_query,
        agent_response=answer,
        tools_used="auto"
    )

agent_executor.invoke(...)

while True:
    query = input("Ask Question: ")

    result = run_agent(
        user_query=query,
        agent=agent_executor,
        memory_used=True
    )

    print(result["output"])