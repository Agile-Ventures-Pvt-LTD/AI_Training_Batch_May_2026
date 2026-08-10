import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GROQ_MODEL=os.getenv("GROQ_MODEL")

BASE_DIR=Path(__file__).resolve().parent.parent
DATASET_PATH=BASE_DIR/ "data"

changes_path=DATASET_PATH/ "changes.json"
sample_queries_path=DATASET_PATH/ "sample_queries.json"
service_health_path=DATASET_PATH/ "service_health.json"
db_path=DATASET_PATH/ "tickets.db"








