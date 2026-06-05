Prompt_Ticket_Summarization= """

Summarize the following customer support ticket into a concise support summary.
Ticket Subject: [Insert Ticket Subject Here]
Ticket Body: [Insert Ticket Body Here]
Customer Name: [Insert Customer Name Here]
Customer Type: [Insert Customer Type Here]
Product Area: [Insert Product Area Here]
Previous Interaction History: [Insert Previous Interaction History Here]
SLA Tier: [Insert SLA Tier Here]
Response Tone: [Insert Response Tone Here]
The summary should include:
1. A short summary of the issue.
2. The core customer problem.
3. The business impact of the issue.
4. The action the customer is requesting.
5. Important context that may be relevant for resolution.
6. Any missing information that would be needed to resolve the issue.
Output the summary in the following JSON format:
{
 "short_summary": "",
 "customer_problem": "",
 "business_impact": "",
 "customer_requested_action": "",
 "important_context": [],
 "missing_information": []
}"""

prompt_Ticket_Classification = """
Classify the following customer support ticket into one primary category and optionally secondary categories.
Ticket Subject: [Insert Ticket Subject Here]
Ticket Body: [Insert Ticket Body Here]
Customer Name: [Insert Customer Name Here]
Customer Type: [Insert Customer Type Here]
Product Area: [Insert Product Area Here]
Previous Interaction History: [Insert Previous Interaction History Here]
SLA Tier: [Insert SLA Tier Here]
Response Tone: [Insert Response Tone Here]
Supported ticket categories:
BILLING_ISSUE
TECHNICAL_BUG
ACCOUNT_ACCESS
FEATURE_REQUEST
SUBSCRIPTION_CHANGE
COMPLIANCE_OR_PRIVACY
PERFORMANCE_ISSUE
HOW_TO_SUPPORT
CANCELLATION_OR_REFUND
ESCALATION_COMPLAINT
OTHER
The classification should identify the primary category that best fits the issue, and optionally any secondary categories if multiple issues are present. The classification should be based on the actual business issue described in the ticket, not just the emotional tone.
Output the classification in the following JSON format:
{
 "primary_category": "",
 "secondary_categories": [],
 "category_reasoning_summary": "",
 "confidence_score": 0.0
}"""

prompt_Sentiment_Analysis = """
Classify the sentiment of the following customer support ticket.
Ticket Subject: [Insert Ticket Subject Here]
Ticket Body: [Insert Ticket Body Here]
Customer Name: [Insert Customer Name Here]
Customer Type: [Insert Customer Type Here]
Product Area: [Insert Product Area Here]
Previous Interaction History: [Insert Previous Interaction History Here]
SLA Tier: [Insert SLA Tier Here]
Response Tone: [Insert Response Tone Here]
Supported sentiment labels:
POSITIVE
NEUTRAL
NEGATIVE
FRUSTRATED
ANGRY
URGENT
The sentiment analysis should identify the overall sentiment of the customer based on their message, as well as any specific emotion signals such as repeated follow-ups, threat of escalation, urgency, frustration, dissatisfaction, or loss of trust.
Output the sentiment analysis in the following JSON format:
{
 "sentiment": "",
 "emotion_signals": [],
 "sentiment_reasoning_summary": "",
 "confidence_score": 0.0
}"""

prompt_Priority_and_Escalation_Risk = """
Classify the priority and escalation risk of the following customer support ticket.
Ticket Subject: [Insert Ticket Subject Here]
Ticket Body: [Insert Ticket Body Here]
Customer Name: [Insert Customer Name Here]
Customer Type: [Insert Customer Type Here]
Product Area: [Insert Product Area Here]
Previous Interaction History: [Insert Previous Interaction History Here]
SLA Tier: [Insert SLA Tier Here]
Response Tone: [Insert Response Tone Here]
Supported priority labels:
LOW
MEDIUM
HIGH
URGENT
Supported escalation risk labels:
LOW
MEDIUM
HIGH
CRITICAL
The priority classification should consider factors such as customer impact, business risk, customer type, SLA tier
, repeated failed support attempts, threat of public escalation, and payment or access impact. The escalation risk classification should identify the likelihood that the issue will escalate if not resolved quickly.
Output the priority and escalation risk analysis in the following JSON format:
{
 "priority": "",
 "escalation_risk": "",
 "risk_triggers": [],
 "recommended_sla_action": "",
 "reasoning_summary": ""
}"""

