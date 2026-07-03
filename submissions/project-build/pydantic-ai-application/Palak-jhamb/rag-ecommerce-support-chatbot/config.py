from dotenv import load_dotenv
load_dotenv()
import os
FOLDER_PATH=os.getenv("FOLDER_PATH")

CHUNK_SIZE=os.getenv("CHUNK_SIZE")
CHUNK_OVERLAP=os.getenv("CHUNK_OVERLAP")
EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL")
DB_PATH=os.getenv("DB_PATH")