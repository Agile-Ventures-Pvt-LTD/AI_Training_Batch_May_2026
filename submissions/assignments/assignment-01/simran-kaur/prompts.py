#--------------------ZERO SHOT PROMPTS--------------------------

#-------------Case 1.1 - Zero-Shot Risk Classification for Vendor Onboarding

ZERO_SHOT_VENDOR_RISK_PROMPT = """
You are an enterprise AI procurement risk analyst.

Your task is to evaluate the following AI vendor and classify overall vendor risk.

Evaluate:
- Privacy risk
- Compliance risk
- Operational risk
- Pricing risk
- Vendor maturity risk

Risk levels:
- LOW
- MEDIUM
- HIGH
- CRITICAL

Instructions:
- Identify explicit and implicit risks
- Avoid generic procurement language
- Be concise and business-oriented
- Return valid JSON only
- Do not include markdown
- Do not explain outside the schema

Required JSON schema:

{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": [],
  "missing_information": [],
  "business_recommendation": "",
  "confidence_score": 0.0
}

Vendor details:

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

#---------------Case 1.2 - Zero-Shot Executive Decision Memo

ZERO_SHOT_EXECUTIVE_DECISION_PROMPT = """
You are a Chief Operating Officer advisor evaluating enterprise AI investment decisions.

Your task is to generate an executive decision memo for the proposed AI customer support chatbot initiative.

The response must:
- Be decision-oriented, not descriptive
- Evaluate business trade-offs
- Consider governance, compliance, ROI, operational impact, and workforce impact
- Avoid unrealistic automation claims
- Explicitly identify approval conditions where appropriate
- Focus on practical enterprise risks and readiness

Decision options:
- APPROVE
- REJECT
- APPROVE_WITH_CONDITIONS

Instructions:
- Do not summarize the scenario
- Do not use generic AI transformation language
- Do not assume AI will fully replace human agents
- Consider implementation readiness and governance maturity
- Return valid JSON only
- Do not include markdown
- Do not include explanations outside the schema

Required JSON schema:

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
"""

#-----------------------------------FEW-SHOT-PROMPTING-------------------------------

#----------------Case 2.1 - Few-Shot Customer Ticket Intent Classification

FEW_SHOT_TICKET_CLASSIFICATION_PROMPT = """
You are an enterprise customer support ticket classifier.

Your task is to classify support tickets into one of the following categories:

CATEGORIES:
- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- COMPLIANCE_CONCERN
- ESCALATION_RISK

You must also assign priority:
LOW | MEDIUM | HIGH | URGENT

RULES:
- Angry tone increases priority but NOT category
- Compliance concerns are NOT bugs
- Feature requests are NOT billing issues
- Escalation risk = threats, public complaints, legal pressure
- Be consistent and structured

OUTPUT FORMAT:
Return a JSON array of objects:
[
  {
    "ticket": "",
    "category": "",
    "priority": "",
    "justification": ""
  }
]

---

EXAMPLES:

Ticket:
"I was charged twice this month and support is ignoring me"
Output:
[
  {
    "ticket": "I was charged twice this month and support is ignoring me",
    "category": "BILLING_ISSUE",
    "priority": "HIGH",
    "justification": "Billing discrepancy with delayed support response increases urgency"
  }
]

Ticket:
"The export button stopped working after update"
Output:
[
  {
    "ticket": "The export button stopped working after update",
    "category": "TECHNICAL_BUG",
    "priority": "HIGH",
    "justification": "Feature malfunction after update indicates a technical regression"
  }
]

Ticket:
"Can you add approval workflows for invoices?"
Output:
[
  {
    "ticket": "Can you add approval workflows for invoices?",
    "category": "FEATURE_REQUEST",
    "priority": "MEDIUM",
    "justification": "Request for new functionality, not a system failure"
  }
]

Ticket:
"We need confirmation our data is not used for AI training"
Output:
[
  {
    "ticket": "We need confirmation our data is not used for AI training",
    "category": "COMPLIANCE_CONCERN",
    "priority": "HIGH",
    "justification": "Data usage policy clarification request indicates compliance sensitivity"
  }
]

