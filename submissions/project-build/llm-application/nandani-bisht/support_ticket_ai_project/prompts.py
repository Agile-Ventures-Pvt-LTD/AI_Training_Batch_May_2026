import json
def input_block(ticket):
    return json.dumps(ticket, indent=2, ensure_ascii=False)


def build_summary_prompt(ticket: dict) -> str:
    return f"""
Role: You are a senior support analyst.
Task: Summarize this customer support ticket into a concise support intelligence summary.
Input:
{input_block(ticket)}
Rules:
- Do not assume facts that are not present in the ticket.
- use only the provided ticket data.
- Remove emotional noise while preserving urgency.
- Identify the core issue, customer request, business impact, and missing information.
- Return valid JSON only.
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


def build_classification_prompt(ticket: dict) -> str:
    return f"""
Role:You are a support operations triage specialist.
Task: Classify the customer support ticket into the most appropriate business category.

Few-shot examples:
Example:
1) Ticket: Customer says they were charged twice after cancelling their subscription, asks for refund, and threatens escalation".
    primary_category: BILLING_ISSUE,
    secondary_categories: ["CANCELLATION_OR_REFUND"]
2) Ticket: User reports API error preventing login, tone is neutral, wants technical debugging.
   Primary category: TECHNICAL_BUG
   Secondary categories: [ACCOUNT_ACCESS]
3) Ticket: Customer asks for a new feature to export reports faster, tone is positive.
   Primary category: FEATURE_REQUEST
   Secondary categories: []
4) Ticket: Customer raises a privacy concern about data sharing and formal legal language.
   Primary category: COMPLIANCE_OR_PRIVACY
   Secondary categories: [SECURITY_INFORMATION]
5) Ticket: Customer complains about support quality and threatens public escalation.
   Primary category: ESCALATION_COMPLAINT
   Secondary categories: [OTHER]

Input:
{input_block(ticket)}
Rules:
- Use only the provided ticket.
- Do not classify based only on emotional tone.
- Identify the underlying business issue.
- Public escalation threat increases risk but does not change the domain category alone.
- Return valid JSON only.
Output JSON:
{{
  "primary_category": "",
  "secondary_categories": [],
  "category_reasoning_summary": "",
  "confidence_score": 0.0
}}
"""


def build_sentiment_prompt(ticket: dict) -> str:
    return f"""
Role: You are a customer experience analyst.
Task: Analyze the customer's sentiment and emotional signals.
Input:
{input_block(ticket)}
Rules:
- Use only the provided ticket.
- Detect the customer's sentiment and emotion without inventing details.
- Identify signals such as urgency, frustration, threats, and repeated failed contact.
- Return valid JSON only.
Output JSON:
{{
  "sentiment": "",
  "emotion_signals": [],
  "sentiment_reasoning_summary": "",
  "confidence_score": 0.0
}}
"""


def build_priority_risk_prompt(ticket: dict) -> str:
    return f"""
Role: You are a support escalation manager.
Task: Determine ticket priority and escalation risk for operational routing.
Few-shot examples are:
1) Customer is premium, has payment issue after cancellation, and threatens escalation publicly.
   Priority: URGENT
   Escalation risk: HIGH
2) Customer reports a minor dashboard display issue with neutral tone.
   Priority: LOW
   Escalation risk: LOW
3) Customer requests a new feature and is positive about the product.
   Priority: MEDIUM
   Escalation risk: LOW
4) Customer raises a privacy compliance concern in formal language.
   Priority: HIGH
   Escalation risk: MEDIUM
5) Customer has an unresolved complaint and threatens public escalation.
   Priority: URGENT
   Escalation risk: CRITICAL
   
Input:
{input_block(ticket)}
Rules:
- Use only the provided ticket.
- Consider customer impact, business risk, SLA tier, customer type, repeated failed attempts, and escalation threats.
- Do not promise any remediation outcome.
- Return valid JSON only.
Output JSON:
{{
  "priority": "",
  "escalation_risk": "",
  "risk_triggers": [],
  "recommended_sla_action": "",
  "reasoning_summary": ""
}}
"""


def build_sensitive_info_prompt(ticket: dict) -> str:
    return f"""
Role: You are a data privacy reviewer.
Task: Detect sensitive information in this support ticket.

Input:
{input_block(ticket)}
Rules:
- Use only the provided ticket.
- Flag sensitive categories without exposing the actual data.
- Do not print or expose customer identifiers or payment details.
- Return valid JSON only.
Output JSON:
{{
  "sensitive_information_detected": false,
  "sensitive_categories": [],
  "evidence_summary": "",
  "handling_recommendations": []
}}
"""


def build_routing_prompt(ticket: dict) -> str:
    return f"""

Role: You are a support operations manager.
Task: Recommend the correct internal support team or queue for this ticket.

Input:
{input_block(ticket)}
Rules:
- Use only the provided ticket.
- Base routing on issue type, risk, and required next action.
- Do not invent new operational teams.
- Return valid JSON only.
Output JSON:
{{
  "recommended_team": "",
  "routing_reason": "",
  "internal_note": "",
  "required_follow_up_information": []
}}
"""


def build_draft_response_prompt(ticket: dict, classification: dict = None) -> str:
    ticket_block = input_block(ticket)
    rules = [
        'Acknowledge the customer concern.',
        'Show empathy.',
        'Summarize the core issue.',
        'Ask for missing information if required.',
        'Avoid unsupported promises.',
        'Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.',
        'If information is missing, say the support team will verify it.',
        'Use the requested response tone.',
        'Keep the response concise but complete.',
    ]
    if classification is not None:
        rules.append('Route the issue according to the classification and escalation risk.')

    rules_block = '\n'.join(f'- {rule}' for rule in rules)
    return f"""Role: You are a senior customer support agent.
Task: Draft a customer-facing response for review by a support agent.
Input:
{ticket_block}
Rules:
{rules_block}
Output JSON:
{{
  "draft_response": "",
  "response_strategy": "",
  "assumptions": [],
  "information_needed_before_sending": []
}}
"""


def build_quality_review_prompt(ticket: dict, draft_customer_response: dict) -> str:
    ticket_block = input_block(ticket)
    response_text = draft_customer_response.get('draft_response', '')
    return f"""Role: You are a support QA reviewer.
Task: Review the generated draft response for empathy, correctness, actionability, policy safety, tone alignment, and completeness.
Input Ticket:
{ticket_block}
Draft Response:
{response_text}
Rules:
- Use only the provided ticket and response.
- Do not promise refunds or cancellations without verification.
- Score the response from 1 to 5.
- Return valid JSON only.
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
