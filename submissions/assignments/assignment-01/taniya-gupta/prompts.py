# prompts.py
"""
Prompt definitions for all cases. Each case's prompt will be fed to the LLM.
"""
import json
__all__ = [ "PROMPT_CASE1_1", "PROMPT_CASE1_2", "VENDOR_NOTE_CASE1_1" , "SITUATION", "PROMPT_CASE2_1", "TICKETS", "TEST_MESSAGES", "PROMPT_CASE2_2", "PROMPT_CASE3_1", "PROMPT_CASE3_2", "CUSTOMER_QUESTION", "RESPONSE_A", "RESPONSE_B", "DEVELOPER_QUESTION", "EXPLANATION_A", "EXPLANATION_B", "PROMPT_CASE4_1", "PROMPT_CASE4_2", "PROMPT_CASE5_1" , "POLICY_TEXT", "CLAIM", "PROMPT_CASE5_2", "SECURITY_CONTEXT", "PROMPT_CASE6_1", "OPTIONS_6_1", "PROMPT_CASE6_2", "PROMPT_CASE7_1", "PROMPT_CASE7_2"]

VENDOR_NOTE_CASE1_1 = """
Vendor: DocuMind AI
The vendor claims their solution can process invoices, contracts, and identity documents using
 OCR and LLM-based extraction. They say the model is hosted in a multi-tenant cloud
 environment. They do not currently provide region-specific data residency, but they are
 planning to add it next year.
They support encryption at rest and in transit. However, customer data may be used for product
 improvement unless customers opt out through a manual request. They have SOC 2 Type I
 certification but not Type II. Their uptime SLA is 99.5%.
The pricing is usage-based and could increase significantly if document volume grows. The
 vendor provides APIs, but rate limits are not clearly documented. They have only been
 operating for 18 months and have 12 enterprise customers.
The business team wants to use this vendor for processing supplier invoices and purchase contracts.
"""

PROMPT_CASE1_1 = f"""
You are a senior enterprise risk analyst. Identify specific risks before onboarding.
Analyze across FIVE dimensions:PRIVACY & DATA GOVERNANCE, COMPLIANCE & CERTIFICATION, OPERATIONAL & TECHNICAL RISK, PRICING & COMMERCIAL RISK, VENDOR MATURITY & STABILITY

RISK LEVELS:
- LOW: Minor gaps
- MEDIUM: Notable gaps needing controls
- HIGH: Significant risk
- CRITICAL: Regulatory/continuity risk
CONFIDENCE SCORE: 0.0–1.0 based on info completeness.
RULES:
- Identify implicit risks too.
- missing_information must list specific questions that could change rating.

Vendor Note:
{VENDOR_NOTE_CASE1_1}
Respond ONLY with JSON:
{{"risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": ["<risk 1>", "<risk 2>", "..."],
  "missing_information": ["<missing detail 1>", "..."],
  "business_recommendation": "<recommendation>",
  "confidence_score": 0.0}}
"""

SITUATION = """The company currently handles customer support through a team of 120 human agents. Ticket volume
has grown by 45% in the last 8 months. Average response time has increased from 3 hours to 11 hours.
The AI team proposes deploying a GenAI chatbot for first-level support. It can answer FAQs, summarize customer issues, and create draft responses for agents. The compliance team is concerned because customer support tickets may contain personal information.
The support team is worried about job losses. The company has not yet implemented AI governance policies.
"""

PROMPT_CASE1_2 = """
You are an executive advisor preparing a decision memo for the COO.
Your task is to make a business decision, not summarize the situation.
Evaluate financial impact, operational readiness, governance, compliance, and people risks before deciding.

SITUATION:
{situation}

Instructions:
1. Calculate estimated ROI using:
   - $30,000/month recurring cost
   - $250,000 implementation cost
   - CTO estimate: 35% ticket reduction 

2. Assess:
   - Financial viability and 12-month payback potential
   - Operational risks and readiness
   - Compliance and data privacy risks
   - Governance gaps
   - Change-management impact on support teams

3. Do NOT assume the chatbot alone will solve response-time issues.

4. AI governance is mandatory before go-live. Minimum controls include:
   - AI usage policy
   - Data retention rules
   - Human review/override process
   - Escalation workflow
   - Output monitoring

Decision Rules:
- APPROVE → only if risks are controlled and ROI is clear
- APPROVE_WITH_CONDITIONS → if viable but conditions must be completed first
- REJECT → if risks or financials are unacceptable

Return ONLY valid JSON in this schema:

{{"decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "rationale": "",
  "financial_considerations": [],
  "operational_considerations": [],
  "people_impact": [],
  "compliance_risks": [],
  "conditions_for_approval": [],
  "final_recommendation": ""
}}""".format(situation=SITUATION)