Ticket:
"My admin account is locked and password reset email never arrives"
Output:
[
  {
    "ticket": "My admin account is locked and password reset email never arrives",
    "category": "ACCOUNT_ACCESS",
    "priority": "URGENT",
    "justification": "User cannot access account and recovery mechanism failing"
  }
]

---

NOW CLASSIFY THESE TICKETS:
1. I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.
2. The export button stopped working after your latest update. Our reporting team is blocked.
3. Can you add approval workflows before invoices are submitted?
4. We need confirmation that our customer data is not being used to train your AI models.
5. My admin account is locked and the password reset email never arrives.
"""



#----------Case 2.2 - Few-Shot Transformation from Requirement to API Contract
FEW_SHOT_API_CONVERSION_PROMPT = """
You are an AI assistant that converts natural language requests into structured API contracts for a leave management system.

SUPPORTED ACTIONS:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

RULES:
- Do NOT invent missing information
- If unclear, set requires_clarification = true
- Never assume dates
- Ambiguous phrases like "next Friday" must be flagged
- Confidence must reflect certainty of parsing

OUTPUT FORMAT:
{
  "action": "",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "",
  "confidence": 0.0
}

---

EXAMPLES:

Input:
"I want leave from 12th June to 15th June"
Output:
{
  "action": "APPLY_LEAVE",
  "parameters": {
    "start_date": "12th June",
    "end_date": "15th June"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.95
}

Input:
"How many casual leaves do I have left?"
Output:
{
  "action": "CHECK_BALANCE",
  "parameters": {},
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.9
}

Input:
"Cancel my leave next Friday"
Output:
{
  "action": "CANCEL_LEAVE",
  "parameters": {
    "leave_date": "next Friday"
  },
  "requires_clarification": true,
  "clarification_question": "Which exact date does 'next Friday' refer to?",
  "confidence": 0.6
}

Input:
"I may take off sometime next week"
Output:
{
  "action": "APPLY_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please specify exact dates for leave request",
  "confidence": 0.4
}

---

NOW CONVERT THESE:
1. I want to take leave from 12th June to 15th June because I am travelling.
2. How many casual leaves do I have left?
3. Cancel my leave request for next Friday.
4. What is the policy for maternity leave?
5. I may take off sometime next week, not sure yet.
"""

#--------------------CHAIN OF THOUGHTS----------------------

#---------Case 3.1 - Business ROI Decision with Hidden Trade-Offs
CHAIN_OF_THOUGHT_ROI_DECISION_PROMPT = """
You are a senior business analyst evaluating an AI investment.

You must reason carefully and internally, but only output a concise reasoning summary and structured results.

CRITICAL RULES:
- Use gross profit, NOT revenue
- Apply gross margin to incremental revenue
- Subtract ALL AI-related monthly costs
- Consider 3-month implementation delay separately (no benefits during this period)
- Payback is measured ONLY after go-live
- Do NOT assume perfect adoption
- Keep reasoning summary brief (no step-by-step math shown)

BUSINESS CONTEXT:
Current monthly revenue: $2,000,000
Expected uplift: 4% to 7%
Gross margin: 40%
Implementation cost: $180,000
Monthly AI cost: $22,000 + $8,000
Implementation time: 3 months
Payback requirement: 12 months after go-live

OUTPUT FORMAT (STRICT JSON):
{
  "incremental_revenue_range": "",
  "incremental_gross_profit_range": "",
  "monthly_net_benefit_range": "",
  "payback_period_range_months": "",
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "reasoning_summary": "",
  "key_assumptions": []
}
"""

#-------Case 3.2 - Root Cause Analysis for ML Model Performance Drop
CHAIN_OF_THOUGHT_RCA_PROMPT = """
You are a senior ML engineer performing root cause analysis for production model degradation.

You must reason internally and provide only concise structured conclusions.

IMPORTANT RULES:
- Distinguish clearly between:
  - data drift
  - concept drift
  - pipeline failure
  - threshold miscalibration
- Do NOT assume pipeline failure unless evidence supports it
- Avoid generic “just retrain the model” recommendations
- Use evidence-based reasoning
- Recommend concrete diagnostics and actions

MODEL PERFORMANCE:

Before deployment:
- Precision: 0.82
- Recall: 0.76
- F1-score: 0.79

After 3 months:
- Precision: 0.61
- Recall: 0.72
- F1-score: 0.66

ADDITIONAL OBSERVATIONS:
- Transaction volume increased by 30%
- New payment channel introduced
- Fraud patterns changed after promotional campaign
- Data pipeline logs show no failed jobs
- Feature distribution for transaction_amount shifted significantly
- Model was not retrained after launch

OUTPUT FORMAT (STRICT JSON):

{
  "most_likely_causes": [],
  "evidence": [],
  "less_likely_causes": [],
  "recommended_diagnostics": [],
  "short_term_actions": [],
  "long_term_actions": [],
  "reasoning_summary": ""
}
"""

#-------------------LLM as a Judge--------------------

#-------Case 4.1 - Judging AI-Generated Customer Support Responses
LLM_JUDGE_SUPPORT_RESPONSE_PROMPT = """
You are an expert evaluator for customer support quality.

Your task is to evaluate two customer support responses using a strict scoring rubric.

SCORING RULES:
- Score each category from 1 to 5
- Do NOT prefer a response simply because it is longer
- Penalize vague, dismissive, or unhelpful answers
- Penalize responses that promise refunds without verification
- Reward empathy, accountability, appropriate escalation, and clear next steps

EVALUATION CRITERIA:
1. Empathy
2. Clarity
3. Helpfulness
4. Professionalism
5. Policy correctness

CUSTOMER MESSAGE:
"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

RESPONSE A:
"We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you."

RESPONSE B:
"I’m sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy."

OUTPUT FORMAT (STRICT JSON):
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
"""


#------------Case 4.2 - Judging Code Explanation Quality
LLM_JUDGE_CODE_EXPLANATION_PROMPT = """
You are an expert Python educator evaluating explanation quality for beginner developers.

Your task is to evaluate two explanations using a strict technical and educational rubric.

IMPORTANT RULES:
- Do NOT reward oversimplification if it becomes inaccurate
- Detect misleading technical claims
- Explain why deep copy is NOT always better
- Evaluate both beginner usefulness and technical correctness
- Scores must be from 1 to 5

EVALUATION CRITERIA:
1. Technical accuracy
2. Beginner clarity
3. Completeness
4. Misleading statements
5. Practical usefulness

QUESTION:
"What is the difference between shallow copy and deep copy in Python?"

EXPLANATION A:
"A shallow copy copies the object but keeps references to nested objects. A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and copy.deepcopy for deep copy."

EXPLANATION B:
"A shallow copy means the copied variable points to the same memory. A deep copy means everything is copied into new memory. So shallow copy is always bad and deep copy is always better."

OUTPUT FORMAT (STRICT JSON):
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
"""

#-----------------SELF CONSISTENCY-------------------

#---------Case 5.1 - Self-Consistency for Complex Policy Interpretation
SELF_CONSISTENCY_POLICY_PROMPT = """
You are evaluating an employee reimbursement claim using company policy rules.

Carefully apply all policy conditions before calculating the reimbursable amount.

IMPORTANT RULES:
- Alcohol is NEVER reimbursable
- Same-day travel (>8 hours without overnight stay) allows ONLY 50% meal reimbursement
- International travel increases meal limit by 25%
- Receipts are required above $25 and ARE provided
- Apply policy rules carefully and consistently
- Return concise reasoning only

POLICY:
- Meal reimbursement limit: $60/day
- International travel: +25% limit increase
- Same-day travel (>8 hours, no overnight): only 50% reimbursement allowed

CLAIM:
- Travel: India to Singapore
- Duration: 14 hours
- Same-day travel
- Meal expense: $70
- Alcohol included: $12
- Receipts provided

OUTPUT FORMAT (STRICT JSON):
{
  "reimbursable_amount": 0,
  "reasoning_summary": ""
}
"""

#----------Case 5.2 - Self-Consistency for Logical Deduction

SELF_CONSISTENCY_SECURITY_PROMPT2 = """
You are a cybersecurity risk analyst.

Apply the rules exactly as written.

RULES:
1. HIGH risk requires BOTH:
   - login from a NEW country
   - more than 5 downloaded files

2. MEDIUM risk requires BOTH:
   - login outside business hours
   - at least one MFA failure

3. CRITICAL risk requires BOTH HIGH and MEDIUM conditions.

4. Business hours are 9 AM to 6 PM local time.

5. A known VPN country is NOT considered a new country.

USER ACTIVITY:
- User: Asha
- Login time: 8:15 PM local time
- Login country: Germany
- Known countries: India, Germany
- Known VPN countries: Germany, Netherlands
- Files downloaded: 8
- MFA failures: 1

IMPORTANT INSTRUCTIONS:
- Germany is already a known country.
- More than 5 downloads ALONE does not create HIGH risk.
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT explain step-by-step reasoning.
- Keep reasoning_summary short and concise.

OUTPUT FORMAT:
{
  "risk_level": "",
  "reasoning_summary": ""
}
"""


#-------------------TREE OF THOUGHTS-----------------

#--------Case 6.1 - Selecting the Best AI Automation Use Case
TREE_OF_THOUGHT_USE_CASE_PROMPT = """
You are an AI strategy consultant helping select ONE best 90-day AI pilot.

You must evaluate all options independently before selecting.

OPTIONS:
1. AI customer support assistant
2. AI sales proposal generator
3. AI contract risk analyzer
4. AI HR policy assistant

EVALUATION CRITERIA (score 1-5):
- business_value_score
- feasibility_score
- risk_score (higher score = LOWER risk)
- pilot_suitability_score
- adoption_score

RULES:
- Do NOT choose based only on business value
- Penalize high-risk and high-complexity systems
- Prefer feasible 90-day MVPs
- Consider data sensitivity carefully
- Explicitly compare trade-offs

OUTPUT FORMAT (STRICT JSON):
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
"""

#----------Case 6.2 - Tree-of-Thought Architecture Selection

TREE_OF_THOUGHT_ARCHITECTURE_PROMPT = """
You are a senior AI system architect.

You must evaluate 4 architecture options for a document QA system:

OPTIONS:
A. Simple RAG with vector DB + LLM API
B. Fine-tune open-source LLM on documents
C. Keyword search only
D. Agentic multi-step RAG with reranking + citation verification

EVALUATION CRITERIA (score 1-5):
- accuracy
- cost efficiency
- privacy safety
- 6-week MVP feasibility
- scalability
- citation reliability

RULES:
- Penalize fine-tuning if documents change frequently
- Do NOT choose the most complex system by default
- MVP must be deliverable in 6 weeks
- Prefer balanced architecture over overengineering
- Consider phased rollout

OUTPUT FORMAT (STRICT JSON):
{
  "architecture_scores": [
    {
      "option": "",
      "scores": {},
      "overall_score": 0,
      "risks": [],
      "mitigations": []
    }
  ],
  "recommended_architecture": "",
  "implementation_rationale": "",
  "risks": [],
  "mitigations": [],
  "mvp_plan": []
}
"""

#---------------REPHRASE AND RESPOND-------------------

#---------Case 7.1 - Ambiguous Business Request Rewriting
REPHRASE_AND_RESPOND_BUSINESS_PROMPT = """
You are a business analyst and AI solution architect.

TASK:
1. Rephrase the vague business request into a clear, measurable problem statement.
2. Then propose a practical AI solution.

IMPORTANT RULES:
- Do NOT keep vague language like "improve productivity"
- Convert it into measurable outcomes
- Do NOT assume hidden requirements
- Keep solution realistic (not enterprise transformation fantasy)

BUSINESS REQUEST:
We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility.

OUTPUT FORMAT (STRICT JSON):
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

#-----------Case 7.2 - Rephrase and Respond for Poorly Written Technical Requirement
REPHRASE_AND_RESPOND_TECH_PROMPT = """
You are a senior software architect.

TASK:
Convert a vague product requirement into a clear technical specification.

IMPORTANT RULES:
- Define missing requirements explicitly
- Replace vague terms like "fast", "secure", "properly" with measurable criteria
- Do NOT assume unknown constraints
- Provide realistic architecture direction

REQUIREMENT:
Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers.

OUTPUT FORMAT (STRICT JSON):
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