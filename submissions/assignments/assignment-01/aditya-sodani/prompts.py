ZERO_SHOT_VENDOR_RISK_PROMPT = """
You are a senior third-party risk analyst specializing in AI vendor assessments.

Your task is to evaluate the following vendor onboarding note and classify the vendor risk level.

You must analyze:
- Privacy risks
- Compliance risks
- Operational risks
- Pricing and scalability risks
- Vendor maturity risks

Risk Levels:
- LOW
- MEDIUM
- HIGH
- CRITICAL

Decision Guidance:
- CRITICAL: Severe compliance, privacy, or operational concerns with high business exposure
- HIGH: Significant unresolved risks that require mitigation before onboarding
- MEDIUM: Moderate risks with manageable controls
- LOW: Minimal concerns and mature operational posture

Important Rules:
- Do not use generic procurement language
- Identify implicit risks, not just explicitly stated ones
- Focus on realistic enterprise risk analysis
- Return ONLY valid JSON
- Confidence score must be between 0 and 1

Required JSON Schema:
{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": [],
  "missing_information": [],
  "business_recommendation": "",
  "confidence_score": 0.0
}

Vendor Note:
Vendor: DocuMind AI

The vendor claims their solution can process invoices, contracts, and identity documents using OCR and LLM-based extraction.

They say the model is hosted in a multi-tenant cloud environment. They do not currently provide region-specific data residency, but they are planning to add it next year.

They support encryption at rest and in transit. However, customer data may be used for product improvement unless customers opt out through a manual request.

They have SOC 2 Type I certification but not Type II. Their uptime SLA is 99.5%.

The pricing is usage-based and could increase significantly if document volume grows.

The vendor provides APIs, but rate limits are not clearly documented.

They have only been operating for 18 months and have 12 enterprise customers.

The business team wants to use this vendor for processing supplier invoices and purchase contracts.
"""


ZERO_SHOT_EXECUTIVE_DECISION_PROMPT = """
You are an executive decision-making advisor supporting a Chief Operating Officer. Your task is to evaluate a business proposal and produce a formal executive decision memo.

The proposal must be assessed strictly from a strategic, financial, operational, compliance, and people-impact perspective. You must behave like a senior leadership advisor, not a summarizer.

### Decision Context:
A company with 120 customer support agents is experiencing a 45% increase in ticket volume over the last 8 months. Average response time has degraded from 3 hours to 11 hours.

A proposal has been made to deploy a GenAI chatbot for first-level customer support. The chatbot will:
- Answer frequently asked questions
- Summarize customer issues
- Draft response suggestions for human agents

Financial details:
- Implementation cost: $250,000
- Ongoing monthly cost: $30,000

Additional context:
- CTO estimates 35% reduction in ticket load
- CFO requires payback within 12 months
- Compliance team raises concerns about handling personal information in customer tickets
- Support team is concerned about job displacement
- No AI governance framework currently exists in the organization

### Your Task:
Produce a structured executive decision memo.

You must:
- Make a clear final decision
- Provide a business justification grounded in ROI, risk, and operational feasibility
- Evaluate compliance and data privacy risks seriously
- Consider workforce and organizational impact
- Avoid overclaiming automation benefits
- Account for the absence of AI governance
- Be explicit about tradeoffs and constraints

### Output Requirements:
Return ONLY valid JSON in the following schema:

{
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "rationale": "",
  "financial_considerations": [],
  "operational_considerations": [],
  "people_impact": [],
  "compliance_risks": [],
  "conditions_for_approval": [],
  "final_recommendation": ""
}

### Output Rules:
- Do not include any extra text outside JSON.
- Do not summarize the scenario.
- Do not be descriptive or generic.
- All fields must be substantively filled.
- Conditions must be specific and enforceable if approval is recommended.
"""



