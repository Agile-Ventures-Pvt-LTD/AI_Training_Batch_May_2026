from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from output_parser import save_output

from config import GROQ_MODEL
from tools import search_policies, generate_grounded_answer
from prompts import AGENT_SYSTEM_PROMPT

llm = ChatGroq(model=GROQ_MODEL, temperature=0)

agent = create_react_agent(
    model=llm,
    tools=[search_policies, generate_grounded_answer],
    prompt=AGENT_SYSTEM_PROMPT,
)


def run(question: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    final_message = result["messages"][-1]
    print("\n=== FINAL RESPONSE ===")
    print(final_message.content)
    return final_message.content


if __name__ == "__main__":
    question = input("Ask a policy question: ")
    final_answer = run(question)
    save_output("sample_run_001", {"question": question, "response": final_answer})

