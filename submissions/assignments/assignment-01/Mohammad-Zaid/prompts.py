# Case 1.1 - Zero-Shot Vendor Risk Classification

case_1_1_zero_shot_system_prompt = """
You are an AI risk analyst.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Each item in 'key_risk_factors' must be short (max 8 words), clear, and specific.
- Avoid long descriptive sentences.
- Use concise phrases like 'Data residency missing' or 'SOC 2 Type I only'.
- Keep 'missing_information' items short and factual.
- Business recommendation can be 1–2 sentences, but not verbose.
"""

case_1_1_zero_shot_user_prompt = """
Vendor: DocuMind AI
Claims: OCR + LLM extraction for invoices, contracts, identity docs.
Environment: Multi-tenant cloud, no region-specific residency yet.
Security: Encryption at rest/in transit, SOC 2 Type I only.
Data use: Customer data may be used unless opt-out.
SLA: 99.5% uptime.
Pricing: Usage-based, unclear API rate limits.
Maturity: 18 months, 12 enterprise customers.

Task: Classify vendor into LOW, MEDIUM, HIGH, or CRITICAL risk.

Schema:
{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": [],
  "missing_information": [],
  "business_recommendation": "",
  "confidence_score": 0.0
}
"""
# Case 1.2 - Zero-Shot Executive Decision Memo

case_1_2_zero_shot_system_prompt = """
You are an executive advisor. 
Always return valid JSON according to the schema provided. 
Your output must be decision-oriented, not a summary. 
Include governance, compliance, ROI, and change-management considerations. 
Do not overpromise automation benefits.
"""

case_1_2_zero_shot_user_prompt = """
Scenario:
Customer support team: 120 agents.
Ticket volume: +45% in 8 months.
Response time: increased from 3 hours to 11 hours.

Proposal: Deploy GenAI chatbot for first-level support.
- Cost: $250,000 implementation, $30,000 monthly.
- Benefits: Answer FAQs, summarize issues, draft responses.
- CTO: expects 35% ticket load reduction.
- CFO: wants payback within 12 months.
- Compliance team: concerned about personal data in tickets.
- Support team: worried about job losses.
- Company: no AI governance policies yet.

Task: Generate an executive decision memo with a clear decision and business conditions.

Schema:
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
# Case 2.1 - Few-Shot Customer Ticket Intent Classification

case_2_1_few_shot_system_prompt = """
You are a customer support ticket classifier.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON array.

Constraints:
- Include examples with ambiguity.
- Angry tone can increase priority but does not change category.
- Distinguish compliance concern from technical bug.
- Distinguish feature request from billing issue.
- Each item must be short and clear.
"""

# Case 2.1 - Few-Shot Customer Ticket Intent Classification

case_2_1_few_shot_system_prompt = """
You are a customer support ticket classifier.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON array.
"""

case_2_1_few_shot_user_prompt = """
Classify customer tickets into categories:
BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS, FEATURE_REQUEST, COMPLIANCE_CONCERN, ESCALATION_RISK

Schema:
[
  {
    "ticket": "",
    "category": "",
    "priority": "LOW | MEDIUM | HIGH | URGENT",
    "justification": ""
  }
]

Examples:
1. Ticket: I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.
   Output: {"ticket": "...", "category": "BILLING_ISSUE", "priority": "URGENT", "justification": "Duplicate charge + angry tone + escalation risk"}

2. Ticket: The export button stopped working after your latest update. Our reporting team is blocked.
   Output: {"ticket": "...", "category": "TECHNICAL_BUG", "priority": "HIGH", "justification": "Critical feature broken"}

3. Ticket: Can you add approval workflows before invoices are submitted?
   Output: {"ticket": "...", "category": "FEATURE_REQUEST", "priority": "MEDIUM", "justification": "Feature request"}

4. Ticket: We need confirmation that our customer data is not being used to train your AI models.
   Output: {"ticket": "...", "category": "COMPLIANCE_CONCERN", "priority": "HIGH", "justification": "Compliance concern"}

