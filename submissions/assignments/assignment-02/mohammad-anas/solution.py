import os
import chromadb
from dotenv import load_dotenv
from groq import Groq
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Setup
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing!")

client = Groq(api_key=api_key)
model_name = 'openai/gpt-oss-120b' 

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def setup_database():
    chromadb_client = chromadb.PersistentClient(path="./assignment2_vector_db")
    vectorstore = Chroma(
        collection_name='tesla_main_collection',
        embedding_function=embedding_model,
        client=chromadb_client
    )
    
    # Check if database is already created to save  time on rerun
    if vectorstore._collection.count() == 0:
        loader = PyPDFDirectoryLoader(".") 
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name='cl100k_base', chunk_size=512, chunk_overlap=16
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Total {len(chunks)} chunks created from PDF.")
        vectorstore.add_documents(documents=chunks)
    else:
        print(f"Loaded existing database with {vectorstore._collection.count()} chunks. ")
        
    return vectorstore.as_retriever(search_kwargs={'k': 3})

def run_query_expansion(retriever, test_query):
    
    print(f"Original Query: {test_query}")
    
    prompt = f"""You are a financial domain expert. Expand the following question into 3 different versions using synonyms to help with database retrieval. 
    Return ONLY a list of questions, each on a new line. Do not number them or use bullet points.
    Question: {test_query}"""
    
    try:
        response = client.chat.completions.create(
            model=model_name, 
            messages=[{'role': 'user', 'content': prompt}], 
            temperature=0
        )
        expanded_queries = response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        print(f"Error: {e}")
        expanded_queries = [test_query]

    print("\nExpanded Queries:")
    for q in expanded_queries:
        print(f" - {q}")

    all_retrieved_docs = []
    for q in expanded_queries:
        if q.strip():
            docs = retriever.invoke(q)
            all_retrieved_docs.extend(docs)

    unique_docs = {doc.page_content: doc for doc in all_retrieved_docs}.values()
    context_for_query = "\n---\n".join([doc.page_content for doc in unique_docs])

    final_prompt = [
        {'role': 'system', 'content': "Answer user queries ONLY using the context provided. If not found, say 'I don't know'."},
        {'role': 'user', 'content': f"<Context>\n{context_for_query}\n</Context>\n\n<Question>\n{test_query}\n</Question>"}
    ]

    ans_response = client.chat.completions.create(model=model_name, messages=final_prompt, temperature=0)
    print(ans_response.choices[0].message.content.strip())

if __name__ == "__main__":
    retriever = setup_database()
    run_query_expansion(retriever, "What were the major risks related to COVID-19 for Tesla?")