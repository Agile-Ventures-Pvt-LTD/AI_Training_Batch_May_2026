from config import *
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_STORE = None

def create_retriever():
    global VECTOR_STORE

    loader = TextLoader("data/logistics_knowledge_base.txt")

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL_NAME
    )

    VECTOR_STORE = FAISS.from_documents(
        chunks,
        embeddings
    )

    return VECTOR_STORE.as_retriever(
        search_kwargs={
            "k":3
        }
    )



def retrieve_rules(query):

    retriever = create_retriever()

    docs = retriever.invoke(query)

    return "\n".join(
        [
            d.page_content
            for d in docs
        ]
    )
 