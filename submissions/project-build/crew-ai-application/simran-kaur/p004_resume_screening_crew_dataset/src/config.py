from dotenv import load_dotenv
load_dotenv()

import os

groq_api_key = os.getenv("GROQ_API_KEY")

dataset_path=os.getenv('DATASET_PATH')

output_path=os.getenv('OUTPUT_PATH')

groq_model= os.getenv('GROQ_MODEL')