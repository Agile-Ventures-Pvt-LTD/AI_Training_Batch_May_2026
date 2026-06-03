zero_shot_exec_decision_prompt = """
You are an executive advisor. Generate a decision memo for the COO based on the scenario below.

Required Output Schema:
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

Constraints:
- No examples in the prompt (zero-shot).
- The output must be decision-oriented, not a summary.
- Must include governance, compliance, ROI, and change-management considerations.
- Must not overpromise automation benefits.

Scenario:
The company currently handles customer support through a team of 120 human agents. Ticket volume has grown by 45% in the last 8 months. Average response time has increased from 3 hours to 11 hours.

The AI team proposes deploying a GenAI chatbot for first-level support. It can answer FAQs, summarize customer issues, and create draft responses for agents. The estimated implementation cost is $250,000, with ongoing monthly cost of $30,000.

The compliance team is concerned because customer support tickets may contain personal information. The support team is worried about job losses. The CTO believes the chatbot can reduce ticket load by 35%. The CFO wants payback within 12 months. The company has not yet implemented AI governance policies.

Task:
Produce a structured executive decision memo in the JSON schema above.
"""

zero_shot_vendor_risk_prompt = """
You are a risk analyst. Classify the vendor into LOW, MEDIUM, HIGH, or CRITICAL risk based on the scenario below.

Required Output Schema:
{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": [],
  "missing_information": [],
  "business_recommendation": "",
  "confidence_score": 0.0
}

Constraints:
- No examples in the prompt (zero-shot).
- Use only clear instructions, decision criteria, and output schema.
- Identify privacy, compliance, operational, pricing, and vendor maturity risks.
- Avoid generic procurement language.
- Confidence score should be between 0.0 and 1.0.

Scenario:
A company is onboarding a new AI-based document processing vendor.

Vendor: DocuMind AI
- Solution processes invoices, contracts, and identity documents using OCR and LLM-based extraction.
- Hosted in a multi-tenant cloud environment.
- No region-specific data residency currently; planned for next year.
- Supports encryption at rest and in transit.
- Customer data may be used for product improvement unless customers opt out manually.
- SOC 2 Type I certification, but not Type II.
- Uptime SLA: 99.5%.
- Pricing is usage-based and could increase significantly with volume growth.
- APIs provided, but rate limits not clearly documented.
- Operating for 18 months with 12 enterprise customers.
- Business team wants to use this vendor for processing supplier invoices and purchase contracts.

Task:
Produce a structured risk classification in the JSON schema above.
"""

few_shot_leave_prompt = """
You are an assistant that converts natural language leave management requests into structured API payloads.

Supported actions:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

Return ONLY valid JSON in this schema:
{
  "action": "",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "",
  "confidence": 0.0
}

Guidelines:
- Do not invent dates or leave types.
- If information is missing, set requires_clarification to true and provide a clarification_question.
- Ambiguous dates like "next Friday" or "sometime next week" must be flagged for clarification.
- Confidence should be between 0.0 and 1.0.

Examples:

User: "I want to take leave from 12th June to 15th June because I am travelling."
Output: {
  "action": "APPLY_LEAVE",
  "parameters": {"start_date": "2024-06-12", "end_date": "2024-06-15", "reason": "travelling"},
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.95
}

User: "How many casual leaves do I have left?"
Output: {
  "action": "CHECK_BALANCE",
  "parameters": {"leave_type": "casual"},
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.9
}

User: "Cancel my leave request for next Friday."
Output: {
  "action": "CANCEL_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Which exact date is 'next Friday'?",
  "confidence": 0.7
}

User: "What is the policy for maternity leave?"
Output: {
  "action": "GET_POLICY",
  "parameters": {"leave_type": "maternity"},
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.9
}

User: "I may take off sometime next week, not sure yet."
Output: {
  "action": "APPLY_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please specify exact start and end dates.",
  "confidence": 0.6
}

Now convert the following user requests into structured API contracts:
1. I want to take leave from 12th June to 15th June because I am travelling.
2. How many casual leaves do I have left?
3. Cancel my leave request for next Friday.
4. What is the policy for maternity leave?
5. I may take off sometime next week, not sure yet.
"""

