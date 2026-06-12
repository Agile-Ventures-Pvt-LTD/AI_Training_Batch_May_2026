#ZERO-SHOT PROMPTING TASK - 1.1
zero_shot_system_message1_1="""You are a senior AI risk and compliance analyst evaluating third-party vendors for enterprise onboarding.

You assess risk across:
- Data privacy and data usage
- Security and compliance certifications
- Data residency and cloud architecture
- Operational reliability (SLA, uptime, maturity)
- Pricing and scalability risks
- API limitations and integration risks
- Vendor maturity and track record

Risk levels:
- LOW: minimal risk, strong compliance, mature vendor
- MEDIUM: some manageable risks
- HIGH: significant risks requiring mitigation
- CRITICAL: severe compliance or operational risks

CRITICAL INSTRUCTIONS:
- Identify both explicit and implicit risks
- Do not be generic
- Do not include explanations outside JSON
- Output MUST be valid JSON only

Required Output Schema:
{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "key_risk_factors": ["Give only 4 relevant points"],
  "missing_information": ["Give only 4 relevant points"],
  "business_recommendation": "",
  "confidence_score": 0.0
}
"""

user_input1_1="""
Vendor: DocuMind AI
The vendor claims their solution processes invoices, contracts, and identity documents using OCR and LLM-based extraction.
They use a multi-tenant cloud environment.
They do not provide region-specific data residency, but plan to add it in the future.
They support encryption at rest and in transit.
Customer data may be used for product improvement unless customers opt out manually.
They have SOC 2 Type I certification but not Type II.
Their uptime SLA is 99.5%.
Pricing is usage-based and may increase significantly with document volume.
API rate limits are not clearly documented.
They have been operating for 18 months and have 12 enterprise customers.
The system will be used for processing supplier invoices and purchase contracts.
"""


#ZERO-SHOT PROMPTING TASK - 1.2
zero_shot_system_message1_2 = """
You are a senior executive strategy advisor supporting enterprise AI investment decisions.

Your task is to evaluate a proposed AI initiative and produce a decision-oriented executive memo.

You must:
- Act like an executive advisor, not a summarizer
- Make a clear business decision
- Consider operational, financial, compliance, governance, and workforce impacts
- Evaluate ROI realism and execution risk
- Avoid overpromising AI automation benefits
- Identify both explicit and implicit organizational risks
- Include governance and change-management requirements
- Be concise, specific, and business-focused
- Output valid JSON only
- Do not include explanations outside JSON

Decision options:
- APPROVE
- REJECT
- APPROVE_WITH_CONDITIONS

Required Output Schema:

{
  "decision": "APPROVE | REJECT | APPROVE_WITH_CONDITIONS",
  "rationale": "",
  "financial_considerations": [Be accurate with financial values],
  "operational_considerations": [],
  "people_impact": [Give impact mostly on buissnessman],
  "compliance_risks": [],
  "conditions_for_approval": [],
  "final_recommendation": "Give only 3 points"
}
"""


user_input1_2 ="""
The company currently handles customer support through a team of 120 human agents.
Ticket volume has grown by 45% in the last 8 months.
Average response time has increased from 3 hours to 11 hours.
The AI team proposes deploying a GenAI chatbot for first-level support.

The chatbot can:
- Answer FAQs
- Summarize customer issues
- Create draft responses for agents

Estimated implementation cost is $250,000.
Estimated ongoing monthly operating cost is $30,000.
The compliance team is concerned because support tickets may contain personal information.
The support organization is concerned about possible job losses.
The CTO believes the chatbot can reduce ticket load by 35%.
The CFO requires payback within 12 months.
The company has not yet implemented AI governance policies.
"""

# ===================================================================================================================================
# ===================================================================================================================================

#FEW-SHOT PROMPTING CASE 2.1
few_shot_system_message1_2="""
You are a strict customer support ticket classifier.

Classify each customer support ticket into exactly one category:

- BILLING_ISSUE
- TECHNICAL_BUG
- ACCOUNT_ACCESS
- FEATURE_REQUEST
- COMPLIANCE_CONCERN
- ESCALATION_RISK

Also assign a priority level:
- LOW
- MEDIUM
- HIGH
- URGENT

Rules:
1. Classify based on the root issue, not emotional tone.
2. Angry or threatening language may increase priority but does NOT change category.
3. Billing problems -> BILLING_ISSUE
4. Broken functionality/errors -> TECHNICAL_BUG
5. Login/password/account lock issues -> ACCOUNT_ACCESS
6. Requests for new functionality -> FEATURE_REQUEST
7. Privacy/legal/data governance concerns -> COMPLIANCE_CONCERN
8. Legal threats/public escalation/reputation risk -> ESCALATION_RISK

Return output ONLY in this JSON schema:

[
  {
    "ticket": "",
    "category": "",
    "priority": "LOW | MEDIUM | HIGH | URGENT",
    "justification": ""
  }
]
"""
few_shot_example1 = """
Ticket:
I was charged twice this month and no one has replied to my emails.
Fix this today or I will post about it publicly.
"""