5. Ticket: My admin account is locked and the password reset email never arrives.
   Output: {"ticket": "...", "category": "ACCOUNT_ACCESS", "priority": "HIGH", "justification": "Account access issue"}

Now classify the following tickets:
1. The billing portal shows incorrect charges for last month.
2. Our VPN stopped working after the latest patch.
3. Please add dark mode to the dashboard.
4. I am worried that your system is storing my personal ID without consent.
5. My account was disabled suddenly and I cannot log in.
"""

# Case 2.2 - Few-Shot Transformation from Requirement to API Contract

case_2_2_few_shot_system_prompt = """
You are an AI assistant that converts natural language leave requests into structured API contracts.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.
"""

case_2_2_few_shot_user_prompt = """
Supported actions: APPLY_LEAVE, CHECK_BALANCE, CANCEL_LEAVE, GET_POLICY

Schema:
{
  "action": "",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "",
  "confidence": 0.0
}

Examples:
1. User: "I want to take leave from 12th June to 15th June because I am travelling."
   Output: {"action": "APPLY_LEAVE", "parameters": {"start_date": "2024-06-12", "end_date": "2024-06-15", "reason": "travelling"}, "requires_clarification": false, "clarification_question": "", "confidence": 0.95}

2. User: "How many casual leaves do I have left?"
   Output: {"action": "CHECK_BALANCE", "parameters": {"leave_type": "casual"}, "requires_clarification": false, "clarification_question": "", "confidence": 0.9}

3. User: "Cancel my leave request for next Friday."
   Output: {"action": "CANCEL_LEAVE", "parameters": {"date": "next Friday"}, "requires_clarification": true, "clarification_question": "Please provide the exact date for 'next Friday'.", "confidence": 0.7}

4. User: "What is the policy for maternity leave?"
   Output: {"action": "GET_POLICY", "parameters": {"policy_type": "maternity"}, "requires_clarification": false, "clarification_question": "", "confidence": 0.9}

5. User: "I may take off sometime next week, not sure yet."
   Output: {"action": "APPLY_LEAVE", "parameters": {"start_date": "next week"}, "requires_clarification": true, "clarification_question": "Please provide exact dates for 'next week'.", "confidence": 0.6}

Now convert the following request into an API contract:
"I want to cancel my sick leave scheduled for 3rd July."
"""
# Case 3.1 - Chain-of-Thought Business ROI Decision with Hidden Trade-Offs

case_3_1_cot_system_prompt = """
You are a business analyst evaluating ROI for AI adoption.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Perform numerical reasoning step by step.
- Use gross margin, not revenue, for payback calculations.
- Subtract monthly AI operating costs (infrastructure + maintenance).
- Consider implementation time separately from payback after go-live.
- Do not invent numbers; only use those provided.
"""

case_3_1_cot_user_prompt = """
Scenario:
Retail company wants to deploy an AI recommendation engine.
Current monthly revenue: $2,000,000
Expected revenue uplift from recommendations: 4% to 7%
Implementation cost: $180,000 one-time
Monthly AI infrastructure cost: $22,000
Monthly maintenance cost: $8,000
Gross margin: 40%
Expected implementation time: 3 months
Leadership requires payback within 12 months after go-live.

Task:
Use reasoning to determine whether the project should be approved.

Schema:
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

# Case 3.2 - Chain-of-Thought Compliance Risk Assessment

case_3_2_cot_system_prompt = """
You are a compliance risk analyst evaluating vendor contracts.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Perform reasoning step by step before giving the final answer.
- Identify risks across data privacy, regulatory compliance, and contractual safeguards.
- Do not invent certifications or policies; only use those provided.
- If information is missing, highlight it in 'missing_information'.
"""

case_3_2_cot_user_prompt = """
Scenario:
Vendor contract states:
- Customer data may be processed in multiple regions without explicit residency guarantees.
- Vendor holds only SOC 2 Type I certification.
- No mention of GDPR, HIPAA, or ISO 27001 compliance.
- SLA guarantees 99.5% uptime.
- No explicit breach notification timeline.
- Vendor reserves the right to use customer data for model training unless opted out.

Task:
Evaluate compliance risks and provide a recommendation.

Schema:
{
  "identified_risks": [],
  "missing_information": [],
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "reasoning_summary": "",
  "confidence": 0.0
}
"""