prompt_sensitive_info_detection="""
The application must detect whether the ticket includes sensitive information.
Supported sensitive information categories:
PAYMENT_INFORMATION
PERSONAL_INFORMATION
ACCOUNT_IDENTIFIER
LEGAL_OR_COMPLIANCE_INFORMATION
SECURITY_INFORMATION
NONE_DETECTED
Output format:
{
 "sensitive_information_detected": true,
 "sensitive_categories": [],
 "evidence_summary": "",
 "handling_recommendations": []
}
The application must not print or expose sensitive information unnecessarily.
The model should flag:
 Payment information
 Personal identifiers
 Bank or card details
 Account IDs
 Legal complaints
 Security issues
 Confidential business information
"""

prompt_suggesting_internal_routing="""
The application must recommend the correct internal team or queue.
Supported teams:
BILLING_SUPPORT
TECHNICAL_SUPPORT
ACCOUNT_MANAGEMENT
SECURITY_TEAM
COMPLIANCE_TEAM
PRODUCT_TEAM
CUSTOMER_SUCCESS
GENERAL_SUPPORT
Output format:
{
 "recommended_team": "",
 "routing_reason": "",
 "internal_note": "",
 "required_follow_up_information": []
}
The routing decision should be based on issue type, risk, and required action


"""


prompt_draft_customer_response_generation="""
The application must generate a professional response that a support agent can 
review and send.
The response must:
1. Acknowledge the customer’s concern.
2. Show empathy.
3. Summarize the issue.
4. Ask for missing information if required.
5. Avoid unsupported promises.
6. Avoid legal or financial commitments unless provided.
7. Explain next steps clearly.
8. Use the requested response tone.
9. Be concise but complete.
Output format:
{
 "draft_response": "",
 "response_strategy": "",
 "assumptions": [],
 "information_needed_before_sending": []
}
Important rule:
The assistant must not promise a refund, service credit, or cancellation 
confirmation unless the ticket input explicitly confirms eligibility.
Good response behavior:
We will verify the cancellation date and duplicate charge.
Bad response behavior:
We have processed your refund.

"""

prompt_response_quality_review="""
The application must review the generated response before final output.
The review should score the response from 1 to 5 on:
Criterion Meaning
Empathy Does the response acknowledge 
customer frustration?
Correctness Does it avoid unsupported 
claims?
Actionability Does it provide clear next steps?
Policy Safety Does it avoid risky promises?
Tone Alignment Does it match the requested 
tone?
Completeness Does it address the issue 
sufficiently?
Output format:
{
 "scores": {
 "empathy": 0,
 "correctness": 0,
 "actionability": 0,
 "policy_safety": 0,
 "tone_alignment": 0,
 "completeness": 0
 },
 "strengths": [],
 "improvement_areas": [],
 "final_review_summary": ""
}


"""