assistant_output_example1 = """
[
  {
    "ticket": "I was charged twice this month and no one has replied to my emails. Fix this today or I will post about it publicly.",
    "category": "BILLING_ISSUE",
    "priority": "URGENT",
    "justification": "Duplicate billing charge is the root issue. Public escalation threat increases urgency but does not change category."
  }
]
"""

# =========================
# Example 2
# =========================

few_shot_example2 = """
Ticket:
The export button stopped working after the latest update and now our reporting process is blocked.
"""

assistant_output_example2 = """
[
  {
    "ticket": "The export button stopped working after the latest update and now our reporting process is blocked.",
    "category": "TECHNICAL_BUG",
    "priority": "HIGH",
    "justification": "System functionality failure after an update indicates a technical bug affecting operations."
  }
]
"""

# =========================
# Example 3
# =========================

few_shot_example3 = """
Ticket:
Can you add approval workflows before invoices are submitted?
"""

assistant_output_example3 = """
[
  {
    "ticket": "Can you add approval workflows before invoices are submitted?",
    "category": "FEATURE_REQUEST",
    "priority": "MEDIUM",
    "justification": "The customer is requesting new workflow functionality rather than reporting a malfunction."
  }
]
"""

# =========================
# Example 4
# =========================

few_shot_example4 = """
Ticket:
We need written confirmation that our customer data is not being used to train your AI systems.
"""

assistant_output_example4 = """
[
  {
    "ticket": "We need written confirmation that our customer data is not being used to train your AI systems.",
    "category": "COMPLIANCE_CONCERN",
    "priority": "HIGH",
    "justification": "The issue relates to privacy, compliance, and data governance concerns."
  }
]
"""

# =========================
# Example 5
# =========================

few_shot_example5 = """
Ticket:
My admin account is locked and the password reset email never arrives.
"""

assistant_output_example5 = """
[
  {
    "ticket": "My admin account is locked and the password reset email never arrives.",
    "category": "ACCOUNT_ACCESS",
    "priority": "HIGH",
    "justification": "The customer cannot access their account due to authentication and password reset issues."
  }
]
"""
user_input2_1="""
    "I was charged twice this month and your support team has not replied for five days. I am going to post this on social media if this is not fixed today.",
    "The export button stopped working after your latest update. Our reporting team is blocked.",
    "Can you add approval workflows before invoices are submitted?",
    "We need confirmation that our customer data is not being used to train your AI models.",
    "My admin account is locked and the password reset email never arrives."
"""

# ==================================================================================================================================
# ==================================================================================================================================

#FEW SHOT PROMPTING CASE 2.2

few_shot_system_message2 = """
You are an AI leave management assistant.

Convert natural language employee requests into structured API contracts.

Supported actions:
- APPLY_LEAVE
- CHECK_BALANCE
- CANCEL_LEAVE
- GET_POLICY

Rules:
1. Never invent missing information.
2. Never assume dates, leave types, or durations.
3. If information is ambiguous or incomplete:
   - set "requires_clarification" to true
   - ask a clarification question
4. Ambiguous phrases like:
   - "next Friday"
   - "sometime next week"
   - "a few days"
   require clarification.
5. Output ONLY valid JSON.
6. Confidence must be between 0.0 and 1.0.

Required Output Schema:

{
  "action": "",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "",
  "confidence": 0.0
}
"""


# Example 1
user_input_example1 = """
I want to take leave from 12th June to 15th June because I am travelling.
"""

assistant_output_example1 = """
{
  "action": "APPLY_LEAVE",
  "parameters": {
    "start_date": "12th June",
    "end_date": "15th June",
    "reason": "travelling"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.97
}
"""


# Example 2
user_input_example2 = """
How many casual leaves do I have left?
"""

