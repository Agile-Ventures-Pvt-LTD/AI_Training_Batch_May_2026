import os
import json
import time
from validators import validate_ticket_input
from groq_client import call_groq_model
from output_parser import parse_json_safely
from config import MODEL_NAME
import prompts

def main():
    print("Starting AI Support Ticket Intelligence Pipeline...\n")
    start_time = time.time()

    # 1. Sample Input from PDF
    ticket_input = {
        "customer_name": "Amit",
        "customer_type": "Premium",
        "ticket_subject": "Charged twice and no response from support",
        "ticket_body": "Hi team, I cancelled my premium subscription last month, but I was still charged again this month. I also noticed that the same invoice amount appears twice on my bank statement. I contacted support two times last week but have not received any proper response. This is extremely frustrating. If this is not resolved today, I will escalate this publicly on LinkedIn and also ask our finance team to block future payments. Please refund the incorrect charge immediately. Regards, Amit",
        "product_area": "Billing and subscription",
        "previous_interaction_history": "Customer says they contacted support two times last week and did not receive a proper response.",
        "sla_tier": "Premium",
        "response_tone": "Professional and empathetic",
        "business_rules": [
            "Do not promise refund before verification.",
            "Do not confirm cancellation unless verified.",
            "Ask for invoice ID or registered account email if required.",
            "Escalate premium customer billing issues to billing support."
        ]
    }

    # 2. Input Validation
    errors = validate_ticket_input(ticket_input)
    if errors:
        print("[ERROR] Ticket Validation Failed:")
        for e in errors: print(f"- {e}")
        return

    payload_str = prompts.format_ticket_payload(ticket_input)

    # 3. Summarization
    print("Step 1/6: Summarizing ticket...")
    summary_raw = call_groq_model(payload_str, prompts.SUMMARY_SYSTEM_PROMPT, temperature=0.1)
    summary_json = parse_json_safely(summary_raw)

    # 4. Classification
    print("Step 2/6: Classifying category...")
    class_raw = call_groq_model(payload_str, prompts.CLASSIFICATION_SYSTEM_PROMPT, temperature=0.1)
    class_json = parse_json_safely(class_raw)

    # 5. Sentiment & Priority (Combined to save time/calls)
    print("Step 3/6: Analyzing sentiment, priority, and escalation risk...")
    risk_raw = call_groq_model(payload_str, prompts.SENTIMENT_PRIORITY_SYSTEM_PROMPT, temperature=0.1)
    risk_json = parse_json_safely(risk_raw)

    # 6. Sensitive Info & Routing (Combined)
    print("Step 4/6: Detecting sensitive info and routing...")
    route_raw = call_groq_model(payload_str, prompts.SENSITIVE_ROUTING_SYSTEM_PROMPT, temperature=0.1)
    route_json = parse_json_safely(route_raw)

    # 7. Draft Response
    print("Step 5/6: Drafting customer response...")
    # Injecting the routing rules and summary so the AI knows what to tell the customer
    draft_context = f"Ticket Payload:\n{payload_str}\n\nRouting Rules:\n{json.dumps(route_json)}"
    draft_raw = call_groq_model(draft_context, prompts.DRAFT_RESPONSE_SYSTEM_PROMPT, temperature=0.3)
    draft_json = parse_json_safely(draft_raw)

    # 8. Quality Review
    print("Step 6/6: Performing response QA review...")
    qa_context = f"Customer Ticket:\n{ticket_input['ticket_body']}\n\nDrafted Response:\n{draft_json.get('draft_response', '')}"
    qa_raw = call_groq_model(qa_context, prompts.QUALITY_REVIEW_SYSTEM_PROMPT, temperature=0.0)
    qa_json = parse_json_safely(qa_raw)

    # 9. Build Final Package
    final_package = {
        "ticket_summary": summary_json,
        "classification": class_json,
        "sentiment_analysis": {
            "sentiment": risk_json.get("sentiment"),
            "emotion_signals": risk_json.get("emotion_signals"),
            "sentiment_reasoning_summary": risk_json.get("sentiment_reasoning_summary")
        },
        "priority_and_risk": {
            "priority": risk_json.get("priority"),
            "escalation_risk": risk_json.get("escalation_risk"),
            "risk_triggers": risk_json.get("risk_triggers"),
            "recommended_sla_action": risk_json.get("recommended_sla_action"),
            "reasoning_summary": risk_json.get("reasoning_summary")
        },
        "sensitive_information_check": {
            "sensitive_information_detected": route_json.get("sensitive_information_detected"),
            "sensitive_categories": route_json.get("sensitive_categories"),
            "evidence_summary": route_json.get("evidence_summary"),
            "handling_recommendations": route_json.get("handling_recommendations")
        },
        "routing_recommendation": {
            "recommended_team": route_json.get("recommended_team"),
            "routing_reason": route_json.get("routing_reason"),
            "internal_note": route_json.get("internal_note"),
            "required_follow_up_information": route_json.get("required_follow_up_information")
        },
        "draft_customer_response": draft_json,
        "response_quality_review": qa_json,
        "generation_metadata": {
            "model_used": MODEL_NAME,
            "temperature_range": "0.0 - 0.3",
            "total_steps_completed": 6,
            "execution_time_seconds": round(time.time() - start_time, 2)
        }
    }

    # 10. Save Output
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/sample_ticket_output.json", "w") as f:
        json.dump(final_package, f, indent=4)
        
    print(f"\n Ticket analysis complete in {final_package['generation_metadata']['execution_time_seconds']} seconds!")
    print(" Output successfully saved to: outputs/sample_ticket_output.json")

if __name__ == "__main__":
    main()