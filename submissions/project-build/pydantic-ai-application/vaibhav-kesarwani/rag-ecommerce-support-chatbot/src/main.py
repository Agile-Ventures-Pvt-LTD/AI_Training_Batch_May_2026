from agent import agent
from schema import RagDeps, RagOutput
from database import pdf_chunks

if __name__ == "__main__":
    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit", "q"]:
            print("Bye...")
            break

        try:
            result = agent.run_sync(user_prompt=query, deps=RagDeps(documents=pdf_chunks()))
            response = result.output

            print("Response : ", response.response)
            print("Used Chunks : ", response.res_id)

        except Exception as e:
            print(e)