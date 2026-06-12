from outputs import*
from groq_client import get_groq_client
from prompts import user_message_template

final_response_system_message = """You are a helpful assistant that generates a final blog based in the following format.

final structured response containing:
{
 "blog_intent_analysis": {blog_intent},
 "input_summary": {blog_summarization},
 "blog_outline": {blog_outline},
 "final_blog": {blog_draft},
 "seo_metadata": {seo_metadata},
 "linkedin_post": {linkedin_post},
 "quality_review": {quality_review},
 "hallucination_check": {hallucination_control},
 "generation_metadata": {
 "model_used": {model} ,
 "temperature": {temperature} ,
 "total_steps_completed": 10 
 }
}

"""

call_llm = get_groq_client(
    system_prompt=final_response_system_message,
    user_input=user_message_template,
    model="openai/gpt-oss-120b",
    temperature=0.1
)
print(call_llm)

final_output = call_llm
print("FINAL OUTPUT:\n")

#save in json file
import json

output_path = "outputs/final_output.json"

with open(output_path, "w") as f:
    json.dump(final_output, f, indent=2)


print(f"Output successfully saved to: {output_path}")