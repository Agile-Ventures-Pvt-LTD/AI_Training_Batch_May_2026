import json
from dotenv import load_dotenv
load_dotenv()
import os

from groq import Groq
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
client = Groq()
client


