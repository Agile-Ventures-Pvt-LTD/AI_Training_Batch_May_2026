ZERO_SHOT_1 = """
You are a third-party vendor risk assessment analyst.

Analyze the vendor onboarding information below.

Classify the vendor into:
LOW, MEDIUM, HIGH, or CRITICAL risk.

Decision Criteria:
- Privacy Risk
- Compliance Risk
- Operational Risk
- Pricing Risk
- Vendor Maturity Risk

Requirements:
- Identify both explicit and implicit risks.
- Use evidence from the scenario.
- Avoid generic statements.
- Return ONLY valid JSON.

Scenario:

Vendor: DocuMind AI

The vendor claims their solution can process invoices, contracts, and identity documents using OCR and LLM-based extraction.

The model is hosted in a multi-tenant cloud environment.

They do not currently provide region-specific data residency but plan to add it next year.

Customer data may be used for product improvement unless customers manually opt out.

They have SOC2 Type II certification but not ISO 27001.

Pricing is usage based and costs may increase significantly as document volume grows.

The vendor provides APIs but operational uptime guarantees are not clearly documented.

The company has been operating for 18 months and serves 12 enterprise customers.

Business wants to use this vendor for supplier invoices and purchase contracts.

Output Schema:

{
    "risk_level":"LOW | MEDIUM | HIGH | CRITICAL",
    "key_risk_factors":[],
    "missing_information":[],
    "business_recommendation":"",
    "confidence_score":0.0
}
"""



ZERO_SHOT_2 = """
You are a Chief Strategy and Risk Advisor preparing an executive decision memo for a COO.

Your task is to evaluate the proposal, make a business decision, identify tradeoffs, and define approval conditions.

Do NOT summarize the scenario.

Act as an executive advisor balancing operational impact, governance readiness, financial return, compliance exposure, workforce implications, and implementation realism.

Decision Options:
- APPROVE
- REJECT
- APPROVE_WITH_CONDITIONS

Evaluation Requirements:
- Assess ROI credibility and cost justification.
- Assess operational feasibility and implementation readiness.
- Assess governance and compliance gaps.
- Assess workforce and change-management risks.
- Challenge unsupported assumptions.
- Avoid overstating automation benefits.
- Explicitly identify missing controls or missing information.

Scenario:

The company operates a customer support organization with 120 human agents.

Ticket volume has grown by 45% in the last 6 months.

Average response time increased from 3 hours to 13 hours.

The AI team proposes deploying a GenAI chatbot for first-level support.

The chatbot would answer FAQs, summarize customer issues, and draft responses for agents.

Estimated implementation cost: $250,000.

Ongoing monthly cost: $30,000.

Support tickets may contain personal information.

Support leadership is concerned about job losses.

The CTO believes ticket load can be reduced by 35%.

The CFO expects payback within 12 months.

The company has not yet implemented formal AI governance policies.

Return ONLY valid JSON.

Output Schema:

{
    "decision":"APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
    "rationale":"",
    "financial_considerations":[],
    "operational_considerations":[],
    "people_impact":[],
    "compliance_risks":[],
    "conditions_for_approval":[],
    "final_recommendation":""
}
"""





