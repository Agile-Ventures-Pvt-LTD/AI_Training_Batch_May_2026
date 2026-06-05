import json

def ticket_classification_prompt(ticket_input):

    return f"""
Role: Senior Support Triage Specialist.

Task:
Classify the ticket.

Supported Categories:
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

Rules:
- Use only ticket data.
- Return ONLY JSON.

Ticket:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{{
    "primary_category": "",
    "secondary_categories": [],
    "category_reasoning_summary": "",
    "confidence_score": 0.0
}}
"""

def input_validation_prompt(ticket_input):
    return """
Role: You are a senior validator specialist.
Task:
Validate the customer support ticket.
Rule: 
- Do not hallucinate from the fabricated data.

Input:
{ticket_input}

Validation Rules:
1. Ticket subject cannot be empty.
2. Ticket body cannot be empty.
3. Ticket body must be at least 30 characters.
4. Response tone must be selected.
5. If previous history is provided, it should be included in the analysis.
6. If ticket body is too long, the system should summarize it first or ask the 
user to reduce the input.

Example validation error:
Ticket body is required and must contain at least 30 characters.

"""

def ticket_summarization_prompt(ticket_input):

    return f"""
Role: You are a Ticket Summarization Expert.

Task:
Summarize the support ticket.

Rules:
- Use only provided data.
- Do not invent facts.
- Return ONLY valid JSON.
- No markdown.
- No explanations.

Ticket:
{json.dumps(ticket_input, indent=2)}

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

def ticket_classification_prompt(ticket_input):

    return f"""
Role: You are a senior Machine Learning Engineer.

Task:
Classify the ticket into one primary category and optional secondary categories.

Rules:
1. Use ONLY the provided ticket.
2. Do not hallucinate.
3. Return ONLY valid JSON.
4. Do not use markdown.
5. Do not explain your answer.

Supported ticket categories:
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

Ticket Input:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{{
    "primary_category": "",
    "secondary_categories": [],
    "category_reasoning_summary": "",
    "confidence_score": 0.0
}}
"""


def sentiment_detection_prompt(ticket_input):

    return f"""
Role: Customer Sentiment Analyst.

Task:
Analyze sentiment.

Rules:
- Return ONLY JSON.
- No explanations.

Ticket:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{{
    "sentiment": "",
    "emotion_signals": [],
    "sentiment_reasoning_summary": "",
    "confidence_score": 0.0
}}
"""


def sentiment_detection_prompt(ticket_input):

    return f"""
Role: Customer Sentiment Analyst.

Task:
Analyze sentiment.

Rules:
- Return ONLY JSON.
- No explanations.

Ticket:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{{
    "sentiment": "",
    "emotion_signals": [],
    "sentiment_reasoning_summary": "",
    "confidence_score": 0.0
}}
"""

def prirority_escalation_detection_prompt(ticket_input):
    return  """
Role: You are a Senior Data Scientist.
Task: You have to detect and classify priority and escalation risk.
Rules:
1. Outout should be in JSON only
2. Use the priority and escalation labels provided. 
3. Provide output from that labels only.
Supported priority labels:
- LOW
- MEDIUM
- HIGH
- URGENT
The application must also classify escalation risk.
Supported escalation risk labels:
- LOW
- MEDIUM
- HIGH
- CRITICAL
Ticket Input:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{
"priority": "",
"escalation_risk": "",
"risk_triggers": [],
"recommended_sla_action": "",
"reasoning_summary": ""\
}

Priority should consider:
1. Customer impact
2. Business risk
3. Customer type
4. SLA tier
5. Repeated failed support attempts
6. Threat of public escalation
7. Payment or access impact
"""

def info_detection_prompt(ticket_input):
    return """ 
Role: You are Senior data scientist.
Task: You must detect whether the ticket includes sensitive information or not.
Rules:
1. Outout should be in JSON only
2. Use the priority and escalation labels provided. 
3. Provide output from that sensitive information categories only.
4. You must not print or expose sensitive information unnecessarily

Supported sensitive information categories:
1.PAYMENT_INFORMATION
2.PERSONAL_INFORMATION
3.ACCOUNT_IDENTIFIER
4.LEGAL_OR_COMPLIANCE_INFORMATION
5.SECURITY_INFORMATION
6.NONE_DETECTED

You should flag:
1.Payment information
2.Personal identifiers
3.Bank or card details
4.Account IDs
5.Legal complaints
6.Security issues
7.Confidential business information

Input:
{ticket_input}
Output JSON:
{
"sensitive_information_detected": true,
"sensitive_categories": [],
"evidence_summary": "",
"handling_recommendations": []
}
""" 


def sentiment_detection_prompt(ticket_input):

    return f"""
Role: Customer Sentiment Analyst.

Task:
Analyze sentiment.

Rules:
- Return ONLY JSON.
- No explanations.

Ticket:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{{
    "sentiment": "",
    "emotion_signals": [],
    "sentiment_reasoning_summary": "",
    "confidence_score": 0.0
}}
"""

def internal_routing_prompt(ticket_input):

    return f"""
Role: Internal Routing Manager.

Task:
Recommend the correct team.

Teams:
- BILLING_SUPPORT
- TECHNICAL_SUPPORT
- ACCOUNT_MANAGEMENT
- SECURITY_TEAM
- COMPLIANCE_TEAM
- PRODUCT_TEAM
- CUSTOMER_SUCCESS
- GENERAL_SUPPORT

Rules:
- Return ONLY JSON.

Ticket:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{{
    "recommended_team": "",
    "routing_reason": "",
    "internal_note": "",
    "required_follow_up_information": []
}}
"""

def draft_cust_resp_generation_prompt(ticket_input):

    return f"""
Role: Customer Support Agent.

Task:
Generate a response draft.

Rules:
- Be empathetic.
- Do not promise refunds.
- Do not confirm cancellation unless verified.
- Return ONLY JSON.

Ticket:
{json.dumps(ticket_input, indent=2)}

Output JSON:
{{
    "draft_response": "",
    "response_strategy": "",
    "assumptions": [],
    "information_needed_before_sending": []
}}
"""


def response_quality_review_prompt(ticket_input):

    return f"""
Role: Support QA Reviewer.

Task:
Review response quality.

Rules:
- Return ONLY JSON.

Ticket:
{json.dumps(ticket_input, indent=2)}

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