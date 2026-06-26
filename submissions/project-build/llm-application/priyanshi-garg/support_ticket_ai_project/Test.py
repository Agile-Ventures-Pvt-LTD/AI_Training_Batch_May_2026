
from groq_client import get_groq_client
from prompts import*
import os
import json
import re

def data_save():

    prompts = [ticket_summarization_message, ticket_classification_message,customer_sentiment_analysis_message, ticket_prioritization_message, sensitive_information_detection_message, internal_routing_message, draft_response_message, response_quality_evaluation_message, metadata_generation]

    i = ["ticket_summary", "classification", "sentiment_analysis", "priority_and_risk", "sensitive_information_check", "routing_recommendation", "draft_customer_response","response_quality_review"]

    for i, template in enumerate(prompts):

        response = get_groq_client(
            system_prompt=template,
            user_input=user_message_template,
            model="openai/gpt-oss-120b",
            temperature=0.1
        )

        cleaned = re.sub(r"^```json\s*", "", response.strip())
        cleaned = re.sub(r"\s*```$", "", cleaned)

        parsed_output = json.loads(cleaned)

        output_path = f"tests/{i}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_output, f, indent=2)

        print(f"Saved: {output_path}")

data_save()



#



