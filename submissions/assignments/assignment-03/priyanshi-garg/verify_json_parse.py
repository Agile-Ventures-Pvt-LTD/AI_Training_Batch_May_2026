import json

raw_output = '''[
  {
    "batch_id": 1,
    "questions": [
      "Why did Tesla report fines in 2022?",
      "How did the 2022 fines affect Tesla's compliance costs?"
    ]
  }
]'''

cleaned_output = raw_output.removeprefix("```json").removesuffix("```").strip()
parsed_output = json.loads(cleaned_output)
if isinstance(parsed_output, dict):
    parsed_output = [parsed_output]

for entry in parsed_output:
    questions = entry.get("questions", [])
    print("type_of_questions", type(questions).__name__)
    print("is_list", isinstance(questions, list))
    print("first_question", questions[0])
