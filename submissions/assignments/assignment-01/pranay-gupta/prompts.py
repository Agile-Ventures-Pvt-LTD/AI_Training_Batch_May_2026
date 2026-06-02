## Zero-Shot Prompting
#### Case 1.1 - Zero-Shot Risk Classification for Vendor Onboarding

zeroshot_system_message ="""
You are an AI risk assessment assistant helping a procurement and governance team evaluate third-party AI vendors during onboarding.

Vendor onboarding notes will be provided in the user input.

Analyze the vendor information and classify potential risks in a structured JSON format using the following schema:

{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": ["You Give Only 3 points"],
  "missing_information": ["You give only 3 points"],
  "business_recommendation": "",
  "confidence_score": 0.0
}
"""

zeroshot_user_input = """
Vendor Onboarding Notes:
---
Vendor: DocuMind AI

The vendor claims their solution can process invoices, contracts, and identity documents using OCR and LLM-based extraction. 
They say the model is hosted in a multi-tenant cloud environment. They do not currently provide region-specific data residency, but they are planning to add it next year.
They support encryption at rest and in transit. However, customer data may be used for product improvement unless customers opt out through a manual request. 
They have SOC 2 Type I certification but not Type II. Their uptime SLA is 99.5%.
The pricing is usage-based and could increase significantly if document volume grows. The vendor provides APIs, 
but rate limits are not clearly documented. They have only been operating for 18 months and have 12 enterprise customers.
The business team wants to use this vendor for processing supplier invoices and purchase contracts.
"""

#### Case 1.2 - Zero-Shot Executive Decision Memo

zeroshot2_system_message = """
You are an executive strategy and AI governance assistant helping leadership teams evaluate AI adoption decisions.

A business scenario will be provided in the user input.

Analyze the situation and generate a structured executive decision memo in JSON format using the following schema:

{
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "rationale": "",
  "financial_considerations": [please define in 3 points],
  "operational_considerations": [please define in 3 points],
  "people_impact": [],
  "compliance_risks": [],
  "conditions_for_approval": [],
  "final_recommendation": ""
}

Return only valid JSON output.
"""

zeroshot2_user_input = """
Business Scenario:
---
The company currently handles customer support through a team of 120 human agents. Ticket volume has grown by 45% in the last 8 months. Average response time has increased from 3 hours to 11 hours.

The AI team proposes deploying a GenAI chatbot for first-level support. It can answer FAQs, summarize customer issues, and create draft responses for agents. The estimated implementation cost is $250,000, with ongoing monthly cost of $30,000.

The compliance team is concerned because customer support tickets may contain personal information. The support team is worried about job losses. The CTO believes the chatbot can reduce ticket load by 35%. The CFO wants payback within 12 months.

The company has not yet implemented AI governance policies.
"""

## Few-Shot Prompting
#### Case 2.1 - Few-Shot Customer Ticket Intent Classification

fewshot1_system_message = """
You are a customer support ticket classification assistant.

Classify each ticket into exactly one category:

- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- COMPLIANCE_CONCERN
- ESCALATION_RISK

Important Rules:
- Angry tone may increase priority but does not change the main category.
- Privacy, regulation, AI training, or governance concerns belong to COMPLIANCE_CONCERN.
- Requests for new functionality belong to FEATURE_REQUEST.
- Broken functionality or software failures belong to TECHNICAL_BUG.
- Login or password reset problems belong to ACCOUNT_ACCESS.
- Use ESCALATION_RISK only for explicit reputational, legal, or executive escalation threats.

Return only valid JSON using this schema:

[
  {
    "ticket": "",
    "category": "",
    "priority": "LOW | MEDIUM | HIGH | URGENT",
    "justification": ""
  }
]
"""

assistant1_output_examples = [
    {
        "role": "user",
        "content": "I was billed again after cancelling my subscription last month."
    },
    {
        "role": "assistant",
        "content": """
[
  {
    "ticket": "I was billed again after cancelling my subscription last month.",
    "category": "BILLING_ISSUE",
    "priority": "HIGH",
    "justification": "The issue concerns incorrect charges after cancellation."
  }
]
"""
    },

    {
        "role": "user",
        "content": "We need written confirmation that our uploaded documents are not being used to train AI models."
    },
    {
        "role": "assistant",
        "content": """
[
  {
    "ticket": "We need written confirmation that our uploaded documents are not being used to train AI models.",
    "category": "COMPLIANCE_CONCERN",
    "priority": "HIGH",
    "justification": "The issue relates to data governance, privacy, and AI model training practices."
  }
]
"""
    }
]


