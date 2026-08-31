# Zero Shot Prompts

# Task.1 Prompt

ZERO_SHOT_PROMPT = """

Analyze the following vendor onboarding information and classify the vendor risk level as:
LOW, MEDIUM, HIGH, or CRITICAL.

You must evaluate:
- Privacy risks
- Compliance risks
- Operational risks
- Pricing and scalability risks
- Vendor maturity risks

Focus on identifying implicit risks, not only explicit statements.

Avoid generic procurement language.

Return ONLY valid JSON using this exact schema:

{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": [],
  "missing_information": [],
  "business_recommendation": "",
  "confidence_score": 0.0
}

Vendor Information:

Vendor: DocuMind AI

The vendor claims their solution can process invoices, contracts, and identity documents using OCR and LLM-based extraction.
They say the model is hosted in a multi-tenant cloud environment.
They do not currently provide region-specific data residency, but they are planning to add it next year.

They support encryption at rest and in transit.
However, customer data may be used for product improvement unless customers opt out through a manual request.
They have SOC 2 Type I certification but not Type II.
Their uptime SLA is 99.5%.

The pricing is usage-based and could increase significantly if document volume grows.
The vendor provides APIs, but rate limits are not clearly documented.
They have only been operating for 18 months and have 12 enterprise customers.

The business team wants to use this vendor for processing supplier invoices and purchase contracts.

"""

# Task 2 Prompt 

ZERO_SHOT_EXECUTIVE_MEMO_PROMPT = """

Analyze the following business situation and produce a decision-oriented executive memo.

Your response must:
- Make a clear business decision
- Focus on operational, financial, compliance, governance, and workforce impact
- Avoid generic summaries
- Avoid overpromising AI automation benefits
- Identify realistic implementation risks and business conditions
- Consider ROI expectations and organizational readiness

Return ONLY valid JSON using this exact schema:

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

Business Situation:

The company currently handles customer support through a team of 120 human agents.

Ticket volume has grown by 45'%' in the last 8 months.

Average response time has increased from 3 hours to 11 hours.

The AI team proposes deploying a GenAI chatbot for first-level support.

The chatbot can:
- answer FAQs,
- summarize customer issues,
- and create draft responses for agents.

The estimated implementation cost is $250,000, with ongoing monthly cost of $30,000.
The compliance team is concerned because customer support tickets may contain personal information.
The support team is worried about job losses.
The CTO believes the chatbot can reduce ticket load by 35%.
The CFO wants payback within 12 months.
The company has not yet implemented AI governance policies.

Task
Create a zero-shot prompt that generates an executive decision memo with a clear decision and business 
conditions.

Constraints
No examples in the prompt.
The output must be decision-oriented, not a summary.
It must include governance, compliance, ROI, and change-management considerations.
It must not overpromise automation benefits.

"""

# Few Shot Prompting

# Task 3 Prompt

