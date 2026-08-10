"""Main Configuration file for Supply Chain Logistics Rerouter."""

import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(ROOT_DIR, os.getenv("OUTPUT_PATH"))
DATA_DIR = os.path.join(ROOT_DIR, os.getenv("DATA_PATH"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
database = os.getenv("DB_PATH")
DB_PATH = os.path.join(ROOT_DIR, database)
data_file_name = os.getenv("data_file_name")

ROUTE_DIR = os.path.join(DATA_DIR, os.getenv("alternate_route_file_name"))
WAREHOUSE_DIR = os.path.join(DATA_DIR, os.getenv("warehouse_file_name"))

file_path = os.path.join(DATA_DIR, data_file_name)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not in .env")