Few_Shot_Customer_Ticket_Intent_Classification_prompt = """
You are an AI system that classifies customer support tickets.

You must classify each ticket into exactly one category:

- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- COMPLIANCE_CONCERN
- ESCALATION_RISK

Important classification rules:
1. Angry or threatening language can increase PRIORITY, but does NOT automatically determine CATEGORY.
2. If the issue is primarily about payment, refunds, invoices, or charges → BILLING_ISSUE.
3. If the issue is about broken functionality, crashes, bugs, or system malfunction → TECHNICAL_BUG.
4. If the issue is about login problems, MFA, locked accounts, password reset issues → ACCOUNT_ACCESS.
5. Requests for new capabilities or enhancements → FEATURE_REQUEST.
6. Questions about legal, privacy, security policy, AI training usage, regulations, audits, or data governance → COMPLIANCE_CONCERN.
7. Use ESCALATION_RISK only when the core issue is threat escalation, legal escalation, executive escalation, or reputational damage rather than the operational issue itself.
8. Priority levels:
   - LOW: minor inconvenience or suggestion
   - MEDIUM: normal operational issue
   - HIGH: business impact, blocked workflow, repeated failures
   - URGENT: severe business risk, public escalation, legal threat, or complete operational blockage

Return output ONLY in this JSON schema:

[
  {
    "ticket": "",
    "category": "",
    "priority": "LOW | MEDIUM | HIGH | URGENT",
    "justification": ""
  }
]

-------------------------
FEW-SHOT EXAMPLES
-------------------------

Example 1
Ticket:
"I was billed for three seats after downgrading our plan last month."

Output:
[
  {
    "ticket": "I was billed for three seats after downgrading our plan last month.",
    "category": "BILLING_ISSUE",
    "priority": "HIGH",
    "justification": "The issue concerns incorrect subscription charges after a downgrade."
  }
]

Example 2
Ticket:
"The mobile app crashes every time we try to upload a PDF invoice."

Output:
[
  {
    "ticket": "The mobile app crashes every time we try to upload a PDF invoice.",
    "category": "TECHNICAL_BUG",
    "priority": "HIGH",
    "justification": "The ticket describes broken application functionality preventing uploads."
  }
]

Example 3
Ticket:
"I cannot log in to the admin portal and password reset emails never arrive."

Output:
[
  {
    "ticket": "I cannot log in to the admin portal and password reset emails never arrive.",
    "category": "ACCOUNT_ACCESS",
    "priority": "HIGH",
    "justification": "The customer is unable to access their account due to authentication and reset issues."
  }
]

Example 4
Ticket:
"Please add multi-stage approval workflows before purchase orders are finalized."

Output:
[
  {
    "ticket": "Please add multi-stage approval workflows before purchase orders are finalized.",
    "category": "FEATURE_REQUEST",
    "priority": "LOW",
    "justification": "The customer is requesting a new product capability rather than reporting a defect."
  }
]

Example 5
Ticket:
"We need written confirmation that our uploaded documents are not used to train AI models."

Output:
[
  {
    "ticket": "We need written confirmation that our uploaded documents are not used to train AI models.",
    "category": "COMPLIANCE_CONCERN",
    "priority": "HIGH",
    "justification": "The issue relates to data governance, privacy, and AI usage policies."
  }
]

Example 6 (Ambiguous Boundary Case)
Ticket:
"The invoice export feature stopped working after yesterday's release."

Output:
[
  {
    "ticket": "The invoice export feature stopped working after yesterday's release.",
    "category": "TECHNICAL_BUG",
    "priority": "HIGH",
    "justification": "Although invoices are mentioned, the primary issue is broken functionality after an update."
  }
]

Example 7 (Angry Tone But Same Category)
Ticket:
"Your billing system is a disaster. If this duplicate charge is not reversed today, I'm escalating this publicly."

Output:
[
  {
    "ticket": "Your billing system is a disaster. If this duplicate charge is not reversed today, I'm escalating this publicly.",
    "category": "BILLING_ISSUE",
    "priority": "URGENT",
    "justification": "The core issue is duplicate billing, while the threatening tone increases urgency."
  }
]

-------------------------
CLASSIFY THESE TICKETS
-------------------------

1. "I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today."

2. "The export button stopped working after your latest update. Our reporting team is blocked."

3. "Can you add approval workflows before invoices are submitted?"

4. "We need confirmation that our customer data is not being used to train your AI models."

5. "My admin account is locked and the password reset email never arrives."

Return only valid JSON.
"""


Few_Shot_Transformation_from_Requirement_to_API_Contract_prompt = """
You are an AI system that converts employee leave-related natural language requests
into structured API contracts.

You must strictly follow the output JSON schema.

-----------------------------------
SUPPORTED ACTIONS
-----------------------------------

1. APPLY_LEAVE
2. CHECK_BALANCE
3. CANCEL_LEAVE
4. GET_POLICY

-----------------------------------
OUTPUT SCHEMA
-----------------------------------

{
  "action": "",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "",
  "confidence": 0.0
}

-----------------------------------
IMPORTANT RULES
-----------------------------------

1. Never invent:
   - dates
   - leave types
   - reasons

2. If required information is missing:
   - set requires_clarification = true

3. If dates are ambiguous:
   - do NOT guess
   - ask clarification

4. Confidence must be between:
   - 0.0 and 1.0

5. Output ONLY valid JSON.

-----------------------------------
FEW-SHOT EXAMPLES
-----------------------------------

Example 1

User:
I want to take leave from 12th June to 15th June because I am travelling.

Output:
{
  "action": "APPLY_LEAVE",
  "parameters": {
    "start_date": "12th June",
    "end_date": "15th June",
    "reason": "travelling"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.96
}

-----------------------------------

Example 2

User:
How many casual leaves do I have left?

Output:
{
  "action": "CHECK_BALANCE",
  "parameters": {
    "leave_type": "casual"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.98
}

-----------------------------------

Example 3

User:
Cancel my leave request for next Friday.

Output:
{
  "action": "CANCEL_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please specify the exact date for next Friday.",
  "confidence": 0.72
}

-----------------------------------

Example 4

User:
What is the policy for maternity leave?

Output:
{
  "action": "GET_POLICY",
  "parameters": {
    "leave_type": "maternity"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.99
}

-----------------------------------

Example 5

User:
I may take off sometime next week, not sure yet.

Output:
{
  "action": "APPLY_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please provide the exact leave dates.",
  "confidence": 0.61
}

-----------------------------------

Example 6

User:
I want leave tomorrow.

Output:
{
  "action": "APPLY_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please provide the leave end date and reason.",
  "confidence": 0.68
}

-----------------------------------


Now convert the following user request into the required JSON format.

User:
{user_input}

Output:
"""


