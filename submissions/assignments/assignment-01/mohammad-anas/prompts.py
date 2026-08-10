#---------------------------------------------------------------
# Case 1.1 - Zero-Shot Risk Classification for Vendor Onboarding
#---------------------------------------------------------------

zero_shot_vendor_prompt="""
You are a vendor risk assesment expert.

Your task is to classify the vendor into one of the risk levels : LOW, MEDIUM, HIGH, CRITICAL.

You have i=to carefully analyze the vendor informations.

You must identiy these risk:
1 - Privacy risk.
2- Compliance risk.
3- Operational Risk.
4- Vendor Maturity Risk.
5- Pricing Risk.

Avoid generic procurement language.

Return output in this json format:

{
 "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
 "key_risk_factors": [],
 "missing_information": [],
 "business_recommendation": "",
 "confidence_score": 0.0
}

Vendor Details:

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
The business team wants to use this vendor for processing supplier invoices and purchase
 contracts.

"""

#--------------------------------------------------------------
# Case 1.2 - Zero-Shot Executive Decision Memo
#--------------------------------------------------------------

zero_shot_executive_prompt="""
You are an Executive AI busu=iness Advisor.

Your task is to generate an executive decesion memo.

You have to choose one decesoin:

APPROVE, 
REJECT, 
APPROVE_WITH_CONDITIONS.

The output must be decesion-oriented, not a summary.

You Must include:
1- Governance Considerations.
2- Compiliance Considerations.
3- ROI Considerations.
4- Change Management Considerations.

Don't overpromise automation advantages.

Return output in this json format:

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
A Chief Operating Officer wants a decision memo based on this situation:
The company currently handles customer support through a team of 120 human agents. Ticket
 volume has grown by 45% in the last 8 months. Average response time has increased from 3
 hours to 11 hours.
The AI team proposes deploying a GenAI chatbot for first-level support. It can answer FAQs,
 summarize customer issues, and create draft responses for agents. The estimated
 implementation cost is $250,000, with ongoing monthly cost of $30,000.
The compliance team is concerned because customer support tickets may contain personal
Page 4
Prompt Engineering Evaluation - Participant Workbook
 information. The support team is worried about job losses. The CTO believes the chatbot can
 reduce ticket load by 35%. The CFO wants payback within 12 months.
 The company has not yet implemented AI governance policies.

"""

#--------------------------------------------------------------
# Case 2.1 - Few-Shot Customer Ticket Intent Classification
#--------------------------------------------------------------

few_shot_ticket_prompt="""
You are a customer support ticket classifier.

Your task is to classify the customer support tickets.

Possible Categories:
1- BILLING_ISSUE
2- TECHNICAL_BUG
3- ACCOUNT_ACCESS
4- FEATURE_REQUEST
5- COMPLIANCE_CONCERN   
6- ESCALATION_RISK

You must learn from the examples below.

Example 1:
Ticket:
"I was charged twice for my subscription.
Output:
{
    "ticket" : "I was charged twice for my subscription.",
    "category": "Billing Issue",
    "priority": "MEDIUM",
    "justification": "Customer reports billing/payment problem."
}
Example 2:
{
    "ticket" : "The export button is not working.",
    "category": "Technical Problem",
    "priority": "HIGH",
    "justification": "Customer reports technical issue."
}
Example 3:
{
    "ticket" : "I can't log into my account.",
    "category": "Account Access",
    "priority": "HIGH",
    "justification": "Customer reports account access problem."
}
Example 4:
{
    "ticket" : "We need confirmation that our customer data is not being used to train your AI models.",
    "category": "Compliance Concern",
    "priority": "HIGH",
    "justification": "Customer reports compliance concern."
}

Example 5:
{
    "ticket" : "Can you add approval workflows before invoices are submitted?", 
    "category": "Feature Request",
    "priority": "MEDIUM",
    "justification": "Customer requests new feature."
}
Rules:

- Angry tone may increase priority.
- Billing issues are usually medium priority unless they involve large sums.
- Distinguish compliance concern from technical issue.

Return only vlid json Schema:

 {
 "ticket": "",
 "category": "",
 "priority": "LOW | MEDIUM | HIGH | URGENT",
 "justification": ""
 }

Now classify these ticket:

1. I was charged twice this month and your support team has not replied for five days. I am
 going to post this on social media if this is not fixed today.
2. The export button stopped working after your latest update. Our reporting team is blocked.
3. Can you add approval workflows before invoices are submitted?
4. We need confirmation that our customer data is not being used to train your AI models.
5. My admin account is locked and the password reset email never arrives.

"""

