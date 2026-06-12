import json
import os
from xml.parsers.expat import model   
def parse_groq_response(response):
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError as e:
        print(f"Error parsing GROQ response: {e}")
        return None


def store_response_in_json(response, output_file_path):
    response_data = {
        "blog_intent_analysis": response
    }
    
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
