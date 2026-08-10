import warnings
from guardrails import Guard
from pydantic import BaseModel
from typing import List
from guardrails import Guard
from guardrails.hub import ProfanityFree
from guardrails.hub import DetectPII, ProvenanceLLM


warnings.filterwarnings("ignore", category=UserWarning, module="guardrails")


class SellerReview(BaseModel):
    title: str
    sentiment: str  
    key_points: List[str]

guard = Guard.for_pydantic(output_class=SellerReview)

raw_output = """
{
  "title": "Review",
  "sentiment": "positive",
  "key_points": ["Mind-bending plot", "Brilliant direction"]
}
"""
validated_output = guard.parse(raw_output)

if validated_output.validation_passed:
    print("Validation Passed!")
    print(validated_output.validated_output)
else:
    print("Validation Failed!")
    print("Reason:", validated_output.reask.fail_results[0].error_message)



raw_output_1 = '''[('title','Review') , ('sentiment','positive'), ('key_points',['Mind-bending plot','Brilliant direction'])]'''

validated_output_1 = guard.parse(raw_output_1)

if validated_output_1.validation_passed:
    print("Validation Passed!")
    print(validated_output_1.validated_output)
else:
    print("Validation Failed!")
    print("Reason:", validated_output_1.reask.fail_results[0].error_message)    

raw_output = '''
{
  "title": "Review",
  "key_points": ["Mind-bending plot", "Brilliant direction"]
}
'''

validated_output = guard.parse(raw_output)

if validated_output.validation_passed:
    print("Validation Passed!")
    print(validated_output.validated_output)
else:
    print("Validation Failed!")
    print("Reason:", validated_output.reask.fail_results[0].error_message)


prompt = """
Generate a structured JSON response for a seller review with the following keys:
- title: name of the seller review
- sentiment: 'positive' or 'negative'
- key_points: a list of 2–3 bullet points summarizing the review

Review: SellerReview
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that always responds in valid JSON only."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)


generated_output = response.choices[0].message.content

validated_output = guard.parse(generated_output)

if validated_output.validation_passed:
    print("Validation Passed!")
    print(validated_output.validated_output)
else:
    print("Validation Failed!")
    print("Reason:", validated_output.reask.fail_results[0].error_message)


guard = Guard().use(ProfanityFree(on_fail="fix"))


'''
What Guardrails does:

1) Sends the user prompt to the LLM through llm_wrapper

2) Gets the LLM response

3) Checks if the LLM response contains profanity

4) Because you set on_fail="fix":

5) If it contains profanity → Guardrails rewrites it using the LLM

6) If not → just return it

'''



response = guard(
    llm_wrapper,
    messages=[{"role": "user", "content": "how to troll to my best friend with abusive language."}],
    model=model
)

print("Validated output:", response.validated_output)