# Case 4.1 - LLM-as-Judge Evaluation with Rubric

case_4_1_judge_system_prompt = """
You are an impartial evaluator (LLM-as-Judge).
Your task is to evaluate two model responses against the rubric provided.
Always return valid JSON according to the schema.
Do not include any text outside the JSON object.

Constraints:
- Judge scores from 1 to 5.
- Do not prefer a response only because it is longer.
- Penalize vague or dismissive answers.
- Check whether the response promises a refund without verification.
- Provide strengths and weaknesses for each response.
"""

case_4_1_judge_user_prompt = """
Scenario:
Two responses were given to a customer complaint about being charged twice.

Response A:
"We apologize for the inconvenience. We will issue a refund immediately."

Response B:
"Thank you for reaching out. We understand your concern. Please provide your account details so we can investigate further."

Task:
Evaluate both responses according to clarity, correctness, and adherence to responsible handling of refunds.
Use the rubric to score each response from 1 to 5.
Identify strengths and weaknesses.
Decide which response is better.

Schema:
{
  "response_a": {"scores": {"clarity": 0, "correctness": 0, "responsibility": 0}, "strengths": [], "weaknesses": []},
  "response_b": {"scores": {"clarity": 0, "correctness": 0, "responsibility": 0}, "strengths": [], "weaknesses": []},
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}
"""
# Case 4.2 - Judging Code Explanation Quality

case_4_2_judge_system_prompt = """
You are an impartial evaluator (LLM-as-Judge).
Your task is to evaluate two code explanations for technical accuracy and beginner usefulness.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Detect technically misleading claims.
- Do not reward oversimplification if it becomes inaccurate.
- Explain why deep copy is not always better.
- Scores must reflect both beginner usefulness and technical accuracy.
- Judge scores from 1 to 5.
"""

case_4_2_judge_user_prompt = """
Scenario:
A junior developer asks:
What is the difference between shallow copy and deep copy in Python?

Explanation A:
"A shallow copy copies the object but keeps references to nested objects. A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and copy.deepcopy for deep copy."

Explanation B:
"A shallow copy means the copied variable points to the same memory. A deep copy means everything is copied into new memory. So shallow copy is always bad and deep copy is always better."

Task:
Evaluate both explanations according to clarity, correctness, and beginner usefulness.
Identify issues, assign scores, and decide which explanation is better.

Schema:
{
  "explanation_a": {"scores": {"clarity": 0, "correctness": 0, "usefulness": 0}, "issues": [], "overall_score": 0},
  "explanation_b": {"scores": {"clarity": 0, "correctness": 0, "usefulness": 0}, "issues": [], "overall_score": 0},
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}
"""

# Case 5.1 - Self-Consistency for Complex Policy Interpretation

case_5_1_self_consistency_system_prompt = """
You are a reimbursement policy evaluator.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Run multiple independent reasoning paths.
- Alcohol must be excluded.
- Apply both international uplift (+25%) and same-day travel rule (50% of daily limit).
- Receipts are mandatory for claims above $25.
- Do not invent policy rules; only use those provided.
"""

case_5_1_self_consistency_user_prompt = """
Scenario:
Organization reimbursement policy:
- Employees can claim reimbursement for business travel meals up to $60 per day.
- Alcohol is not reimbursable.
- If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.
- For international travel, the daily meal limit increases by 25%.
- Receipts are mandatory for claims above $25.

Employee claim:
- Travel: India to Singapore, same-day business meeting.
- Duration: 14 hours.
- Expenses: $70 total, including $12 for alcohol.
- Receipts: Provided.

Task:
Use self-consistency prompting to calculate the reimbursable amount.

Schema:
{
  "individual_answers": [],
  "final_reimbursable_amount": 0,
  "consistency_count": {},
  "final_decision": "",
  "reasoning_summary": ""
}
"""

