import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client= Groq(
    os.environ['GROQ_API_KEY'] == os.getenv('GROQ_API_KEY')
)

response = client.chat.completions.create(
    model = GROQ_MODEL,
    messages=[
        {'role': 'system', 'content': 'system_prompt' },
        {'role': 'user', 'content': 'user_message'},
        {'role':'assistant', 'content':'assistant_message'}
    ],
    temperature=0,
    max_tokens=500,
    n = 1

)
response.choices[0].message.content