BUSINESS_ROI_DECISION_WITH_HIDDEN_TRADE_OFFS_PROMPT = """
You are a senior financial strategy analyst evaluating AI investment proposals for executive leadership.

Your task is to perform careful business ROI reasoning for an AI recommendation engine deployment proposal.

You must reason step-by-step internally, but return only:
- concise reasoning summaries
- final calculations
- final decision output

Do NOT expose detailed chain-of-thought calculations.

--------------------------------------------------
BUSINESS SCENARIO
--------------------------------------------------

A retail company wants to deploy an AI recommendation engine.

Current monthly revenue: $2,000,000

Expected revenue uplift from recommendations:
- Minimum uplift: 4%
- Maximum uplift: 7%

Implementation cost:
- $180,000 one-time

Monthly AI operating costs:
- Infrastructure cost: $22,000/month
- Maintenance cost: $8,000/month

Gross margin:
- 40%

Implementation timeline:
- 3 months before go-live

Leadership requirement:
- Payback must occur within 12 months AFTER go-live

--------------------------------------------------
CRITICAL REASONING RULES
--------------------------------------------------

You MUST:

1. Calculate incremental revenue range correctly.

2. Convert revenue uplift into incremental gross profit using the 40% gross margin.

3. Subtract ALL monthly AI operating costs:
   - infrastructure
   - maintenance

4. Use NET monthly business benefit for payback calculations.

5. Treat implementation time separately:
   - 3-month implementation period occurs BEFORE go-live
   - payback window starts AFTER go-live

6. Do NOT calculate payback using gross revenue.

7. Do NOT ignore operating expenses.

8. Be financially precise and realistic.

9. If assumptions are required, state them explicitly.

10. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "incremental_revenue_range": "",
  "incremental_gross_profit_range": "",
  "monthly_net_benefit_range": "",
  "payback_period_range_months": "",
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "reasoning_summary": "",
  "key_assumptions": []
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- All calculations must be financially consistent.
- Reasoning summary must be concise.
- Do not reveal hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.
- Confidence language should reflect uncertainty ranges appropriately.

"""

ROOT_CAUSE_ANALYSIS_FOR_ML_MODEL_PERFORMANCE_DROP_PROMPT = """
You are a senior machine learning reliability engineer specializing in fraud detection systems, ML monitoring, model drift analysis, and production AI diagnostics.

Your task is to perform a structured root cause analysis for a deployed fraud detection model whose performance degraded after deployment.

You must reason carefully and analytically before producing the final answer.

You should internally reason step-by-step, but ONLY return:
- concise reasoning summaries
- structured findings
- actionable diagnostics
- operational recommendations

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
MODEL PERFORMANCE DATA
--------------------------------------------------

Before deployment:
- Precision: 0.82
- Recall: 0.76
- F1-score: 0.79

After 3 months:
- Precision: 0.61
- Recall: 0.72
- F1-score: 0.66

--------------------------------------------------
ADDITIONAL OBSERVATIONS
--------------------------------------------------

- Transaction volume increased by 30%
- A new payment channel was introduced
- Fraud patterns changed after a promotional campaign
- Data pipeline logs show no failed jobs
- Feature distribution for transaction_amount shifted significantly
- Model was not retrained after deployment

--------------------------------------------------
CRITICAL REASONING REQUIREMENTS
--------------------------------------------------

You MUST carefully distinguish between:

1. Data Drift
   - Statistical feature distribution changes
   - Input pattern shifts

2. Concept Drift
   - Fraud behavior changes
   - Label/outcome relationship changes

3. Pipeline Failure
   - Data corruption
   - Missing transformations
   - Processing failures

4. Threshold Miscalibration
   - Classification threshold no longer optimal
   - Precision/recall balance changes

--------------------------------------------------
IMPORTANT ANALYTICAL RULES
--------------------------------------------------

1. Do NOT claim pipeline failure solely because performance degraded.

2. Use the evidence provided carefully.

3. Treat feature distribution shift as meaningful evidence.

4. Analyze why precision dropped more significantly than recall.

5. Consider operational changes:
   - new payment channel
   - traffic increase
   - promotional campaign

6. Avoid simplistic "just retrain the model" recommendations.

7. Recommend concrete diagnostics and validation procedures.

8. Separate:
   - likely causes
   - less likely causes
   - evidence
   - remediation actions

9. Focus on realistic ML production reasoning.

10. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "most_likely_causes": [],
  "evidence": [],
  "less_likely_causes": [],
  "recommended_diagnostics": [],
  "short_term_actions": [],
  "long_term_actions": [],
  "reasoning_summary": ""
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- Recommendations must be technically actionable.
- Diagnostics must be specific and measurable.
- Reasoning summary must be concise.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.
- Do not hallucinate unavailable evidence.

"""

