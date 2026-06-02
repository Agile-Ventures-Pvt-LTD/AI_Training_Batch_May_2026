# =========================================================
# ZERO SHOT CASE 1.1
# =========================================================

zero_shot_prompt = """
You are an enterprise AI risk analyst.

Analyze the vendor onboarding scenario carefully.

Classify the vendor risk level as:
LOW, MEDIUM, HIGH, or CRITICAL.

Focus on:
- privacy risks
- compliance risks
- operational risks
- pricing risks
- vendor maturity risks

Return ONLY valid JSON.

Schema:
{
    "risk_level": "",
    "key_risk_factors": [],
    "missing_information": [],
    "business_recommendation": "",
    "confidence_score": 0.0
}

Vendor Scenario:

Vendor: DocuMind AI

The vendor claims their solution can process invoices, contracts, and identity documents using OCR and LLM-based extraction.

They say the model is hosted in a multi-tenant cloud environment.

They do not currently provide region-specific data residency.

Customer data may be used for product improvement unless customers opt out.

SOC 2 Type I but not Type II.

Usage-based pricing.

Vendor operating for 18 months with 12 enterprise customers.
"""


# =========================================================
# ZERO SHOT CASE 1.2
# =========================================================

zero_shot_executive_prompt = """
You are a senior executive strategy advisor.

Generate a decision-oriented executive memo.

Return ONLY valid JSON.

Schema:
{
    "decision": "",
    "rationale": "",
    "financial_considerations": [],
    "operational_considerations": [],
    "people_impact": [],
    "compliance_risks": [],
    "conditions_for_approval": [],
    "final_recommendation": ""
}

Scenario:

Customer support team has 120 agents.

Ticket volume increased by 45%.

Average response time increased from 3 hours to 11 hours.

AI chatbot implementation cost is $250,000 with monthly cost of $30,000.

Compliance concerns exist around customer data.
"""


# =========================================================
# FEW SHOT CASE 2.1
# =========================================================

few_shot_ticket_prompt = """
You are a customer support classifier.

Return ONLY valid JSON.

Schema:
[
    {
        "ticket": "",
        "category": "",
        "priority": "",
        "justification": ""
    }
]

Examples:

Ticket:
"My payment failed twice."

Output:
{
    "ticket": "My payment failed twice.",
    "category": "BILLING_ISSUE",
    "priority": "HIGH",
    "justification": "Billing deduction issue."
}

Ticket:
"The export button crashes."

Output:
{
    "ticket": "The export button crashes.",
    "category": "TECHNICAL_BUG",
    "priority": "HIGH",
    "justification": "Critical feature failure."
}

Now classify:

1. I was charged twice this month.

2. Export button stopped working.

3. Add approval workflows.

4. Is customer data used for AI training?

5. My account is locked.
"""


# =========================================================
# FEW SHOT CASE 2.2
# =========================================================

few_shot_api_prompt = """
You are an AI leave management assistant.

Convert requests into structured API payloads.

Return ONLY valid JSON.

Schema:
{
    "action": "",
    "parameters": {},
    "requires_clarification": true,
    "clarification_question": "",
    "confidence": 0.0
}

User:
"I want leave from 12th June to 15th June."

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

Now convert:

1. Cancel my leave next Friday.
2. Show maternity leave policy.
3. How many earned leaves do I have left?
"""


# =========================================================
# CHAIN OF THOUGHT CASE 3.1
# =========================================================

cot_roi_prompt = """
You are a business strategy analyst.

Perform numerical reasoning internally.

Return ONLY valid JSON.

Schema:
{
    "incremental_revenue_range": "",
    "incremental_gross_profit_range": "",
    "monthly_net_benefit_range": "",
    "payback_period_range_months": "",
    "decision": "",
    "reasoning_summary": "",
    "key_assumptions": []
}

Revenue: $2,000,000
Revenue uplift: 4% to 7%
Implementation cost: $180,000
Monthly AI cost: $30,000
Gross margin: 40%
"""