TEST_TICKETS = [
    "I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.",
    "The export button stopped working after your latest update. Our reporting team is blocked.",
    "Can you add approval workflows before invoices are submitted?",
    "We need confirmation that our customer data is not being used to train your AI models.",
    "My admin account is locked and the password reset email never arrives.",
]

PROMPT_CASE2_1 = """
You are a customer support triage assistant. Classify each ticket into ONE category and assign ONE priority level.

CATEGORIES:
- BILLING_ISSUE → charges, invoices, refunds, payments
- TECHNICAL_BUG → broken features, crashes, software errors
- ACCOUNT_ACCESS → login, password reset, permission/access issues
- FEATURE_REQUEST → requests for new functionality
- COMPLIANCE_CONCERN → privacy, GDPR, data usage, AI governance, security concerns
- ESCALATION_RISK → explicit legal threats, chargebacks, social media, executive escalation

PRIORITY:
- LOW → minor issue, little urgency
- MEDIUM → moderate impact or frustration
- HIGH → serious business impact or urgency
- URGENT → immediate operational, legal, financial, or reputational risk

RULES:
- Angry tone increases priority.
- Explicit legal/social/media escalation = ESCALATION_RISK.
- Privacy or data-sharing concerns = COMPLIANCE_CONCERN even if caused by a bug.
- Requests for new functionality = FEATURE_REQUEST.
- Login or password-reset problems = ACCOUNT_ACCESS.

Return ONLY a valid JSON array.
Tickets:
{tickets}
Output format:
[ {{ "ticket": "<original ticket>",
    "category": "<category>",
    "priority": "<LOW | MEDIUM | HIGH | URGENT>",
    "justification": "<short reason>"
  }}]""".format(tickets=json.dumps(TEST_TICKETS, indent=2))

TEST_MESSAGES = [
    "I want to take leave from 12th June to 15th June because I am travelling.",
    "How many casual leaves do I have left?",
    "Cancel my leave request for next Friday.",
    "What is the policy for maternity leave?",
    "I may take off sometime next week, not sure yet.",
]

PROMPT_CASE2_2 = """You are an API translator for a leave management assistant. Convert each user message into ONE structured API contract.

SUPPORTED ACTIONS:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

RULES:
- Never guess dates or leave types.
- Relative dates like "next Friday" require clarification.
- Only set requires_clarification=false when all required fields are present.

Required fields:
- APPLY_LEAVE → start_date, end_date, leave_type, reason
- CANCEL_LEAVE → exact date or request ID
- CHECK_BALANCE → leave_type
- GET_POLICY → leave_type

Date format:
- YYYY-MM-DD

Confidence:0.0 - 1.0
Return ONLY a valid JSON array.
User messages:
{messages}

Output format:
[  {{ "action": "<APPLY_LEAVE | CHECK_BALANCE | CANCEL_LEAVE | GET_POLICY>",
    "parameters": {{}},
    "requires_clarification": true,
    "clarification_question": "<question or empty string>",
    "confidence": 0.0
  }}]""".format(messages=json.dumps(TEST_MESSAGES, indent=2))

PROMPT_CASE3_1 = """
You are a financial analyst evaluating an AI recommendation engine project. Calculate the financial impact and make a decision based on payback period.

PROJECT DETAILS:
- Monthly revenue: $2,000,000
- Revenue uplift: 4% to 7%
- One-time implementation cost: $180,000
- Monthly infrastructure cost: $22,000
- Monthly maintenance cost: $8,000
- Gross margin: 40%
- Implementation time: 3 months
- Required payback: within 12 months after go-live

CALCULATIONS:
1. Calculate incremental monthly revenue range.
2. Convert revenue uplift into gross profit using 40% margin.
3. Total monthly operating cost = $30,000.
4. Monthly net benefit = gross profit - operating cost.
5. Payback period = $180,000 ÷ monthly net benefit.

DECISION RULES:
- APPROVE → both low and high case payback ≤ 12 months
- APPROVE_WITH_CONDITIONS → only high case ≤ 12 months
- REJECT → even high case > 12 months

Do calculations internally and return ONLY valid JSON:
{{"incremental_revenue_range": "",
  "incremental_gross_profit_range": "",
  "monthly_net_benefit_range": "",
  "payback_period_range_months": "",
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "reasoning_summary": "",
  "key_assumptions": [  "",    ""  ]}}
"""

