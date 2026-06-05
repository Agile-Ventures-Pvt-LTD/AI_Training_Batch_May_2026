system_prompt = """
Ticket Summarization
The application must summarize the ticket into a concise support summary.
Output format:
{
}
"short_summary": "",
"customer_problem": "",
"business_impact": "",
"customer_requested_action": "",
"important_context": [],
"missing_information": []
The summary should:
 Remove emotional noise while preserving urgency.
 Identify the core issue.
 Identify what the customer wants.
 Identify missing information needed for resolution.
 Not invent details



# Ticket Classification
The application must classify the ticket into one primary category and optionally 
secondary categories.
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

Output format:
{
}
"primary_category": "",
"secondary_categories": [],
"category_reasoning_summary": "",
"confidence_score": 0.0
The model should not classify based only on emotional tone. It must identify the 
actual business issue

# Sentiment and Customer Emotion Detection
The application must classify customer sentiment.
Supported sentiment labels:
POSITIVE
NEUTRAL
NEGATIVE
FRUSTRATED
ANGRY
URGENT
Output format:
{
"sentiment": "",
"emotion_signals": [],
"sentiment_reasoning_summary": "",
"confidence_score": 0.0
}

The sentiment analysis should identify signals such as:
 Repeated follow-ups
 Threat of escalation
 Urgency
 Frustration
 Dissatisfaction
 Loss of trust

# Priority and Escalation Risk Detection
The application must classify ticket priority.
Supported priority labels:
LOW
MEDIUM
HIGH
URGENT
The application must also classify escalation risk.
Supported escalation risk labels:
LOW
MEDIUM
HIGH
CRITICAL
Output format:
{
}
"priority": "",
"escalation_risk": "",
"risk_triggers": [],
"recommended_sla_action": "",
"reasoning_summary": ""

Priority should consider:
1. Customer impact
2. Business risk
3. Customer type
4. SLA tier
5. Repeated failed support attempts
6. Threat of public escalation
7. Payment or access impact


# Sensitive Information Detection
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

# Suggested Internal Routing
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

The routing decision should be based on issue type, risk, and required action.


# Draft Customer Response Generation
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
9. Be concise but complete

Output format:
{
"draft_response": "",
"response_strategy": "",
"assumptions": [],
"information_needed_before_sending": []}

Important rule:
The assistant must not promise a refund, service credit, or cancellation 
confirmation unless the ticket input explicitly confirms eligibility.
Good response behavior: We will verify the cancellation date and duplicate charge.
Bad response behavior: We have processed your refund.


# Response Quality Review
The application must review the generated response before final output.
The review should score the response from 1 to 5 on:
Empathy: Does the response acknowledge customer frustration?
Correctness: Does it avoid unsupported claims?
Actionability: Does it provide clear next steps?
Policy Safety: Does it avoid risky promises?
Tone Alignment: Does it match the requested tone?
Completeness: Does it address the issue sufficiently?

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
"final_review_summary": ""}


### EXPECTED SAMPLE OUTPUT{
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
],"information_needed_before_sending": [
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
"temperature": 0.2,"total_steps_completed": 8
}
}
"""
#############################################################
ticket_summarization_prompt= """
Ticket Summarization
The application must summarize the ticket into a concise support summary.
Output format:
{
}
"short_summary": "",
"customer_problem": "",
"business_impact": "",
"customer_requested_action": "",
"important_context": [],
"missing_information": []
The summary should:
 Remove emotional noise while preserving urgency.
 Identify the core issue.
 Identify what the customer wants.
 Identify missing information needed for resolution.
 Not invent details
"""

ticket_classification_prompt = """Ticket Classification
The application must classify the ticket into one primary category and optionally 
secondary categories.
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

Output format:
{
}
"primary_category": "",
"secondary_categories": [],
"category_reasoning_summary": "",
"confidence_score": 0.0
The model should not classify based only on emotional tone. It must identify the 
actual business issue
"""

sentiment_prompt = """
Sentiment and Customer Emotion Detection
The application must classify customer sentiment.
Supported sentiment labels:
POSITIVE
NEUTRAL
NEGATIVE
FRUSTRATED
ANGRY
URGENT
Output format:
{
"sentiment": "",
"emotion_signals": [],
"sentiment_reasoning_summary": "",
"confidence_score": 0.0
}

The sentiment analysis should identify signals such as:
 Repeated follow-ups
 Threat of escalation
 Urgency
 Frustration
 Dissatisfaction
 Loss of trust

 """

priority_prompts= """
Priority and Escalation Risk Detection
The application must classify ticket priority.
Supported priority labels:
LOW
MEDIUM
HIGH
URGENT
The application must also classify escalation risk.
Supported escalation risk labels:
LOW
MEDIUM
HIGH
CRITICAL
Output format:
{
}
"priority": "",
"escalation_risk": "",
"risk_triggers": [],
"recommended_sla_action": "",
"reasoning_summary": ""

Priority should consider:
1. Customer impact
2. Business risk
3. Customer type
4. SLA tier
5. Repeated failed support attempts
6. Threat of public escalation
7. Payment or access impact
"""

sensitive_prompts="""
Sensitive Information Detection
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
}
"sensitive_information_detected": true,
"sensitive_categories": [],
"evidence_summary": "",
"handling_recommendations": []

The application must not print or expose sensitive information unnecessarily.
The model should flag:
 Payment information
 Personal identifiers
 Bank or card details
 Account IDs
 Legal complaints
 Security issues
 Confidential business information"""

internal_routing = """
Suggested Internal Routing
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

The routing decision should be based on issue type, risk, and required action."""

customer_response_prompts="""
Draft Customer Response Generation
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
9. Be concise but complete

Output format:
{
"draft_response": "",
"response_strategy": "",
"assumptions": [],
"information_needed_before_sending": []}

Important rule:
The assistant must not promise a refund, service credit, or cancellation 
confirmation unless the ticket input explicitly confirms eligibility.
Good response behavior: We will verify the cancellation date and duplicate charge.
Bad response behavior: We have processed your refund."""

response_quality_prompts=""" Response Quality Review
The application must review the generated response before final output.
The review should score the response from 1 to 5 on:
Empathy: Does the response acknowledge customer frustration?
Correctness: Does it avoid unsupported claims?
Actionability: Does it provide clear next steps?
Policy Safety: Does it avoid risky promises?
Tone Alignment: Does it match the requested tone?
Completeness: Does it address the issue sufficiently?

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
"final_review_summary": ""}
"""

