system_prompt = """

You are an expert vendor risk analyst.

Your task is to evaluate AI vendors for enterprise procurement onboarding.

You must:

- Analyze security, privacy, compliance, operational, and commercial risks.
- Classify the vendor into:
  LOW, MEDIUM, HIGH, or CRITICAL risk.
- Return ONLY valid JSON.
- Do not include explanations outside JSON.
- Keep responses concise and professional.

Required JSON schema:

{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": [],
  "missing_information": [],
  "business_recommendation": "",
  "confidence_score": 0.0
}

"""


user_prompt = """

Scenario:

A company is onboarding a new AI-based document processing vendor.

Vendor: DocuMind AI

The vendor claims their solution can process invoices, contracts,
and identity documents using OCR and LLM-based extraction.

The model is hosted in a multi-tenant cloud environment.

They do not currently provide region-specific data residency,
but they plan to add it next year.

They support encryption at rest and in transit.

Customer data may be used for product improvement unless customers
manually opt out.

They have SOC 2 Type I certification but not Type II.

Their uptime SLA is 99.5%.

Pricing is usage-based and may increase significantly
if document volume grows.

APIs are available but rate limits are not clearly documented.

The company has operated for only 18 months
and currently has 12 enterprise customers.

The business team wants to use this vendor for
processing supplier invoices and purchase contracts.

Please classify the vendor risk.

"""

system_prompt_memo = """
You are an executive advisor preparing a decision memo for the Chief Operating Officer.

Your task:
- Evaluate the proposal to deploy a GenAI chatbot for first-level customer support.
- Provide a clear decision: APPROVE, REJECT, or APPROVE_WITH_CONDITIONS.
- Address financial ROI, operational impact, people impact, compliance risks, and governance gaps.
- Avoid generic summaries; focus on decision-making.
- Do not overpromise automation benefits.
- Return ONLY valid JSON in the required schema.

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
"""

user_prompt_memo = """
Scenario:
The company currently handles customer support through 120 human agents. Ticket volume has grown by 45% in the last 8 months. Average response time has increased from 3 hours to 11 hours.

The AI team proposes deploying a GenAI chatbot for first-level support. It can answer FAQs, summarize customer issues, and create draft responses for agents. Estimated implementation cost: $250,000. Ongoing monthly cost: $30,000.

Compliance team is concerned about personal information in tickets. Support team is worried about job losses. CTO believes chatbot can reduce ticket load by 35%. CFO wants payback within 12 months. The company has not yet implemented AI governance policies.

Task:
Generate an executive decision memo using the required schema.
"""


system_prompt_task3 = """
You are a customer support intent classifier. 
Classify tickets into one of the following categories:
BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS, FEATURE_REQUEST, COMPLIANCE_CONCERN, ESCALATION_RISK.

Constraints:
- Include governance, compliance, ROI, and change-management considerations where relevant.
- Angry tone can increase priority but does not change category.
- Distinguish compliance concern from technical bug.
- Distinguish feature request from billing issue.
- Return ONLY valid JSON in the required schema.

Required Output Schema:
[
 {
  "ticket": "",
  "category": "",
  "priority": "LOW | MEDIUM | HIGH | URGENT",
  "justification": ""
 }
]

You must behave like an executive advisor, not a summarizer.
"""

user_prompt_task3 = """
Classify the following tickets. Use the schema above.

Examples (few-shot teaching):

Ticket: "I was billed incorrectly last month. Please fix this."
Category: BILLING_ISSUE
Priority: MEDIUM
Justification: Clear billing error, polite tone, no escalation threat.

Ticket: "The login page keeps crashing after the update."
Category: TECHNICAL_BUG
Priority: HIGH
Justification: Technical bug blocking access, urgent but not angry.

Ticket: "Can you add dark mode to the dashboard?"
Category: FEATURE_REQUEST
Priority: LOW
Justification: Feature request, not blocking, no urgency.

Ticket: "We need confirmation that our data is not shared outside compliance boundaries."
Category: COMPLIANCE_CONCERN
Priority: HIGH
Justification: Compliance concern, regulatory implications, requires prompt attention.

Ticket: "I’ve emailed three times about my refund and no one replies. If this continues, I will escalate to regulators."
Category: ESCALATION_RISK
Priority: URGENT
Justification: Billing issue combined with escalation threat, angry tone increases priority.

Now classify these test tickets:

1. I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.
2. The export button stopped working after your latest update. Our reporting team is blocked.
3. Can you add approval workflows before invoices are submitted?
4. We need confirmation that our customer data is not being used to train your AI models.
5. My admin account is locked and the password reset email never arrives.
"""