FEW_SHOT_TICKET_CLASSIFICATION_PROMPT = """
You are a customer support ticket classification system.

Your task is to classify customer tickets into exactly one category:

- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- COMPLIANCE_CONCERN
- ESCALATION_RISK

Rules:
- Angry or emotional tone may increase priority but does NOT automatically change category.
- Distinguish technical failures from compliance or policy concerns.
- Distinguish feature requests from operational problems.
- Assign only ONE best-fit category.
- Provide concise but specific justification.
- Focus on the primary customer intent.

Return ONLY valid JSON using this schema:

[
  {
    "ticket": "",
    "category": "",
    "priority": "LOW | MEDIUM | HIGH | URGENT",
    "justification": ""
  }
]

Training Examples:

Example 1:
Ticket:
"I was billed for a premium subscription after cancellation."

Output:
{
  "ticket": "I was billed for a premium subscription after cancellation.",
  "category": "BILLING_ISSUE",
  "priority": "HIGH",
  "justification": "Customer reports incorrect billing after account cancellation."
}

Example 2:
Ticket:
"The dashboard crashes every time we upload CSV files."

Output:
{
  "ticket": "The dashboard crashes every time we upload CSV files.",
  "category": "TECHNICAL_BUG",
  "priority": "HIGH",
  "justification": "Core platform functionality is failing during file upload."
}

Example 3:
Ticket:
"I cannot log into the admin portal and password reset emails never arrive."

Output:
{
  "ticket": "I cannot log into the admin portal and password reset emails never arrive.",
  "category": "ACCOUNT_ACCESS",
  "priority": "URGENT",
  "justification": "User is fully blocked from account access."
}

Example 4:
Ticket:
"Can you add role-based approvals before payments are processed?"

Output:
{
  "ticket": "Can you add role-based approvals before payments are processed?",
  "category": "FEATURE_REQUEST",
  "priority": "MEDIUM",
  "justification": "Customer is requesting a new workflow capability."
}

Example 5:
Ticket:
"We need written confirmation that our uploaded documents are not used to train AI models."

Output:
{
  "ticket": "We need written confirmation that our uploaded documents are not used to train AI models.",
  "category": "COMPLIANCE_CONCERN",
  "priority": "HIGH",
  "justification": "Customer is requesting clarification regarding data governance and AI usage."
}

Example 6:
Ticket:
"I have contacted support three times about duplicate invoices and nobody has responded."

Output:
{
  "ticket": "I have contacted support three times about duplicate invoices and nobody has responded.",
  "category": "BILLING_ISSUE",
  "priority": "URGENT",
  "justification": "Primary issue is duplicate billing, while delayed support response increases urgency."
}

Now classify these tickets:

1. I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.
2. The export button stopped working after your latest update. Our reporting team is blocked.
3. Can you add approval workflows before invoices are submitted?
4. We need confirmation that our customer data is not being used to train your AI models.
5. My admin account is locked and the password reset email never arrives.
"""

# Task 4 Prompt

FEW_SHOT_LEAVE_API_PROMPT = """
You are an API contract generation system for an AI-powered leave management assistant.

Your task is to convert user requests into structured API payloads.

Supported actions:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

Rules:
- Do NOT invent dates.
- Do NOT invent leave types.
- If required information is missing or ambiguous, set:
  "requires_clarification": true
- Generate a clarification question when needed.
- Ambiguous dates such as:
  - "next Friday"
  - "sometime next week"
  must not be converted into exact dates.
- Confidence should reflect certainty of extracted information.

Return ONLY valid JSON using this schema:

{
  "action": "",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "",
  "confidence": 0.0
}

Training Examples:

Example 1:

User:
"I want to apply for casual leave from 10 July to 12 July because I am attending a wedding."

Output:
{
  "action": "APPLY_LEAVE",
  "parameters": {
    "leave_type": "casual",
    "start_date": "10 July",
    "end_date": "12 July",
    "reason": "attending a wedding"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.96
}

Example 2:

User:
"How many sick leaves do I have remaining?"

Output:
{
  "action": "CHECK_BALANCE",
  "parameters": {
    "leave_type": "sick"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.98
}

Example 3:

User:
"Cancel my leave for next Friday."

Output:
{
  "action": "CANCEL_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please provide the exact date for the leave request you want to cancel.",
  "confidence": 0.62
}

Example 4:

User:
"What is the maternity leave policy?"

Output:
{
  "action": "GET_POLICY",
  "parameters": {
    "policy_type": "maternity leave"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.97
}

Example 5:

User:
"I might take leave sometime next week."

Output:
{
  "action": "APPLY_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please provide the exact leave dates and leave type.",
  "confidence": 0.45
}

Now convert these user requests:

1. I want to take leave from 12th June to 15th June because I am travelling.

2. How many casual leaves do I have left?

3. Cancel my leave request for next Friday.

4. What is the policy for maternity leave?

5. I may take off sometime next week, not sure yet.
"""

# Task 5 Prompts

CHAIN_OF_THOUGHT_ROI_PROMPT = """
You are a strategic financial analyst.

Analyze the following AI investment proposal carefully.

You must:
- Perform step-by-step financial reasoning internally.
- Use gross profit, NOT total revenue, for ROI calculations.
- Subtract ongoing monthly AI operating costs from benefits.
- Treat implementation time separately from payback after go-live.
- Consider best-case and worst-case ranges.
- Return only concise reasoning summaries, not detailed chain-of-thought calculations.

Return ONLY valid JSON using this exact schema:

{
  "incremental_revenue_range": "",
  "incremental_gross_profit_range": "",
  "monthly_net_benefit_range": "",
  "payback_period_range_months": "",
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "reasoning_summary": "",
  "key_assumptions": []
}

Business Scenario:

A retail company wants to deploy an AI recommendation engine.

Current monthly revenue: $2,000,000

Expected revenue uplift from recommendations: 4% to 7%

Implementation cost: $180,000 one-time

Monthly AI infrastructure cost: $22,000

Monthly maintenance cost: $8,000

Gross margin: 40%

Expected implementation time: 3 months

Leadership requires payback within 12 months after go-live.

Important:
- Use monthly incremental gross profit for payback calculations.
- Include AI operating costs in monthly net benefit calculations.
- Do not expose detailed hidden reasoning.
- Return concise reasoning summaries only.
"""

