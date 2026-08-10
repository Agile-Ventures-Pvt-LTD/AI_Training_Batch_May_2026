import json

summarize_prompt = """
    You are a Senior support analyst.
    Return valid JSON only. Do not include markdown.
        
    Analyze this support ticket and summarize the ticket into a concise support summary.
    
    {user_input}
    
    The summary should:
    - Remove emotional noise while preserving urgency.
    - Identify the core issue.
    - Identify what the customer wants.
    - Identify missing information needed for resolution.
    - Not invent details
    
    And strictly return it in JSON format with following structure:
    {{
        "short_summary": "",
        "customer_problem": "",
        "business_impact": "",
        "customer_requested_action": "",
        "important_context": [],
        "missing_information": []
    }}
    
    Rules:
    - Do not invent information.
    - Base your summary only on the provided input.
    - Return valid JSON only.
"""

classification_prompt = """
    You are a Support Operations Triage Specialist.
    Return valid JSON only. Do not include markdown.
    
    Analyze this ticket and classify the ticket into one primary category and optionally secondary categories.
    
    {user_input}
    
    There are the supported ticket categories:
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
    
    And strictly return it in JSON format with following structure:
    {{
        "primary_category": "",
        "secondary_categories": [],
        "category_reasoning_summary": "",
        "confidence_score": 0.0
    }}
    
    Rules:
    - Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
    - If information is missing, ask for it or say that the support team will verify it.
    - Base your summary only on the provided input.
    - Return valid JSON only.
    - Don't classify based only on emotional tone. It must identify the actual business issue.
"""


sentiment_prompt = [
    {
        "role": "system",
        "content": (
            "You are a Customer Experience Analyst. "
            "Return valid JSON only. Do not include markdown."
        )
    },
    {
        "role": "user",
        "content": """
        Analyze this ticket and classify customer sentiment.
        
        {user_input}
        
        There are the supported sentiment labels:
        - POSITIVE
        - NEUTRAL
        - NEGATIVE
        - FRUSTRATED
        - ANGRY
        - URGENT
        
        And strictly return it in JSON format with following structure:
        {{
            "sentiment": "",
            "emotion_signals": [],
            "sentiment_reasoning_summary": "",
            "confidence_score": 0.0
        }}
        
        Rules:
        - Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
        - If information is missing, ask for it or say that the support team will verify it.
        - Base your summary only on the provided input.
        - Return valid JSON only.
        - Identify signals such as:
            - Repeated follow-ups
            - Threat of escalation
            - Urgency
            - Frustration
            - Dissatisfaction
            - Loss of trust
        """
        
    },
]


escalation_and_priority_prompt = [
    {
        "role": "system",
        "content": (
            "You are a Support Escalation Manager."
            "Return valid JSON only. Do not include markdown."
        )
    },
    {
        "role": "user",
        "content": """
        Analyze this ticket and sentiment analysis and classify ticket priority and escalation risk.
        
        Ticket:
        {user_input}
        
        Sentiment Analysis:
        {sentiment_analysis}
        
        Supported escalation risk labels:
        - LOW
        - MEDIUM
        - HIGH
        - CRITICAL
        
        And strictly return it in JSON format with following structure:
        {{
            "priority": "",
            "escalation_risk": "",
            "risk_triggers": [],
            "recommended_sla_action": "",
            "reasoning_summary": ""
        }}
        
        Rules:
        - Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
        - Do not invent a numeric SLA time window unless it is present in the input.
        - If information is missing, ask for it or say that the support team will verify it.
        - Base your summary only on the provided input.
        - Return valid JSON only.
        - Priority should consider:
            1. Customer impact
            2. Business risk
            3. Customer type
            4. SLA tier
            5. Repeated failed support attempts
            6. Threat of public escalation
            7. Payment or access impact
        """
        
    },
]