Final_prompt = """

Role:
You are a senior support operations triage specialist.

Here is the example of input and output of the following task

{
 "customer_name": "Amit",
 "customer_type": "Premium",
 "ticket_subject": "Charged twice and no response from support",
 "ticket_body": "Hi team, I cancelled my premium subscription last 
month, but I was still charged again this month. I also noticed that 
the same invoice amount appears twice on my bank statement. I 
contacted support two times last week but have not received any proper
response. This is extremely frustrating. If this is not resolved 
today, I will escalate this publicly on LinkedIn and also ask our 
finance team to block future payments. Please refund the incorrect 
charge immediately. Regards, Amit",
 "product_area": "Billing and subscription",
 "previous_interaction_history": "Customer says they contacted 
support two times last week and did not receive a proper response.",
 "sla_tier": "Premium",
 "response_tone": "Professional and empathetic",
 "business_rules": [
 "Do not promise refund before verification.",
 "Do not confirm cancellation unless verified.",
 "Ask for invoice ID or registered account email if required.",
 "Escalate premium customer billing issues to billing support."
 ]
}

Using above all and the expected output is - 
{
 "ticket_summary": {
 "short_summary": "The customer reports being charged after 
cancelling a premium subscription and also seeing a duplicate charge. 
They are frustrated due to lack of prior support response and are 
requesting a refund.",
 "customer_problem": "Possible incorrect billing after cancellation
and possible duplicate charge.",
 "business_impact": "Risk of public escalation and payment block by
customer finance team.",
 "customer_requested_action": "Refund the incorrect charge 
immediately.",
 "important_context": [
 "Customer says they cancelled last month.",
 "Customer says they contacted support twice last week.",
 "Customer threatens public escalation on LinkedIn.",
 "Customer is on premium tier."
 ],
 "missing_information": [
 "Invoice ID",
 "Registered account email",
 "Cancellation confirmation date",
 "Charge transaction details"
 ]
 },
 "classification": {
 "primary_category": "BILLING_ISSUE",
 "secondary_categories": [
 "CANCELLATION_OR_REFUND",
 "ESCALATION_COMPLAINT"
 ],
 "category_reasoning_summary": "The core issue is billing after 
cancellation and duplicate charge, with escalation risk due to 
unresolved prior contacts.",
 "confidence_score": 0.93
 },
 "sentiment_analysis": {
 "sentiment": "FRUSTRATED",
 "emotion_signals": [
 "Customer says the situation is extremely frustrating.",
 "Customer contacted support twice without proper response.",
 "Customer threatens public escalation."
 ],
 "sentiment_reasoning_summary": "The customer expresses 
dissatisfaction, urgency, and loss of trust.",
 "confidence_score": 0.95
 },
 "priority_and_risk": {
 "priority": "URGENT",
 "escalation_risk": "HIGH",
 "risk_triggers": [
 "Premium customer",
 "Payment-related issue",
 "Repeated unresolved support attempts",
 "Threat of public escalation",
 "Request for immediate refund"
 ],
 "recommended_sla_action": "Route to billing support immediately 
and prioritize same-day review.",
 "reasoning_summary": "The billing impact, premium tier, repeated 
failed support attempts, and public escalation threat justify urgent 
handling."
 },
 "sensitive_information_check": {
 "sensitive_information_detected": true,
 "sensitive_categories": [
 "PAYMENT_INFORMATION"
 ],
 "evidence_summary": "The customer refers to bank statement charges
and subscription billing.",
 "handling_recommendations": [
 "Do not expose billing details unnecessarily.",
 "Ask for invoice ID or registered account email through secure 
channel.",
 "Escalate to billing support."
 ]
 },
 "routing_recommendation": {
 "recommended_team": "BILLING_SUPPORT",
 "routing_reason": "The issue involves cancellation, duplicate 
charge, refund request, and payment verification.",
 "internal_note": "Verify cancellation status, invoice history, and
duplicate charge before promising refund.",
 "required_follow_up_information": [
 "Invoice ID",
 "Registered account email",
 "Cancellation confirmation",
 "Transaction date"
 ]
 },
 "draft_customer_response": {
 "draft_response": "Hi Amit, I’m sorry for the frustration this has
caused, especially after you already contacted support twice. I 
understand that you are seeing a charge after cancelling your premium 
subscription and may also have been charged twice. We will escalate 
this to our billing support team for urgent review. To help verify the
cancellation date and the duplicate charge, please share your invoice 
ID or registered account email through the secure support channel. 
Once the billing details are verified, our team will confirm the next 
steps regarding refund eligibility. Thank you for your patience while 
we review this on priority.",
 "response_strategy": "Acknowledge frustration, summarize the 
issue, escalate to billing, ask for verification details, and avoid 
promising refund before verification.",
 "assumptions": [
 "The refund has not yet been verified.",
 "The cancellation date needs confirmation.",
 "The duplicate charge needs billing review."
 ],
 "information_needed_before_sending": [
 "Invoice ID",
 "Registered account email",
 "Cancellation confirmation"
 ]
 },
 "response_quality_review": {
 "scores": {
 "empathy": 5,
 "correctness": 5,
 "actionability": 5,
 "policy_safety": 5,
 "tone_alignment": 5,
 "completeness": 4
 },
 "strengths": [
 "Acknowledges customer frustration.",
 "Does not promise refund before verification.",
 "Provides clear next steps.",
 "Routes the issue appropriately."
 ],
 "improvement_areas": [
 "Could mention expected response timeline if SLA rules are 
known."
 ],
 "final_review_summary": "The response is safe, professional, 
empathetic, and suitable for agent review."
 },
 "generation_metadata": {
 "model_used": "llama-3.3-70b-versatile",
 "temperature": 0.2,
 "total_steps_completed": 8
 }
}


Rules:
- Use only the provided ticket.
- Do not invent customer history.
- Do not classify based only on emotional tone.
- Return valid JSON only.

"""

user_message="""
"customer_name": "{customer_name}",
"customer_type": "{customer_type}",
"ticket_subject": "{ticket_subject}",
"ticket_body": "{ticket_body}",
"product_area": "{product_area}",
"previous_interaction_history": "{previous_interaction_history}",
"sla_tier": "{sla_tier}",
"response_tone": "{response_tone}",
"business_rules": "{business_rules}"
"""