#---------------------------------------------------------------------
# Case 2.2 - Few-Shot Transformation from Requirement to API Contract
#---------------------------------------------------------------------

few_shot_api_prompt = """
You are an AI K=leave management assistant.

Your task is to transform the following requirement into an API contract.

Supported Actions:
APPLY_LEAVE
CHECK_BALANCE
CANCEL_LEAVE
GET_POLICY

Learn from the examples below.

Example 1:
User: 
"I want to apply for leave from September 1st to September 5th."
Output: {
    "action": "APPLY_LEAVE",
    "parameters": {
        "start_date": "1st September",
        "end_date": "5th September",
        "reason": travelling
    },
    "requires_clarification": false,
    "clarification_questions": "",
    "confidence": 0.95
}

Example 2:
User:
"How many leave days do I have left this year?"
Output: {
    "action": "CHECK_BALANCE",
    "parameters": {
    "leave_type": "casual"
    },
    "requires_clarification": false,
    "clarification_questions": "",
    "confidence": 0.9
}
Example 3:
User:
"I need to cancel my leave for next week." 
Output: {
    "action": "CANCEL_LEAVE",
    "parameters": {
        "leave_id": "12345"
    },
    "requires_clarification": false,
    "clarification_questions": "",
    "confidence": 0.92
}
Example 4:
User:
"What is the company's policy on sick leave?"
Output: {
    "action": "GET_POLICY",
    "parameters": {
        "leave_type": "sick"
    },
    "requires_clarification": false,
    "clarification_questions": "",
    "confidence": 0.88
}

Rules:
- Do Not invent days.
- Do not envent leave tpees.
If infirmation is missing, set queries_clarificaton to true.
- Handle ambigious dates carefully.

return only valid json schema:

{
 "action": "",
 "parameters": {},
 "requires_clarification": true,
 "clarification_question": "",
 "confidence": 0.0
}

Example user messages:
1. I want to take leave from 12th June to 15th June because I am travelling.
2. How many casual leaves do I have left?
3. Cancel my leave request for next Friday.
4. What is the policy for maternity leave?
5. I may take off sometime next week, not sure yet.

"""

#---------------------------------------------------------------------
# Case 3.1 - Business ROI Decision with Hidden Trade-Offs
#---------------------------------------------------------------------

cot_roi_prompt = """
You are a senior business analyst.

Reason carefully and privately before answering.

Do not reveal full chain of thought.

Return only a concise reasoning summary and final answer.

Task:
Determine whether this AI recommendation engine project should be approved.

Scenario:

A retail company wants to deploy an AI recommendation engine.

Current monthly revenue: $2,000,000

Expected revenue uplift from recommendations:
3% to 7%

Implementation cost:
$180,000 one-time

Monthly AI infrastructure cost:
$22,000

Monthly maintenance cost:
$8,000

Gross margin:
40%

Expected implementation time:
3 months

Leadership requires payback within 12 months after go-live.

Important rules:
- Perform numerical reasoning.
- Use gross margin, NOT revenue, for payback.
- Subtract monthly AI operating costs.
- Consider implementation time separately.

Return ONLY valid JSON.

Required JSON Schema:

{
    "incremental_revenue_range": "",
    "incremental_gross_profit_range": "",
    "monthly_net_benefit_range": "",
    "payback_period_range_months": "",
    "decision": "",
    "reasoning_summary": "",
    "key_assumptions": []
}
"""

#---------------------------------------------------------------------
# Case 3.2 - Root Cause Analysis for ML Model Performance Drop
#---------------------------------------------------------------------