# =========================================================
# CHAIN OF THOUGHT CASE 3.2
# =========================================================

# =========================================================
# CHAIN OF THOUGHT CASE 3.2
# =========================================================

cot_ml_prompt = """
You are a senior ML analyst specializing in fraud detection systems.

Reason step-by-step internally before generating the final answer.

Do not expose detailed chain-of-thought reasoning.
Return only concise reasoning summaries.

Distinguish carefully between:
- data drift
- concept drift
- pipeline failure
- threshold miscalibration

Do not assume pipeline failure unless evidence explicitly supports it.

Use metric degradation patterns, feature distribution shifts, transaction behavior changes, and deployment context as evidence for hypothesis evaluation.

Recommend concrete diagnostics such as:
- feature drift analysis
- threshold evaluation
- confusion matrix review
- calibration analysis
- segment-wise performance analysis
- monitoring of new payment channel behavior

Do not provide a generic retrain-only answer.

Provide both short-term mitigations and long-term corrective actions.

Prioritize evidence-based ML reasoning instead of generic troubleshooting advice.

Return ONLY valid JSON.

Schema:
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

Fraud model degraded after deployment.

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
"""


# =========================================================
# LLM JUDGE CASE 4.1
# =========================================================

llm_judge_support_prompt = """
You are an expert customer support quality evaluator.

Evaluate both responses using a structured scoring rubric.

Reason carefully before scoring.

Do not prefer a response only because it is longer.

Penalize:
- vague responses
- dismissive language
- lack of empathy
- missing escalation handling
- unsafe refund promises without verification

Check whether the response:
- acknowledges customer frustration
- provides actionable next steps
- follows proper billing verification process
- avoids guaranteeing refunds prematurely
- demonstrates professionalism

Score each category from 1 to 5 where:
1 = Poor
2 = Weak
3 = Acceptable
4 = Good
5 = Excellent

Evaluation Dimensions:
- empathy
- clarity
- actionability
- policy_compliance
- professionalism

Return ONLY valid JSON.

Schema:
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
I was charged for a premium plan even though I cancelled last month.
I already contacted support twice and no one responded.
I want a refund immediately.

Response A:
We are sorry for the inconvenience.
Please check your billing settings and make sure your cancellation was completed.
Refunds are subject to our policy.
Thank you.

Response B:
I’m sorry this has been frustrating, especially after you contacted support twice.
I can help escalate this as a billing issue.
Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility.
If the duplicate charge is confirmed, we will process the refund according to the billing policy.
"""

# =========================================================
# LLM JUDGE CASE 4.2
# =========================================================
llm_judge_python_prompt = """
You are an expert Python educator and technical evaluator.

Evaluate both explanations using a structured scoring rubric.

Reason carefully before scoring.

Do not reward explanations that oversimplify concepts inaccurately.

Detect technically misleading claims.

Check whether the explanation:
- is technically accurate
- is beginner-friendly
- explains nested object behavior correctly
- avoids misleading memory model explanations
- correctly explains why deep copy is not always better
- provides practical understanding

Score each category from 1 to 5 where:
1 = Poor
2 = Weak
3 = Acceptable
4 = Good
5 = Excellent

Evaluation Dimensions:
- technical_accuracy
- beginner_clarity
- conceptual_correctness
- practical_usefulness
- completeness

Return ONLY valid JSON.

Schema:
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
What is the difference between shallow copy and deep copy in Python?

Explanation A:
A shallow copy copies the object but keeps references to nested objects.
A deep copy recursively copies nested objects too.
Use copy.copy for shallow copy and copy.deepcopy for deep copy.

Explanation B:
A shallow copy means the copied variable points to the same memory.
A deep copy means everything is copied into new memory.
So shallow copy is always bad and deep copy is always better.
"""

# =========================================================
# SELF CONSISTENCY CASE 5.1
# =========================================================
 

