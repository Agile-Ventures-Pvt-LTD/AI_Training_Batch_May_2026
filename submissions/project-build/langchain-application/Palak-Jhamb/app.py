from groq_client import GroqClient
client=GroqClient()
from pathlib import Path
from prompts import classify_system, Classify_user
import json
import datetime
import chromadb
from langchain_chroma import Chroma
from config import DB_PATH
from embeddings import get_embedding_model

embedding_model = get_embedding_model()
chromadb_client = chromadb.Client()
vectorstore = Chroma(
    collection_name="amazon_docs",
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    client=chromadb_client,
    persist_directory=DB_PATH
)

user_query=input("Enter your query: ")
raw_response = client.generate(
system_prompt=classify_system,
user_prompt=Classify_user.format(query=user_query)
)
print(raw_response)
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)


output_file = output_dir / "classification.json"

with open(output_file, "w") as f:
    json.dump(raw_response, f, indent=4)
my_dict = json.loads(raw_response)

current_condition = my_dict['requires_retrieval']


print(my_dict)
if my_dict[current_condition]==True:
    from retriever import retrieve_documents
    retrieved_docs = retrieve_documents(vectorstore, user_query)
    print(retrieved_docs)
    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )
# from retriever import retrieve_documents
# retrieved_docs = retrieve_documents(vectorstore, user_query)
# print(retrieved_docs)
# context = "\n\n".join(
#         doc.page_content
#         for doc in retrieved_docs
#     )
context="not required"


from prompts import rag_system, rag_user
raw_response_rag = client.generate(
system_prompt=rag_system,
user_prompt=rag_user.format(query=user_query, retrieved_docs=context)
)
print(raw_response_rag)
output_file = output_dir / "rag_response_rag.json"
with open(output_file, "w") as f:
    json.dump(raw_response_rag, f, indent=4)

output_dir = Path("logs")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "query_logs.json"
log_entry = {
"timestamp": datetime.datetime.now().isoformat(),
"question": user_query,
"query_type": raw_response,
"retrieved_sources": context,
"answer": raw_response_rag,
}
with open(output_file, "w") as f:
    json.dump(log_entry, f, indent=4)