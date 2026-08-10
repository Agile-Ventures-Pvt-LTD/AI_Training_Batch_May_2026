from src.agent import agent
from src.schema import RagDeps, RagOutput
from src.database import get_text_chunks , load_pdf_documents

if __name__ == "__main__":
    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit", "q"]:
            print("Bye...")
            break

        try:
            result = agent.run_sync(user_prompt=query, deps=RagDeps(documents=get_text_chunks(load_pdf_documents())))
            response = result.output

            print("Response : ", response.response)
            print("Used Chunks : ", response.res_id)

        except Exception as e:
            print(e)