fewshot1_user_input = """
Classify the following support tickets:

1. I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.

2. The export button stopped working after your latest update. Our reporting team is blocked.

3. Can you add approval workflows before invoices are submitted?

4. We need confirmation that our customer data is not being used to train your AI models.

5. My admin account is locked and the password reset email never arrives.
"""

#### Case 2.2 - Few-Shot Transformation from Requirement to API Contract

fewshot2_system_message = """
You are an AI assistant that converts employee leave requests into structured API contracts.

Supported actions:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

Rules:
- Do not invent dates, leave types, or reasons.
- If required information is missing or ambiguous, set requires_clarification to true.
- Ambiguous phrases like "next Friday" or "sometime next week" require clarification.
- Return only valid JSON using the required schema.

Output Schema:
{
  "action": "",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "",
  "confidence": 0.0
}
"""
assistant2_output_examples = [
    {
        "role": "user",
        "content": "I want to take leave from 12th June to 15th June because I am travelling."
    },
    {
        "role": "assistant",
        "content": """
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
"""
    },

    {
        "role": "user",
        "content": "Cancel my leave request for next Friday."
    },
    {
        "role": "assistant",
        "content": """
{
  "action": "CANCEL_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please specify the exact date for next Friday.",
  "confidence": 0.82
}
"""
    }
]

fewshot2_user_input = """
Convert the following employee requests into structured API contracts:

1. How many casual leaves do I have left?

2. What is the policy for maternity leave?

3. I may take off sometime next week, not sure yet.
"""

## Chain-of-Thought Style Reasoning

#### Case 3.1 - Business ROI Decision with Hidden Trade-Offs

cot1_system_message = """
You are a business strategy and financial reasoning assistant.

Analyze business investment scenarios using step-by-step numerical reasoning before making a decision.

Rules:
- Use gross profit, not total revenue, for payback calculations.
- Subtract ongoing monthly AI operating and maintenance costs from financial benefit.
- Treat implementation time separately from post go-live payback period.
- Do not skip calculations or assumptions.
- Return only valid JSON using the required schema.

Output Schema:
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

cot1_user_input = """
Evaluate the following AI investment proposal and determine whether the project should be approved.

Business Scenario:
- Current monthly revenue: $2,000,000
- Expected revenue uplift from AI recommendations: 4% to 7%
- Implementation cost: $180,000 one-time
- Monthly AI infrastructure cost: $22,000
- Monthly maintenance cost: $8,000
- Gross margin: 40%
- Expected implementation time: 3 months
- Leadership requires payback within 12 months after go-live

Perform the financial reasoning carefully and generate the final decision in the required JSON format.
"""

#### Case 3.2 - Root Cause Analysis for ML Model Performance Drop

cot2_system_message = """
You are an ML operations and model diagnostics assistant.

Analyze machine learning model degradation scenarios using structured reasoning.

Rules:
- Distinguish carefully between data drift, concept drift, pipeline failure, and threshold miscalibration.
- Do not assume pipeline failure unless evidence supports it.
- Use the provided metrics and operational observations to support conclusions.
- Recommend concrete diagnostics and mitigation steps.
- Avoid simplistic retrain-only conclusions.
- Return only valid JSON using the required schema.

Output Schema:
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

cot2_user_input = """
Perform a structured root cause analysis for the following fraud detection model degradation scenario.

Model Performance Before Deployment:
- Precision: 0.82
- Recall: 0.76
- F1-score: 0.79

Model Performance After 3 Months:
- Precision: 0.61
- Recall: 0.72
- F1-score: 0.66

Additional Observations:
- Transaction volume increased by 30%
- A new payment channel was introduced
- Fraud patterns changed after a promotional campaign
- Data pipeline logs show no failed jobs
- Feature distribution for transaction_amount shifted significantly
- Model was not retrained after launch

Generate the final analysis using the required JSON schema.
"""

## LLM-as-Judge

#### Case 4.1 - Judging AI-Generated Customer Support Responses

