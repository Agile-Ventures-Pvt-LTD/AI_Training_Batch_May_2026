from langchain_groq import ChatGroq
from retriever import retriever
from prompts import Grounded_Answer_Prompt
from dotenv import load_dotenv
load_dotenv()
from logger import log_query

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)


chat_history = []

print("\nEnterprise RAG Started")
print("Type 'exit' to quit.\n")

while True:

    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

   

    history_text = "\n".join(
        chat_history[-6:]
    )

    

    retrieval_query = f"""
    Conversation History:
    {history_text}

    Current Question:
    {query}
    """


    docs = retriever.invoke(
        retrieval_query
    )


    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )



    



    prompt = Grounded_Answer_Prompt.format(
            context=context,
            history=history_text,
            query=query
    )

    answer=llm.invoke(prompt)
    print(answer)
    

    

    print("\nSources Used:\n")

    seen = set()
    source="Amazon-2025-Annual-report.pdf"

    for doc in docs:
        source="Amazon-2025-Annual-report.pdf"

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        key = (source, page)

        if key not in seen:

            print(
                f"{source} | Page {page}"
            )

            seen.add(key)

    log_query(
                query,
                answer,
                source
            )

    

    chat_history.append(
        f"User: {query}"
    )

    chat_history.append(
        f"Assistant: {answer}"
    )

 