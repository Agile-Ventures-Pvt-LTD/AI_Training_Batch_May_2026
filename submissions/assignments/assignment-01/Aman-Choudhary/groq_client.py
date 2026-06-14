import json
import os

from groq import Groq

from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

#client = Groq(
#    api_key="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"
#)

#------------------LLM CALL---------------------

def call_llm(prompt,user_prompt,
             model="llama-3.3-70b-versatile",
             temperature=0.2):

    response = client.chat.completions.create(
        model=model,
        messages=[
               {
                    "role": "system",
                    "content": prompt
               },
               {
                    "role": "user",
                    "content": user_prompt
               }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content


#--------------JSON EXTRACTION---------------

    
def extract_json(response_text):

    try:
        # find first and last brace
        start = response_text.find("{")
        end = response_text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON found in response")

        json_text = response_text[start:end+1]

        return json.loads(json_text)

    except Exception as e:
        return {
            "error": str(e),
            "raw_response": response_text
        }
    

#----------SAVE OUTPUT--------------------    


def save_output(filename, data):

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4)

      

#---------COMPLETE CASE RUNNER---------------

def run_case(case_name,
             prompt,user_prompt,
             output_file,
             temperature=0.2):
    

    raw_response = call_llm(
        prompt=prompt,
        user_prompt=user_prompt,
        temperature=temperature
    )

    parsed_response = extract_json(raw_response)

    result = {
        "case_name": case_name,
        "raw_response": raw_response,
        "parsed_response": parsed_response
    }

    save_output(output_file, result)
    

    return result        