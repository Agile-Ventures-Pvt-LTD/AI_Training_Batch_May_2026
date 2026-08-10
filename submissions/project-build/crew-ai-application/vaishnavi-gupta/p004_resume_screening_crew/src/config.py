import os 
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')
DATASET_PATH = os.getenv('DATASET_PATH')
OUTPUT_PATH = os.getenv('OUTPUT_PATH')