#########################################################################
Few_Shot_Customer_Risk_Prompt="""
A company receives customer support tickets. The model must classify each ticket into one
 category:
BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS, FEATURE_REQUEST, COMPLIANCE_CONCERN,
 ESCALATION_RISK
Test tickets:
1. I was charged twice this month and your support team has not replied for five days. I am
 going to post this on social media if this is not fixed today.
2. The export button stopped working after your latest update. Our reporting team is blocked.
3. Can you add approval workflows before invoices are submitted?
4. We need confirmation that our customer data is not being used to train your AI models.
5. My admin account is locked and the password reset email never arrives.

Task
Write a few-shot prompt using at least five examples that teaches the model how to classify tickets.
Page 5
Prompt Engineering Evaluation - Participant Workbook
Required Output Schema
[
 {
 "ticket": "",
 "category": "",
 "priority": "LOW | MEDIUM | HIGH | URGENT",
 "justification": ""
 }
]
Constraints
 Include examples with ambiguity.
 Teach that angry tone can increase priority but does not automatically change category.
 Distinguish compliance concern from technical bug.
 Distinguish feature request from billing issue.
"""

Few_Shot_Transformation = """Participants are building a simple AI-powered leave management assistant. The assistant
 receives natural language requests and converts them into API payloads.
Supported actions:
APPLY_LEAVE, CHECK_BALANCE, CANCEL_LEAVE, GET_POLICY
Example user messages:
1. I want to take leave from 12th June to 15th June because I am travelling.
2. How many casual leaves do I have left?
3. Cancel my leave request for next Friday.
4. What is the policy for maternity leave?
5. I may take off sometime next week, not sure yet.

Required Output Schema
{
 "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
 "rationale": "",
 "financial_considerations": [],
 "operational_considerations": [],
 "people_impact": [],
 "compliance_risks": [],
 "conditions_for_approval": []"""


Few_Shot_Customer_Ticket_Prompt_Intent = """
A company receives customer support tickets. The model must classify each ticket into one
 category:
BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS, FEATURE_REQUEST, COMPLIANCE_CONCERN,
 ESCALATION_RISK
Test tickets:
1. I was charged twice this month and your support team has not replied for five days. I am
 going to post this on social media if this is not fixed today.
2. The export button stopped working after your latest update. Our reporting team is blocked.
3. Can you add approval workflows before invoices are submitted?
4. We need confirmation that our customer data is not being used to train your AI models.
5. My admin account is locked and the password reset email never arrives.
Task
Write a few-shot prompt using at least five examples that teaches the model how to classify tickets.
Page 5
Prompt Engineering Evaluation - Participant Workbook
Required Output Schema
[
 {
 "ticket": "",
 "category": "",
 "priority": "LOW | MEDIUM | HIGH | URGENT",
 "justification": ""
 }
]
Constraints
 Include examples with ambiguity.
 Teach that angry tone can increase priority but does not automatically change category.
 Distinguish compliance concern from technical bug.
 Distinguish feature request from billing issue.
"""

Few_Shot_Transformation = '''Scenario
Participants are building a simple AI-powered leave management assistant. The assistant
 receives natural language requests and converts them into API payloads.
Supported actions:
APPLY_LEAVE, CHECK_BALANCE, CANCEL_LEAVE, GET_POLICY
Example user messages:
1. I want to take leave from 12th June to 15th June because I am travelling.
2. How many casual leaves do I have left?
3. Cancel my leave request for next Friday.
4. What is the policy for maternity leave?
5. I may take off sometime next week, not sure yet.
Task
Create a few-shot prompt that converts each user request into a structured API contract.
Required Output Schema
{
 "action": "",
 "parameters": {},
 "requires_clarification": true,
 "clarification_question": "",
 "confidence": 0.0
}
Constraints
 Provide examples for valid and incomplete requests.
 The model must not invent dates or leave types.
 If information is missing, set requires_clarification to true.
 Ambiguous dates such as next Friday or sometime next week must be handled carefull'''

