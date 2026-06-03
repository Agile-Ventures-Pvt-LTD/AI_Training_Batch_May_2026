# ___________________________________________
#
# ZERO-SHOT PROMPTING
# ___________________________________________


# Case 1.1 — Vendor Risk Classification
case_1_1_prompt = """
You are an enterprise AI procurement risk analyst.

Your task is to evaluate the following vendor onboarding scenario and classify the overall vendor risk level.

Instructions:
- Analyze privacy, compliance, operational, pricing, scalability, and vendor maturity risks.
- Identify implicit risks, not only explicitly stated risks.
- Avoid generic procurement language.
- Use only the provided information.
- Be concise but specific.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Risk Classification Rules:
- LOW → Minimal operational and compliance concerns.
- MEDIUM → Noticeable risks requiring monitoring.
- HIGH → Significant operational, compliance, or business concerns.
- CRITICAL → Severe risks likely to block onboarding.

Required JSON Schema:
{
    "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
    "key_risk_factors": [],
    "missing_information": [],
    "business_recommendation": "",
    "confidence_score": 0.0
}

Vendor Scenario:

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
""".strip()



# Case 1.2 — Zero-Shot Executive Decision Memo
case_1_2_prompt = """
You are a senior enterprise strategy advisor preparing a decision memo for executive leadership.

Your task is to evaluate the following AI deployment proposal and provide a business decision recommendation.

Instructions:
- Focus on executive-level decision making, not summarization.
- Evaluate governance, compliance, ROI, operational impact, and organizational change risks.
- Do not overpromise AI automation benefits.
- Consider both financial and human impact.
- Use only the provided information.
- Be concise but specific.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Decision Rules:
- APPROVE → Benefits clearly outweigh risks and major controls already exist.
- REJECT → Risks, governance gaps, or ROI concerns make implementation unsuitable.
- APPROVE_WITH_CONDITIONS → Implementation is viable only if specific safeguards or requirements are met.

Required JSON Schema:
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

Scenario:

The company currently handles customer support through a team of 120 human agents.

Ticket volume has grown by 45% in the last 8 months.

Average response time has increased from 3 hours to 11 hours.

The AI team proposes deploying a GenAI chatbot for first-level support.

It can answer FAQs, summarize customer issues, and create draft responses for agents.

The estimated implementation cost is $250,000, with ongoing monthly cost of $30,000.

The compliance team is concerned because customer support tickets may contain personal information.

The support team is worried about job losses.

The CTO believes the chatbot can reduce ticket load by 35%.

The CFO wants payback within 12 months.

The company has not yet implemented AI governance policies.
""".strip()



# ==============================
# FEW-SHOT PROMPTING
# ==============================


# Case 2.1 — Few-Shot Customer Ticket Intent Classification
case_2_1_prompt = """
You are a customer support ticket classification system.

Your task is to classify customer support tickets into exactly one category.

Possible Categories:
- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- COMPLIANCE_CONCERN
- ESCALATION_RISK

Instructions:
- Classify based on the primary intent of the ticket.
- Angry tone may increase priority but does not automatically change category.
- Distinguish compliance concerns from technical issues.
- Distinguish feature requests from operational problems.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required Output Schema:
[
    {
        "ticket": "",
        "category": "",
        "priority": "LOW | MEDIUM | HIGH | URGENT",
        "justification": ""
    }
]

Examples:

Ticket:
"I was charged twice for the same invoice and nobody from billing has responded."

Output:
{
    "ticket": "I was charged twice for the same invoice and nobody from billing has responded.",
    "category": "BILLING_ISSUE",
    "priority": "HIGH",
    "justification": "The primary issue is duplicate billing with delayed support response."
}

Ticket:
"Our users cannot log in after the latest release deployment."

Output:
{
    "ticket": "Our users cannot log in after the latest release deployment.",
    "category": "ACCOUNT_ACCESS",
    "priority": "URGENT",
    "justification": "The core issue involves inability to access accounts affecting multiple users."
}

Ticket:
"We need confirmation that uploaded documents are not used to train AI models."

Output:
{
    "ticket": "We need confirmation that uploaded documents are not used to train AI models.",
    "category": "COMPLIANCE_CONCERN",
    "priority": "HIGH",
    "justification": "The request relates to privacy, data governance, and AI usage concerns."
}

Ticket:
"Can you add approval workflows before expense submissions are finalized?"

Output:
{
    "ticket": "Can you add approval workflows before expense submissions are finalized?",
    "category": "FEATURE_REQUEST",
    "priority": "MEDIUM",
    "justification": "The customer is requesting a new workflow capability."
}

Ticket:
"The dashboard crashes whenever we export reports after the new update."

Output:
{
    "ticket": "The dashboard crashes whenever we export reports after the new update.",
    "category": "TECHNICAL_BUG",
    "priority": "HIGH",
    "justification": "The issue describes broken application functionality after an update."
}

Now classify the following tickets:

1. I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.

2. The export button stopped working after your latest update. Our reporting team is blocked.

3. Can you add approval workflows before invoices are submitted?

4. We need confirmation that our customer data is not being used to train your AI models.

5. My admin account is locked and the password reset email never arrives.
""".strip()