LLM_AS_JUDGE_CUSTOMER_SUPPORT_RESPONSE_EVALUATION_PROMPT = """
You are an expert AI quality evaluator specializing in customer support communication assessment.

Your task is to evaluate two AI-generated customer support responses using a precise scoring rubric.

You must behave like a professional evaluation judge, not like a chatbot.

You should internally reason carefully before scoring, but ONLY return:
- structured scores
- strengths
- weaknesses
- concise evaluation summaries

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
CUSTOMER QUESTION
--------------------------------------------------

"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

--------------------------------------------------
RESPONSE A
--------------------------------------------------

"We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you."

--------------------------------------------------
RESPONSE B
--------------------------------------------------

"I’m sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy."

--------------------------------------------------
EVALUATION RUBRIC
--------------------------------------------------

Evaluate each response on a scale from 1 to 5 for the following categories:

1. Empathy
- Does the response acknowledge frustration appropriately?
- Does it recognize the repeated support issue?

2. Helpfulness
- Does the response guide the customer toward resolution?
- Are next steps actionable and useful?

3. Professionalism
- Is the tone respectful, calm, and customer-safe?

4. Policy Compliance
- Does the response avoid guaranteeing refunds without verification?
- Does it follow reasonable support process behavior?

5. Specificity
- Does the response provide concrete actions instead of vague statements?

--------------------------------------------------
SCORING RULES
--------------------------------------------------

1 = Very Poor
2 = Poor
3 = Acceptable
4 = Good
5 = Excellent

--------------------------------------------------
IMPORTANT EVALUATION RULES
--------------------------------------------------

1. Do NOT prefer a response simply because it is longer.

2. Penalize:
- vague responses
- dismissive language
- blame-shifting to the customer
- lack of actionable guidance

3. Penalize responses that:
- promise refunds without verification
- bypass verification procedures

4. Reward responses that:
- acknowledge customer frustration appropriately
- provide clear escalation or verification steps
- maintain professionalism under tension

5. Be strict and consistent in scoring.

6. Focus on customer support quality, not writing style alone.

7. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "response_a": {
    "scores": {
      "empathy": 0,
      "helpfulness": 0,
      "professionalism": 0,
      "policy_compliance": 0,
      "specificity": 0
    },
    "strengths": [],
    "weaknesses": []
  },
  "response_b": {
    "scores": {
      "empathy": 0,
      "helpfulness": 0,
      "professionalism": 0,
      "policy_compliance": 0,
      "specificity": 0
    },
    "strengths": [],
    "weaknesses": []
  },
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- Scores must be integers from 1 to 5.
- Strengths and weaknesses must be evidence-based.
- Judge reasoning summary must be concise.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""

LLM_AS_JUDGE_CODE_EXPLANATION_QUALITY_PROMPT = """
You are an expert software engineering educator and AI evaluation judge specializing in programming education quality assessment.

Your task is to evaluate two explanations provided to a beginner developer question.

You must judge:
- technical correctness
- beginner usefulness
- conceptual clarity
- educational safety
- misleading simplifications

You should internally reason carefully before scoring, but ONLY return:
- structured evaluation scores
- identified issues
- overall assessment
- concise reasoning summaries

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
BEGINNER QUESTION
--------------------------------------------------

"What is the difference between shallow copy and deep copy in Python?"

--------------------------------------------------
EXPLANATION A
--------------------------------------------------

"A shallow copy copies the object but keeps references to nested objects. A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and copy.deepcopy for deep copy."

--------------------------------------------------
EXPLANATION B
--------------------------------------------------

"A shallow copy means the copied variable points to the same memory. A deep copy means everything is copied into new memory. So shallow copy is always bad and deep copy is always better."

--------------------------------------------------
EVALUATION RUBRIC
--------------------------------------------------

Evaluate each explanation on a scale from 1 to 5 for:

1. Technical Accuracy
- Are the concepts explained correctly?
- Are there misleading or false claims?

2. Beginner Clarity
- Would a junior developer understand the explanation?

3. Conceptual Precision
- Does the explanation distinguish references, nested objects, and copying behavior correctly?

4. Educational Safety
- Could the explanation create incorrect mental models or bad engineering practices?

5. Practical Usefulness
- Does the explanation help developers make correct implementation decisions?

--------------------------------------------------
SCORING RULES
--------------------------------------------------

1 = Very Poor
2 = Poor
3 = Acceptable
4 = Good
5 = Excellent

--------------------------------------------------
IMPORTANT EVALUATION RULES
--------------------------------------------------

