from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)


def test_leave_policy():

    docs = retriever.invoke(
        "When is the amazon LEO scheduled?"
    )

    assert len(docs) > 0


def test_reimbursement():

    docs = retriever.invoke(
        "What is AWS?"
    )

    assert len(docs) > 0


def test_compliance():

    docs = retriever.invoke(
        "What compliance requirements exist?"
    )

    assert len(docs) > 0