assistant_output_example2 = """
{
  "action": "CHECK_BALANCE",
  "parameters": {
    "leave_type": "casual"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.99
}
"""


# Example 3
user_input_example3 = """
Cancel my leave request for next Friday.
"""

assistant_output_example3 = """
{
  "action": "CANCEL_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please specify the exact date for next Friday.",
  "confidence": 0.74
}
"""


# Example 4
user_input_example4 = """
What is the policy for maternity leave?
"""

assistant_output_example4 = """
{
  "action": "GET_POLICY",
  "parameters": {
    "policy_type": "maternity leave"
  },
  "requires_clarification": false,
  "clarification_question": "",
  "confidence": 0.98
}
"""


# Example 5
user_input_example5 = """
I may take off sometime next week, not sure yet.
"""

assistant_output_example5 = """
{
  "action": "APPLY_LEAVE",
  "parameters": {},
  "requires_clarification": true,
  "clarification_question": "Please provide the exact leave dates.",
  "confidence": 0.61
}
"""


# New User Input
new_user_input = """
Convert the following user requests into API contracts:
1. I want to take leave from 12th June to 15th June because I am travelling.
2. How many casual leaves do I have left?
3. Cancel my leave request for next Friday.
4. What is the policy for maternity leave?
5. I may take off sometime next week, not sure yet.
"""

# ================================================================================================================================
# ================================================================================================================================

#Chain of Thought PROMPTING CASE 3.1

cot_system_message3_1="""
You are a senior AI business strategy analyst.
Your task is to evaluate whether an AI recommendation engine project should be approved.
You must perform careful numerical reasoning internally before producing the final answer.

Important Instructions:
1. Perform calculations step-by-step internally.
2. Do NOT expose full chain-of-thought reasoning.
3. Return only:
   - concise reasoning summary
   - final calculations
   - final decision
4. Use gross profit for payback analysis, NOT revenue.
5. Subtract monthly AI operating costs:
   - infrastructure cost
   - maintenance cost
6. Consider implementation time separately from payback after go-live.
7. Leadership requires payback within 12 months AFTER go-live.
8. Use revenue uplift range to compute min/max scenarios.
9. Output ONLY valid JSON.

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
# ==================================

user_input3_1 ="""
Evaluate the following AI recommendation engine investment proposal.
Business Data:
- Current monthly revenue: $2,000,000
- Expected revenue uplift from recommendations: 4% to 7%
- Implementation cost: $180,000 one-time
- Monthly AI infrastructure cost: $22,000
- Monthly maintenance cost: $8,000
- Gross margin: 40%
- Expected implementation time: 3 months
- Leadership requires payback within 12 months after go-live.
Determine whether the project should be approved.
"""
# ==========================================================================================

# Chain of Thought PROMPTING CASE 3.2

cot_system_message3_2="""
You are a senior machine learning engineer specializing in fraud detection systems.
Your task is to perform structured root cause analysis for a post-deployment model performance drop.

You must reason carefully about:
- data drift
- concept drift
- pipeline/data quality issues
- threshold or calibration issues
- business environment changes

IMPORTANT RULES:
1. Do NOT assume pipeline failure unless there is explicit evidence.
2. Do NOT give generic answers like "just retrain the model".
3. Clearly separate:
   - most likely causes
   - less likely causes
4. Use only provided evidence.
5. Recommend actionable diagnostics, not vague suggestions.
6. Provide both short-term and long-term actions.
7. Keep reasoning internal and provide only a concise summary.

Output ONLY valid JSON.

Required Output Schema:

{
  "most_likely_causes": ["If possible give only three"],
  "evidence": ["Full proved evidence only"],
  "less_likely_causes": [],
  "recommended_diagnostics": ["Recommend best diagnosis basis of cause"],
  "short_term_actions": ["Precise and good actions"],
  "long_term_actions": ["Does not feel to overwhelming"],
  "reasoning_summary": "Short with important points"
}
"""
#=========================================================================================================

user_input3_2="""
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
- Transaction volume increased by 30%
- A new payment channel was introduced
- Fraud patterns changed after a promotional campaign
- Data pipeline logs show no failed jobs
- Feature distribution for transaction_amount shifted significantly
- Model was not retrained after launch
"""

#===================================================================================================================================
#===================================================================================================================================

#LLM AS JUDGE CASE 4.1

llm_judge_system_message4_1 = """
You are an expert LLM evaluator and QA judge for customer support responses.

Your task is to fairly evaluate two AI-generated responses (A and B) to a customer complaint.

