from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# Function to call LLM
def call_llm(system_message,
             user_message,
             model="openai/gpt-oss-120b",
             temperature=0.2):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content


# Extract JSON
def extract_json(response_text):

    try:
        return json.loads(response_text)

    except:

        match = re.search(r'\{.*\}', response_text, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except:
                return None

    return None



# Main function
def run_case(system_message,
             user_message,
             temperature=0.2):

    response = call_llm(
        system_message=system_message,
        user_message=user_message,
        temperature=temperature
    )

    parsed_output = extract_json(response)

    return parsed_output

# Function to save output
def save_output(filename, data):

    existing_data = []

    # Check if file already exists
    if os.path.exists(filename):

        with open(filename, "r") as file:

            try:
                existing_data = json.load(file)

            except:
                existing_data = []

    # If existing data is not list, convert to list
    if not isinstance(existing_data, list):
        existing_data = [existing_data]

    # Append new data
    existing_data.append(data)

    # Save updated list
    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)