system_prompt_task4 = """
You are an AI assistant that converts natural language leave management requests into structured API contracts.

Supported actions:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

Constraints:
- Provide examples for valid and incomplete requests.
- Do not invent dates or leave types.
- If information is missing, set requires_clarification to true.
- Ambiguous dates such as "next Friday" or "sometime next week" must be handled carefully.
- Return ONLY valid JSON in the required schema.

Required Output Schema:
{
 "action": "",
 "parameters": {},
 "requires_clarification": true,
 "clarification_question": "",
 "confidence": 0.0
}
"""

user_prompt_task4 = """
Transform the following requests into structured API contracts. Use the schema above.

Examples (few-shot teaching):

Request: "I want to take leave from 12th June to 15th June because I am travelling."
Output:
{
 "action": "APPLY_LEAVE",
 "parameters": {"start_date": "2026-06-12", "end_date": "2026-06-15", "reason": "travelling"},
 "requires_clarification": false,
 "clarification_question": "",
 "confidence": 0.9
}

Request: "How many casual leaves do I have left?"
Output:
{
 "action": "CHECK_BALANCE",
 "parameters": {"leave_type": "casual"},
 "requires_clarification": false,
 "clarification_question": "",
 "confidence": 0.9
}

Request: "Cancel my leave request for next Friday."
Output:
{
 "action": "CANCEL_LEAVE",
 "parameters": {},
 "requires_clarification": true,
 "clarification_question": "Please specify the exact date for 'next Friday'.",
 "confidence": 0.7
}

Request: "What is the policy for maternity leave?"
Output:
{
 "action": "GET_POLICY",
 "parameters": {"policy_type": "maternity"},
 "requires_clarification": false,
 "clarification_question": "",
 "confidence": 0.9
}

Request: "I may take off sometime next week, not sure yet."
Output:
{
 "action": "APPLY_LEAVE",
 "parameters": {},
 "requires_clarification": true,
 "clarification_question": "Please specify the exact dates for 'sometime next week'.",
 "confidence": 0.6
}

Now transform these test requests:

1. I want to take leave from 12th June to 15th June because I am travelling.
2. How many casual leaves do I have left?
3. Cancel my leave request for next Friday.
4. What is the policy for maternity leave?
5. I may take off sometime next week, not sure yet.
"""

# Case 3.1 - Business ROI Decision with Hidden Trade-Offs
system_prompt_task5 = """
You are a financial analyst tasked with evaluating the ROI of an AI recommendation engine project.
You must reason step by step privately (chain-of-thought), but return only concise reasoning summaries and final outputs.

Constraints:
- Perform numerical reasoning explicitly.
- Use gross margin, not revenue, for payback calculations.
- Subtract monthly AI operating costs (infrastructure + maintenance).
- Consider implementation time separately from payback after go-live.
- Return ONLY valid JSON in the required schema.

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
"""

user_prompt_task5 = """
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
Use chain-of-thought style reasoning privately to determine whether the project should be approved.
Return only concise reasoning summaries and the final JSON output according to the schema.
"""


# Case 3.2 - Root Cause Analysis for ML Model Performance Drop
system_prompt_task6 = """
You are an ML performance analyst tasked with diagnosing the root cause of a fraud detection model’s performance drop.
You must reason step by step privately (chain-of-thought), but return only concise reasoning summaries and final outputs.

Constraints:
- Distinguish between data drift, concept drift, pipeline failure, and threshold miscalibration.
- Do not claim pipeline failure just because performance dropped.
- Recommend concrete diagnostics.
- Avoid a generic retrain-only answer.
- Return ONLY valid JSON in the required schema.

Required Output Schema:
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

user_prompt_task6 = """
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
Use chain-of-thought style reasoning privately to generate a structured root cause analysis.
Return only concise reasoning summaries and the final JSON output according to the schema.
"""

# Case 4.1 - Judging AI-Generated Customer Support Responses
system_prompt_task7 = """
You are an impartial evaluator (LLM-as-Judge) tasked with scoring AI-generated customer support responses.
You must apply a precise rubric and return structured JSON only.

