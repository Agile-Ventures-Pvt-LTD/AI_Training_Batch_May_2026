import uuid
from config import Config
from db_utils import DB
from memory import Memory
from tools import init_tools
from agent import create_helpdesk_agent

db = DB(Config.DB_PATH)
memory = Memory(db)

init_tools(db, memory)

agent_executor=create_helpdesk_agent()
session_id=str(uuid.uuid4())
chat_history=[]

print("AI helpdesk ticket operations agent")
print(f"Session id: {session_id}")
print("Type exit to stop\n")

while True:
    user_input= input("User: ")
    if not user_input.strip():
        continue
    if user_input.lower() in ["exit"]:
        break
    try:
        response=agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        agent_response = response.get("output", "Sorry I dont understand")
        print(f"Agent: {agent_response}\n")

        chat_history.append(("human", user_input))
        chat_history.append(("ai", agent_response))

        memory.save_conversation(session_id, user_input, agent_response, [])

    except Exception as e:
        print("Encountered error")
        print(e)