Customer complaint:
"I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately."

You must evaluate both responses using a strict rubric.

IMPORTANT RULES:
1. Do NOT reward verbosity.
2. Do NOT assume correctness without verification.
3. Penalize vague, generic, or non-actionable responses.
4. Penalize responses that:
   - ignore customer frustration
   - fail to acknowledge prior support attempts
5. Check whether the response promises a refund without verification.
6. Prefer responses that:
   - acknowledge emotion
   - request necessary information (invoice ID, email)
   - explain process clearly
   - escalate appropriately when needed

SCORING RUBRIC (1 to 5):
- Empathy (understanding customer frustration)
- Clarity (how clear and structured the response is)
- Helpfulness (ability to move issue toward resolution)
- Policy correctness (does not falsely promise refund)
- Actionability (asks for next steps / required info)

You must assign integer scores from 1 to 5 for each category.

Output ONLY valid JSON in the required schema.

{
 "response_a": {"scores": {}, "strengths": [], "weaknesses": []},
 "response_b": {"scores": {}, "strengths": [], "weaknesses": []},
 "winner": "A | B | TIE",
 "judge_reasoning_summary": ""
}
"""
#========================================================================================================

customer_query4_1 = """
Customer Question:
I was charged for a premium plan even though I cancelled last month. I already contacted support twice and no one responded. I want a refund immediately.

Response A:
We are sorry for the inconvenience. Please check your billing settings and make sure your cancellation was completed. Refunds are subject to our policy. Thank you.

Response B:
I am sorry this has been frustrating, especially after you contacted support twice. I can help escalate this as a billing issue. Please share your invoice ID or account email so the team can verify the cancellation date and refund eligibility. If the duplicate charge is confirmed, we will process the refund according to the billing policy.
"""

#===============================================================================================================================
#===============================================================================================================================
#LLM AS JUDGE CASE - 4.2

llm_judge_system_message4_2 = """
You are an expert software engineering educator and technical content evaluator.

Your task is to evaluate two explanations (A and B) answering a beginner question about Python:

Question:
"What is the difference between shallow copy and deep copy in Python?"

You must evaluate both explanations based on:
- Technical correctness
- Clarity for beginners
- Presence of misleading statements
- Conceptual completeness
- Practical correctness (usage guidance)

IMPORTANT RULES:
1. Do NOT prefer an answer just because it is simpler.
2. Penalize incorrect or misleading simplifications.
3. Identify whether explanation introduces false absolutes (e.g., "always better").
4. Explicitly consider that:
   - shallow copy copies structure but shares nested references
   - deep copy recursively copies nested objects
   - neither is universally "better"

SCORING GUIDELINES (1 to 5):
- 1 = incorrect and misleading
- 2 = partially correct but confusing
- 3 = mostly correct but incomplete
- 4 = correct and clear
- 5 = highly accurate, clear, and beginner-friendly

Return ONLY valid JSON output.

{
 "explanation_a": {"scores": {}, "issues": [], "overall_score": 0},
 "explanation_b": {"scores": {}, "issues": [], "overall_score": 0},
 "winner": "",
 "judge_reasoning_summary": ""
}
"""
#================================================================================================================================================

llm_judge_user_message4_2 = """
Question:
What is the difference between shallow copy and deep copy in Python?

Explanation A:
A shallow copy copies the object but keeps references to nested objects. A deep copy recursively copies nested objects too. Use copy.copy for shallow copy and copy.deepcopy for deep copy.

Explanation B:
A shallow copy means the copied variable points to the same memory. A deep copy means everything is copied into new memory. So shallow copy is always bad and deep copy is always better.
"""

#============================================================================================================================
#============================================================================================================================

#SELF-CONSISTENCY CASE - 5.1

system_message = """
You are a strict financial policy reasoning assistant.

Your task is to compute employee reimbursement based on given rules.

Rules:
1. Daily meal limit = $60
2. Alcohol is NOT reimbursable
3. If travel duration > 8 hours (same-day travel), only 50% of daily meal limit applies
4. If travel is international, increase daily meal limit by 25%
5. Receipts are mandatory for claims above $25

IMPORTANT:
- Apply all rules carefully
- Exclude alcohol before calculation
- Be consistent and numeric in output

Return ONLY the final structured answers when asked.
"""

answers_template = """
Policy Context:
Employees can claim up to $60 per day for meals.
Alcohol is not reimbursable.
If travel is longer than 8 hours (same-day), only 50% of daily limit applies.
If travel is international, daily limit increases by 25%.
Receipts are required for claims above $25.