cot_ml_root_cause_prompt = """
You are a machine learning diagnostics expert.

Reason carefully and privately.

Do not reveal hidden reasoning.

Return only concise reasoning summary and structured output.

Scenario:

A fraud detection model degraded after deployment.

Before deployment:
Precision: 0.82
Recall: 0.76
F1-score: 0.79

After 3 months:
Precision: 0.61
Recall: 0.72
F1-score: 0.66

Additional observations:

- Transaction volume increased by 30%
- A new payment channel was introduced
- Fraud patterns changed after a promotional campaign
- Data pipeline logs show no failed jobs
- Feature distribution for transaction_amount shifted significantly
- Model was not retrained after launch

Rules:
- Distinguish between data drift, concept drift,
pipeline failure, and threshold miscalibration.
- Do not claim pipeline failure just because performance dropped.
- Recommend concrete diagnostics.
- Avoid generic retrain-only answers.

Return ONLY valid JSON.

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
"""

#---------------------------------------------------------------------
# Case 4.1 - Judging AI-Generated Customer Support Responses
#---------------------------------------------------------------------

llm_judge_support_prompt = """
You are an expert evaluator for customer support quality.

Your task is to judge two responses using a clear rubric.

Customer Question:

"I was charged for a premium plan even though
I cancelled last month.

I already contacted support twice and no one responded.

I want a refund immediately."

Response A:

"We are sorry for the inconvenience.
Please check your billing settings and make sure your cancellation was completed.
Refunds are subject to our policy.
Thank you."

Response B:

"I am sorry this has been frustrating,
especially after you contacted support twice.

I can help escalate this as a billing issue.

Please share your invoice ID or account email
so the team can verify the cancellation date
and refund eligibility.

If the duplicate charge is confirmed,
we will process the refund according to policy."

Evaluation Rules:
- Score from 1 to 5
- Do not prefer longer responses automatically
- Check whether the response promises refund without verification
- Penalize vague or dismissive responses

Return ONLY valid JSON.

Required JSON Schema:

{
    "response_a": {
        "score": 0,
        "strengths": [],
        "weaknesses": []
    },

    "response_b": {
        "score": 0,
        "strengths": [],
        "weaknesses": []
    },

    "winner": "",
    "judge_reasoning_summary": ""
}
"""



#---------------------------------------------------------------------
# Case 4.2 - Judging Code Explanation Quality
#---------------------------------------------------------------------


llm_judge_python_prompt = """
You are a technical evaluator.

Your task is to judge which explanation is better
for a beginner developer.

Question:

"What is the difference between shallow copy
and deep copy in Python?"

Explanation A:

"A shallow copy copies the object
but keeps references to nested objects.

A deep copy recursively copies nested objects too.

Use copy.copy for shallow copy
and copy.deepcopy for deep copy."

Explanation B:

"A shallow copy means the copied variable points
to the same memory.

A deep copy means everything is copied into new memory.

So shallow copy is always bad
and deep copy is always better."

Evaluation Rules:
- Detect technically misleading claims
- Do not reward oversimplification if inaccurate
- Explain why deep copy is NOT always better
- Scores should reflect beginner usefulness
and technical accuracy

Return ONLY valid JSON.

Required JSON Schema:

{
    "explanation_a": {
        "scores": [],
        "issues": [],
        "overall_score": 0
    },

    "explanation_b": {
        "scores": [],
        "issues": [],
        "overall_score": 0
    },

    "winner": "",
    "judge_reasoning_summary": ""
}
"""

#---------------------------------------------------------------------
# Case 5.1 - Self-Consistency for Complex Policy Interpretation
#---------------------------------------------------------------------


self_consistency_policy_prompt = """
You are an expert policy interpretation assistant.

Analyze the reimbursement policy carefully.

Policy:
- Employees can claim reimbursement for business travel meals up to $60 per day.
- Alcohol is not reimbursable.
- If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.
- For international travel, the daily limit increases by 25%.
- Receipts are mandatory for claims above $25.

Employee claim:
- Employee traveled from India to Singapore for a same-day business meeting.
- Travel duration: 14 hours
- Meal expenses submitted: $70
- Includes $12 alcohol
- Receipts provided

Run independent reasoning and return only valid JSON.

Output Schema:
{
    "individual_answers": [],
    "final_reimbursable_amount": 0,
    "consistency_count": {},
    "final_decision": "",
    "reasoning_summary": ""
}

Constraints:
- Apply same-day travel rule.
- Apply international uplift.
- Exclude alcohol.
- Do not exceed reimbursement limits.
- Think carefully before deciding.
"""