sensitive_information_detection_prompt = [
    {
        "role": "system",
        "content": (
            "You are a Data Privacy Reviewer."
            "Return valid JSON only. Do not include markdown."
        )
    },
    {
        "role": "user",
        "content": """
        Analyze this ticket and detect whether the ticket includes sensitive information.
        
        {user_input}
        
        Supported sensitive information categories:
        - PAYMENT_INFORMATION
        - PERSONAL_INFORMATION
        - ACCOUNT_IDENTIFIER
        - LEGAL_OR_COMPLIANCE_INFORMATION
        - SECURITY_INFORMATION
        - NONE_DETECTED
        
        
        
        
        And strictly return it in JSON format with following structure:
        {{
            "sensitive_information_detected": true,
            "sensitive_categories": [],
            "evidence_summary": "",
            "handling_recommendations": []
        }}
        
        Rules:
        - Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
        - If information is missing, ask for it or say that the support team will verify it.
        - Base your summary only on the provided input.
        - Return valid JSON only.
        - Aim is to make sure application must not print or expose sensitive information unnecessarily.
        - The model should flag:
            - Payment information
            - Personal identifiers
            - Bank or card details
            - Account IDs
            - Legal complaints
            - Security issues
            - Confidential business information
        """
        
    },
]



routing_recommendation_prompt = [
    {
        "role": "system",
        "content": (
            "You are a Support Operations Manager"
            "Return valid JSON only. Do not include markdown."
        )
    },
    {
        "role": "user",
        "content": """
        Analyze this ticket and this priority and risk classification and recommend the correct internal team or queue.
        
        Ticket:
        {user_input}
        
        Priority and Risk Classification:
        {priority_and_risk}
        
        Supported teams:
        - BILLING_SUPPORT
        - TECHNICAL_SUPPORT
        - ACCOUNT_MANAGEMENT
        - SECURITY_TEAM
        - COMPLIANCE_TEAM
        - PRODUCT_TEAM
        - CUSTOMER_SUCCESS
        - GENERAL_SUPPORT
        
        
        
        And strictly return it in JSON format with following structure:
        {{
            "recommended_team": "",
            "routing_reason": "",
            "internal_note": "",
            "required_follow_up_information": []
        }}
        
        Rules:
        - Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
        - Do not invent a numeric SLA time window unless it is present in the input.
        - If information is missing, ask for it or say that the support team will verify it.
        - Base your summary only on the provided input.
        - Return valid JSON only.
        - Aim is to make sure routing decision should be based on issue type, risk, and required action.
        """
        
    },
]



draft_generation_prompt = [
    {
        "role": "system",
        "content": (
            "You are a Senior Customer Support Agent"
            "Return valid JSON only. Do not include markdown."
        )
    },
    {
        "role": "user",
        "content": """
        Analyze this ticket and generate a professional response that a support agent can review and send.
        
        {user_input}
        
        And strictly return it in JSON format with following structure:
        {{
            "draft_response": "",
            "response_strategy": "",
            "assumptions": [],
            "information_needed_before_sending": []
        }}
        
        Rules:
        - Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
        - Do not invent a numeric SLA time window unless it is present in the input.
        - If information is missing, ask for it or say that the support team will verify it.
        - Base your summary only on the provided input.
        - Return valid JSON only.
        - DO NOT promise a refund, service credit, or cancellation confirmation unless the ticket input explicitly confirms eligibility.
        - The response must:
            1. Acknowledge the customer's concern.
            2. Show empathy.
            3. Summarize the issue.
            4. Ask for missing information if required.
            5. Avoid unsupported promises.
            6. Avoid legal or financial commitments unless provided.
            7. Explain next steps clearly.
            8. Use the requested response tone.
            9. Be concise but complete.
        """
        
    }
]

response_quality_review = [
    {
        "role": "system",
        "content": (
            "You are a Support Operations Manager"
            "Return valid JSON only. Do not include markdown."
        )
    },
    {
        "role": "user",
        "content": """
        Analyze this ticket summary and review the generated response before it is passed on as final output.
        
        Ticket summary:
        {ticket_summary}
        
        Generated Response:
        {draft_customer_response}
        
        And strictly return it in JSON format with following structure:
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
        
        Rules:
        - Do not invent account status, refund status, cancellation status, SLA commitments, legal conclusions, or policy promises.
        - If information is missing, ask for it or say that the support team will verify it.
        - Base your summary only on the provided input.
        - Return valid JSON only.
        - Score the response from 1 to 5 on:
            -Empathy -> Does the response acknowledge customer frustration?
            -Correctness -> Does it avoid unsupported claims?
            -Actionability -> Does it provide clear next steps?
            -Policy Safety -> Does it avoid risky promises?
            -Tone Alignment -> Does it match the requested tone?
            -Completeness -> Does it address the issue sufficiently?
        """
        
    },
]