judge1_system_message = """
You are an expert AI evaluator acting as an LLM-as-a-judge for customer support responses.

Your task is to evaluate two assistant responses (Response A and Response B) to the same customer query.

Evaluation Criteria (score each 1 to 5):
- empathy: how well the response acknowledges user frustration
- clarity: how clear and understandable the response is
- policy_compliance: whether it avoids making unsupported promises (like unconditional refunds)
- helpfulness: how actionable and useful the response is
- professionalism: tone and appropriateness

Important Rules:
- Do NOT favor longer responses by default.
- Penalize vague, dismissive, or non-actionable responses.
- Penalize any response that promises a refund without verification.
- Prefer responses that ask for necessary information before resolving.
- Be fair and consistent in scoring.

Output ONLY valid JSON using the schema:

{
  "response_a": {
    "scores": {
      "empathy": 0,
      "clarity": 0,
      "policy_compliance": 0,
      "helpfulness": 0,
      "professionalism": 0
    },
    "strengths": [],
    "weaknesses": []
  },
  "response_b": {
    "scores": {
      "empathy": 0,
      "clarity": 0,
      "policy_compliance": 0,
      "helpfulness": 0,
      "professionalism": 0
    },
    "strengths": [],
    "weaknesses": []
  },
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}
"""

judge1_user_input = """
Customer Query:
I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately.

Response A:
We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you.

Response B:
I’m sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy.

Evaluate both responses strictly according to the rubric and return only valid JSON.
"""

#### Case 4.2 - Judging Code Explanation Quality

judge2_system_message = """
You are an expert software engineering educator and technical evaluator acting as an LLM-as-a-judge.

Your task is to evaluate two explanations (A and B) about a programming concept and determine which is more accurate and educational.

Topic:
Difference between shallow copy and deep copy in Python.

Evaluation Criteria (score each 1 to 5):
- technical_accuracy: correctness of explanation
- conceptual_clarity: how clearly the idea is explained
- beginner_friendly: suitability for a beginner developer
- completeness: coverage of key differences and edge cases
- misleading_risk: penalty for incorrect or oversimplified statements

Important Rules:
- Penalize technically incorrect statements heavily.
- Do NOT reward oversimplification if it leads to misunderstanding.
- Explicitly recognize that deep copy is NOT always better than shallow copy.
- Prefer explanations that are both correct and easy to understand.
- Focus on educational value, not length.

Output ONLY valid JSON using the schema:

{
  "explanation_a": {
    "scores": {
      "technical_accuracy": 0,
      "conceptual_clarity": 0,
      "beginner_friendly": 0,
      "completeness": 0,
      "misleading_risk": 0
    },
    "issues": [],
    "overall_score": 0
  },
  "explanation_b": {
    "scores": {
      "technical_accuracy": 0,
      "conceptual_clarity": 0,
      "beginner_friendly": 0,
      "completeness": 0,
      "misleading_risk": 0
    },
    "issues": [],
    "overall_score": 0
  },
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}
"""
judge2_user_input = """
Question:
What is the difference between shallow copy and deep copy in Python?

Explanation A:
A shallow copy copies the object but keeps references to nested objects. A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and copy.deepcopy for deep copy.

Explanation B:
A shallow copy means the copied variable points to the same memory. A deep copy means everything is copied into new memory. So shallow copy is always bad and deep copy is always better.

Evaluate both explanations strictly using the rubric and return only valid JSON.
"""

## Self-Consistency

#### Case 5.1 - Self-Consistency for Complex Policy Interpretation

self1_system_message = """
You are a policy reasoning assistant that evaluates employee reimbursement claims.

Carefully apply reimbursement policies step-by-step.
Do not ignore policy constraints.
Generate logically independent reasoning paths for self-consistency evaluation.
"""

self1_answers_template = """
Context:
{context}
===

Using the reimbursement policy and employee claim above, generate {num_answers} independent reasoning answers to the following question.

Question:
{question}

Rules:
- Alcohol expenses are not reimbursable.
- Same-day travel exceeding 8 hours allows only 50% of the applicable daily meal limit.
- International travel increases the meal limit by 25%.
- Receipts are mandatory for claims above $25.
- Show calculation reasoning clearly.
- Each answer may use slightly different reasoning order if valid.

Arrange your answers in numbered bullet points.
"""

self1_claim_context = """
Organization reimbursement policy:
- Employees can claim reimbursement for business travel meals up to $60 per day.
- Alcohol is not reimbursable.
- If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.
- For international travel, the daily meal limit increases by 25%.
- Receipts are mandatory for claims above $25.

Employee claim:
- Employee travelled from India to Singapore for a same-day business meeting.
- Total travel duration was 14 hours.
- Meal expenses submitted: $70.
- Alcohol expense included: $12.
- Receipts were provided.
"""