# ==========================
# CASE 5.2 - SELF CONSISTENCY
# ==========================

self_consistency_security_prompt = """
You are a cybersecurity risk analysis assistant.

Security rules:
1. If a user logs in from a new country and downloads more than 5 files, flag HIGH risk.
2. If a user logs in outside business hours and fails MFA once, flag MEDIUM risk.
3. If both HIGH and MEDIUM are true, escalate to CRITICAL.
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

Return only valid JSON.

Output Schema:
{
    "runs": [],
    "risk_level_votes": {},
    "final_risk_level": "",
    "disagreement_analysis": "",
    "final_reasoning_summary": ""
}

Constraints:
- Germany is already known.
- Germany is also a known VPN country.
- More than 5 downloads alone does NOT trigger HIGH risk.
- Carefully analyze business hours + MFA.
"""

# ==========================
# CASE 6.1 - TREE OF THOUGHT
# ==========================

tree_of_thought_usecase_prompt = """
You are an executive AI strategy advisor.

Evaluate all AI automation options carefully.

Option 1: AI customer support assistant
- High ticket volume
- Moderate implementation complexity
- Contains personal customer data
- Potential cost savings: high
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
- Requires strong accuracy and traceability
- User adoption risk: medium

Option 4: AI internal HR policy assistant
- High employee usage
- Medium sensitivity
- Low implementation complexity
- Potential cost savings: medium
- User adoption risk: low

Evaluate each option across:
- business value
- feasibility
- risk
- 90-day pilot suitability
- adoption

Return only JSON.

Output Schema:
{
    "options_evaluated": [],
    "recommended_option": "",
    "why_not_others": [],
    "final_recommendation": ""
}

Constraints:
- Scores must be from 1 to 5.
- Lower risk gets higher score.
- Do not select only on business value.
- Explicitly compare trade-offs.
"""

# ==========================
# CASE 6.2 - TREE OF THOUGHT
# ==========================

tree_of_thought_architecture_prompt = """
You are an AI systems architect.

Startup requirements:
- Users upload PDF documents.
- Users ask questions about uploaded documents.
- System must show source citations.
- Initial users: 500
- Expected growth: 20,000 users in 12 months
- Budget is limited.
- Documents contain confidential business information.
- Accuracy matters.
- MVP must launch in 6 weeks.

Architecture options:

Option A:
Simple RAG using vector database and hosted LLM API

Option B:
Fine-tune an open-source LLM on all documents

Option C:
Keyword search only without LLM

Option D:
Multi-step retrieval with query rewriting, reranking, and citation verification

Evaluate across:
- accuracy
- cost
- privacy
- timeline
- scalability
- citation reliability

Return valid JSON only.

Output Schema:
{
    "architecture_scores": [],
    "recommended_architecture": "",
    "implementation_rationale": "",
    "risks": [],
    "mitigations": [],
    "mvp_plan": []
}

Constraints:
- Penalize fine-tuning if documents change frequently.
- Respect 6-week timeline.
- Do not blindly choose most complex option.
- Consider phased approach.
"""

# ==========================
# CASE 7.1 - REPHRASE & RESPOND
# ==========================

rephrase_business_prompt = """
You are an AI business consultant.

Stakeholder request:
'We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility.'

First rephrase the vague request into a clearer business problem.

Then propose a realistic AI solution.

Return valid JSON only.

Output Schema:
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

Constraints:
- Avoid generic response.
- Convert vague language into measurable outcomes.
- Define productivity and visibility.
- Suggest realistic AI use case.
"""


# ==========================
# CASE 7.2 - REPHRASE & RESPOND
# ==========================

rephrase_technical_prompt = """
You are a senior software architect.

Poor technical requirement:

'Create an AI feature where users upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers.'

Rephrase this into a clear technical requirement.

Then provide an implementation proposal.

Return valid JSON only.

Output Schema:
{
    "rephrased_requirement": "",
    "functional_requirements": [],
    "non_functional_requirements": [],
    "security_requirements": [],
    "acceptance_criteria": [],
    "recommended_solution_approach": "",
    "open_questions": []
}

Constraints:
- Identify missing details.
- Define measurable meaning of secure, fast, properly.
- Recommend practical system design.
- Avoid unrealistic promise of never giving wrong answers.
"""