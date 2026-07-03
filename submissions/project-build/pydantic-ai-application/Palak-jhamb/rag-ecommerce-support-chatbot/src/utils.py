#this is used to create vector database
from database import create_vector_store
from config import FOLDER_PATH
result=create_vector_store(FOLDER_PATH)