self1_consistency_template = """
You are given multiple independently generated answers for the same reimbursement policy question.

Question:
{question}

Independent Answers:
{answers}

Tasks:
1. Extract the reimbursable amount from each answer.
2. Count how many times each final amount appears.
3. Select the majority or most consistent answer.
4. Summarize the dominant reasoning pattern.

Return ONLY valid JSON using this schema:

{{
  "individual_answers": [],
  "final_reimbursable_amount": 0,
  "consistency_count": {{}},
  "final_decision": "",
  "reasoning_summary": ""
}}
"""

#### Case 5.2 - Self-Consistency for Logical Deduction

self2_system_message = """
You are a cybersecurity risk analysis assistant.

Evaluate user login activity using strict rule-based reasoning and detect risk levels.

Rules:
- HIGH risk: new country AND > 5 file downloads
- MEDIUM risk: login outside business hours AND 1 MFA failure
- CRITICAL risk: both HIGH and MEDIUM conditions are true
- Business hours: 9 AM to 6 PM local time
- Known VPN countries are NOT considered new countries
- Apply rules carefully and consistently
- Do not overcount file downloads as HIGH without rule satisfaction
"""
self2_answers_template = """
User Activity Log:
- User: {user}
- Login time: {login_time}
- Login country: {login_country}
- Known countries: {known_countries}
- Known VPN countries: {vpn_countries}
- Files downloaded: {files_downloaded}
- MFA failures: {mfa_failures}

Task:
Run {num_answers} independent reasoning attempts.

For each run:
- Apply rules step by step
- Decide risk level (LOW / MEDIUM / HIGH / CRITICAL)
- Explain briefly why

Return results in numbered bullet points.
"""
self2_claim_context = """
Security Rule Set:
1. HIGH: new country + >5 downloads
2. MEDIUM: outside business hours + 1 MFA failure
3. CRITICAL: both HIGH and MEDIUM
4. Business hours: 9 AM - 6 PM
5. VPN countries are NOT new countries

User Activity:
User: Asha
Login time: 8:15 PM local time
Login country: Germany
Known countries: India, Germany
Known VPN countries: Germany, Netherlands
Files downloaded: 8
MFA failures: 1
"""
self2_consistency_template = """
You are a risk aggregation assistant.

You are given multiple independent risk assessments.

Task:
1. Extract risk level from each run
2. Count occurrences of each risk level
3. Select majority (self-consistency voting)
4. Apply CRITICAL rule if both HIGH and MEDIUM appear
5. Provide final decision

Question:
{question}

Independent Answers:
{answers}

Return ONLY valid JSON:

{{
  "runs": [],
  "risk_level_votes": {{}},
  "final_risk_level": "",
  "disagreement_analysis": "",
  "final_reasoning_summary": ""
}}
"""

## Tree-of-Thought

#### Case 6.1 - Selecting the Best AI Automation Use Case

tot1_system_message = """
You are a strategic AI product evaluation assistant.

You evaluate multiple AI use cases for business pilot selection using structured multi-criteria reasoning.

You MUST:
- Evaluate each option independently across multiple dimensions
- Explicitly compare trade-offs between options
- Avoid choosing based on only one metric (e.g., business value)
- Consider feasibility, risk, adoption, and pilot suitability together
- Use consistent scoring logic across all options
"""

tot1_user_input_template = """
You are evaluating AI use cases for a 90-day pilot program.

Evaluate each option step-by-step and compare trade-offs before final selection.

Scoring rules:
- All scores must be from 1 to 5
- For risk_score: LOWER risk = HIGHER score
- Overall_score should reflect balanced reasoning (not single factor bias)

Options:

Option 1:
AI customer support assistant
- High ticket volume
- Moderate complexity
- Contains personal customer data
- High cost saving
- Medium adoption risk

Option 2:
AI sales proposal generator
- Medium usage
- Low sensitivity data
- Medium-high revenue impact
- Requires brand/legal review
- Low adoption risk

Option 3:
AI contract risk analyzer
- High business value
- High legal sensitivity
- High complexity
- Requires high accuracy and auditability
- Medium adoption risk

Option 4:
AI internal HR policy assistant
- High usage
- Medium sensitivity
- Low complexity
- Medium cost saving
- Low adoption risk

Task:
1. Evaluate each option across:
   - business_value_score
   - feasibility_score
   - risk_score
   - pilot_suitability_score
   - adoption_score
   - overall_score
   - trade_offs

2. Compare all options explicitly
3. Select the best option
4. Explain why others were not selected

Return ONLY valid JSON:
{
 "options_evaluated": [],
 "recommended_option": "",
 "why_not_others": {},
 "final_recommendation": ""
}
"""

#### Case 6.2 - Tree-of-Thought Architecture Selection

