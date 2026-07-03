import asyncio
from src.guardrails_config import input_guardrail
from src.guardrails_config import output_guardrail
from dataclasses import dataclass
from rag.retriever import Retriever
from src.agent import rag_agent


@dataclass
class AgentDependencies:
    retriever: Retriever



async def main():

    retriever = Retriever()

    deps = AgentDependencies(
        retriever=retriever
    )

    print('='*20)
    print('Ask Question')
    print('='*20)

    question = input("Question:")

    if question.lower() == "exit":
        break

    try:

        safe_input = input_guardrail(question)

    except Exception as e:

        print(e)
        return

    response = await rag_agent.run(

            safe_input,

            deps=deps,

            )

    try:

        safe_output = output_guardrail(response)

    except Exception as e:

        print(e)
        return

    print("\nAssistant:\n")
    print(safe_output)


if __name__ == "__main__":
    main()