few_shot_ticket_prompt_new = """
You are a support ticket classifier. Classify each ticket into one of:
BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS, FEATURE_REQUEST, COMPLIANCE_CONCERN, ESCALATION_RISK.

Return ONLY valid JSON in this schema:
[
  {
    "ticket": "",
    "category": "",
    "priority": "LOW | MEDIUM | HIGH | URGENT",
    "justification": ""
  }
]

Guidelines:
- Angry tone can increase priority but does not change category.
- Distinguish COMPLIANCE_CONCERN from TECHNICAL_BUG.
- Distinguish FEATURE_REQUEST from BILLING_ISSUE.
- Include justification for category and priority.

Examples:
Ticket: "I was charged twice last month and no one replied."
Output: {"ticket":"...","category":"BILLING_ISSUE","priority":"URGENT","justification":"Double charge + delay + escalation risk"}

Ticket: "Export button stopped working after update."
Output: {"ticket":"...","category":"TECHNICAL_BUG","priority":"HIGH","justification":"Critical feature broken"}

Ticket: "Can you add approval workflows before invoices are submitted?"
Output: {"ticket":"...","category":"FEATURE_REQUEST","priority":"MEDIUM","justification":"New functionality request"}

Ticket: "We need confirmation that our customer data is not being used to train your AI models."
Output: {"ticket":"...","category":"COMPLIANCE_CONCERN","priority":"HIGH","justification":"Privacy concern"}

Ticket: "My admin account is locked and reset email never arrives."
Output: {"ticket":"...","category":"ACCOUNT_ACCESS","priority":"HIGH","justification":"Access blocked"}

Now classify the following test tickets:
1. I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.
2. The export button stopped working after your latest update. Our reporting team is blocked.
3. Can you add approval workflows before invoices are submitted?
4. We need confirmation that our customer data is not being used to train your AI models.
5. My admin account is locked and the password reset email never arrives.
"""


chain_of_thought_roi_prompt = """
You are a financial analyst. Read the scenario and determine whether the AI recommendation project should be approved. 
Perform numerical reasoning step by step privately, but return ONLY the final structured JSON output.

Required Output Schema:
{
  "incremental_revenue_range": "",
  "incremental_gross_profit_range": "",
  "monthly_net_benefit_range": "",
  "payback_period_range_months": "",
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "reasoning_summary": "",
  "key_assumptions": []
}

Guidelines:
- Use gross margin, not revenue, for payback.
- Subtract monthly AI operating costs (infrastructure + maintenance).
- Consider implementation time separately from payback after go-live.
- Do not overpromise; provide ranges where applicable.

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

Task:
Perform reasoning privately, then output only the JSON schema filled with values and a concise reasoning summary.
"""

chain_of_thought_root_cause_prompt = """
You are a machine learning reliability analyst. Read the scenario and generate a structured root cause analysis.
Perform reasoning step by step privately, but return ONLY the final JSON output in this schema:

{
  "most_likely_causes": [],
  "evidence": [],
  "less_likely_causes": [],
  "recommended_diagnostics": [],
  "short_term_actions": [],
  "long_term_actions": [],
  "reasoning_summary": ""
}

Constraints:
- Distinguish between data drift, concept drift, pipeline failure, and threshold miscalibration.
- Do not claim pipeline failure just because performance dropped.
- Recommend concrete diagnostics (e.g., distribution checks, retraining experiments, threshold tuning).
- Avoid generic "just retrain" answers.

Scenario:
A fraud detection model has degraded after deployment.

Before deployment:
Precision: 0.82
Recall: 0.76
F1-score: 0.79

After 3 months:
Precision: 0.61
Recall: 0.72
F1-score: 0.66

Additional observations:
- Transaction volume increased by 30%.
- A new payment channel was introduced.
- Fraud patterns changed after a promotional campaign.
- Data pipeline logs show no failed jobs.
- Feature distribution for transaction_amount shifted significantly.
- Model was not retrained after launch.

Task:
Perform structured reasoning privately, then output only the JSON schema filled with values and a concise reasoning summary.
"""

