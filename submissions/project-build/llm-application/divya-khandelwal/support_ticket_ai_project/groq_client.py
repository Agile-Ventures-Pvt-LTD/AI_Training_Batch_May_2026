import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

def call_groq_model(final_prompt, user_template, ticket_request):
    formatted_user_message = user_template.format(
        customer_name=ticket_request["customer_name"],
        customer_type=ticket_request["customer_type"],
        ticket_subject=ticket_request["ticket_subject"],
        ticket_body=ticket_request["ticket_body"],
        product_area=ticket_request["product_area"],
        previous_interaction_history=ticket_request["previous_interaction_history"],
        sla_tier=ticket_request["sla_tier"],
        response_tone=ticket_request["response_tone"],
        business_rules=ticket_request["business_rules"],
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": formatted_user_message},
        ],
        temperature=0.2,
        max_tokens=1500,
    )

    return response.choices[0].message.content