# Task 6 Prompt

CHAIN_OF_THOUGHT_ML_ROOT_CAUSE_PROMPT = """
You are a senior machine learning reliability engineer.

Analyze the following ML model degradation scenario and perform a structured root cause analysis.

You must:
- Reason carefully about possible causes internally.
- Distinguish between:
  - data drift,
  - concept drift,
  - pipeline failure,
  - and threshold miscalibration.
- Do NOT assume pipeline failure simply because performance dropped.
- Recommend concrete diagnostics and investigation steps.
- Avoid giving a simplistic “just retrain the model” answer.
- Return concise reasoning summaries only.

Return ONLY valid JSON using this exact schema:

{
  "most_likely_causes": [],
  "evidence": [],
  "less_likely_causes": [],
  "recommended_diagnostics": [],
  "short_term_actions": [],
  "long_term_actions": [],
  "reasoning_summary": ""
}

Scenario:

Before deployment:
- Precision: 0.82
- Recall: 0.76
- F1-score: 0.79

After 3 months:
- Precision: 0.61
- Recall: 0.72
- F1-score: 0.66

Additional observations:
- Transaction volume increased by 30%.
- A new payment channel was introduced.
- Fraud patterns changed after a promotional campaign.
- Data pipeline logs show no failed jobs.
- Feature distribution for transaction_amount shifted significantly.
- Model was not retrained after launch.

Important:
- Use structured ML reasoning.
- Distinguish operational causes from statistical causes.
- Return concise reasoning summaries only.
"""

# Task 7 Prompt

LLM_AS_JUDGE_SUPPORT_RESPONSE_PROMPT = """
You are an expert customer support quality evaluator.

Your task is to evaluate two AI-generated customer support responses using a structured scoring rubric.

Scoring Rules:
- Score each category from 1 to 5.
- Do NOT prefer a response simply because it is longer.
- Penalize vague, dismissive, or unhelpful responses.
- Penalize responses that promise refunds without verification.
- Reward empathy, accountability, actionable next steps, and policy-safe handling.

Evaluation Categories:
- empathy
- clarity
- actionability
- policy_compliance
- professionalism

Return ONLY valid JSON using this exact schema:

{
  "response_a": {
    "scores": {},
    "strengths": [],
    "weaknesses": []
  },
  "response_b": {
    "scores": {},
    "strengths": [],
    "weaknesses": []
  },
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}

Customer Question:

"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

Response A:

"We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you."

Response B:

"I'm sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy."

Important:
- Evaluate quality, not verbosity.
- Focus on customer handling effectiveness.
- Check whether refund handling follows verification procedures.
"""

# Task 8 Prompt

LLM_AS_JUDGE_CODE_EXPLANATION_PROMPT = """
You are an expert Python educator and technical reviewer.

Your task is to evaluate two explanations about shallow copy vs deep copy in Python.

Evaluation Goals:
- Assess technical accuracy.
- Assess beginner friendliness.
- Detect misleading or incorrect claims.
- Do NOT reward oversimplification when it becomes inaccurate.
- Explain why deep copy is NOT always better.
- Consider correctness, nuance, clarity, and educational usefulness.

Scoring Categories (1 to 5):
- technical_accuracy
- beginner_clarity
- conceptual_correctness
- nuance_and_limitations
- educational_usefulness

Scoring Rules:
- Score each category from 1 to 5.
- Penalize technically misleading simplifications.
- Penalize absolute claims such as:
  "deep copy is always better"
- Reward explanations that distinguish references from recursive copying behavior.
- Do NOT prefer longer explanations automatically.

Return ONLY valid JSON using this exact schema:

{
  "explanation_a": {
    "scores": {},
    "issues": [],
    "overall_score": 0
  },
  "explanation_b": {
    "scores": {},
    "issues": [],
    "overall_score": 0
  },
  "winner": "",
  "judge_reasoning_summary": ""
}

Question:

"What is the difference between shallow copy and deep copy in Python?"

Explanation A:

"A shallow copy copies the object but keeps references to nested objects. A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and copy.deepcopy for deep copy."

Explanation B:

"A shallow copy means the copied variable points to the same memory. A deep copy means everything is copied into new memory. So shallow copy is always bad and deep copy is always better."

Important:
- Evaluate educational quality and technical correctness.
- Explain why deep copy may be unnecessary, expensive, or undesirable in some cases.
"""