FEW_SHOT_1 = """
You are a customer support intent classifier and a JSON generator.

Possible Categories:
- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- COMPLIANCE_CONCERN
- ESCALATION_RISK

Priority Rules:
LOW | MEDIUM | HIGH | URGENT

Learn classification behavior from the examples below.

Example 1

Ticket:
"My credit card was charged twice this month."

Output:
{
"category":"BILLING_ISSUE",
"priority":"MEDIUM",
"justification":"Duplicate payment problem."
}

Example 2

Ticket:
"The dashboard export button crashes every time we click download."

Output:
{
"category":"TECHNICAL_BUG",
"priority":"HIGH",
"justification":"Core functionality failure."
}

Example 3

Ticket:
"I cannot log into my admin account and password reset emails never arrive."

Output:
{
"category":"ACCOUNT_ACCESS",
"priority":"URGENT",
"justification":"Access blockage affecting account use."
}

Example 4

Ticket:
"Will our uploaded documents be used to train your AI systems?"

Output:
{
"category":"COMPLIANCE_CONCERN",
"priority":"HIGH",
"justification":"Data handling and privacy concern."
}

Example 5

Ticket:
"Please add approval workflows for finance invoices."

Output:
{
"category":"FEATURE_REQUEST",
"priority":"LOW",
"justification":"Request for new capability."
}

Boundary Guidance:
- Angry language can increase priority but does NOT automatically change category.
- Feature request must not be confused with billing issue.
- Compliance concerns focus on privacy, regulation, or data handling.
- Use semantic intent, not emotional tone alone.

Now classify these tickets.

Return ONLY valid JSON.
Do not include explanations,text,mardown or multiple JSON blocks.

Tickets:

1. "I was charged twice this month and your support team has not replied for five days. I will post this on social media if not fixed today."

2. "The export button stopped working after your latest update. Our reporting team is blocked."

3. "Can you add approval workflows before invoices are submitted?"

4. "We need confirmation that our customer data is not being used to train your AI models."

5. "My admin account is locked and password reset email never arrives."

Output Schema:

{
"ticket":"",
"category":"",
"priority":"",
"justification":""
}

"""



FEW_SHOT_2 = """
You are an API contract generator for an AI leave management assistant.

Supported Actions:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

Learn behavior from examples.

Example 1

User:
"I want to take leave from 12 June to 15 June because I am travelling."

Output:
{
"action":"APPLY_LEAVE",
"parameters":{
    "start_date":"12 June",
    "end_date":"15 June",
    "reason":"travelling"
},
"requires_clarification":false,
"clarification_question":"",
"confidence":0.96
}

Example 2

User:
"How many casual leaves do I have left?"

Output:
{
"action":"CHECK_BALANCE",
"parameters":{
    "leave_type":"casual"
},
"requires_clarification":false,
"clarification_question":"",
"confidence":0.98
}

Example 3

User:
"Cancel my leave request for next Friday."

Output:
{
"action":"CANCEL_LEAVE",
"parameters":{},
"requires_clarification":true,
"clarification_question":"Please specify the exact calendar date for next Friday.",
"confidence":0.78
}

Example 4

User:
"What is the policy for maternity leave?"

Output:
{
"action":"GET_POLICY",
"parameters":{
    "policy_type":"maternity_leave"
},
"requires_clarification":false,
"clarification_question":"",
"confidence":0.99
}

Boundary Rules:

- Never invent dates.
- Never invent leave types.
- Ambiguous timing requires clarification.
- Incomplete requests should not become completed payloads.
- Use the safest valid interpretation.

Now transform these requests.

Requests:

1. "I may take off sometime next week, not sure yet."
2. "How many casual leaves do I still have?"
3. "Cancel my leave for next Friday."
4. "I want leave from 5 July to 9 July."
5. "What is the policy for maternity leave?"

STRICT OUTPUT RULES:

- Return ONLY a JSON ARRAY.
- Do NOT add explanations.
- Do NOT number outputs.
- Do NOT write "Here are the transformations".
- One JSON object per request.

Required format:

[
{
"action":"",
"parameters":{},
"requires_clarification":false,
"clarification_question":"",
"confidence":0.0
}
]
"""





CHAIN_OF_THOUGHT_1 = """
You are a senior business strategy analyst.

Perform internal numerical reasoning carefully before answering.

Do calculations privately.

Return only concise reasoning summary and final structured output.

Scenario:

A retail company wants to deploy an AI recommendation engine.

Current monthly revenue: $2,000,000

Expected revenue lift from recommendations: 4% to 7%

Implementation cost: $180,000 one-time

Monthly AI infrastructure cost: $22,000

Monthly maintenance cost: $8,000

Gross margin: 40%

Expected implementation time: 3 months

Leadership requires payback within 12 months after go-live.

Required reasoning rules:

- Use gross margin, not revenue, for payback calculation.
- Use the full expected revenue lift range.
- Subtract monthly AI operating costs.
- Treat implementation time separately from post-launch payback.
- Explicitly check whether leadership's requirement is met.

Return ONLY valid JSON.

Output Schema:

{
"incremental_revenue_range":"",
"incremental_gross_profit_range":"",
"monthly_net_benefit_range":"",
"payback_period_range_months":"",
"decision":"APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
"reasoning_summary":"",
"key_assumptions":[]
}
"""