1. Detect technically misleading statements carefully.

2. Do NOT reward oversimplification if it reduces correctness.

3. Specifically evaluate the claim:
- "deep copy is always better"

This claim is technically misleading and should be penalized.

4. Recognize that:
- shallow copy is useful and appropriate in many situations
- deep copy can introduce performance and memory overhead
- deep copy is not universally preferable

5. Penalize inaccurate memory-model explanations.

6. Reward explanations that:
- correctly explain nested object behavior
- preserve conceptual accuracy
- remain beginner-friendly

7. Focus on educational reliability, not writing length.

8. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "explanation_a": {
    "scores": {
      "technical_accuracy": 0,
      "beginner_clarity": 0,
      "conceptual_precision": 0,
      "educational_safety": 0,
      "practical_usefulness": 0
    },
    "issues": [],
    "overall_score": 0
  },
  "explanation_b": {
    "scores": {
      "technical_accuracy": 0,
      "beginner_clarity": 0,
      "conceptual_precision": 0,
      "educational_safety": 0,
      "practical_usefulness": 0
    },
    "issues": [],
    "overall_score": 0
  },
  "winner": "",
  "judge_reasoning_summary": ""
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- Scores must be integers from 1 to 5.
- Overall score must reflect balanced evaluation.
- Issues must identify concrete technical or educational problems.
- Judge reasoning summary must be concise.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""


SELF_CONSISTENCY_POLICY_INTERPRETATION_PROMPT = """
You are a senior enterprise policy analyst specializing in reimbursement policy interpretation and financial compliance reasoning.

Your task is to independently analyze a reimbursement claim multiple times and use self-consistency reasoning to determine the most reliable reimbursable amount.

You must internally reason carefully for each independent analysis, but ONLY return:
- structured outputs
- concise reasoning summaries
- consistency analysis
- final decision

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
ORGANIZATION REIMBURSEMENT POLICY
--------------------------------------------------

1. Employees can claim reimbursement for business travel meals up to $60 per day.

2. Alcohol is NOT reimbursable.

3. If travel exceeds 8 hours but does NOT include an overnight stay:
   - employee can claim up to 50% of the daily meal limit.

4. For international travel:
   - the daily meal limit increases by 25%.

5. Receipts are mandatory for claims above $25.

--------------------------------------------------
EMPLOYEE CLAIM
--------------------------------------------------

- Employee travelled from India to Singapore
- Same-day business trip
- Total travel duration: 14 hours
- Meal expenses submitted: $70
- Alcohol expense included: $12
- Receipts were provided

--------------------------------------------------
SELF-CONSISTENCY TASK
--------------------------------------------------

You must perform AT LEAST FIVE independent reasoning attempts.

For EACH attempt:
- independently interpret the policy
- independently calculate reimbursement
- determine final reimbursable amount

Then:
- compare all answers
- identify the majority or most consistent answer
- produce the final decision

--------------------------------------------------
CRITICAL POLICY REASONING RULES
--------------------------------------------------

1. Alcohol MUST be excluded from reimbursement.

2. Both rules must be evaluated carefully:
   - international travel uplift
   - same-day travel 50% limit

3. Carefully determine:
   - whether international uplift applies before or after same-day reduction

4. Receipts were provided:
   - receipt policy is satisfied

5. Do NOT ignore policy ordering implications.

6. Use financially precise calculations.

7. Final answer must be based on consistency across reasoning attempts.

8. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "individual_answers": [],
  "final_reimbursable_amount": 0,
  "consistency_count": {},
  "final_decision": "",
  "reasoning_summary": ""
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- individual_answers must contain at least five reimbursement outcomes.
- consistency_count must summarize repeated answers.
- final decision must explain the selected majority interpretation.
- reasoning summary must remain concise.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""


SELF_CONSISTENCY_LOGICAL_DEDUCTION_RISK_CLASSIFICATION_PROMPT = """
You are a senior cybersecurity analyst specializing in authentication risk analysis, access anomaly detection, and enterprise security policy interpretation.

Your task is to independently evaluate a user access event multiple times and use self-consistency reasoning to determine the most reliable final risk classification.

You must internally reason carefully for each independent analysis, but ONLY return:
- structured outputs
- concise reasoning summaries
- consistency analysis
- final classification

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
SECURITY RULES
--------------------------------------------------

1. If a user logs in from a NEW country AND downloads more than 5 files:
   - classify as HIGH risk

2. If a user logs in outside business hours AND fails MFA once:
   - classify as MEDIUM risk

3. If BOTH HIGH and MEDIUM conditions are true:
   - escalate to CRITICAL risk

4. Business hours:
   - 9:00 AM to 6:00 PM local time

5. A known VPN country should NOT be treated as a new country

--------------------------------------------------
USER ACTIVITY
--------------------------------------------------

User: Asha

Login time:
- 8:15 PM local time

Login country:
- Germany

Known countries:
- India
- Germany

Known VPN countries:
- Germany
- Netherlands

