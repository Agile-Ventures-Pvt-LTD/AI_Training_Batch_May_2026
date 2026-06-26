from groq_client import get_groq_client
from prompts import*
import json


final_ticket_intelligence_message =  f"""You are a helpful assistant that generates a final ticket intelligence report based on the provided information.

1. Validate ticket input using these criteria:
{Validation_message}
2. Summarize the ticket using:
{ticket_summarization_message}
3. Classify the ticket category using:
{ticket_classification_message}
4. Analyze the customer sentiment using:
{customer_sentiment_analysis_message}
5. Detect priority and escalation risk using:
{ticket_prioritization_message}
6. Detect sensitive information using:
{sensitive_information_detection_message}
7. Recommend internal routing using:
{internal_routing_message}
8. Draft customer response using:
{draft_response_message}
9. Review generated response:
{response_quality_evaluation_message}

Build final ticket intelligence package.
The application must produce one final structured output:
{{
"ticket_summary": load_json("ticket_summary.json"),
"classification": load_json("classification.json"),
"sentiment_analysis": load_json("sentiment_analysis.json"),
"priority_and_risk": load_json("priority and risk analysis.json"),
"sensitive_information_check": load_json("sensitive_information_check.json"),
"routing_recommendation": load_json("routing_recommendation.json"),
"draft_customer_response": load_json("draft_customer_response.json"),
"response_quality_review": load_json("response_quality_review.json"),
"generation_metadata": load_json("generation_metadata.json"),
 "generation_metadata": {{
 "model_used": model,
 "temperature": temperature,
 "total_steps_completed": 10
 }}
}}


Use the provided user input below as the source material:
{user_message_template}
"""

call_llm = get_groq_client(
    system_prompt=final_ticket_intelligence_message,
    user_input=user_message_template,
    model="openai/gpt-oss-120b",
    temperature=0.1
)

output_path = "outputs/final_output.json"
import json

final_output = json.loads(call_llm)

with open("outputs/final_output.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)

print("Output successfully saved to outputs/final_output.json")