self_consistency_policy_prompt = """
You are an enterprise reimbursement policy analyst.

Reason carefully and independently before generating the answer.

Apply policy rules exactly as written.

Do not expose detailed chain-of-thought reasoning.
Return only concise reasoning summaries.

Important Policy Rules:
- Alcohol is never reimbursable.
- International travel increases the meal limit by 25%.
- Same-day travel exceeding 8 hours allows reimbursement up to 50% of the daily meal limit.
- Receipts are required for claims above $25.
- Apply all relevant policy rules carefully before calculating the final reimbursable amount.

Carefully determine:
- whether the international uplift applies before or after the same-day reduction
- the correct adjusted meal limit
- the reimbursable amount after excluding alcohol

Do not assume missing information.

Return ONLY valid JSON.

Schema:
{
    "reimbursable_amount": 0,
    "reasoning": ""
}

Scenario:

Organization reimbursement policy:
- Employees can claim reimbursement for business travel meals up to $60 per day.
- Alcohol is not reimbursable.
- If travel exceeds 8 hours but does not include an overnight stay, the employee can claim up to 50% of the daily meal limit.
- For international travel, the daily meal limit increases by 25%.
- Receipts are mandatory for claims above $25.

Employee claim:
- Employee travelled from India to Singapore for a same-day business meeting
- Total travel duration was 14 hours
- Meal expenses submitted: $70
- Alcohol expense: $12
- Receipts were provided
"""

# =========================================================
# SELF CONSISTENCY CASE 5.2
# =========================================================


self_consistency_security_prompt = """
You are a cybersecurity risk analyst.

Reason carefully and independently before generating the answer.

Apply all security rules exactly as written.

Do not expose detailed chain-of-thought reasoning.
Return only concise reasoning summaries.

Important Rules:
1. HIGH risk requires:
   - login from a new country
   AND
   - more than 5 file downloads

2. MEDIUM risk requires:
   - login outside business hours
   AND
   - at least one MFA failure

3. If both HIGH and MEDIUM conditions are true,
   escalate to CRITICAL.

4. Business hours are 9 AM to 6 PM local time.

5. Known VPN countries must NOT be treated as new countries.

Important Reasoning Constraints:
- More than five downloads alone does NOT satisfy HIGH risk.
- Germany is already a known country.
- Germany is also a known VPN country.
- Evaluate each rule independently before determining final risk level.

Do not assume additional security incidents.

Return ONLY valid JSON.

Schema:
{
    "risk_level": "",
    "reasoning": ""
}

Scenario:

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
"""
# =========================================================
# TREE OF THOUGHT CASE 6.1
# =========================================================
tree_of_thought_prompt = """
You are an enterprise AI strategy advisor.

Use a tree-of-thought reasoning approach.

Evaluate each option independently across:
- business value
- feasibility
- implementation risk
- 90-day pilot suitability
- user adoption likelihood

Then compare trade-offs across all options before making a final recommendation.

Reason step-by-step internally but do not expose detailed chain-of-thought reasoning.

Return only concise evaluation summaries.

Important Constraints:
- Scores must range from 1 to 5.
- Higher risk should receive LOWER implementation viability.
- Lower operational and compliance risk should receive HIGHER risk scores.
- Do not select an option based only on business value.
- Explicitly compare trade-offs between complexity, adoption, implementation speed, sensitivity, and expected ROI.
- Consider whether each option is realistic for a 90-day pilot.
- Consider compliance and legal sensitivity carefully.
- Prioritize balanced decision-making over fashionable AI choices.

Return ONLY valid JSON.

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

Scenario:

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
"""
# =========================================================
# TREE OF THOUGHT CASE 6.2
# =========================================================