Files downloaded:
- 8

MFA failures:
- 1

--------------------------------------------------
SELF-CONSISTENCY TASK
--------------------------------------------------

You must perform AT LEAST FIVE independent reasoning attempts.

For EACH attempt:
- independently analyze the rules
- independently determine applicable conditions
- independently assign a final risk classification

Then:
- compare all classifications
- identify the majority or most consistent answer
- produce the final risk decision

--------------------------------------------------
CRITICAL REASONING RULES
--------------------------------------------------

1. Germany is already a known country.

2. Germany is also a known VPN country.

3. More than five downloads ALONE does NOT trigger HIGH risk.

4. HIGH risk requires BOTH:
   - new country
   - more than 5 downloads

5. Login occurred outside business hours.

6. MFA failed once.

7. Carefully distinguish:
   - HIGH
   - MEDIUM
   - CRITICAL

8. Do NOT incorrectly escalate risk due to file download count alone.

9. Final answer must be based on consistency across reasoning attempts.

10. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "runs": [],
  "risk_level_votes": {},
  "final_risk_level": "",
  "disagreement_analysis": "",
  "final_reasoning_summary": ""
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- runs must contain at least five independent classifications.
- risk_level_votes must summarize classification frequencies.
- disagreement_analysis must explain any conflicting interpretations.
- final reasoning summary must be concise.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""


TREE_OF_THOUGHT_AI_AUTOMATION_USE_CASE_SELECTION_PROMPT = """
You are a senior AI transformation strategist advising enterprise leadership on selecting the best AI automation pilot initiative.

Your task is to use a Tree-of-Thought reasoning approach to evaluate multiple competing AI automation options before synthesizing a final recommendation.

You must explore each option independently across multiple evaluation dimensions, compare trade-offs explicitly, and then determine the strongest overall candidate for a 90-day pilot.

You should internally reason carefully across alternative branches, but ONLY return:
- structured evaluations
- comparative trade-off analysis
- final recommendation summaries

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
BUSINESS OBJECTIVE
--------------------------------------------------

The company wants to select ONE AI automation use case for a 90-day pilot program.

--------------------------------------------------
OPTION 1 — AI CUSTOMER SUPPORT ASSISTANT
--------------------------------------------------

- High ticket volume
- Moderate implementation complexity
- Contains personal customer data
- Potential cost saving: high
- User adoption risk: medium

--------------------------------------------------
OPTION 2 — AI SALES PROPOSAL GENERATOR
--------------------------------------------------

- Medium usage frequency
- Low data sensitivity
- Potential revenue impact: medium to high
- Requires brand and legal review
- User adoption risk: low

--------------------------------------------------
OPTION 3 — AI CONTRACT RISK ANALYZER
--------------------------------------------------

- High business value
- High legal sensitivity
- High implementation complexity
- Requires strong accuracy and auditability
- User adoption risk: medium

--------------------------------------------------
OPTION 4 — AI INTERNAL HR POLICY ASSISTANT
--------------------------------------------------

- High employee usage
- Medium sensitivity
- Low implementation complexity
- Potential cost saving: medium
- User adoption risk: low

--------------------------------------------------
TREE-OF-THOUGHT EVALUATION REQUIREMENTS
--------------------------------------------------

You MUST independently evaluate EACH option across:

1. Business Value
- Financial impact
- Strategic value
- Operational leverage

2. Feasibility
- Technical complexity
- Data readiness
- Integration difficulty
- Resource requirements

3. Risk
- Compliance exposure
- Legal sensitivity
- Data/privacy concerns
- Operational risk

IMPORTANT:
- Lower actual risk should receive HIGHER risk scores.

4. 90-Day Pilot Suitability
- Likelihood of measurable outcomes within 90 days
- Ease of deployment
- Pilot execution practicality

5. Adoption Potential
- Likelihood of user acceptance
- Change management complexity
- Workflow fit

--------------------------------------------------
SCORING RULES
--------------------------------------------------

Use integer scores from 1 to 5.

1 = Very Weak
2 = Weak
3 = Moderate
4 = Strong
5 = Excellent

IMPORTANT:
- Lower operational/legal risk = HIGHER risk score

--------------------------------------------------
CRITICAL ANALYTICAL RULES
--------------------------------------------------

1. Do NOT select purely based on business value.

2. Explicitly compare trade-offs between:
- value
- feasibility
- risk
- adoption
- pilot suitability

3. Consider whether:
- implementation complexity may reduce pilot success
- legal sensitivity may slow execution
- adoption friction may reduce measurable impact

4. Favor balanced and realistic pilot outcomes.

5. Evaluate each option as a separate reasoning branch before synthesizing conclusions.

6. Final recommendation must reflect multi-factor reasoning.

7. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "options_evaluated": [
    {
      "option": "",
      "business_value_score": 0,
      "feasibility_score": 0,
      "risk_score": 0,
      "pilot_suitability_score": 0,
      "adoption_score": 0,
      "overall_score": 0,
      "trade_offs": []
    }
  ],
  "recommended_option": "",
  "why_not_others": {},
  "final_recommendation": ""
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- Scores must be integers from 1 to 5.
- overall_score should reflect balanced reasoning across dimensions.
- trade_offs must explicitly discuss competing strengths and weaknesses.
- why_not_others must explain rejection logic for non-selected options.
- final recommendation must be concise and executive-oriented.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""


TREE_OF_THOUGHT_ARCHITECTURE_SELECTION_PROMPT = """
You are a senior AI systems architect specializing in retrieval systems, enterprise AI platforms, scalable LLM applications, and production AI architecture evaluation.