# Task 9 Prompt

SELF_CONSISTENCY_POLICY_PROMPT = """
You are a corporate travel reimbursement policy analyst.

Analyze the reimbursement policy carefully and calculate the final reimbursable amount.

Important Rules:
- Perform reasoning carefully before answering.
- Alcohol is NEVER reimbursable.
- Same-day travel exceeding 8 hours allows reimbursement up to 50% of the daily meal limit.
- International travel increases the daily meal limit by 25%.
- Receipts are required only for claims above $25.
- Return concise reasoning only.

Return ONLY valid JSON using this schema:

{
  "reimbursable_amount": 0,
  "reasoning": ""
}

Policy:

Employees can claim reimbursement for business travel meals up to $60 per day.

Alcohol is not reimbursable.

If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.

For international travel, the daily meal limit increases by 25%.

Receipts are mandatory for claims above $25.

Employee Claim:

An employee travelled from India to Singapore for a same-day business meeting.

Total travel duration was 14 hours.

The employee submitted meal expenses of $70, including $12 for alcohol.

Receipts were provided.

Important:
- Apply both the international adjustment and same-day travel rule carefully.
- Do not expose detailed hidden reasoning.
"""

# Task 10 Prompt
SELF_CONSISTENCY_SECURITY_PROMPT = """
You are a cybersecurity risk analyst.

Analyze the access log carefully and determine the final risk classification.

Important Rules:
1. If a user logs in from a new country AND downloads more than 5 files,
   classify as HIGH risk.

2. If a user logs in outside business hours AND fails MFA once,
   classify as MEDIUM risk.

3. If both HIGH and MEDIUM conditions are true,
   escalate to CRITICAL risk.

4. Business hours are 9 AM to 6 PM local time.

5. A known VPN country should NOT be treated as a new country.

Instructions:
- Reason carefully before deciding.
- Do NOT assume large downloads alone create HIGH risk.
- Distinguish carefully between known countries and new countries.
- Return concise reasoning only.

Return ONLY valid JSON using this schema:

{
  "risk_level": "",
  "reasoning": ""
}

User Activity:

User: Asha

Login time: 8:15 PM local time

Login country: Germany

Known countries:
- India
- Germany

Known VPN countries:
- Germany
- Netherlands

Files downloaded: 8

MFA failures: 1

Important:
- Germany is already a known country.
- Germany is also a known VPN country.
- More than 5 downloads alone does NOT trigger HIGH risk.
"""

# Task 11 Prompt
TREE_OF_THOUGHT_AI_USE_CASE_PROMPT = """
You are an enterprise AI strategy advisor.

Your task is to evaluate multiple AI automation pilot options using a tree-of-thought reasoning approach.

Instructions:
- Evaluate EACH option independently across:
  - business value
  - feasibility
  - operational/legal risk
  - 90-day pilot suitability
  - user adoption likelihood

- Then compare trade-offs across all options before making a recommendation.

Scoring Rules:
- Scores must be from 1 to 5.
- Higher risk should receive LOWER scores.
- Lower risk should receive HIGHER scores.
- Do NOT choose based only on business value.
- Consider implementation complexity, governance risk, adoption risk, and pilot feasibility.
- Explicitly compare strengths and weaknesses across options.
- Use concise reasoning summaries only.

Return ONLY valid JSON using this exact schema:

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

Options:

Option 1: AI customer support assistant
- High ticket volume
- Moderate implementation complexity
- Contains personal customer data
- Potential cost saving: high
- User adoption risk: medium

Option 2: AI sales proposal generator
- Medium usage frequency
- Low data sensitivity
- Potential revenue impact: medium to high
- Requires brand and legal review
- User adoption risk: low

Option 3: AI contract risk analyzer
- High business value
- High legal sensitivity
- High implementation complexity
- Requires strong accuracy and auditability
- User adoption risk: medium

Option 4: AI internal HR policy assistant
- High employee usage
- Medium sensitivity
- Low implementation complexity
- Potential cost saving: medium
- User adoption risk: low

Important:
- Compare multiple reasoning branches before final recommendation.
- Consider realistic 90-day pilot constraints.
- Avoid simplistic “highest value wins” reasoning.
"""