PROMPT_CASE3_2 = """
You are a senior ML engineer analyzing why a fraud detection model degraded in production.
MODEL PERFORMANCE:
Before deployment:
- Precision: 0.82
- Recall: 0.76
- F1: 0.79
After 3 months:
- Precision: 0.61
- Recall: 0.72
- F1: 0.66

OBSERVATIONS:
1. Transaction volume increased by 30%
2. New payment channel introduced
3. Fraud behavior changed after a promotional campaign
4. No failed pipeline jobs
5. transaction_amount feature distribution shifted significantly
6. Model has not been retrained

ANALYZE:
- Data drift
- Concept drift
- Pipeline/data quality issues
- Threshold miscalibration

IMPORTANT:
- Do not claim pipeline failure without evidence.
- Precision dropped much more than recall, suggesting increased false positives.
- Consider how feature distribution shifts may affect model calibration.

Return ONLY valid JSON:
{{"most_likely_causes": ["", ""  ],
  "evidence": [  ""  ],
  "less_likely_causes": [  ""  ],
  "recommended_diagnostics": [  "",   ""  ],
  "short_term_actions": [    ""  ],
  "long_term_actions": [    ""  ],
  "reasoning_summary": ""}}"""

CUSTOMER_QUESTION = """I was charged for a premium plan even though I cancelled last month.
I already contacted support twice and no one responded. I want a refund immediately."""

RESPONSE_A = """We are sorry for the inconvenience. Please check your billing settings and
make sure your cancellation was completed. Refunds are subject to our policy. Thank you."""

RESPONSE_B = """I'm sorry this has been frustrating, especially after you contacted support
twice. I can help escalate this as a billing issue. Please share your invoice ID or account
email so the team can verify the cancellation date and refund eligibility. If the duplicate
charge is confirmed, we will process the refund according to the billing policy."""

DEVELOPER_QUESTION = "What is the difference between shallow copy and deep copy in Python?"

EXPLANATION_A = """A shallow copy copies the object but keeps references to nested objects.
A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and
copy.deepcopy for deep copy."""

EXPLANATION_B = """A shallow copy means the copied variable points to the same memory.
A deep copy means everything is copied into new memory. So shallow copy is always bad
and deep copy is always better."""

PROMPT_CASE4_2 = """You are a senior software engineer evaluating two explanations for a junior developer.

QUESTION:
"{question}"
EXPLANATION A:
"{exp_a}"
EXPLANATION B:
"{exp_b}"

Score each explanation (1–5) on:Technical Accuracy, Beginner Accessibility, Completeness,Avoidance of Misleading Claims, Practical Usefulness

Return ONLY valid JSON:
{{"explanation_a": {{
    "scores": {{
      "technical_accuracy": 0,
      "beginner_accessibility": 0,
      "completeness": 0,
      "avoidance_of_misleading_claims": 0,
      "practical_usefulness": 0 }},
    "issues": [],
    "overall_score": 0
  }}, "explanation_b": {{
    "scores": {{
      "technical_accuracy": 0,
      "beginner_accessibility": 0,
      "completeness": 0,
      "avoidance_of_misleading_claims": 0,
      "practical_usefulness": 0
    }}, "issues": [],
    "overall_score": 0
  }}, "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}}""".format(question=DEVELOPER_QUESTION, exp_a=EXPLANATION_A, exp_b=EXPLANATION_B)