llm_judge_support_prompt = """
You are an impartial evaluator. Judge the quality of AI-generated customer support responses.

Customer question:
"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

Response A:
"We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you."

Response B:
"I'm sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy."

Return ONLY valid JSON in this schema:
{
  "response_a": {"scores": {}, "strengths": [], "weaknesses": []},
  "response_b": {"scores": {}, "strengths": [], "weaknesses": []},
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}

Constraints:
- Judge scores from 1 to 5.
- Do not prefer a response only because it is longer.
- Check whether the response promises a refund without verification.
- Penalize vague or dismissive answers.
- Highlight strengths and weaknesses clearly.

Task:
Evaluate both responses according to these rules and output only the JSON schema filled with values.
"""

llm_judge_code_explanation_prompt = """
You are an impartial evaluator. Judge the quality of two AI-generated explanations for a junior developer question.

Question:
"What is the difference between shallow copy and deep copy in Python?"

Explanation A:
"A shallow copy copies the object but keeps references to nested objects. A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and copy.deepcopy for deep copy."

Explanation B:
"A shallow copy means the copied variable points to the same memory. A deep copy means everything is copied into new memory. So shallow copy is always bad and deep copy is always better."

Return ONLY valid JSON in this schema:
{
  "explanation_a": {"scores": {}, "issues": [], "overall_score": 0},
  "explanation_b": {"scores": {}, "issues": [], "overall_score": 0},
  "winner": "",
  "judge_reasoning_summary": ""
}

Constraints:
- Detect technically misleading claims.
- Do not reward oversimplification if it becomes inaccurate.
- Explain why deep copy is not always better.
- Scores should reflect beginner usefulness and technical accuracy.
- Provide clear issues for each explanation.
- Select a winner or TIE based on rubric.

Task:
Evaluate both explanations according to these rules and output only the JSON schema filled with values.
"""


self_consistency_policy_prompt = """
You are a reimbursement policy evaluator. Use self-consistency prompting to calculate the reimbursable amount.
Run at least five independent reasoning paths internally, then output only the final structured JSON.

Required Output Schema:
{
  "individual_answers": [],
  "final_reimbursable_amount": 0,
  "consistency_count": {},
  "final_decision": "",
  "reasoning_summary": ""
}

Constraints:
- Run at least five independent model calls internally.
- Extract the reimbursable amount from each reasoning path.
- Select the majority or most consistent answer.
- Alcohol must be excluded from reimbursement.
- Apply both international uplift (+25%) and same-day travel rule (50% of daily limit).
- Receipts are mandatory for claims above $25.

Scenario:
Organization reimbursement policy:
- Employees can claim reimbursement for business travel meals up to $60 per day.
- Alcohol is not reimbursable.
- If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.
- For international travel, the daily meal limit increases by 25%.
- Receipts are mandatory for claims above $25.

Employee claim:
- Travel: India to Singapore for a same-day business meeting.
- Total travel duration: 14 hours.
- Submitted meal expenses: $70, including $12 for alcohol.
- Receipts were provided.

Task:
Perform self-consistency reasoning privately, then output only the JSON schema filled with values and a concise reasoning summary.
"""

self_consistency_risk_prompt = """
You are a security risk evaluator. Use self-consistency prompting to determine the final risk classification.
Run at least five independent reasoning paths internally, then output only the final structured JSON.

Required Output Schema:
{
  "runs": [],
  "risk_level_votes": {},
  "final_risk_level": "",
  "disagreement_analysis": "",
  "final_reasoning_summary": ""
}

Constraints:
- Run at least five independent model calls internally.
- Germany is a known country and also a known VPN country, so it is NOT treated as new.
- More than five downloads alone does not satisfy HIGH risk unless combined with a new country condition.
- Login is outside business hours (after 6 PM) and MFA failed once → MEDIUM risk condition is satisfied.
- If both HIGH and MEDIUM conditions are true, escalate to CRITICAL.
- Provide clear disagreement analysis if runs differ.

Scenario:
User activity:
- User: Asha
- Login time: 8:15 PM local time
- Login country: Germany
- Known countries: India, Germany
- Known VPN countries: Germany, Netherlands
- Files downloaded: 8
- MFA failures: 1

Rules:
1. If a user logs in from a new country and downloads more than 5 files, flag as HIGH risk.
2. If a user logs in outside business hours and fails MFA once, flag as MEDIUM risk.
3. If both HIGH and MEDIUM conditions are true, escalate to CRITICAL.
4. Business hours are 9 AM to 6 PM local time.
5. A known VPN country should not be treated as a new country.

Task:
Perform self-consistency reasoning privately, then output only the JSON schema filled with values and a concise reasoning summary.
"""

