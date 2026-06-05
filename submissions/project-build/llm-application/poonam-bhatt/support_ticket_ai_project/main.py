from output_parser import run_pipeline
from groq_client import parse_json_safe

ticket={
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





result = run_pipeline(ticket)

file_path = parse_json_safe(result)
