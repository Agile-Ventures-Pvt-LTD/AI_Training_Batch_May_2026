import json
def summarization_prompt(ticket):
    return f"""
Role:
You are a Senior Support Analyst.
Task:
Summarize the customer support ticket.
Input:
{json.dumps(ticket, indent=2)}
Rules:
- Use only provided ticket.
- Do not invent information.
{{
    "short_summary":"",
    "customer_problem":"",
    "business_impact":"",
    "customer_requested_action":"",
    "important_context":[],
    "missing_information":[]
}}
"""
def classification_prompt(ticket):
    return f"""
Role:
You are a Support Operations Triage Specialist.
Task:
Classify the support ticket.
Few-Shot
Ticket:
I was charged twice and need refund.
Output:
{{
    "primary_category":"BILLING_ISSUE"
}}

Dashboard crashes while exporting.

Output:
{{
    "primary_category":"TECHNICAL_BUG"
}}
Please add dark mode.

Output:
{{
    "primary_category":"FEATURE_REQUEST"
}}
Input:
{json.dumps(ticket, indent=2)}

{{
    "primary_category":"",
    "secondary_categories":[],
    "category_reasoning_summary":"",
    "confidence_score":0.0
}}
"""
def sentiment_prompt(ticket):

    return f"""
Role:
You are a Customer Experience Analyst.

Task:
Analyze customer sentiment.

Input:
{json.dumps(ticket, indent=2)}
Return valid JSON only.
{{
    "sentiment":"",
    "emotion_signals":[],
    "sentiment_reasoning_summary":"",
    "confidence_score":0.0
}}
"""

def risk_prompt(ticket):

    return f"""
Role:
You are a Support Escalation Manager.

Task:
Determine priority and escalation risk.

Input:
{json.dumps(ticket, indent=2)}

Return valid JSON only.
{{
    "priority":"",
    "escalation_risk":"",
    "risk_triggers":[],
    "recommended_sla_action":"",
    "reasoning_summary":""
}}
"""


def sensitive_info_prompt(ticket):

    return f"""
Role:
You are a Data Privacy Reviewer.

Task:
Detect sensitive information.

Input:
{json.dumps(ticket, indent=2)}
{{
    "sensitive_information_detected":true,
    "sensitive_categories":[],
    "evidence_summary":"",
    "handling_recommendations":[]
}}
"""
def routing_prompt(ticket):

    return f"""
Role:
You are a Support Operations Manager.

Task:
Recommend the correct internal team.

Input:
{json.dumps(ticket, indent=2)}

{{
    "recommended_team":"",
    "routing_reason":"",
    "internal_note":"",
    "required_follow_up_information":[]
}}
"""
def response_prompt(ticket):

    return f"""
Role:
You are a Senior Customer Support Agent.

Task:
Draft customer response.

Input:
{json.dumps(ticket, indent=2)}

Rules:
- Show empathy.
- Do not promise refunds.
- Do not promise cancellation.
- Do not invent account status.
- Ask for missing information.
{{
    "draft_response":"",
    "response_strategy":"",
    "assumptions":[],
    "information_needed_before_sending":[]
}}
"""
def quality_review_prompt(ticket):
    return f"""
Role:
You are a Support QA Reviewer.
Task:
Review the generated response.
Input:
{json.dumps(ticket, indent=2)}
{{
    "scores": {{
        "empathy":0,
        "correctness":0,
        "actionability":0,
        "policy_safety":0,
        "tone_alignment":0,
        "completeness":0
    }},
    "strengths":[],
    "improvement_areas":[],
    "final_review_summary":""
}}
"""