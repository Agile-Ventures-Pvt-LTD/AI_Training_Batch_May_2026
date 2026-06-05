ticket_summarization_prompt = """
You are a senior support analyst.
Your task is to summarize the customer support ticket into a concise summary.

Input:
Ticket subject: {ticket_subject}
Ticket body: {ticket_body}
Previous interaction history: {previous_interaction_history}
Customer type: {customer_type}
Product area: {product_area}
SLA tier: {sla_tier}
Response tone: {response_tone}
rules:
- Use only the provided ticket text and context.
- Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
- Identify the core issue, the requested action, the business impact, and missing information.

Output JSON:
{{
  "short_summary": "",
  "customer_problem": "",
  "business_impact": "",
  "customer_requested_action": "",
  "important_context": [],
  "missing_information": []
}}
"""

ticket_classification_prompt = """
You are a support operations triage specialist.
Your task is to classify the customer support ticket into the correct primary category and optional secondary categories from the given categories.
Input:
Ticket subject: {ticket_subject}
Ticket body: {ticket_body}
Product area: {product_area}
Customer type: {customer_type}
SLA tier: {sla_tier}
rules:
- Use only the provided ticket.
- Do not invent customer history or external policy.
- Do not classify based only on emotional tone.

Categories:
- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- SUBSCRIPTION_CHANGE
- COMPLIANCE_OR_PRIVACY
- PERFORMANCE_ISSUE
- HOW_TO_SUPPORT
- CANCELLATION_OR_REFUND
- ESCALATION_COMPLAINT
- OTHER

examples:
1. Billing issue with angry tone -> BILLING_ISSUE
2. Technical bug with neutral tone -> TECHNICAL_BUG

Output JSON:
{{
  "primary_category": "",
  "secondary_categories": [],
  "category_reasoning_summary": "",
  "confidence_score": 0.0
}}
"""

ticket_sentiment_prompt = """
You are a customer experience analyst.
Your task is to analyze the customer support ticket sentiment and emotion signals.
Input:
Ticket subject: {ticket_subject}
Ticket body: {ticket_body}
Previous interaction history: {previous_interaction_history}

rules:
- Use only the provided ticket text.
- Identify signals such as urgency, frustration, escalation threat, and repeated failed support attempts.
- Return valid JSON only.
Output JSON:
{{
  "sentiment": "",
  "emotion_signals": [],
  "sentiment_reasoning_summary": "",
  "confidence_score": 0.0
}}
"""

priority_and_risk_prompt = """
You are a support escalation manager.
Your task is to determine the ticket priority and escalation risk.
Input:
Ticket subject: {ticket_subject}
Ticket body: {ticket_body}
Customer type: {customer_type}
SLA tier: {sla_tier}
Previous interaction history: {previous_interaction_history}
rules:
- Use only the provided ticket.
- Do not invent account status, refunds, or cancellations.
- Return only a concise reasoning summary.
Output JSON:
{{
  "priority": "",
  "escalation_risk": "",
  "risk_triggers": [],
  "recommended_sla_action": "",
  "reasoning_summary": ""
}}
"""

sensitive_information_prompt = """
You are a data privacy reviewer.
Your task is to detect whether the ticket contains any sensitive information and classify the categories.
Input:
Ticket subject: {ticket_subject}
Ticket body: {ticket_body}
Business rules:
- Use only the provided ticket.
- Do not expose or print sensitive customer details.
- Flag payment information, personal identifiers, account identifiers, legal or compliance issues, and security information.
- Return valid JSON only.

Categories: 
PAYMENT_INFORMATION
PERSONAL_INFORMATION
ACCOUNT_IDENTIFIER
LEGAL_OR_COMPLIANCE_INFORMATION
SECURITY_INFORMATION
NONE_DETECTED

Output JSON:
{{
  "sensitive_information_detected": false,
  "sensitive_categories": [],
  "evidence_summary": "",
  "handling_recommendations": []
}}
"""

routing_recommendation_prompt = """
You are a support operations manager.
Your task is to recommend the correct internal team or queue for this ticket.
Input:
Ticket subject: {ticket_subject}
Ticket body: {ticket_body}
Primary category: {primary_category}
Secondary categories: {secondary_categories}
Priority: {priority}
Escalation risk: {escalation_risk}
Business rules:
- Use only the provided ticket and classification results.
- Do not invent team names apart from the given.

Teams:
- BILLING_SUPPORT
- TECHNICAL_SUPPORT
- ACCOUNT_MANAGEMENT
- SECURITY_TEAM
- COMPLIANCE_TEAM
- PRODUCT_TEAM
- CUSTOMER_SUCCESS
- GENERAL_SUPPORT
Output JSON:
{{
  "recommended_team": "",
  "routing_reason": "",
  "internal_note": "",
  "required_follow_up_information": []
}}
"""

draft_response_prompt = """
You are a senior customer support agent.
Your task is to draft a professional response for the ticket. Keep the response concise.
Input:
Customer name: {customer_name}
Ticket subject: {ticket_subject}
Ticket body: {ticket_body}
Primary category: {primary_category}
Priority: {priority}
Escalation risk: {escalation_risk}
Response tone: {response_tone}
rules:
- Use only the provided ticket
- Do not promise a refund or cancellation unless explicitly verified in the input.
- If information is missing, ask for it or state that the team will verify it.
- Acknowledge concern, show empathy, summarize the issue, and explain next steps.

Output JSON:
{{
  "draft_response": "",
  "response_strategy": "",
  "assumptions": [],
  "information_needed_before_sending": []
}}
Important rule : Do not promise a refund, service credit, or cancellation 
confirmation unless the ticket input explicitly confirms eligibility.
"""

quality_review_prompt = """
You are a support QA reviewer.
Your task is to review the draft response for empathy, correctness, actionability, policy safety, tone alignment, and completeness.
Input:
Draft response: {draft_response}
Response tone: {response_tone}
Business rules:
- Use only the provided draft response.
- Do not invent details beyond the draft response.
Output JSON:
{{
  "scores": {{
    "empathy": 0,
    "correctness": 0,
    "actionability": 0,
    "policy_safety": 0,
    "tone_alignment": 0,
    "completeness": 0
  }},
  "strengths": [],
  "improvement_areas": [],
  "final_review_summary": ""
}}
"""