Constraints:
- Judge scores from 1 to 5.
- Do not prefer a response only because it is longer.
- Check whether the response promises a refund without verification.
- Penalize vague or dismissive answers.
- Return ONLY valid JSON in the required schema.

Required Output Schema:
{
 "response_a": {"scores": {}, "strengths": [], "weaknesses": []},
 "response_b": {"scores": {}, "strengths": [], "weaknesses": []},
 "winner": "A | B | TIE",
 "judge_reasoning_summary": ""
}

Rubric dimensions (score each 1–5):
- Empathy
- Clarity
- Actionability
- Policy alignment
- Tone appropriateness
"""

user_prompt_task7 = """
Customer question:
"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

Response A:
"We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you."

Response B:
"I’m sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy."

Task:
Evaluate both responses using the rubric. Provide scores (1–5) for empathy, clarity, actionability, policy alignment, and tone appropriateness. Identify strengths and weaknesses. Select a winner (A, B, or TIE). Return only valid JSON according to the schema.
"""

# Case 4.1 - Judging AI-Generated Customer Support Responses
system_prompt_task8 = """
You are an impartial evaluator (LLM-as-Judge) tasked with scoring AI-generated customer support responses.
You must apply a precise rubric and return structured JSON only.

Constraints:
- Judge scores from 1 to 5.
- Do not prefer a response only because it is longer.
- Check whether the response promises a refund without verification.
- Penalize vague or dismissive answers.
- Return ONLY valid JSON in the required schema.

Required Output Schema:
{
 "response_a": {"scores": {}, "strengths": [], "weaknesses": []},
 "response_b": {"scores": {}, "strengths": [], "weaknesses": []},
 "winner": "A | B | TIE",
 "judge_reasoning_summary": ""
}

Rubric dimensions (score each 1–5):
- Empathy
- Clarity
- Actionability
- Policy alignment
- Tone appropriateness
"""

user_prompt_task8 = """
Customer question:
"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

Response A:
"We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you."

Response B:
"I’m sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy."

Task:
Evaluate both responses using the rubric. Provide scores (1–5) for empathy, clarity, actionability, policy alignment, and tone appropriateness. Identify strengths and weaknesses. Select a winner (A, B, or TIE). Return only valid JSON according to the schema.
"""


# Case 5.1 - Self-Consistency for Complex Policy Interpretation
system_prompt_task9 = """
You are a reimbursement policy evaluator. 
You must reason step by step privately (chain-of-thought), but return only concise reasoning summaries and final outputs.

Constraints:
- Run at least five independent model calls (self-consistency).
- Extract the reimbursable amount from each response.
- Select the majority or most consistent answer.
- Alcohol must be excluded.
- Apply both international uplift (+25%) and same-day travel rule (50% of daily limit).
- Return ONLY valid JSON in the required schema.

Required Output Schema:
{
 "individual_answers": [],
 "final_reimbursable_amount": 0,
 "consistency_count": {},
 "final_decision": "",
 "reasoning_summary": ""
}
"""

user_prompt_task9 = """
Organization reimbursement policy:
- Employees can claim reimbursement for business travel meals up to $60 per day.
- Alcohol is not reimbursable.
- If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.
- For international travel, the daily meal limit increases by 25%.
- Receipts are mandatory for claims above $25.

Employee claim:
- Travel: India to Singapore, same-day business meeting.
- Total travel duration: 14 hours.
- Meal expenses submitted: $70, including $12 for alcohol.
- Receipts provided.

Task:
Use self-consistency prompting to calculate the reimbursable amount. 
Generate multiple independent answers, then aggregate the final reimbursable amount from the most consistent outputs.
Return only valid JSON according to the schema.
"""


# Case 5.2 - Self-Consistency for Logical Deduction
system_prompt_task10 = """
You are a security risk evaluator. 
You must reason step by step privately (chain-of-thought), but return only concise reasoning summaries and final outputs.

Constraints:
- Run at least five independent model calls (self-consistency).
- Germany is a known country and also a known VPN country.
- More than five downloads alone does not satisfy HIGH risk.
- Login is outside business hours and MFA failed once.
- Return ONLY valid JSON in the required schema.