def _ticket_context(ticket: dict) -> str:
    return json.dumps(ticket, indent=2, ensure_ascii=False)


def build_analysis_messages(ticket: dict) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are a customer support ticket intelligence analyst. "
                "Return valid JSON only. Do not include markdown."
            ),
        },
        {
            "role": "user",
            "content": (
                "Analyze this support ticket and return exactly this JSON schema:\n"
                "{\n"
                '  "category": "short issue category",\n'
                '  "sentiment": "positive|neutral|negative",\n'
                '  "urgency": "low|medium|high|critical",\n'
                '  "priority_score": 1,\n'
                '  "risk_flags": ["short risk flag"],\n'
                '  "summary": "2-3 sentence factual summary",\n'
                '  "customer_intent": "what the customer wants",\n'
                '  "required_information": ["missing detail support needs"],\n'
                '  "recommended_team": "team name",\n'
                '  "next_best_actions": ["action for support agent"]\n'
                "}\n\n"
                "Rules:\n"
                "- priority_score must be an integer from 1 to 10.\n"
                "- Preserve uncertainty. Do not invent account, refund, or cancellation facts.\n"
                "- Use the SLA tier, customer type, prior history, and business rules when judging urgency.\n\n"
                f"Ticket:\n{_ticket_context(ticket)}"
            ),
        },
    ]


def build_response_messages(ticket: dict, analysis: dict) -> list[dict[str, str]]:
    payload = {"ticket": ticket, "analysis": analysis}
    return [
        {
            "role": "system",
            "content": (
                "You draft safe, empathetic customer support replies. "
                "Return valid JSON only. Do not include markdown."
            ),
        },
        {
            "role": "user",
            "content": (
                "Draft an agent-ready response for the customer and return exactly this JSON schema:\n"
                "{\n"
                '  "response_subject": "email subject",\n'
                '  "customer_response": "polished reply to customer",\n'
                '  "internal_note": "private note for support team",\n'
                '  "compliance_checks": ["business rule followed"],\n'
                '  "escalation_required": true,\n'
                '  "escalation_reason": "reason or empty string"\n'
                "}\n\n"
                "Rules:\n"
                "- Match the requested response tone.\n"
                "- Do not promise a refund, cancellation, credit, or completed action unless verified.\n"
                "- Ask only for missing information that is necessary to move the case forward.\n"
                "- Keep the customer response concise and practical.\n\n"
                f"Ticket and analysis:\n{json.dumps(payload, indent=2, ensure_ascii=False)}"
            ),
        },
    ]


def build_final_output_messages(ticket: dict, analysis: dict, response: dict) -> list[dict[str, str]]:
    payload = {"ticket": ticket, "analysis": analysis, "draft_response": response}
    return [
        {
            "role": "system",
            "content": (
                "You are a support operations QA reviewer. "
                "Return valid JSON only. Do not include markdown."
            ),
        },
        {
            "role": "user",
            "content": (
                "Create the final structured support-ticket intelligence output. "
                "Return exactly this JSON schema:\n"
                "{\n"
                '  "ticket_intelligence": {},\n'
                '  "recommended_actions": [],\n'
                '  "agent_response": {},\n'
                '  "quality_assurance": {\n'
                '    "business_rules_satisfied": [],\n'
                '    "needs_human_review": true,\n'
                '    "review_reason": "short reason"\n'
                "  }\n"
                "}\n\n"
                "Rules:\n"
                "- ticket_intelligence must include category, sentiment, urgency, priority_score, summary, risk_flags, and recommended_team.\n"
                "- agent_response must include response_subject, customer_response, internal_note, escalation_required, and escalation_reason.\n"
                "- Mark needs_human_review true when billing, refund, legal, public escalation, or account verification risk is present.\n\n"
                f"Inputs:\n{json.dumps(payload, indent=2, ensure_ascii=False)}"
            ),
        },
    ]
