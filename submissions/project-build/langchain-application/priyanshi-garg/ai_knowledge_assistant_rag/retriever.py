from langchain_chroma import Chroma

from embedding import embedding

from config import TOP_K

db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding,
    collection_name="knowledge_base"
)

retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": TOP_K
    }
)


def retrieve(question):

    docs = retriever.invoke(question)

    return docs

docs = retriever.invoke("test query")

print("Retrieved docs:", len(docs))

for d in docs[:2]:
    print(d.page_content[:300])