PROMPT_CASE4_1 = """You are a customer support quality evaluator comparing two responses.

CUSTOMER QUESTION:
"{question}"
RESPONSE A:
"{response_a}"
RESPONSE B:
"{response_b}"

Score each response (1–5) on: Empathy, Issue Ownership, Next Steps Clarity, Refund Handling, Professionalism

Key rule:
Do NOT reward vague or generic apologies.
Do NOT reward responses that deflect responsibility.

Return ONLY valid JSON:
{{  "response_a": {{
    "scores": {{
      "empathy": 0,
      "issue_ownership": 0,
      "next_steps_clarity": 0,
      "refund_handling": 0,
      "professionalism": 0
    }}, "strengths": [],
    "weaknesses": []
  }}, "response_b": {{
    "scores": {{
      "empathy": 0,
      "issue_ownership": 0,
      "next_steps_clarity": 0,
      "refund_handling": 0,
      "professionalism": 0
    }},  "strengths": [],
    "weaknesses": []
  }}, "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}}""".format(question=CUSTOMER_QUESTION, response_a=RESPONSE_A, response_b=RESPONSE_B)  

POLICY_TEXT = """Reimbursement Policy:
- Business travel meals: up to $60 per day
- Alcohol: NOT reimbursable
- Travel >8 hours but no overnight stay: claim up to 50% of daily meal limit
- International travel: daily meal limit increases by 25%
- Receipts mandatory for claims above $25"""

CLAIM = """Employee claim:
- Travel: India to Singapore, same-day (no overnight stay)
- Total travel duration: 14 hours
- Meal expenses submitted: $70 (including $12 alcohol)
- Receipts: provided"""

PROMPT_CASE5_1 = """You are a payroll analyst applying a reimbursement policy to an employee claim.
Use the policy and claim below:
{policy}
{claim}

Follow the calculation rules in order:
1. Remove ineligible items (e.g., alcohol).
2. Compute base daily limit and apply any travel multipliers.
3. Apply time-based rule (e.g., same-day travel reduction).
4. Compare eligible expenses against final limit and cap reimbursement.
5. Apply receipt-based adjustments if required.

Important: Always apply multiplier rules BEFORE time-based reductions.
Return ONLY valid JSON in this format:
{{ "reimbursable_amount": <number>,
  "calculation_steps": [
    "<step 1>", "<step 2>","<step 3>"
  ], "reasoning": "<brief explanation>"
}}""".format(policy=POLICY_TEXT, claim=CLAIM)

SECURITY_CONTEXT = """Security Rules:
1. New country login + downloads >5 files → HIGH risk
2. Login outside business hours (9AM-6PM local) + MFA failure once → MEDIUM risk
3. HIGH + MEDIUM both true → CRITICAL
4. Known VPN country does NOT count as new country

User Activity for Asha:
- Login time: 8:15 PM local time (outside business hours)
- Login country: Germany
- Known countries: India, Germany
- Known VPN countries: Germany, Netherlands
- Files downloaded: 8
- MFA failures: 1"""

PROMPT_CASE5_2 = """You are a security analyst applying access control rules to determine risk level.
{context}
ANALYSIS — evaluate rules:
RULE 1 (HIGH risk):
- Condition: new country AND downloads > 5
- Germany is a known country and also a known VPN country
- Known VPN countries are NOT treated as "new country"
- Therefore: new country = FALSE
- Rule 1 does NOT trigger (even though downloads = 8)

RULE 2 (MEDIUM risk):
- Condition: login outside business hours AND 1 MFA failure
- Login time: 8:15 PM (business hours: 9 AM–6 PM) → OUTSIDE hours ✓
- MFA failures: 1 ✓
- Rule 2 triggers

RULE 3 (CRITICAL):
- Requires BOTH Rule 1 and Rule 2
- Rule 1 is false → Rule 3 does not trigger

FINAL RISK LEVEL: MEDIUM
Return ONLY valid JSON:
{{  "rule_1_triggered": false,
  "rule_2_triggered": true,
  "rule_3_triggered": false,
  "risk_level": "MEDIUM",
  "reasoning": "<brief explanation why Rule 1 does not trigger despite 8 downloads>"
}}
"""