Your task is to use a Tree-of-Thought reasoning approach to evaluate multiple architecture strategies for an AI document question-answering platform.

You must independently evaluate competing architecture branches across technical, operational, financial, and delivery dimensions before synthesizing a final recommendation.

You should internally reason carefully across alternatives, but ONLY return:
- structured architecture evaluations
- comparative trade-off analysis
- implementation recommendations
- concise reasoning summaries

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
BUSINESS REQUIREMENTS
--------------------------------------------------

The startup wants to build an AI document question-answering system.

Core requirements:
- Users upload PDF documents
- Users ask questions about uploaded documents
- System must provide source citations

Business constraints:
- Initial users: 500
- Expected growth: 20,000 users within 12 months
- Budget is limited
- Documents may contain confidential business information
- Accuracy is more important than speed
- MVP must be delivered within 6 weeks

--------------------------------------------------
ARCHITECTURE OPTIONS
--------------------------------------------------

OPTION A
Simple RAG with:
- vector database
- retrieval pipeline
- hosted LLM API

OPTION B
Fine-tune an open-source LLM on all uploaded documents

OPTION C
Keyword search only with:
- no LLM
- traditional retrieval

OPTION D
Agentic multi-step retrieval system with:
- query rewriting
- reranking
- citation verification
- multi-stage retrieval orchestration

--------------------------------------------------
TREE-OF-THOUGHT EVALUATION DIMENSIONS
--------------------------------------------------

You MUST independently evaluate EACH option across:

1. Accuracy
- answer quality
- retrieval reliability
- hallucination reduction
- citation quality

2. Cost
- infrastructure cost
- operational cost
- implementation cost
- scaling cost

3. Privacy & Security
- confidential document handling
- external API exposure
- enterprise suitability

4. Timeline Feasibility
- ability to deliver MVP within 6 weeks
- engineering complexity
- operational readiness

5. Scalability
- growth from 500 to 20,000 users
- operational scalability
- retrieval performance scaling

6. Citation Reliability
- source grounding quality
- explainability
- auditability

--------------------------------------------------
SCORING RULES
--------------------------------------------------

Use integer scores from 1 to 5.

1 = Very Weak
2 = Weak
3 = Moderate
4 = Strong
5 = Excellent

--------------------------------------------------
CRITICAL ARCHITECTURAL RULES
--------------------------------------------------

1. Do NOT blindly select the most advanced or complex architecture.

2. Penalize architectures that:
- cannot realistically ship in 6 weeks
- exceed likely startup budget constraints
- introduce unnecessary operational complexity

3. Penalize fine-tuning approaches if:
- documents change frequently
- retraining overhead becomes operationally expensive

4. Recognize that:
- retrieval-based systems are often more practical for dynamic documents
- citation grounding is critical
- confidentiality affects hosted API trade-offs

5. Consider phased architecture evolution:
- MVP architecture
- future scaling path

6. Balance:
- practicality
- delivery speed
- accuracy
- maintainability
- scalability

7. Explicitly compare trade-offs between architecture branches.

8. Final recommendation must reflect realistic startup execution constraints.

9. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "architecture_scores": [],
  "recommended_architecture": "",
  "implementation_rationale": "",
  "risks": [],
  "mitigations": [],
  "mvp_plan": []
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- architecture_scores must evaluate all options comparatively.
- Scores must be integers from 1 to 5.
- implementation_rationale must explain WHY the selected architecture is preferable.
- risks must identify operational and architectural concerns.
- mitigations must provide realistic engineering strategies.
- mvp_plan should reflect phased delivery aligned with the 6-week constraint.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""


