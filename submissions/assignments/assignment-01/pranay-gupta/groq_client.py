## Groq-client-setup

from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import os

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
client

