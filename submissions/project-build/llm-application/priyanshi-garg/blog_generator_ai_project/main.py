from groq_client import get_groq_client
from prompts import  Validation_message, user_message_template
from intent_classification import intent_classification_system_message
from input_summarization import system_message_for_summarization
from prompts import blog_outline_system_message
from blog_generation import blog_generation_system_message
from seo_metadata_generation import metadata_generation_system_message
from linkedin_post_generation import linkedin_post_generation_system_message
from quality_review import quality_review_system_message
from hallicunatin_control import hallucination_system_message
import json


prompt = f"""You are a helpful assistant that generates a final blog based on the following workflow.

1. Validate the user input using these criteria:
{Validation_message}
2. Detect the intent of the user input using:
{intent_classification_system_message}
3. Generate an input summary using:
{system_message_for_summarization}
4. Create a detailed blog outline using:
{blog_outline_system_message}
5. Draft the final blog using:
{blog_generation_system_message}
6. Extract SEO metadata using:
{metadata_generation_system_message}
7. Create an engaging LinkedIn post using:
{linkedin_post_generation_system_message}
8. Conduct a quality review using:
{quality_review_system_message}
9. Perform a hallucination check using:
{hallucination_system_message}

Use the provided user input below as the source material:
{user_message_template}
"""

call_llm = get_groq_client(
    system_prompt=prompt,
    user_input=user_message_template,
    model="openai/gpt-oss-120b",
    temperature=0.1
)
print(call_llm)

final_output = call_llm
print("HALLUCINATION CONTROL:\n")


output_path = "output/final_output.json"

with open(output_path, "w") as f:
    json.dump(final_output, f, indent=2)


print(f"Output successfully saved to: {output_path}")