# Case 2.2 — Few-Shot Requirement to API Contract
case_2_2_prompt = """
You are an AI leave-management request parser.

Your task is to convert natural language leave-management requests into structured API contracts.

Supported Actions:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

Instructions:
- Do not invent dates, leave types, or reasons.
- If required information is missing or ambiguous, set requires_clarification to true.
- Ambiguous phrases like "next Friday" or "sometime next week" require clarification.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required Output Schema:
[
    {
        "action": "",
        "parameters": {},
        "requires_clarification": true,
        "clarification_question": "",
        "confidence": 0.0
    }
]

Examples:

User Request:
"I want to take casual leave from 12 June to 15 June because I am travelling."

Output:
{
    "action": "APPLY_LEAVE",
    "parameters": {
        "leave_type": "casual",
        "start_date": "12 June",
        "end_date": "15 June",
        "reason": "travelling"
    },
    "requires_clarification": false,
    "clarification_question": "",
    "confidence": 0.95
}

User Request:
"How many sick leaves do I have left?"

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

User Request:
"Cancel my leave request for next Friday."

Output:
{
    "action": "CANCEL_LEAVE",
    "parameters": {},
    "requires_clarification": true,
    "clarification_question": "Please specify the exact date for next Friday.",
    "confidence": 0.82
}

User Request:
"What is the policy for maternity leave?"

Output:
{
    "action": "GET_POLICY",
    "parameters": {
        "leave_type": "maternity"
    },
    "requires_clarification": false,
    "clarification_question": "",
    "confidence": 0.97
}

User Request:
"I may take off sometime next week."

Output:
{
    "action": "APPLY_LEAVE",
    "parameters": {},
    "requires_clarification": true,
    "clarification_question": "Please specify the exact leave dates and leave type.",
    "confidence": 0.75
}

Now convert the following requests:

1. I want to take leave from 12th June to 15th June because I am travelling.

2. How many casual leaves do I have left?

3. Cancel my leave request for next Friday.

4. What is the policy for maternity leave?

5. I may take off sometime next week, not sure yet.

Return the final answer as a JSON array only.
""".strip()



# ==============================
# CHAIN-OF-THOUGHT REASONING
# ==============================


# Case 3.1 — Business ROI Decision with Hidden Trade-Offs
case_3_1_prompt = """
You are a senior AI business strategy analyst.

Your task is to evaluate whether an AI recommendation engine project should be approved.

Instructions:
- Perform careful numerical reasoning before making the decision.
- Use gross profit, NOT total revenue, when evaluating payback.
- Subtract ongoing AI operating costs from projected gains.
- Treat implementation time separately from post-launch payback.
- Think step-by-step internally, but return only concise reasoning summaries.
- Use only the provided information.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required JSON Schema:
{
    "incremental_revenue_range": "",
    "incremental_gross_profit_range": "",
    "monthly_net_benefit_range": "",
    "payback_period_range_months": "",
    "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
    "reasoning_summary": "",
    "key_assumptions": []
}

Scenario:

A retail company wants to deploy an AI recommendation engine.

Current monthly revenue: $2,000,000

Expected revenue uplift from recommendations: 4% to 7%

Implementation cost: $180,000 one-time

Monthly AI infrastructure cost: $22,000

Monthly maintenance cost: $8,000

Gross margin: 40%

Expected implementation time: 3 months

Leadership requires payback within 12 months after go-live.
""".strip()