OPTIONS_6_1 = {
    "Option 1: AI Customer Support Assistant": {
        "ticket_volume": "high",
        "implementation_complexity": "moderate",
        "data_sensitivity": "personal customer data",
        "cost_saving_potential": "high",
        "user_adoption_risk": "medium",
    },
    "Option 2: AI Sales Proposal Generator": {
        "usage_frequency": "medium",
        "data_sensitivity": "low",
        "revenue_impact": "medium to high",
        "requires": "brand and legal review",
        "user_adoption_risk": "low",
    },
    "Option 3: AI Contract Risk Analyzer": {
        "business_value": "high",
        "legal_sensitivity": "high",
        "implementation_complexity": "high",
        "requires": "strong accuracy and auditability",
        "user_adoption_risk": "medium",
    },
    "Option 4: AI Internal HR Policy Assistant": {
        "employee_usage": "high",
        "data_sensitivity": "medium",
        "implementation_complexity": "low",
        "cost_saving_potential": "medium",
        "user_adoption_risk": "low",
    },
}

PROMPT_CASE6_1 = """You are an AI strategy advisor helping select ONE use case for a 90-day pilot.

Evaluate each option independently, then choose the best one.
SCORING (1–5 scale):
- business_value: impact to business (5 = highest)
- feasibility: can it be built in 90 days (5 = easiest)
- risk: safety/compliance risk (5 = low risk, 1 = high risk)
- pilot_suitability: suitability for a 90-day test
- adoption: expected user adoption (5 = high adoption)
- overall_score = weighted average:
  (business_value * 0.25 +
   feasibility * 0.25 +
   risk * 0.2 +
   pilot_suitability * 0.2 +
   adoption * 0.1)

OPTIONS:
{options}
CONTEXT FOR OPTIONS:

1) Customer Support Assistant
- High ROI potential due to ticket volume
- Clear 90-day measurable impact
- Privacy risk (customer data)
- Harder implementation + reputational risk
Risk: medium

2) Sales Proposal Generator
- Low compliance risk
- High adoption in sales teams
- Medium ROI visibility in 90 days
- Needs legal/brand review before use
Risk: relatively low

3) Contract Risk Analyzer
- Very high business value long term
- Very high legal/compliance risk
- Hard to validate in 90 days
- Requires legal-grade accuracy
Risk: high (not suitable for pilot)

4) HR Policy Assistant
- Easy to build and deploy
- High internal adoption
- Low-medium business impact
- Clear success metrics
Risk: low

RULE:
Pick the option that best balances measurable 90-day value + low risk, not just highest value.

RETURN ONLY JSON:
{{  "options_evaluated": [
    {{"option": "<name>",
      "business_value": 0,
      "feasibility": 0,
      "risk": 0,
      "pilot_suitability": 0,
      "adoption": 0,
      "overall_score": 0,
      "trade_offs": ["...", "..."]
    }}  ],
  "recommended_option": "<name>",
  "why_not_others": {{
    "Option 1": "...",
    "Option 2": "...",
    "Option 3": "..."
  }},  "final_recommendation": "<2–3 sentence summary>"
}}""".format(options=json.dumps(OPTIONS_6_1, indent=2))

PROMPT_CASE6_2 = """You are a solutions architect designing a PDF question-answering system.
Users upload PDFs and ask questions with source citations.
Constraints:
- 500 initial users → 20K in 12 months
- MVP in 6 weeks
- Limited budget
- Confidential documents → privacy matters
- Accuracy is more important than speed

ARCHITECTURE OPTIONS:
A. RAG (vector DB + hosted LLM API)
B. Fine-tune LLM on documents
C. Keyword search only
D. Complex agentic system (query rewriting + reranking + citation validation)

SCORING (1–5, higher is better):
- accuracy
- cost_efficiency (5 = cheap)
- privacy (5 = fully controlled/on-prem)
- timeline_fit (5 = doable in 6 weeks)
- scalability (to 20K users)
- citation_quality

KEY GUIDANCE:
- Prioritize MVP feasibility + accuracy + citations
- Avoid over-engineering

OPTION NOTES:
A. Simple RAG
- Fast to build (2–3 weeks)
- Good citation support via retrieved chunks
- Scales well with hosted infra
- Privacy concern: data sent to LLM API
→ Recommended: YES (best MVP choice)

B. Fine-tuning
- Not suitable: new uploads require retraining
- Too slow and expensive for MVP
→ Recommended: NO

C. Keyword search
- Fast and private
- Fails semantic understanding and QA quality
- No real answer synthesis
→ Recommended: NO (only as helper tool)

D. Agentic system
- Best theoretical accuracy
- Too complex for 6-week MVP
- High engineering risk
→ Recommended: NO for MVP (future upgrade)

OUTPUT (JSON ONLY):
{{  "architecture_scores": [
    {{ "option": "A | B | C | D",
      "accuracy": 0,
      "cost_efficiency": 0,
      "privacy": 0,
      "timeline_fit": 0,
      "scalability": 0,
      "citation_quality": 0,
      "overall_score": 0,
      "notes": "<key trade-off>"
    }}
  ], "recommended_architecture": "A | B | C | D",
  "reasoning": "<why this option is best>",
  "risks": ["...", "..."],
  "mitigations": ["...", "..."],
  "mvp_plan": ["step 1", "step 2", "step 3"]
}}
"""

