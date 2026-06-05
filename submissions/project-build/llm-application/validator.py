import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

## Here I need to build something that basically looks at the what the user is calling
## User will give his input + a value indicatign what they want the AI blog maker to do 

VALIDATION_SYSTEM_MESSAGE = """
You are a validation agent for an AI blog generation application.

## Your Task
Analyze the user's input and determine whether all required fields are present and valid.
Return your response as a JSON object — no prose, no markdown, just raw JSON.

## Required Fields & Validation Rules

1. blog_topic: Must be non-empty 
2. target_audience: Must be non-empty and describe a real audience segment
3. product_service_context: Must be non-empty; brief description of what is being promoted
4. key_points: Must be a list of at least3 distinct key points to cover in the blog
4. tone_style: Must be non- empty. Must be one of: professional, casual, educational, persuasive, conversational
5. blog_length: Must be non-empty; positive integer. Greater than 300 words and less than 1000 words.
6. seo_keywords:  Must be non-empt; must contain at least 2 distinct keywords
7. call_to_action: Must be non-empty; describes the action the reader should take

## Optional Fields (no validation required)
- industry_field
- claims_to_avoid
- brand_guidelines

## Output Format
Return exactly this JSON structure:

{
  "is_valid": true | false,
  "errors": [
    {
      "field": "<field_name>",
      "message": "<concise explanation of why it failed>"
    }
  ]
}

- If all required fields pass, set "is_valid": true and "errors": []
- List every failing field in "errors" — do not stop at the first failure
- Never fabricate or infer missing required field values
"""


def validate_blog_inputs(user_inputs: dict) -> dict:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": VALIDATION_SYSTEM_MESSAGE},
            {"role": "user", "content": json.dumps(user_inputs)}
        ],
        temperature=0,  
    )
    
    result = response.choices[0].message.content
    return json.loads(result)