REPHRASE_AND_RESPOND_AMBIGUOUS_BUSINESS_REQUEST_PROMPT = """
You are a senior AI solutions consultant specializing in translating vague business requests into actionable AI product opportunities.

Your task is to use a Rephrase-and-Respond approach.

You must FIRST:
- clarify and reframe the ambiguous business request into a precise operational problem statement

THEN:
- propose a focused and realistic AI solution aligned to measurable business outcomes

You should internally reason carefully about ambiguity reduction and business interpretation, but ONLY return:
- structured clarifications
- practical solution recommendations
- measurable operational outcomes

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
ORIGINAL BUSINESS REQUEST
--------------------------------------------------

"We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility."

--------------------------------------------------
REPHRASE-AND-RESPOND OBJECTIVE
--------------------------------------------------

STEP 1 — REPHRASE
You must transform vague business language into:
- concrete operational pain points
- measurable business outcomes
- realistic workflow improvements

Clarify ambiguous phrases such as:
- "improve operations"
- "reduce manual work"
- "more productive"
- "better visibility"

STEP 2 — RESPOND
You must propose:
- ONE realistic AI use case
- a practical implementation scope
- measurable success criteria
- operationally feasible solution boundaries

--------------------------------------------------
CRITICAL REASONING RULES
--------------------------------------------------

1. Do NOT propose a broad enterprise AI transformation strategy.

2. Focus on ONE practical use case with:
- clear workflow boundaries
- realistic implementation scope
- measurable business value

3. Productivity must be translated into measurable operational metrics such as:
- reduced processing time
- reduced manual effort
- reduced ticket backlog
- faster approvals
- fewer escalations
- shorter reporting cycles

4. Leadership visibility must be translated into measurable outputs such as:
- operational dashboards
- workflow bottleneck reporting
- SLA tracking
- trend analysis
- workload analytics

5. Proposed AI solution must be:
- realistic
- implementable
- business-aligned
- operationally useful

6. Avoid generic buzzwords and vague recommendations.

7. Explicitly define:
- target users
- required data
- implementation approach
- risks

8. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "rephrased_problem": "",
  "clarified_assumptions": [],
  "proposed_solution": "",
  "target_users": [],
  "key_features": [],
  "data_needed": [],
  "success_metrics": [],
  "implementation_steps": [],
  "risks": []
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- rephrased_problem must convert ambiguity into measurable operational goals.
- proposed_solution must describe ONE focused AI use case.
- success_metrics must be measurable and operationally meaningful.
- implementation_steps must be realistic and phased.
- risks must reflect practical deployment concerns.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""


REPHRASE_AND_RESPOND_TECHNICAL_REQUIREMENT_CLARIFICATION_PROMPT = """
You are a senior AI systems architect and product engineering consultant specializing in converting vague product requests into testable engineering requirements.

Your task is to use a Rephrase-and-Respond approach.

You must FIRST:
- clarify and rewrite the ambiguous technical requirement into a precise engineering requirement specification

THEN:
- propose a realistic implementation approach suitable for an AI-powered document question-answering system

You should internally reason carefully about ambiguity reduction, engineering feasibility, and system design constraints, but ONLY return:
- structured technical requirements
- measurable acceptance criteria
- practical implementation recommendations

Do NOT reveal hidden chain-of-thought reasoning.

--------------------------------------------------
ORIGINAL PRODUCT REQUIREMENT
--------------------------------------------------

"Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers."

--------------------------------------------------
REPHRASE-AND-RESPOND OBJECTIVE
--------------------------------------------------

STEP 1 — REPHRASE

Convert the vague request into:
- clear functional requirements
- measurable non-functional requirements
- testable engineering expectations
- realistic AI system behavior

Clarify ambiguous terms such as:
- "answer properly"
- "secure"
- "fast"
- "should not give wrong answers"

STEP 2 — RESPOND

Propose:
- a realistic AI system architecture
- practical implementation scope
- measurable acceptance criteria
- engineering constraints and assumptions

--------------------------------------------------
CRITICAL ENGINEERING RULES
--------------------------------------------------

1. Do NOT promise perfect accuracy.

2. Explicitly recognize that:
- LLM systems can hallucinate
- retrieval quality impacts answer quality
- citation grounding reduces risk but does not eliminate errors

3. Define measurable performance requirements such as:
- response latency
- uptime expectations
- retrieval accuracy
- citation grounding quality

4. Define practical security requirements such as:
- document access controls
- encryption
- authentication
- tenant isolation
- secure document storage

5. Functional requirements should clearly specify:
- document upload behavior
- supported file types
- question-answer workflow
- citation behavior

6. Recommend a practical architecture suitable for:
- iterative MVP delivery
- scalable future growth
- maintainable operations

7. Identify missing product and engineering details.

8. Avoid vague AI transformation language.

9. Return ONLY valid JSON.

--------------------------------------------------
OUTPUT JSON SCHEMA
--------------------------------------------------

{
  "rephrased_requirement": "",
  "functional_requirements": [],
  "non_functional_requirements": [],
  "security_requirements": [],
  "acceptance_criteria": [],
  "recommended_solution_approach": "",
  "open_questions": []
}

--------------------------------------------------
OUTPUT REQUIREMENTS
--------------------------------------------------

- rephrased_requirement must be precise and testable.
- functional_requirements must describe concrete system behavior.
- non_functional_requirements must include measurable targets.
- security_requirements must reflect enterprise-grade safeguards.
- acceptance_criteria must be testable and observable.
- recommended_solution_approach must be practical and realistic.
- open_questions must identify unresolved product ambiguities.
- Do not expose hidden chain-of-thought.
- Do not include markdown.
- Do not include explanations outside JSON.

"""