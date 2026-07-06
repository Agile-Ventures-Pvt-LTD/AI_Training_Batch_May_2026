from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

loader = TextLoader("data/logistics_knowledge_base.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=200,
    chunk_overlap=50
)
#less chunk_size since small database

chunks = text_splitter.split_documents(documents)   

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

db = FAISS.from_documents(chunks, embeddings)
db.save_local("faiss_index")

new_vectorstore = FAISS.load_local(
       "faiss_index", embeddings, allow_dangerous_deserialization=True
   )

system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
llm=ChatGroq(model="llama-3.3-70b-versatile")
create_docs_chain=create_stuff_documents_chain(llm,prompt)
retrieval_chain=create_retrieval_chain(new_vectorstore.as_retriever(), create_docs_chain)

# res = retrieval_chain.invoke({"input": "What happens when warehouse operating has above 85 percent utilization"})
# print(res["answer"])

def get_rag_context(query: str) -> str:
    docs = new_vectorstore.as_retriever().invoke(query)
    return "\n".join([doc.page_content for doc in docs])
