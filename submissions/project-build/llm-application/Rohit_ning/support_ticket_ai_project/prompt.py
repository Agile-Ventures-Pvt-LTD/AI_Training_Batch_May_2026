basic_rules = """
- Use only the provided ticket text.
- Do not invent facts, refund status, or cancellation details.
- Output valid JSON only.
- Keep the response concise and structured.
"""

TICKET_SUMMARY_PROMPT = """Role:
You are a senior support analyst.
Task:
Summarize the customer support ticket into a concise support summary with the required fields.
Input:
{context}
Rules:
{basic_rules}
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

CLASSIFICATION_PROMPT = """Role:
You are a support operations triage specialist.
Task:
Classify the customer support ticket into one primary category and optional secondary categories.
Rules:
{basic_rules}
Examples:
1. Ticket: "I was charged after canceling my premium subscription and see two charges on my bank statement."
   Primary: BILLING_ISSUE
   Secondary: [CANCELLATION_OR_REFUND, ESCALATION_COMPLAINT]

2. Ticket: "The dashboard is loading forever and shows 404 errors on the reports page."
   Primary: TECHNICAL_BUG
   Secondary: [PERFORMANCE_ISSUE]

3. Ticket: "Can you add a feature to export all invoices as CSV?"
   Primary: FEATURE_REQUEST
   Secondary: []

4. Ticket: "I am concerned my account data is being shared without my permission."
   Primary: COMPLIANCE_OR_PRIVACY
   Secondary: [SECURITY_INFORMATION]

5. Ticket: "I want to cancel because support has not responded to my two prior tickets and this is unacceptable!"
   Primary: ESCALATION_COMPLAINT
   Secondary: [CANCELLATION_OR_REFUND]

Input:
{context}

Output JSON:
{{
 "primary_category": "",
 "secondary_categories": [],
 "category_reasoning_summary": "",
 "confidence_score": 0.0
}}
"""

SENTIMENT_PROMPT = """Role:
You are a customer experience analyst.
Task:
Analyze the customer sentiment and emotion signals from the support ticket.
Input:
{context}
Rules:
{basic_rules}
Output JSON:
{{
 "sentiment": "",
 "emotion_signals": [],
 "sentiment_reasoning_summary": "",
 "confidence_score": 0.0
}}
"""

PRIORITY_RISK_PROMPT = """Role:
You are a support escalation manager.
Task:
Determine ticket priority and escalation risk for this customer support ticket.
Input:
{context}
Rules:
{basic_rules}
Output JSON:
{{
 "priority": "",
 "escalation_risk": "",
 "risk_triggers": [],
 "recommended_sla_action": "",
 "reasoning_summary": ""
}}
"""

SENSITIVE_PROMPT = """Role:
You are a data privacy reviewer.
Task:
Detect whether the ticket includes sensitive information and classify the sensitive categories.
Input:
{context}
Rules:
{basic_rules}
Output JSON:
{{
 "sensitive_information_detected": false,
 "sensitive_categories": [],
 "evidence_summary": "",
 "handling_recommendations": []
}}
"""

ROUTING_PROMPT = """Role:
You are a support operations manager.
Task:
Recommend the internal team or queue that should handle this ticket.
Input:
{context}
Rules:
{basic_rules}
Output JSON:
{{
 "recommended_team": "",
 "routing_reason": "",
 "internal_note": "",
 "required_follow_up_information": []
}}
"""

RESPONSE_PROMPT = """Role:
You are a senior customer support agent.
Task:
Draft a professional customer response for agent review.
Input:
{context}
Rules:
{basic_rules}
- Acknowledge the customer concern.
- Show empathy.
- Summarize the issue.
- Ask for missing information if required.
- Avoid unsupported promises.
- Do not invent refund or cancellation status.
Output JSON:
{{
 "draft_response": "",
 "response_strategy": "",
 "assumptions": [],
 "information_needed_before_sending": []
}}
"""

QUALITY_PROMPT = """Role:
You are a support QA reviewer.
Task:
Review the generated draft response for empathy, correctness, actionability, policy safety, tone, and completeness.
Input:
{context}
Rules:
{basic_rules}
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

