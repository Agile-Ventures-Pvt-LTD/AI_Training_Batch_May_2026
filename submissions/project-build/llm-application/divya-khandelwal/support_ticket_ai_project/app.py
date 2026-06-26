from groq_client import call_groq_model
from validators import validate_groq_api_key, validate_ticket_request
import os
import json
from dotenv import load_dotenv
from prompts import Final_prompt, user_message
from output_parser import store_response_in_json
load_dotenv()

def main():

    api_key = os.environ["GROQ_API_KEY"]
    try:
        validate_groq_api_key(api_key)
    except ValueError as e:
        print(f"API Key validation error: {e}")
        return
    
    
    ticket_request = {
                "customer_name": "Amit",
                "customer_type": "Premium",
                "ticket_subject": "Charged twice and no response from support",
                "ticket_body": """Hi team, I cancelled my premium subscription last 
                month, but I was still charged again this month. I also noticed that 
                the same invoice amount appears twice on my bank statement. I 
                contacted support two times last week but have not received any proper
                response. This is extremely frustrating. If this is not resolved 
                today, I will escalate this publicly on LinkedIn and also ask our 
                finance team to block future payments. Please refund the incorrect 
                charge immediately. Regards, Amit""",
                "product_area": "Billing and subscription",
                "previous_interaction_history": """Customer says they contacted 
                support two times last week and did not receive a proper response.""",
                "sla_tier": "Premium",
                "response_tone": "Professional and empathetic",
                "business_rules": [
                "Do not promise refund before verification.",
                "Do not confirm cancellation unless verified.",
                "Ask for invoice ID or registered account email if required.",
                "Escalate premium customer billing issues to billing support."]
    }
    
    try:
        validate_ticket_request(ticket_request)
    except ValueError as e:
        print(f"Blog request validation error: {e}")
        return 
    
    
    response = call_groq_model(Final_prompt, user_message, ticket_request)
    
   
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True) 
    output_file_path = os.path.join(output_folder, "sample_ticket_output.json")
    
    store_response_in_json(response, output_file_path)
    
    print(f"GROQ Model Response has been saved to {output_file_path}")

if __name__ == "__main__":
    main()