CHAIN_OF_THOUGHT_2 = """
You are a senior ML reliability engineer performing production model investigation.

Perform careful internal reasoning before answering.

Return only concise reasoning summary and structured analysis.

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

- Transaction volume increased by 30%.
- A new payment channel was introduced.
- Fraud patterns changed after a promotional campaign.
- Data pipeline logs show no failed jobs.
- Feature distribution for transaction_amount shifted significantly.
- Model was not retrained after launch.

Reasoning Requirements:

- Distinguish between data drift, concept drift, threshold miscalibration, and pipeline failure.
- Do NOT infer pipeline failure solely from performance decline.
- Use evidence-based reasoning.
- Recommend concrete diagnostics.
- Avoid a generic retrain-only answer.
- Consider multiple competing causes.

Return ONLY valid JSON.

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





LLM_AS_A_JUDGE1 = """
You are an expert AI evaluator. Your job is to fairly compare two customer support responses (A and B) using a strict rubric.

IMPORTANT RULES:
- Do NOT prefer longer responses.
- Penalize vague, generic, or dismissive answers.
- Do NOT reward promises of refunds unless verification steps are included.
- Focus on correctness, empathy, clarity, and actionability.
- Be strict and consistent.

CUSTOMER QUERY:
"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

RESPONSE A:
{response_a}

RESPONSE B:
{response_b}

EVALUATION RUBRIC (score 1–5 each):
1. Empathy & tone (understanding frustration)
2. Actionability (clear next steps for user)
3. Policy correctness (no false promises, correct refund handling)
4. Specificity (asks for needed info like invoice/email)
5. Trust & professionalism

SCORING GUIDE:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

OUTPUT FORMAT (STRICT JSON ONLY):
{
 "response_a": {
   "scores": {
     "empathy": 0,
     "actionability": 0,
     "policy_correctness": 0,
     "specificity": 0,
     "trust": 0
   },
   "strengths": [],
   "weaknesses": []
 },
 "response_b": {
   "scores": {
     "empathy": 0,
     "actionability": 0,
     "policy_correctness": 0,
     "specificity": 0,
     "trust": 0
   },
   "strengths": [],
   "weaknesses": []
 },
 "winner": "A | B | TIE",
 "judge_reasoning_summary": ""
}

"""





LLM_AS_A_JUDGE2 = """
You are an expert Python educator and evaluator.

Your task is to evaluate two explanations (A and B) for a junior developer.

QUESTION:
What is the difference between shallow copy and deep copy in Python?

EXPLANATION A:
<<<EXPLANATION_A>>>

EXPLANATION B:
<<<EXPLANATION_B>>>

---

CRITICAL EVALUATION RULES:

- Penalize technically incorrect explanations.
- Do NOT reward oversimplification if it becomes misleading.
- Detect misconceptions explicitly.
- Deep copy is NOT always better.
- Shallow copy is NOT "same memory" (this is incorrect framing).
- Evaluate from a beginner learning perspective.

---

CORE CONCEPTS YOU MUST CHECK:

✔ Shallow copy:
- Creates new outer object
- Inner objects are still referenced

✔ Deep copy:
- Recursively copies everything
- Fully independent structure

✔ Misconceptions to penalize:
- "shallow copy = same memory" ❌
- "deep copy is always better" ❌

---

SCORING DIMENSIONS (1–5):

- technical_accuracy
- beginner_clarity
- concept_completeness
- misconception_handling
- practical_correctness

---

OUTPUT FORMAT (STRICT JSON ONLY):

