from groq_client import parse_json_safe
import json
from groq_client import call_groq
from prompts import (ticket_summarizer_prompt,ticket_classifier,
                      ticket_analyzer,priority_escalation_prompt,
                      detection_prompt,routing_prompt,customer_service_agent_prompt,
                      qa_reviewer_prompt)
def run_pipeline(ticket):

    results = {}

    
    summary_raw = call_groq(ticket_summarizer_prompt)
    results["ticket_summary"] = parse_json_safe(summary_raw)

 
    class_raw = call_groq(ticket_classifier)
    results["classification"] = parse_json_safe(class_raw)

    sent_raw = call_groq(ticket_analyzer)
    results["sentiment_analysis"] = parse_json_safe(sent_raw)

  
    priority_raw = call_groq(priority_escalation_prompt)
    results["priority_and_risk"] = parse_json_safe(priority_raw)

    
    sensitive_raw = call_groq(detection_prompt)
    results["sensitive_information_check"] = parse_json_safe(sensitive_raw)

   
    routing_raw = call_groq(routing_prompt)
    results["routing_recommendation"] = parse_json_safe(routing_raw)

    
    response_raw = call_groq(customer_service_agent_prompt)
    results["draft_customer_response"] = parse_json_safe(response_raw)

    review_raw = call_groq(qa_reviewer_prompt)
    results["response_quality_review"] = parse_json_safe(review_raw)

   
    results["generation_metadata"] = {
        "model_used": "llama-3.1-70b-versatile",
        "temperature": 0,
        "total_steps_completed": 8
    }

    return results

