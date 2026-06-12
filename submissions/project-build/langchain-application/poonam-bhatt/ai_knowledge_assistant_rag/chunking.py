#Chunking

from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)



#In this chunking we take the chunk size of 1000
#And also we used chunk_overlap to retain the information that can be lost from the end...