{
  "explanation_a": {
    "scores": {
      "technical_accuracy": 0,
      "beginner_clarity": 0,
      "concept_completeness": 0,
      "misconception_handling": 0,
      "practical_correctness": 0
    },
    "issues": [],
    "overall_score": 0
  },
  "explanation_b": {
    "scores": {
      "technical_accuracy": 0,
      "beginner_clarity": 0,
      "concept_completeness": 0,
      "misconception_handling": 0,
      "practical_correctness": 0
    },
    "issues": [],
    "overall_score": 0
  },
  "winner": "A | B | TIE",
  "judge_reasoning_summary": ""
}
"""





'''SELF_CONSISTENCY_PROMPT1 = """
You are a strict policy reasoning engine.

You must follow the policy step-by-step and compute a final numeric answer.

IMPORTANT RULES:
- Do NOT skip steps
- Do NOT assume extra rules
- Always apply rules in this order:
  1. Remove non-reimbursable items (alcohol)
  2. Apply international uplift (+25%)
  3. Apply same-day travel rule (50% reduction if applicable)
  4. Apply reimbursement cap
- Receipts only affect eligibility, not amount calculation (assume valid if provided)
- Output ONLY the final number

POLICY:
- Base daily meal limit = 60
- Alcohol = not reimbursable
- International travel = +25% to meal limit
- Same-day travel (>8 hours, no overnight) = 50% of final daily limit
- Receipts required if claim > 25 (already satisfied)

SCENARIO:
Travel: India → Singapore (international)
Duration: 14 hours (same-day travel)
Expenses: 70 total, including 12 alcohol
Receipts: provided

Return ONLY final reimbursable amount (number only).
"""
'''


SELF_CONSISTENCY_PROMPT1 = """
You are a strict policy engine.

Solve step-by-step internally.

FINAL OUTPUT RULE:
Return ONLY JSON:

{
  "result": <final_reimbursable_amount>,
  "reasoning": "short explanation"
}

RULES:
- Remove alcohol
- Apply international uplift (+25%)
- Apply same-day reduction (50%)
- Compute final value

SCENARIO:
India → Singapore
14 hours
Expenses: 70 (12 alcohol)
Receipts provided
"""


SELF_CONSISTENCY_RISK_PROMPT2 = """
You are a cybersecurity risk classification engine.

You must classify user activity into ONE of:
LOW, MEDIUM, HIGH, CRITICAL

IMPORTANT RULES (must follow exactly):

1. HIGH risk:
   - ONLY if user logs in from a NEW country (not in known countries)
   AND downloads more than 5 files

2. MEDIUM risk:
   - Login outside business hours (9 AM–6 PM local time)
   AND exactly 1 MFA failure

3. CRITICAL risk:
   - If BOTH HIGH and MEDIUM conditions are satisfied

4. IMPORTANT EXCEPTIONS:
   - Known VPN countries do NOT count as new countries

5. DO NOT assume HIGH risk only from downloads.

---

USER DATA:
User: Asha
Login time: 8:15 PM
Login country: Germany
Known countries: India, Germany
Known VPN countries: Germany, Netherlands
Files downloaded: 8
MFA failures: 1

---

TASK:
Think carefully and classify risk.

OUTPUT RULE:
Return ONLY JSON:
{ "risk": "<LOW|MEDIUM|HIGH|CRITICAL>" }
"""





TREE_OF_THOUGHT_1 = """
You are a strategic AI transformation advisor.

Use a Tree-of-Thought reasoning approach.

INSTRUCTIONS:

Step 1:
Evaluate EACH option independently as a separate reasoning branch.

Step 2:
For each branch, score the option across:
- business_value
- feasibility
- risk
- 90_day_pilot_suitability
- adoption

Step 3:
Explicitly compare trade-offs across branches.

Step 4:
Synthesize a final recommendation.

IMPORTANT RULES:

- Scores must be integers from 1 to 5.
- Higher risk score = LOWER actual risk.
- Do NOT choose based only on business value.
- Consider implementation complexity, adoption, sensitivity, and pilot practicality.
- Compare branches before choosing.

OPTIONS:

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

OUTPUT RULE:

Return ONLY valid JSON.

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