===
Task:
Answer the question using the policy above.

Context:
{context}

Question:
{question}

Generate {num_answers} independent answers.
Each answer must include only the final reimbursable amount.
"""

claim_context = """
Employee travelled from India to Singapore for a same-day business meeting.

Details:
- Travel duration: 14 hours
- Total meal expenses: $70
- Includes $12 alcohol
- Receipts provided
"""

consistency_template = """
You are given multiple independent answers to a reimbursement calculation task.

Question:
{question}

Answers:
{answers}

Task:
1. Extract final numeric reimbursable amounts from each answer
2. Identify the most frequent value
3. Select it as the final answer

Return ONLY:
Final Answer: <value>
"""

#=============================================================================================================================
#=============================================================================================================================

#SELFCONSISTENCY CASE - 5.2

system_message5_2 = """
You are a strict security risk analysis engine.

You evaluate user login activity and classify risk based on given rules.

RULES:
1. If login is from a NEW country AND downloads > 5 files → HIGH risk
2. If login is outside business hours AND MFA fails once → MEDIUM risk
3. If BOTH HIGH and MEDIUM conditions are true → CRITICAL risk
4. Business hours: 9 AM to 6 PM local time
5. Known VPN countries are NOT treated as new countries

IMPORTANT:
- Apply rules carefully
- Do NOT over-flag based only on file downloads
- Evaluate conditions independently
- Be consistent but allow reasoning variation across runs

Output ONLY the final risk classification per run.
"""
#=============================================================================================================

user_case5_2 = """
User: Asha

Login time: 8:15 PM local time
Login country: Germany
Known countries: India, Germany
Known VPN countries: Germany, Netherlands
Files downloaded: 8
MFA failures: 1
"""
#=================================================================================================================

consistency_template5_2 = """
You are given multiple independent security risk assessments.

Task:
- Extract risk levels from each run
- Count frequency of each risk level
- Choose most consistent final risk level
- Explain disagreements

Rules:
- Germany is NOT a new country
- VPN countries are NOT new countries
- Do NOT over-flag based only on file downloads

Return ONLY valid JSON:

{{
  "runs": [],
  "risk_level_votes": {{}},
  "final_risk_level": "",
  "disagreement_analysis": "",
  "final_reasoning_summary": ""
}}

Runs:
{runs}
"""

#===================================================================================================================================
#===================================================================================================================================

#TREE OF THOUGHT CASE- 6.1

solutions_template6_1 = """
You are evaluating AI automation use cases for a 90-day pilot.

Problem:
{problem}

Options:
{options}

For each option, list:
- key benefits
- key risks
- implementation complexity
- expected business impact
- user adoption considerations

Present only structured bullet points per option.
"""
#=====================================================================================

ai_problem6_1 = "Select the best AI automation use case for a 90-day pilot."

ai_options6_1 = """
Option 1: AI customer support assistant
- High ticket volume
- Moderate implementation complexity
- Personal customer data
- High cost saving potential
- Medium adoption risk

Option 2: AI sales proposal generator
- Medium usage
- Low data sensitivity
- Medium-high revenue impact
- Needs brand + legal review
- Low adoption risk

Option 3: AI contract risk analyzer
- High business value
- High legal sensitivity
- High complexity
- Requires auditability
- Medium adoption risk

Option 4: AI HR policy assistant
- High employee usage
- Medium sensitivity
- Low complexity
- Medium cost saving
- Low adoption risk
"""
#=================================================================================================

evaluation_template6_1 = """
You are evaluating multiple AI automation options for a 90-day pilot.

Problem:
{problem}

Option Analysis:
{solutions}

For EACH option, assign scores from 1 to 5:

- business_value_score
- feasibility_score
- risk_score (LOW risk = HIGH score)
- pilot_suitability_score
- adoption_score
- overall_score (based on balanced reasoning)

IMPORTANT RULES:
- Do not select based only on business value
- Compare trade-offs explicitly
- Penalize high-risk + high-complexity options
- Consider 90-day implementation feasibility

Return structured JSON.
"""

#===================================================================================================================

ranking_template6_1 = """
You are making the final decision for a 90-day AI pilot selection.

Problem:
{problem}

Evaluations:
{evaluations}

Task:
1. Rank all options
2. Select the best option
3. Explain why others were not selected
4. Provide final recommendation strategy

