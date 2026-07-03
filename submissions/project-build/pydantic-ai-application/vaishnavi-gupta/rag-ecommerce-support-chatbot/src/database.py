from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from config import DATA_PATH
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL
from langchain_chroma import Chroma
from config import VECTOR_DB_PATH
from src.embeddings import embedding_model
from config import TOP_K
from src.vector_store import get_vector_store



from config import (
    GROQ_API_KEY,
    MODEL_NAME
)

model = GroqModel(
    MODEL_NAME,
    api_key=GROQ_API_KEY,
)


class Citation(BaseModel):
    source_file: str
    chunk_id: str
    snippet: str


class RetrievedChunk(BaseModel):
    chunk_id: str
    source_file: str
    content: str
    score: float


class FinalAnswer(BaseModel):
    answer: str = Field(
        description="Final grounded answer"
    )

    citations: list[Citation]

    confidence: str

    recommended_next_step: str




def load_documents() -> list[Document]:
    """
    Load the pdf file from DATA_PATH.
    """

    documents: list[Document] = []

    for file in Path(DATA_PATH).glob("*.pdf"):

        loader = TextLoader(
            str(file),
            encoding="utf-8"
        )

        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = file.name
            doc.metadata["policy_domain"] = file.stem

        documents.extend(docs)

    return documents


from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


def split_documents(
    docs: list[Document]
) -> list[Document]:

    chunks = text_splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk_{i+1}"

    return chunks

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


def get_vector_store() -> Chroma:

    return Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embedding_model,
    )
def build_vector_store(chunks):

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(VECTOR_DB_PATH),
    )

    return vector_store


def get_retriever():

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(

        search_type="similarity",

        search_kwargs={
            "k": TOP_K
        }

    )

    return retriever

from src.vector_store import get_vector_store


def similarity_search(question: str):

    vector_store = get_vector_store()

    return vector_store.similarity_search_with_score(
        question,
        k=4
    )