# Task 12 Prompt

TREE_OF_THOUGHT_ARCHITECTURE_PROMPT = """
You are a senior AI systems architect.

Your task is to evaluate multiple architecture options for an AI document question-answering system using a tree-of-thought reasoning approach.

Requirements:
- Users upload PDF documents.
- Users ask questions about uploaded documents.
- The system must provide source citations.
- Initial users: 500
- Expected growth: 20,000 users within 12 months.
- Budget is limited.
- Documents may contain confidential business information.
- Accuracy is more important than speed.
- MVP must be delivered in 6 weeks.

Architecture Options:

Option A:
Simple RAG with vector database and hosted LLM API

Option B:
Fine-tune an open-source LLM on all documents

Option C:
Keyword search only with no LLM

Option D:
Agentic multi-step retrieval with query rewriting, reranking, and citation verification

Evaluation Dimensions:
- accuracy
- implementation complexity
- infrastructure cost
- privacy/security
- scalability
- citation reliability
- 6-week MVP feasibility

Instructions:
- Evaluate EACH architecture independently first.
- Then compare trade-offs across all options.
- Do NOT blindly prefer the most advanced or complex architecture.
- Penalize fine-tuning approaches if documents change frequently.
- Respect the 6-week MVP timeline.
- Consider phased delivery approaches.
- Accuracy and citation reliability are higher priority than speed.
- Use concise reasoning summaries only.

Scoring Rules:
- Scores must be from 1 to 5.
- Higher scores indicate better suitability.

Return ONLY valid JSON using this exact schema:

{
  "architecture_scores": [],
  "recommended_architecture": "",
  "implementation_rationale": "",
  "risks": [],
  "mitigations": [],
  "mvp_plan": []
}
"""

# Task 13 Prompt
REPHRASE_AND_RESPOND_PROMPT = """
You are a senior AI business analyst and solution architect.

Your task is to handle ambiguous business requests using a two-step approach:

STEP 1: Rephrase the problem
- Convert the vague request into a clear, specific, and measurable problem statement.
- Define what “productivity” and “visibility” could realistically mean in a business context.

STEP 2: Propose a solution
- Design a practical AI solution that directly addresses the clarified problem.
- Avoid generic digital transformation language.
- Focus on realistic, implementable AI use cases.

Business Request:
"We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility."

Output Requirements:
- Be specific and measurable
- Avoid vague enterprise buzzwords
- Focus on actionable AI systems, not strategy consulting outputs

Return ONLY valid JSON using this schema:

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
"""

# Task 14 Prompt
REPHRASE_AND_RESPOND_TECHNICAL_REQUIREMENT_PROMPT = """
You are a senior software architect and requirements engineer.

Your task is to convert a vague product requirement into a structured, testable engineering specification using a rephrase-and-respond approach.

STEP 1: Rephrase the requirement
- Convert the vague description into a clear, precise, and unambiguous engineering requirement.
- Identify what "secure", "fast", and "properly" must mean in measurable terms.

STEP 2: Expand into engineering specification
- Break the requirement into functional, non-functional, and security requirements.
- Identify missing details and clarify assumptions.
- Propose a realistic technical architecture suitable for an AI document Q&A system.

Important constraints:
- Do NOT assume perfect accuracy ("no wrong answers" is not realistic).
- Define measurable SLAs for performance and security.
- Identify ambiguities and open questions explicitly.
- Focus on implementable system design, not abstract ideas.

Product Requirement:
"Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers."

Return ONLY valid JSON using this schema:

{
  "rephrased_requirement": "",
  "functional_requirements": [],
  "non_functional_requirements": [],
  "security_requirements": [],
  "acceptance_criteria": [],
  "recommended_solution_approach": "",
  "open_questions": []
}
"""