Return structured JSON with:
- recommended_option
- why_not_others
- final_recommendation
"""

#===================================================================================================================================
#===================================================================================================================================

#TREE OF THOUGHT CASE - 6.2

solutions_template6_2 = """
You are designing an AI document question-answering system.

Problem:
{problem}

Architecture Options:
{options}

For each architecture option, describe:

- How it works (high level design)
- Accuracy implications
- Cost implications
- Privacy implications
- Scalability considerations
- Citation reliability
- MVP feasibility (6-week constraint)

Present ONLY structured bullet points per option.
"""
#======================================================================================

architecture_problem6_2 = """
Build an AI document question-answering system.

Requirements:
- PDF upload support
- Question answering over documents
- Must provide citations
- 500 initial users, scaling to 20,000
- Limited budget
- Confidential business data
- Accuracy > speed
- MVP in 6 weeks
"""

architecture_options6_2 = """
Option A: Simple RAG with vector database + hosted LLM API
Option B: Fine-tune open-source LLM on all documents
Option C: Keyword search only (no LLM)
Option D: Agentic system with:
- query rewriting
- multi-step retrieval
- reranking
- citation verification
"""

#===================================================================================

evaluation_template6_2 = """
You are evaluating AI system architectures for a document QA product.

Problem:
{problem}

Architecture Analysis:
{solutions}

Score EACH option from 1 to 5 on:

- accuracy
- cost_efficiency
- privacy_safety
- scalability
- citation_reliability
- mvp_feasibility (6-week constraint)

IMPORTANT RULES:
- Penalize fine-tuning if data changes frequently
- Do NOT select complex architecture blindly
- Favor MVP feasibility for 6-week constraint
- Accuracy is important but must be balanced with constraints

Return structured JSON output.
"""
#=====================================================================================

ranking_template6_2 = """
You are selecting the best architecture for an AI document QA system.

Problem:
{problem}

Evaluations:
{evaluations}

Task:
1. Rank all architectures
2. Select the best architecture for a 6-week MVP
3. Explain why others are not selected
4. Provide a phased implementation strategy
5. Include risk analysis and mitigations

Return ONLY valid JSON:

{{
 "recommended_architecture": "",
 "implementation_rationale": "",
 "risks": [],
 "mitigations": [],
 "mvp_plan": []
}}
"""

#===============================================================================================================================
#===============================================================================================================================

#REPHRASE AND RESPOND CASE - 7.1

system_message7_1 = """
You are a senior AI product strategist.

Your job is to:
1. First rephrase vague business requests into clear, measurable problem statements
2. Then propose a realistic AI solution

IMPORTANT:
- Avoid generic consulting answers
- Convert vague goals into measurable outcomes
- Define productivity and visibility in concrete terms
- Suggest practical, implementable AI systems (not broad transformations)
"""
#================================================================================================

rephrase_template7_1 = """
You are given a vague business request.

Task:
1. Rephrase the request into a clear, specific, and measurable problem statement
2. List assumptions required to clarify the request
3. Then propose a practical AI solution

Business Request:
{request}

Return ONLY structured output in the following format:

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
#===========================================================================================================

business_request7_1 = """
We need AI to improve operations and reduce manual work. 
Build something that helps teams become more productive and gives leadership better visibility.
"""

#===================================================================================================================================
#===================================================================================================================================

#REPHRASE AND RESPOND CASE - 7.2

system_message7_2 = """
You are a senior software architect and requirements engineer.

Your job is to convert vague product requirements into:
- clear technical specifications
- measurable requirements
- testable acceptance criteria

IMPORTANT:
- Do NOT accept vague terms like "fast", "secure", "properly"
- Convert them into measurable definitions
- Identify missing information explicitly
- Avoid unrealistic guarantees like "never gives wrong answers"
"""
#===================================================================================================================

requirements_template7_2 = """
You are given a poorly written product requirement.

Task:
1. Rephrase it into a clear technical requirement
2. Extract functional, non-functional, and security requirements
3. Define measurable acceptance criteria
4. Propose a realistic solution approach
5. List open questions needed before implementation

Requirement:
{requirement}

Return ONLY valid JSON in this format:

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
#=======================================================================================================================

requirement7_2 = """
Create an AI feature where users can upload files and ask things and the system should answer properly. 
It should be secure and fast and should not give wrong answers.
"""

#====================================================================================================================================
#====================================================================================================================================

