import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

VALIDATION_SYSTEM_MESSAGE = """
You are a validation agent for an AI-powered customer support ticket intelligence system.

## Your Task
Analyze the user's input and determine whether all required fields are present and valid.
Return your response as a JSON object — no prose, no markdown, just raw JSON.

## Required Fields & Validation Rules

1. ticket_subject: Must be non-empty.
2. ticket_body: Must be non-empty and at least 30 characters long.
3. response_tone: Must be non-empty. Must be one of: professional, empathetic, concise, formal, professional and empathetic.

## Optional Fields (no validation required)
- customer_name
- customer_type         (free, paid, premium, enterprise)
- product_area          (billing, login, dashboard, api, reports, subscription)
- previous_interaction_history
- sla_tier              (standard, premium, enterprise)
- business_rules        (list of policy strings)

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
- If ticket_body is present but under 30 characters, report it as a validation error with a clear message
"""


def validate_ticket_inputs(user_inputs: dict) -> dict:
    """
    Validate a support ticket input dict against FR-2 rules.
    Returns {"is_valid": bool, "errors": [...]} 
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": VALIDATION_SYSTEM_MESSAGE},
            {"role": "user", "content": json.dumps(user_inputs)},
        ],
        temperature=0,
    )

    result = response.choices[0].message.content
    clean = result.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean)
