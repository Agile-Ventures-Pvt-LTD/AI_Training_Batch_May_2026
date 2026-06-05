import json

SUMMARY_PROMPT = """
Role:
You are a senior support analyst.

Task:
Summarize the customer ticket.

Input:
{ticket}

Rules:
- Use only provided information.
- Do not invent facts.
- Remove emotional noise.
- Preserve urgency.
- Return valid JSON only.

Output JSON:

{{
 "short_summary":"",
 "customer_problem":"",
 "business_impact":"",
 "customer_requested_action":"",
 "important_context":[],
 "missing_information":[]
}}
"""

CLASSIFICATION_PROMPT = """
Role:
You are a support operations triage specialist.

Task:
Classify the ticket.

Ticket:
{ticket}

Return JSON:

{{
 "primary_category":"",
 "secondary_categories":[],
 "category_reasoning_summary":"",
 "confidence_score":0.0
}}
"""

SENTIMENT_PROMPT = """
Role:
You are a customer experience analyst.

Task:
Analyze sentiment.

Ticket:
{ticket}

Return JSON:

{{
 "sentiment":"",
 "emotion_signals":[],
 "sentiment_reasoning_summary":"",
 "confidence_score":0.0
}}
"""

PRIORITY_PROMPT = """
Role:
You are a support escalation manager.

Task:
Detect priority and escalation risk.

Ticket:
{ticket}

Return JSON:

{{
 "priority":"",
 "escalation_risk":"",
 "risk_triggers":[],
 "recommended_sla_action":"",
 "reasoning_summary":""
}}
"""

SENSITIVE_PROMPT = """
Role:
You are a data privacy reviewer.

Task:
Detect sensitive information.

Ticket:
{ticket}

Return JSON:

{{
 "sensitive_information_detected":true,
 "sensitive_categories":[],
 "evidence_summary":"",
 "handling_recommendations":[]
}}
"""

ROUTING_PROMPT = """
Role:
You are a support operations manager.

Task:
Recommend routing.

Ticket:
{ticket}

Return JSON:

{{
 "recommended_team":"",
 "routing_reason":"",
 "internal_note":"",
 "required_follow_up_information":[]
}}
"""

RESPONSE_PROMPT = """
Role:
You are a senior customer support agent.

Task:
Generate a professional customer response.

Ticket:
{ticket}

Rules:
- Be empathetic.
- Do not promise refunds.
- Do not promise cancellation confirmation.
- Ask for missing information if needed.
- Use tone: {tone}

Return JSON:

{{
 "draft_response":"",
 "response_strategy":"",
 "assumptions":[],
 "information_needed_before_sending":[]
}}
"""

QUALITY_PROMPT = """
Role:
You are a support QA reviewer.

Review this response.

Response:
{response}

Return:

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