VAGUE_REQUEST_7_1 = """We need AI to improve operations and reduce manual work. Build something that
helps teams become more productive and gives leadership better visibility."""

PROMPT_CASE7_1= """You are an AI product consultant using a Rephrase-and-Solve approach.

TASK FLOW:
1) REPHRASE THE PROBLEM
Convert the vague request into a precise, measurable problem statement.
Make it specific enough that an engineering team could build from it.

Turn vague terms into measurable definitions:
- "improve operations" → specify process + metric
- "reduce manual work" → specify tasks + time saved
- "more productive" → define output, speed, or error rate
- "better visibility" → define data, audience, frequency, format
The result must include measurable outcomes (numbers, time, or KPIs).

2) ASSUMPTIONS
List key assumptions required due to missing information
(e.g., industry, team size, workflows, tools used).

3) SOLUTION
Propose ONE concrete AI-powered product feature.
No generic strategy—must be buildable.
Original request:
"{request}"

REQUIREMENTS:
- Rephrased problem must be specific + measurable
- Solution must name a real AI technique (e.g., RAG, classification, forecasting, anomaly detection)
- Metrics must be numeric and testable
- Risks must be specific to the solution

OUTPUT (JSON ONLY):
{{ "rephrased_problem": "<clear measurable problem>",
  "assumptions": [
    "<assumption 1>",
    "<assumption 2>"
  ],
  "solution": "<single AI feature>",
  "target_users": ["<role>", "<role>"],
  "key_features": ["<feature>", "<feature>"],
  "data_needed": ["<data source>", "<data source>"],
  "success_metrics": ["<measurable KPI>", "<measurable KPI>"],
  "implementation_steps": ["<step 1>", "<step 2>", "<step 3>"],
  "risks": ["<specific risk>", "<specific risk>"]
}}
"""

VAGUE_REQUIREMENT_7_2 = """Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers."""
PROMPT_CASE7_2 = """You are a senior product engineer translating vague requirements into a clear engineering specification.

TASK FLOW:
1) REPHRASE REQUIREMENT
Convert vague statements into precise, testable engineering requirements.
Make everything measurable and implementation-ready.

Clarify:
- file upload → file types, size limits, post-upload behavior
- questions → natural language vs structured input
- “good answers” → accuracy target, citations, confidence scoring
- “secure” → auth, encryption, access control, audit logging
- “fast” → latency (e.g., p95 response time)
- “no wrong answers” → replace with realistic accuracy + hallucination mitigation

2) MISSING INFORMATION
List critical unanswered questions that would change system design decisions.

3) SOLUTION APPROACH
Recommend ONE concrete architecture (named system design), with justification.

Original requirement:
"{requirement}"

RULES:
- All non-functional requirements must include measurable thresholds (e.g., <2s latency, 99.9% uptime)
- Security must specify actual controls (not generic statements)
- Acceptance criteria must be testable (pass/fail)
- Open questions must affect architecture decisions

OUTPUT (JSON ONLY):
{{
  "rephrased_requirement": "<engineer-ready requirement>",
  "functional_requirements": [
    "<requirement 1>",
    "<requirement 2>"
  ],
  "non_functional_requirements": [
    "<measurable requirement>"
  ],
  "security_requirements": [
    "<specific control>",
    "<specific control>"
  ],
  "acceptance_criteria": [
    "<testable criterion>",
    "<testable criterion>"
  ],
  "recommended_architecture": "<named system design>",
  "open_questions": [
    "<key design question>",
    "<key design question>"
  ]}}"""