# Case 3.2 — Root Cause Analysis for ML Model Performance Drop
case_3_2_prompt = """
You are a senior machine learning systems analyst.

Your task is to perform a structured root cause analysis for an ML fraud detection model whose performance degraded after deployment.

Instructions:
- Carefully distinguish between:
  - data drift
  - concept drift
  - pipeline failure
  - threshold miscalibration
- Do not assume pipeline failure unless evidence supports it.
- Recommend concrete diagnostics and remediation steps.
- Avoid generic "just retrain the model" responses.
- Think step-by-step internally, but return only concise reasoning summaries.
- Use only the provided information.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required JSON Schema:
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

A fraud detection model has degraded after deployment.

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
""".strip()




# ==============================
# LLM-AS-JUDGE
# ==============================


# Case 4.1 — Judging AI-Generated Customer Support Responses
case_4_1_prompt = """
You are an expert customer support quality evaluator.

Your task is to evaluate two customer support responses using a structured scoring rubric.

Evaluation Criteria:
- Empathy
- Professionalism
- Problem Resolution Quality
- Clarity
- Policy Safety

Scoring Rules:
- Score each category from 1 to 5.
- Do not prefer a response simply because it is longer.
- Penalize vague or dismissive responses.
- Penalize unsafe promises such as guaranteeing refunds without verification.
- Reward empathy, actionable guidance, and escalation handling.

Return ONLY valid JSON.
Do not include markdown formatting.
Do not include explanations outside JSON.

Required JSON Schema:
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
"I’m sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy."
""".strip()


# Case 4.2 — Judging Code Explanation Quality
case_4_2_prompt = """
You are an expert programming educator and technical reviewer.

Your task is to evaluate two explanations about shallow copy and deep copy in Python.

Evaluation Criteria:
- Technical Accuracy
- Beginner Friendliness
- Clarity
- Completeness
- Misleading Statements

Scoring Rules:
- Score each category from 1 to 5.
- Penalize technically incorrect simplifications.
- Do not reward oversimplification if it reduces correctness.
- Explain why deep copy is not always better.
- Focus on educational usefulness for beginner developers.

Return ONLY valid JSON.
Do not include markdown formatting.
Do not include explanations outside JSON.

Required JSON Schema:
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
""".strip()



# ==============================
# SELF-CONSISTENCY
# ==============================


# Case 5.1 — Self-Consistency for Complex Policy Interpretation
case_5_1_prompt = """
You are an enterprise reimbursement policy analyst.

Your task is to calculate the reimbursable amount for the following employee expense claim.

Instructions:
- Carefully apply all reimbursement rules.
- Exclude non-reimbursable expenses.
- Apply international travel adjustment correctly.
- Apply same-day travel adjustment correctly.
- Think step-by-step internally, but return only concise reasoning.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required JSON Schema:
{
    "reimbursable_amount": 0,
    "reasoning_summary": ""
}

Policy:

- Employees can claim reimbursement for business travel meals up to $60 per day.
- Alcohol is not reimbursable.
- If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.
- For international travel, the daily meal limit increases by 25%.
- Receipts are mandatory for claims above $25.

Employee Claim:

- Employee travelled from India to Singapore for a same-day business meeting.
- Total travel duration was 14 hours.
- Meal expenses submitted: $70
- Alcohol expense included: $12
- Receipts were provided.
""".strip()


# Case 5.2 — Self-Consistency for Logical Deduction
case_5_2_prompt = """
You are a security risk analysis system.

Your task is to determine the final access risk classification using the provided rules.

Instructions:
- Carefully apply all rules exactly as written.
- Do not assume HIGH risk unless all HIGH-risk conditions are satisfied.
- Treat known VPN countries appropriately.
- Think step-by-step internally, but return only concise reasoning.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required JSON Schema:
{
    "risk_level": "",
    "reasoning_summary": ""
}

Rules:

1. If a user logs in from a new country and downloads more than 5 files, flag as HIGH risk.

2. If a user logs in outside business hours and fails MFA once, flag as MEDIUM risk.

3. If both HIGH and MEDIUM conditions are true, escalate to CRITICAL.

4. Business hours are 9 AM to 6 PM local time.

5. A known VPN country should not be treated as a new country.

User Activity:

- User: Asha
- Login time: 8:15 PM local time
- Login country: Germany
- Known countries: India, Germany
- Known VPN countries: Germany, Netherlands
- Files downloaded: 8
- MFA failures: 1
""".strip()