TREE_OF_THOUGHT_2 = """
You are a senior AI system architect evaluating architecture choices for a document-based AI Q&A system.

Use Tree-of-Thought reasoning:

Step 1: Evaluate EACH architecture option independently (as separate reasoning branches)

Step 2: Score each option across:
- accuracy
- cost_efficiency
- privacy
- timeline_fit (6-week MVP constraint)
- scalability
- citation_reliability

Step 3: Compare trade-offs across all options

Step 4: Select the best architecture and justify

IMPORTANT RULES:

- Do NOT always choose the most advanced or complex system.
- Penalize solutions that exceed the 6-week MVP timeline.
- Penalize fine-tuning if documents change frequently.
- Accuracy is important, but must be balanced with cost and timeline.
- Prefer phased / practical MVP strategies.
- Consider future scalability but prioritize MVP delivery.

ARCHITECTURE OPTIONS:

Option A: Simple RAG with vector database + hosted LLM API
Option B: Fine-tune an open-source LLM on all documents
Option C: Keyword search only (no LLM)
Option D: Agentic multi-step system with retrieval + reranking + citation verification

---

SCORING SCALE:
1 = very poor
5 = excellent

---

OUTPUT FORMAT (STRICT JSON ONLY):

{
  "architecture_scores": [
    {
      "option": "",
      "accuracy": 0,
      "cost_efficiency": 0,
      "privacy": 0,
      "timeline_fit": 0,
      "scalability": 0,
      "citation_reliability": 0,
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





REPHRASE_AND_RESPOND_1 = """
You are a senior AI product strategist.

Use the Rephrase-and-Respond technique.

STEP 1: Rephrase the vague business request into a clear, structured problem statement.
- Convert abstract goals into measurable, operational objectives.
- Define what "productivity" and "visibility" could realistically mean.
- Remove ambiguity.

STEP 2: Based on the clarified problem, propose a practical AI solution.
- Must be realistic and implementable.
- Avoid generic transformation or vague AI adoption statements.
- Focus on a specific use case.

ORIGINAL REQUEST:
"We need AI to improve operations and reduce manual work. Build something that helps teams become more productive and gives leadership better visibility."

---

OUTPUT FORMAT (STRICT JSON ONLY):

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

---

RULES:
- Do NOT remain vague.
- Convert "productivity" into measurable metrics (e.g., time saved, task automation rate).
- Convert "visibility" into dashboards, KPIs, reporting systems.
- Propose ONE focused AI system, not a broad AI strategy.
- Ensure solution is implementable in a real organization.
"""






REPHRASE_AND_RESPOND_2 = """
You are a senior software architect and requirements analyst.

Use the Rephrase-and-Respond technique:

STEP 1: Rephrase the vague product requirement into a clear, testable technical requirement.
- Identify missing details
- Remove vague terms like "properly", "fast", "secure"
- Convert them into measurable engineering requirements

STEP 2: Based on the clarified requirement, propose a realistic system design approach.

ORIGINAL REQUIREMENT:
"Create an AI feature where users can upload files and ask things and the system should answer properly. It should be secure and fast and should not give wrong answers."

---

IMPORTANT RULES:
- Convert vague terms into measurable constraints:
  - "fast" → latency targets (e.g., < 2s response time)
  - "secure" → authentication, encryption, access control
  - "properly / not wrong" → factual grounding, retrieval systems, hallucination reduction methods
- Identify missing requirements explicitly
- Do NOT assume unrealistic guarantees like “never give wrong answers”
- Propose practical engineering architecture

---

OUTPUT FORMAT (STRICT JSON ONLY):

{
  "rephrased_requirement": "",
  "functional_requirements": [],
  "non_functional_requirements": [],
  "security_requirements": [],
  "acceptance_criteria": [],
  "recommended_solution_approach": "",
  "open_questions": []
}

---

GUIDELINES:

Functional requirements:
- file upload
- document parsing
- Q&A system
- retrieval system

Non-functional:
- latency
- scalability
- accuracy expectations (probabilistic, not absolute)

Security:
- authentication
- authorization
- encryption
- data isolation

Acceptance criteria:
- measurable test conditions (NOT vague statements)

Solution approach:
- recommend practical architecture (likely RAG-based system)

Open questions:
- missing requirements (file types, size limits, user roles, etc.)
"""