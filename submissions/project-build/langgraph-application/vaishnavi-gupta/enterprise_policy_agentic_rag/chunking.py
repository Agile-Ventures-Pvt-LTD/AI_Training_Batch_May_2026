import time
import chromadb

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=700,
    chunk_overlap=100
)

enetrprise_policy_agentic_rag_dataset1 = 'enetrprise_policy_agentic_rag_dataset1'


i = 0 # Initialize the starting index for the chunks

while i < len(enetrprise_policy_agentic_rag_dataset1): # Iterate while the index is less than the total number of chunks
    vectorstore.add_documents( # Add documents to the vector store in batches of 500
        documents=enetrprise_policy_agentic_rag_dataset1[i:i+500], # Get the current batch of 500 chunks
        ids=["text_" + str(i) for i in range(i, i+500)] # Assign unique IDs to each chunk in the batch
    )

    i += 500 # Increment the index by 500 to move to the next batch
    time.sleep(30) # Pause for 30 seconds to avoid rate limiting issues with the vector store