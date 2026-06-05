from groq_client import get_groq_client
from prompts import user_message_template, Validation_message 

call_llm = get_groq_client(
    system_prompt=Validation_message,
    user_input=user_message_template,
    model="openai/gpt-oss-120b",
    temperature=0.1
)
print(call_llm)