tree_of_thought_use_case_prompt = """
You are a strategic advisor. Use a tree-of-thought approach to evaluate each AI automation option across multiple dimensions.
Perform reasoning step by step privately, but return ONLY the final structured JSON.

Required Output Schema:
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

Constraints:
- Scores should be from 1 to 5.
- Lower risk should receive a higher risk score.
- Do not choose only on business value.
- Explicitly compare trade-offs.
- Pilot suitability should reflect feasibility within 90 days.

Scenario:
A company wants to select one AI automation use case for a 90-day pilot.

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

Task:
Perform tree-of-thought reasoning privately, then output only the JSON schema filled with values and a concise recommendation.
"""


tree_of_thought_architecture_prompt = """
You are a solution architect. Use a tree-of-thought approach to evaluate architecture options for an AI document question-answering system.
Perform reasoning step by step privately, but return ONLY the final structured JSON.

Required Output Schema:
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
- Do not choose the most complex option blindly.
- Respect the 6-week MVP timeline.
- Consider a phased approach.
- Scores should be from 1 to 5.

Scenario:
A startup wants to build an AI document question-answering system.

Requirements:
- Users upload PDF documents.
- Users ask questions about uploaded documents.
- The system must show source citations.
- Initial users: 500
- Expected growth: 20,000 users in 12 months
- Budget is limited.
- Documents may contain confidential business information.
- Accuracy is more important than speed.
- MVP must be delivered in 6 weeks.

Architecture options:
Option A: Simple RAG with vector database and hosted LLM API
Option B: Fine-tune an open-source LLM on all documents
Option C: Use keyword search only with no LLM
Option D: Build agentic multi-step retrieval with query rewriting, reranking, and citation verification

Task:
Perform tree-of-thought reasoning privately, then output only the JSON schema filled with values and a concise recommendation.
"""

ambiguous_request_rewrite_prompt = """
You are a business analyst. Use the rephrase-and-respond technique to turn a vague stakeholder request into a clear problem statement and propose a practical AI solution.

Required Output Schema:
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
- The response must not be generic.
- Convert vague language into measurable outcomes.
- Define what productivity and visibility could mean.
- Propose a realistic AI use case, not a broad transformation program.

Scenario:
A business stakeholder says:
"We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility."

Task:
1. Rephrase the vague request into a clear, measurable problem statement.
2. Clarify assumptions about productivity and visibility.
3. Propose a practical AI solution with target users, key features, required data, success metrics, implementation steps, and risks.
4. Output only the JSON schema filled with values.
"""

poorly_written_requirement_prompt = """
You are a product requirements analyst. Use the rephrase-and-respond technique to convert a vague technical requirement into a clear specification and implementation proposal.

Required Output Schema:
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
- Define measurable requirements for 'secure', 'fast', and 'properly'.
- Recommend a practical design approach.
- Avoid overcommitting to 'never giving wrong answers' — instead, define accuracy expectations and fallback mechanisms.

Scenario:
A product manager gives this requirement:
"Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers."

Task:
1. Rephrase the vague requirement into a clear technical requirement.
2. Define functional, non-functional, and security requirements.
3. Specify acceptance criteria with measurable outcomes.
4. Recommend a realistic solution approach.
5. List open questions that need clarification.
6. Output only the JSON schema filled with values.
"""
