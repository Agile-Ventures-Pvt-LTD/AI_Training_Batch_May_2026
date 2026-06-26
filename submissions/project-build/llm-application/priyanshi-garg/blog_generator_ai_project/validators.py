from jsonschema import validate, ValidationError
import json

from streamlit import text
from app import call_llm

try:
    parsed_output = json.loads(call_llm)

    validate(instance=parsed_output, schema=schema)

    print("VALID JSON OUTPUT:\n")
    print(json.dumps(parsed_output, indent=2))

except json.JSONDecodeError:
    print("ERROR: Model output is not valid JSON.")

except ValidationError as e:
    print("SCHEMA VALIDATION ERROR:")
    print(e)


import os
os.makedirs("outputs", exist_ok=True)

# File path
output_path = "outputs/blog.md"

# Save JSON output
with open(output_path, "w") as f:
    text.dump(parsed_output, f, indent=2)

print(f"Output successfully saved to: {output_path}")