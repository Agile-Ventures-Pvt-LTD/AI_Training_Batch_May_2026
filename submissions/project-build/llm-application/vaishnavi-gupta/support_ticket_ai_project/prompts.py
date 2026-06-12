def TICKET_SUMMARY_PROMPT(ticket):          #role-shot prompting

    return f"""
ROLE:
You are a Senior Support Analyst.

TASK:
Summarize the ticket.

INPUT:
{ticket}

RULES:
- Use only provided information.
- Remove emotional noise.
- Do not invent facts.
- Return JSON only.

OUTPUT:

{{
"short_summary":"",
"customer_problem":"",
"business_impact":"",
"customer_requested_action":"",
"important_context":[],
"missing_information":[]
}}
"""


def CLASSIFICATION_PROMPT(ticket):          #few-shot prompting

    return f"""

EXAMPLES:

Ticket:
Charged twice after cancellation

Output:
{{
"primary_category":"BILLING_ISSUE"
}}

Ticket:
Cannot login after password reset

Output:
{{
"primary_category":"ACCOUNT_ACCESS"
}}

NOW CLASSIFY:

{ticket}

RETURN:

{{
"primary_category":"",
"secondary_categories":[],
"category_reasoning_summary":"",
"confidence_score":
}}
"""


def SENTIMENT_PROMPT(ticket):                #role-shot prompting

    return f"""
ROLE:
Customer Experience Analyst

TASK:
Analyze sentiment.

INPUT:
{ticket}

OUTPUT:

{{
"sentiment":"",
"emotion_signals":[],
"sentiment_reasoning_summary":"",
"confidence_score":
}}
"""


def RISK_PROMPT(ticket):                     #zero-shot prompting

    return f"""


Determine:

1. Priority
2. Escalation Risk

INPUT:
{ticket}

OUTPUT:

{{
"priority":"",
"escalation_risk":"",
"risk_triggers":[],
"recommended_sla_action":"",
"reasoning_summary":""
}}
"""

def SENSITIVE_PROMPT(ticket):               #role-shot prompting

    return f"""
ROLE:
Data Privacy Reviewer

Identify sensitive information.

INPUT:
{ticket}

OUTPUT:

{{
"sensitive_information_detected": true,
"sensitive_categories":[],
"evidence_summary":"",
"handling_recommendations":[]
}}
"""


def ROUTING_PROMPT(                        #role-shot prompting
        ticket,
        category,
        risk
):

    return f"""
ROLE:
Support Operations Manager

TICKET:
{ticket}

CATEGORY:
{category}

RISK:
{risk}

OUTPUT:

{{
"recommended_team":"",
"routing_reason":"",
"internal_note":"",
"required_follow_up_information":[]
}}
"""


def RESPONSE_PROMPT(ticket):               #zero-shot prompting      

    return f"""


TASK:
Generate customer response.

INPUT:
{ticket}

RULES:

- Do NOT promise refunds.
- Do NOT confirm cancellation.
- Do NOT invent account status.
- Ask for missing information.
- Be empathetic.
- Explain next steps.

OUTPUT:

{{
"draft_response":"",
"response_strategy":"",
"assumptions":[],
"information_needed_before_sending":[]
}}
"""


def REVIEW_PROMPT(response):                #role-shot prompting

    return f"""
ROLE:
Support QA Reviewer

Review:

{response}

OUTPUT:

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