tree_of_thought_architecture_prompt = """
You are a senior AI systems architect.

Use a tree-of-thought reasoning approach.

Evaluate each architecture option independently across:
- accuracy
- implementation cost
- privacy and security
- MVP delivery timeline
- scalability
- citation reliability
- operational complexity

Then compare architectural trade-offs before selecting the final recommendation.

Reason step-by-step internally but do not expose detailed chain-of-thought reasoning.

Return only concise evaluation summaries.

Important Constraints:
- Respect the 6-week MVP timeline.
- Do not automatically choose the most advanced or complex architecture.
- Penalize fine-tuning approaches if documents change frequently.
- Accuracy and citation reliability are more important than speed.
- Budget is limited and must influence the recommendation.
- Consider confidential business data handling.
- Consider long-term scalability separately from MVP simplicity.
- Consider phased implementation approaches when appropriate.

Evaluate trade-offs carefully between:
- simplicity vs capability
- speed vs accuracy
- cost vs scalability
- privacy vs operational complexity

Return ONLY valid JSON.

Schema:
{
  "architecture_scores": [],
  "recommended_architecture": "",
  "implementation_rationale": "",
  "risks": [],
  "mitigations": [],
  "mvp_plan": []
}

Scenario:

Requirements:
- Users upload PDF documents
- Users ask questions about uploaded documents
- The system must show source citations
- Initial users: 500
- Expected growth: 20,000 users in 12 months
- Budget is limited
- Documents may contain confidential business information
- Accuracy is more important than speed
- MVP must be delivered in 6 weeks

Architecture Options:

Option A:
Simple RAG with vector database and hosted LLM API

Option B:
Fine-tune an open-source LLM on all documents

Option C:
Use keyword search only with no LLM

Option D:
Build agentic multi-step retrieval with query rewriting, reranking, and citation verification
"""


# =========================================================
# REPHRASE AND RESPOND CASE 7.1
# =========================================================

rephrase_prompt = """
You are a business AI consultant.

Rephrase vague request clearly.

Return ONLY valid JSON.

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

Request:
We need AI to improve operations.
"""


# =========================================================
# REPHRASE AND RESPOND CASE 7.1
# =========================================================

rephrase_prompt = """
You are an enterprise AI business consultant.

Use a rephrase-and-respond approach.

First:
- identify ambiguity
- infer realistic operational goals
- convert vague business language into measurable business problems

Then:
- propose a focused and realistic AI solution
- avoid broad enterprise transformation recommendations
- prioritize practical operational improvements

Reason carefully before generating the response.

Do not expose detailed chain-of-thought reasoning.
Return only concise reasoning summaries.

Important Constraints:
- Do not provide generic AI recommendations.
- Define measurable interpretations of:
  - productivity
  - operational efficiency
  - leadership visibility
- Propose a realistic use case that could be implemented incrementally.
- Avoid suggesting company-wide AI transformation programs.
- Focus on one practical operational workflow.
- Include concrete KPIs and measurable success metrics.
- Identify assumptions explicitly instead of inventing missing business context.

Return ONLY valid JSON.

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

Business Request:

We need AI to improve operations and reduce manual work.
Build something that helps teams become more productive
and gives leadership better visibility.
"""
# =========================================================
# REPHRASE AND RESPOND CASE 7.2
# =========================================================

rephrase_technical_prompt = """
You are a senior AI systems architect and product requirements analyst.

Use a rephrase-and-respond approach.

First:
- identify ambiguity and missing technical details
- convert vague product language into testable engineering requirements
- define measurable expectations for security, speed, and answer quality

Then:
- propose a practical implementation approach
- avoid unrealistic guarantees
- identify open technical and product questions

Reason carefully before generating the response.

Do not expose detailed chain-of-thought reasoning.
Return only concise reasoning summaries.

Important Constraints:
- Do not promise perfect accuracy or zero hallucinations.
- Define measurable performance expectations.
- Convert vague terms such as:
  - secure
  - fast
  - proper answers
  into concrete engineering requirements.
- Recommend a realistic architecture suitable for document question answering.
- Explicitly identify missing product requirements.
- Include both functional and non-functional requirements.
- Include practical security controls for uploaded files and document access.
- Focus on an MVP-friendly implementation approach.

Return ONLY valid JSON.

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

Original Requirement:

Create an AI feature where users can upload files and ask things
and the system should answer properly.
It should be secure and fast and should not give wrong answers.
"""