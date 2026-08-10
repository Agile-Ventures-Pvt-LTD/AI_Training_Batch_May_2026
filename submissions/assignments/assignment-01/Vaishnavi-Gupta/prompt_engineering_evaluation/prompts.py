ZERO_SHOT_RISK_PROMPT = """
You are a senior AI risk analyst.

Classify the vendor into one of:
LOW, MEDIUM, HIGH, CRITICAL risk.

Evaluate:
- privacy risk
- compliance risk
- operational risk
- pricing risk
- vendor maturity risk

Return ONLY valid JSON:

{
 "risk_level": "",
 "key_risk_factors": [],
 "missing_information": [],
 "business_recommendation": "",
 "confidence_score": 0.0
}

Do not include any extra text.
"""


ZERO_SHOT_EXEC_MEMO_PROMPT = """
You are an executive decision-making AI advisor.

Decide whether to approve a GenAI chatbot project.

Consider:
- ROI (payback within 12 months requirement)
- compliance risks (PII exposure)
- operational impact
- workforce impact
- governance readiness

Return ONLY valid JSON:

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

Be strict and decision-oriented, not descriptive.
"""


FEW_SHOT_TICKET_PROMPT = """
You are a customer support ticket classifier.

Categories:
BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS,
FEATURE_REQUEST, COMPLIANCE_CONCERN, ESCALATION_RISK

Rules:
- Angry tone increases priority, not category
- Compliance ≠ bug
- Billing ≠ feature request

Examples:

Ticket: I was charged twice last month
Category: BILLING_ISSUE
Priority: HIGH
Justification: duplicate billing complaint

Ticket: export button broken after update
Category: TECHNICAL_BUG
Priority: MEDIUM
Justification: functionality failure after release

Ticket: add approval workflow before invoices
Category: FEATURE_REQUEST
Priority: LOW
Justification: enhancement request

Ticket: confirm you are not training on my data
Category: COMPLIANCE_CONCERN
Priority: HIGH
Justification: data usage concern

Ticket: my admin account is locked
Category: ACCOUNT_ACCESS
Priority: URGENT
Justification: blocked access to system

Now classify:

Return JSON ONLY:
[
 {
  "ticket": "",
  "category": "",
  "priority": "",
  "justification": ""
 }
]
"""


FEW_SHOT_API_PROMPT = """
You convert user requests into structured API contracts.

Actions:
APPLY_LEAVE, CHECK_BALANCE, CANCEL_LEAVE, GET_POLICY

Rules:
- Never invent dates
- If unclear → requires_clarification = true
- Handle vague time carefully

Example:
Input: I want leave from 1 June to 3 June
Output:
{
 "action": "APPLY_LEAVE",
 "parameters": {"start_date": "1 June", "end_date": "3 June"},
 "requires_clarification": false,
 "clarification_question": "",
 "confidence": 0.9
}

Input: I may take leave next week
Output:
{
 "action": "APPLY_LEAVE",
 "parameters": {},
 "requires_clarification": true,
 "clarification_question": "Which exact dates next week?",
 "confidence": 0.4
}

Now process:

Return JSON ONLY.
"""


COT_ROI_PROMPT = """
You are a financial analyst.

Compute ROI for AI recommendation system.

IMPORTANT:
- Use gross profit, not revenue
- Subtract AI costs
- Separate implementation vs operational phase

Return ONLY JSON:

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


COT_RCA_PROMPT = """
You are a senior Machine Learning Reliability Engineer.

You are analyzing a production fraud detection model performance degradation.

You must produce a structured root cause analysis.

IMPORTANT:
- Do NOT assume pipeline failure unless explicitly supported
- Distinguish clearly between:
  - data drift
  - concept drift
  - threshold miscalibration
  - distribution shift
  - external behavioral changes
- Avoid generic answers like "retrain model"

You must reason step-by-step internally, but ONLY output structured JSON.

Return JSON:

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
- Each cause must be tied to provided evidence
- Do not hallucinate missing system failures
- Prefer statistically and operationally grounded explanations
"""


LLM_JUDGE_PROMPT = """
You are an impartial evaluator.

Score responses from 1 to 5 on:
- correctness
- clarity
- helpfulness
- safety
- compliance accuracy

Do NOT prefer longer answers.

Return JSON:

{
 "response_a": {"scores": {}, "strengths": [], "weaknesses": []},
 "response_b": {"scores": {}, "strengths": [], "weaknesses": []},
 "winner": "",
 "judge_reasoning_summary": ""
}
"""


LLM_JUDGE_CODE_PROMPT = """
You are an expert Python educator and code correctness reviewer.

You are evaluating two explanations of:
"shallow copy vs deep copy in Python"

You must evaluate:

1. Technical correctness
2. Depth of explanation
3. Misleading statements
4. Beginner friendliness
5. Conceptual completeness

IMPORTANT RULES:
- Do NOT prefer longer answers
- Penalize incorrect simplifications
- Explicitly detect misleading claims like:
  "shallow copy is always bad" (FALSE)
- Deep copy is NOT always better — evaluate fairness

Return JSON ONLY:

{
 "explanation_a": {
   "scores": {
     "correctness": 0,
     "clarity": 0,
     "depth": 0,
     "misleading_penalty": 0,
     "beginner_friendliness": 0
   },
   "issues": [],
   "overall_score": 0
 },
 "explanation_b": {
   "scores": {
     "correctness": 0,
     "clarity": 0,
     "depth": 0,
     "misleading_penalty": 0,
     "beginner_friendliness": 0
   },
   "issues": [],
   "overall_score": 0
 },
 "winner": "",
 "judge_reasoning_summary": ""
}

Scoring rule:
- Higher correctness outweighs clarity
- Any misleading statement reduces score heavily
"""


SELF_CONSISTENCY_PROMPT = """
Solve reimbursement calculation.

Rules:
- Alcohol not reimbursable
- International +25%
- Same-day travel 50% cap applies
- Receipts required above $25

Return ONLY:
{
 "final_amount": 0,
 "steps": []
}
"""


SELF_CONSISTENCY_SECURITY_PROMPT = """
You are a cybersecurity risk analyst.

You must classify user risk level based on access logs.

Rules:
1. New country + >5 file downloads → HIGH risk
2. Outside business hours + 1 MFA failure → MEDIUM risk
3. If BOTH HIGH and MEDIUM → CRITICAL
4. Known VPN countries do NOT count as "new country"
5. Business hours: 9 AM – 6 PM local time

IMPORTANT SELF-CONSISTENCY INSTRUCTION:
You are one of multiple independent reasoning runs.
Do NOT try to align with previous outputs.
Reason independently each time.

Return ONLY:
{
 "risk_level": "",
 "reasoning": "",
 "key_factors": []
}
"""


TOT_PROMPT = """
Evaluate options using multi-criteria reasoning.

Score:
1–5 scale:
business_value
feasibility
risk (lower risk = higher score)
pilot_suitability
adoption

Return JSON ONLY.
"""


TOT_ARCHITECTURE_PROMPT = """
You are a Principal AI Architect.

You must evaluate multiple architecture options for a document QA system.

You MUST:
1. Evaluate EACH option independently
2. Score across:
   - accuracy
   - cost
   - privacy
   - scalability
   - timeline fit (6 weeks MVP)
   - citation reliability
3. Then compare trade-offs
4. Then select best option

IMPORTANT RULES:
- Do NOT choose based on complexity alone
- Penalize solutions that violate 6-week MVP constraint
- Penalize fine-tuning if data changes frequently
- Prefer practical MVP-first architecture

Return JSON ONLY:

{
 "architecture_scores": [],
 "recommended_architecture": "",
 "implementation_rationale": "",
 "risks": [],
 "mitigations": [],
 "mvp_plan": []
}

Scoring:
- 1 = poor, 5 = excellent
"""


REPHRASE_PROMPT = """
First rephrase the problem clearly.

Then propose solution.

Return JSON:

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


REPHRASE_TECHNICAL_REQUIREMENT_PROMPT = """
You are a Senior Product Architect and Systems Engineer.

You are given a vague product requirement.

Your job:
STEP 1: Rephrase it into a clear technical requirement
STEP 2: Extract structured system specifications
STEP 3: Identify missing details explicitly

IMPORTANT RULES:
- Do NOT assume security = perfect safety
- Do NOT assume system can always give correct answers
- Do NOT hallucinate missing constraints
- Convert vague terms into measurable engineering requirements

Interpret:
- "secure" → authentication, authorization, encryption, audit logs
- "fast" → latency targets (e.g., <2s response)
- "properly" → accuracy + validation + fallback behavior

Return JSON ONLY:

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