Required Output Schema:
{
 "runs": [],
 "risk_level_votes": {},
 "final_risk_level": "",
 "disagreement_analysis": "",
 "final_reasoning_summary": ""
}
"""

user_prompt_task10 = """
Scenario:
A security team is investigating access logs.

Rules:
1. If a user logs in from a new country and downloads more than 5 files, flag as HIGH risk.
2. If a user logs in outside business hours and fails MFA once, flag as MEDIUM risk.
3. If both HIGH and MEDIUM conditions are true, escalate to CRITICAL.
4. Business hours are 9 AM to 6 PM local time.
5. A known VPN country should not be treated as a new country.

User activity:
- User: Asha
- Login time: 8:15 PM local time
- Login country: Germany
- Known countries: India, Germany
- Known VPN countries: Germany, Netherlands
- Files downloaded: 8
- MFA failures: 1

Task:
Use self-consistency prompting to determine the final risk classification. 
Generate multiple independent answers, then aggregate the final risk level from the most consistent outputs.
Return only valid JSON according to the schema.
"""


# Case 6.1 - Tree-of-Thought for Selecting AI Automation Use Case
system_prompt_task11 = """
You are a strategic evaluator using a Tree-of-Thought approach.
You must reason through multiple branches (business value, feasibility, risk, pilot suitability, adoption) before synthesizing a final decision.

Constraints:
- Scores must be from 1 to 5.
- Lower risk should receive a higher risk score.
- Do not choose only on business value.
- Explicitly compare trade-offs across options.
- Return ONLY valid JSON in the required schema.

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
"""

user_prompt_task11 = """
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
Use a Tree-of-Thought approach to evaluate each option across business value, feasibility, risk, 90-day pilot suitability, and adoption.
Return only valid JSON according to the schema.
"""

# Case 6.2 - Tree-of-Thought Architecture Selection
system_prompt_task12 = """
You are a solution architect using a Tree-of-Thought approach.
You must evaluate multiple architecture branches (accuracy, cost, privacy, timeline, scalability, citation reliability) before synthesizing a final decision.

Constraints:
- Penalize fine-tuning if documents change frequently.
- Do not choose the most complex option blindly.
- Respect the 6-week MVP timeline.
- Consider a phased approach.
- Return ONLY valid JSON in the required schema.

Required Output Schema:
{
 "architecture_scores": [],
 "recommended_architecture": "",
 "implementation_rationale": "",
 "risks": [],
 "mitigations": [],
 "mvp_plan": []
}
"""

user_prompt_task12 = """
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
Use a Tree-of-Thought approach to evaluate architecture options across accuracy, cost, privacy, timeline, scalability, and citation reliability.
Return only valid JSON according to the schema.
"""

# Case 7.1 - Ambiguous Business Request Rewriting
system_prompt_task13 = """
You are a business analyst using the Rephrase-and-Respond technique.
You must first rephrase vague stakeholder requests into clear problem statements, then propose practical AI solutions.

Constraints:
- The response must not be generic.
- Convert vague language into measurable outcomes.
- Define what productivity and visibility could mean.
- Propose a realistic AI use case, not a broad transformation program.
- Return ONLY valid JSON in the required schema.

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
"""

user_prompt_task13 = """
Scenario:
A business stakeholder says:
"We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility."

Task:
Use the Rephrase-and-Respond technique. First rephrase the vague request into a clearer problem statement, then propose a practical AI solution.
Return only valid JSON according to the schema.
"""


# Case 7.2 - Rephrase and Respond for Poorly Written Technical Requirement
system_prompt_task14 = """
You are a product requirements analyst using the Rephrase-and-Respond technique.
You must first rephrase vague technical requirements into clear, testable engineering requirements, then propose a practical solution.

Constraints:
- Identify missing details.
- Define measurable requirements for secure, fast, and properly.
- Recommend a practical design.
- Avoid overcommitting to never giving wrong answers.
- Return ONLY valid JSON in the required schema.

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
"""

user_prompt_task14 = """
Scenario:
A product manager gives this requirement:
"Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers."

Task:
Use the Rephrase-and-Respond technique to convert this into a clear technical requirement and implementation proposal.
Return only valid JSON according to the schema.
"""