# ==============================
# TREE-OF-THOUGHT
# ==============================


# Case 6.1 — Selecting the Best AI Automation Use Case
case_6_1_prompt = """
You are an enterprise AI strategy advisor.

Your task is to evaluate multiple AI automation opportunities and recommend the best option for a 90-day pilot program.

Instructions:
- Evaluate each option independently before comparing them.
- Consider:
  - business value
  - feasibility
  - implementation risk
  - pilot suitability
  - user adoption likelihood
- Lower operational and compliance risk should receive a higher risk score.
- Do not choose only based on business value.
- Explicitly compare trade-offs across options.
- Think step-by-step internally, but return only concise reasoning summaries.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Scoring Rules:
- Scores must range from 1 to 5.
- Higher scores are better.

Required JSON Schema:
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
""".strip()

# Case 6.2 — Tree-of-Thought Architecture Selection
case_6_2_prompt = """
You are a senior AI systems architect.

Your task is to evaluate multiple architecture options for an AI document question-answering system and recommend the best MVP architecture.

Instructions:
- Evaluate each architecture independently before making comparisons.
- Consider:
  - accuracy
  - implementation complexity
  - cost
  - privacy
  - scalability
  - citation reliability
  - MVP delivery timeline
- Penalize architectures that are difficult to implement within 6 weeks.
- Penalize unnecessary complexity for an MVP.
- Penalize fine-tuning approaches if documents change frequently.
- Consider phased implementation approaches when appropriate.
- Accuracy is more important than speed.
- Think step-by-step internally, but return only concise reasoning summaries.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required JSON Schema:
{
    "architecture_scores": [],
    "recommended_architecture": "",
    "implementation_rationale": "",
    "risks": [],
    "mitigations": [],
    "mvp_plan": []
}

System Requirements:
- Users upload PDF documents.
- Users ask questions about uploaded documents.
- The system must show source citations.
- Initial users: 500
- Expected growth: 20,000 users in 12 months
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
""".strip()




# ==============================
# REPHRASE-AND-RESPOND
# ==============================


# Case 7.1 — Ambiguous Business Request Rewriting
case_7_1_prompt = """
You are an enterprise AI solutions consultant.

Your task is to first clarify an ambiguous business request and then propose a realistic AI solution.

Instructions:
- First convert vague language into a measurable business problem.
- Clearly state assumptions used for clarification.
- Define what productivity and leadership visibility mean in practical operational terms.
- Propose a focused and realistic AI solution rather than a broad AI transformation program.
- Avoid generic consulting language.
- Think step-by-step internally, but return only concise reasoning summaries.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required JSON Schema:
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

Business Request:

"We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility."
""".strip()




# Case 7.2 — Rephrase Technical Requirement into Engineering Specification
case_7_2_prompt = """
You are a senior AI systems analyst.

Your task is to convert an ambiguous technical request into a clear engineering specification.

Instructions:
- First identify ambiguity and missing constraints.
- Convert vague requirements into measurable engineering objectives.
- Explicitly separate:
  - functional requirements
  - non-functional requirements
  - assumptions
  - dependencies
  - risks
- Avoid inventing unavailable technical details.
- Avoid overengineering the solution.
- Think step-by-step internally, but return only concise reasoning summaries.
- Return ONLY valid JSON.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

Required JSON Schema:
{
    "rephrased_requirement": "",
    "functional_requirements": [],
    "non_functional_requirements": [],
    "assumptions": [],
    "dependencies": [],
    "open_questions": [],
    "risks": [],
    "recommended_next_steps": []
}

Technical Request:

"We need a smart AI search system for all company documents. Employees should quickly find information and it should scale as the company grows."
""".strip()