# Case 5.2 - Self-Consistency for Logical Deduction

case_5_2_self_consistency_system_prompt = """
You are a security risk evaluator.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Run multiple independent reasoning paths.
- Germany is a known country and also a known VPN country.
- More than five downloads alone does not satisfy HIGH risk.
- Login outside business hours + MFA failure once = MEDIUM risk.
- If both HIGH and MEDIUM conditions are true, escalate to CRITICAL.
- Do not invent rules; only use those provided.
"""

case_5_2_self_consistency_user_prompt = """
Scenario:
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

Schema:
{
  "runs": [],
  "risk_level_votes": {},
  "final_risk_level": "",
  "disagreement_analysis": "",
  "final_reasoning_summary": ""
}
"""
# Case 6.1 - Tree-of-Thought Reasoning: Selecting the Best AI Automation Use Case

case_6_1_tree_of_thought_system_prompt = """
You are a business analyst using a tree-of-thought reasoning approach.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Evaluate each option across business value, feasibility, risk, 90-day pilot suitability, and adoption.
- Scores must be from 1 to 5.
- Lower risk should receive a higher risk score.
- Do not choose only on business value.
- Explicitly compare trade-offs.
- Provide reasoning for why the recommended option was chosen and why others were not.
"""

case_6_1_tree_of_thought_user_prompt = """
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
Use a tree-of-thought approach to evaluate each option across business value, feasibility, risk, 90-day pilot suitability, and adoption.

Schema:
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

# Case 6.2 - Tree-of-Thought Reasoning: Architecture Selection

case_6_2_tree_of_thought_system_prompt = """
You are a solution architect using a tree-of-thought reasoning approach.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Evaluate each architecture option across accuracy, cost, privacy, timeline, scalability, and citation reliability.
- Penalize fine-tuning if documents change frequently.
- Do not choose the most complex option blindly.
- Respect the 6-week MVP timeline.
- Consider a phased approach.
- Scores must be from 1 to 5.
"""

case_6_2_tree_of_thought_user_prompt = """
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
Use tree-of-thought prompting to evaluate architecture options across accuracy, cost, privacy, timeline, scalability, and citation reliability.

Schema:
{
  "architecture_scores": [
    {
      "option": "",
      "accuracy_score": 0,
      "cost_score": 0,
      "privacy_score": 0,
      "timeline_score": 0,
      "scalability_score": 0,
      "citation_reliability_score": 0,
      "overall_score": 0,
      "trade_offs": []
    }
  ],
  "recommended_architecture": "",
  "implementation_rationale": "",
  "risks": [],
  "mitigations": [],
  "mvp_plan": []
}
"""
# Case 7.1 - Rephrase-and-Respond: Ambiguous Business Request Rewriting

case_7_1_rephrase_system_prompt = """
You are a business analyst using the rephrase-and-respond technique.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- First rephrase the vague request into a clearer problem statement.
- Convert vague language into measurable outcomes.
- Define what productivity and visibility could mean.
- Propose a realistic AI use case, not a broad transformation program.
"""

case_7_1_rephrase_user_prompt = """
Scenario:
A business stakeholder says:
"We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility."

Task:
Use the rephrase-and-respond technique. First rephrase the vague request into a clearer problem statement, then propose a practical AI solution.

Schema:
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
# Case 7.2 - Rephrase-and-Respond: Poorly Written Technical Requirement

case_7_2_rephrase_system_prompt = """
You are a product requirements analyst using the rephrase-and-respond technique.
Always return valid JSON according to the schema provided.
Do not include any text outside the JSON object.

Constraints:
- Identify missing details.
- Define measurable requirements for 'secure', 'fast', and 'properly'.
- Recommend a practical design.
- Avoid overcommitting to never giving wrong answers.
"""

case_7_2_rephrase_user_prompt = """
Scenario:
A product manager gives this requirement:
"Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers."

Task:
Use rephrase-and-respond to convert this into a clear technical requirement and implementation proposal.

Schema:
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