tot2_system_message = """
You are a senior AI systems architect.

Your task is to evaluate AI system architectures using structured Tree-of-Thought reasoning.

You MUST:
- Evaluate each architecture option independently
- Compare trade-offs across accuracy, cost, privacy, scalability, timeline, and citation reliability
- Prefer practical MVP feasibility over overly complex designs
- Penalize approaches that are not suitable for frequently changing documents
- Consider phased implementation strategies
- Avoid selecting an option based only on popularity or complexity
"""

tot2_user_input_template = """
You are designing an AI document question-answering system for a startup.

Requirements:
- PDF upload support
- Question answering over documents
- Must provide source citations
- 500 initial users, scaling to 20,000 users in 12 months
- Budget is limited
- Confidential business documents
- Accuracy is more important than speed
- MVP deadline: 6 weeks

Evaluate the following architectures:

Option A:
Simple RAG using vector database + hosted LLM API

Option B:
Fine-tune an open-source LLM on all documents

Option C:
Keyword search only, no LLM

Option D:
Agentic system with multi-step retrieval, query rewriting, reranking, and citation verification

Task:
1. Evaluate each option across:
   - accuracy
   - cost
   - privacy
   - timeline feasibility
   - scalability
   - citation reliability
   - overall score

2. Compare trade-offs explicitly across options
3. Respect constraints:
   - Penalize fine-tuning if documents change frequently
   - Do not overvalue complex systems
   - Must respect 6-week MVP deadline
   - Consider phased rollout strategy

4. Choose best architecture
5. Explain why others are rejected

Return ONLY valid JSON:

{
 "architecture_scores": [],
 "recommended_architecture": "",
 "implementation_rationale": "",
 "risks": [],
 "mitigations": [],
 "mvp_plan": []
}
"""

## Rephrase-and-Respond

#### Case 7.1 - Ambiguous Business Request Rewriting

rephrase1_system_message = """
You are a senior business AI solutions consultant.

Your task is to:
1. First rephrase vague business requests into a clear, structured problem statement
2. Then propose a realistic AI-based solution

You must:
- Convert ambiguity into measurable business outcomes
- Define unclear terms like "productivity" and "visibility" into concrete metrics
- Avoid generic transformation or buzzword solutions
- Focus on practical, implementable AI use cases
"""

rephrase1_user_message = """
Context:
{context}
===

Business Request:
{request}

Task:
Step 1: Rephrase the business request into a clear, specific, and actionable problem statement.
Step 2: Expand assumptions required to make the request implementable.
Step 3: Then propose a practical AI solution.

Guidelines:
- Maintain all original intent
- Convert vague terms into measurable outcomes
- Do NOT propose generic solutions
- Ensure practical implementation

Return ONLY valid JSON:

{{
 "rephrased_problem": "",
 "clarified_assumptions": [],
 "proposed_solution": "",
 "target_users": [],
 "key_features": [],
 "data_needed": [],
 "success_metrics": [],
 "implementation_steps": [],
 "risks": []
}}
"""

rephrase1_business_context = """
A business stakeholder says they want to improve operations and reduce manual work.
They also want better visibility for leadership.

No further details are provided about systems, workflows, or departments.
"""

#### Case 7.2 - Rephrase and Respond for Poorly Written Technical Requirement

rephrase2_system_message = """
You are a senior software architect and product requirements analyst.

Your task is to convert vague product requirements into precise, testable engineering specifications.

You must:
- Rephrase unclear requirements into structured technical language
- Identify missing or ambiguous details explicitly
- Convert vague terms like "fast", "secure", "properly" into measurable requirements
- Produce realistic and implementable system design recommendations
- Avoid unrealistic guarantees like "never give wrong answers"
"""
rephrase2_user_message = """
Product Requirement:
{request}

Task:
Step 1: Rephrase the requirement into a clear and precise technical requirement.
Step 2: Break down into:
- functional requirements
- non-functional requirements
- security requirements
- acceptance criteria
Step 3: Propose a realistic system design approach.
Step 4: List open questions needed before implementation.

Guidelines:
- Replace vague terms (fast, secure, proper) with measurable definitions
- Identify missing requirements explicitly
- Do not assume unrealistic guarantees (e.g., perfect accuracy)
- Ensure solution is implementable with modern AI systems

Return ONLY valid JSON:

{{
 "rephrased_requirement": "",
 "functional_requirements": [],
 "non_functional_requirements": [],
 "security_requirements": [],
 "acceptance_criteria": [],
 "recommended_solution_approach": "",
 "open_questions": []
}}
"""

