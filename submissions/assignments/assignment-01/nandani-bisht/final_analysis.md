# Assignment 01 - Prompt Engineering

## Participant Name
Nandani Bisht

# 2. Project Title
Evaluation of Prompt Engineering Techniques Across Multiple AI Use Cases

# 3. Short Description of What You Have Built

This project evaluates the effectiveness of seven prompt engineering techniques across multiple real-world business and technical scenarios. The goal was to analyze how different prompting strategies influence output quality, consistency, reasoning ability, and decision-making.

The techniques evaluated include:

Zero-Shot Prompting
Few-Shot Prompting
Chain-of-Thought (CoT)
LLM-as-Judge
Self-Consistency
Tree-of-Thought (ToT)
Rephrase-and-Respond

For each technique, multiple test cases were designed, executed, and analyzed to identify strengths, weaknesses, and potential improvements.

# 4. Steps to Run the Code
Prerequisites
Python 3.10+
OpenAI API Key
Required Python packages installed
Installation
pip install -r requirements.txt
Configure Environment Variables

Create a .env file:

OPENAI_API_KEY=your_api_key_here
Execute Individual Cases

Run the corresponding Python script:

python case_1_1_vendor_risk.py
python case_1_2_executive_memo.py
python case_2_1_ticket_classification.py
...
Run Complete Evaluation
python main.py
Generate Final Results

Outputs are generated as structured JSON responses and summarized in the final analysis report.

# 5. Libraries or Packages Required

Required Python libraries:

openai
python-dotenv
pydantic
json
collections
statistics

Example installation:

pip install openai python-dotenv pydantic

Additional libraries may be required depending on implementation details.

## Case 1.1 - Zero-Shot Vendor Risk Classification

### Prompt Design Rationale
The prompt combines a role definition with explicit constraints and a strict JSON schema. No examples are provided. The model is told to act as a vendor risk analyst, and the scenario details are passed directly in the user section. The goal was to check whether the model could identify both obvious and implicit risks without any prior demonstrations.

### What Worked
The model classified the vendor as HIGH risk and correctly identified issues that were not stated outright, like the lack of SOC 2 Type II, multi-tenant architecture, and usage-based pricing risk at scale. The JSON output matched the schema on the first call without needing any post-processing.

### What Failed
The confidence score came back as 0.78 with no explanation for why that specific number was chosen. It feels arbitrary. The model also could have flagged the 18-month operating history more prominently as a maturity risk.

### Improvements
Adding a note to the prompt that ties confidence score to the number of unresolved risk factors would make that field more meaningful. Also worth adding a constraint that asks the model to call out risks that are not explicitly stated in the vendor notes.

---

## Case 1.2 - Zero-Shot Executive Decision Memo

### Prompt Design Rationale
The system prompt positions the model as an executive advisor writing a memo for a COO. The schema forces a decision (APPROVE, REJECT, or APPROVE_WITH_CONDITIONS) along with structured considerations across financial, operational, compliance, and people dimensions.

### What Worked
The model returned APPROVE_WITH_CONDITIONS and gave a reasonable breakdown across all schema fields. It picked up on the missing AI governance policy and flagged the support team's job-loss concern as a people impact item. The schema kept the output focused on decision-making rather than general summarization.

### What Failed
The financial considerations section repeated some points from the rationale. The model also did not quantify the ROI clearly enough given that the numbers were in the scenario.

### Improvements
Adding a constraint that requires the model to cite actual figures from the scenario when filling in financial considerations would tighten that section. A secondary constraint around avoiding repetition across schema fields would also help.

---

## Case 2.1 - Few-Shot Customer Ticket Classification

### Prompt Design Rationale
Five examples were included in the user prompt to teach the model how to distinguish between BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS, FEATURE_REQUEST, COMPLIANCE_CONCERN, and ESCALATION_RISK. The examples were chosen to cover boundary cases: angry tone vs category, compliance vs technical, and feature request vs billing.

### What Worked
The model classified all five test tickets correctly. It correctly categorized the social media threat as ESCALATION_RISK at URGENT priority, not just a billing issue. The data usage inquiry was correctly identified as a COMPLIANCE_CONCERN rather than a TECHNICAL_BUG.

### What Failed
The justifications are thorough but occasionally over-explain. For the admin account lockout, the justification mentions governance and ROI when a simpler operational explanation would have been enough.

### Improvements
Trimming the justification examples to be more concise would likely produce shorter, cleaner justifications from the model. Adding an example that overlaps billing and compliance would help handle more ambiguous tickets.

---

## Case 2.2 - Few-Shot Leave Request Parsing

### Prompt Design Rationale
The system prompt defines four supported actions and instructs the model to flag missing or ambiguous date information. Five examples were used to teach the format and edge cases like relative dates ("next Friday") and uncertain intent ("sometime next week").

### What Worked
Ambiguous requests were correctly flagged with requires_clarification set to true. The confidence scores reflected the level of specificity in each request.

### What Failed
For "sometime next week" the model still populated an action field rather than returning a lower-confidence placeholder. This could cause downstream issues if the action is used without verifying the clarification.

### Improvements
Adding an example where the action itself is unclear (not just the dates) would help the model handle fully ambiguous requests more carefully.

---

## Case 3.1 - Chain-of-Thought ROI Decision

### Prompt Design Rationale
The system prompt instructs the model to reason through the calculation privately but return only concise summaries. Specific constraints prevent common errors: using gross margin instead of revenue for payback, subtracting operating costs, and separating implementation time from the payback window.

### What Worked
The model calculated a payback range correctly using gross margin and subtracted monthly operating costs before arriving at the net benefit range. The decision to APPROVE came with a clear payback calculation tied to the schema fields.

### What Failed
The ranges given are fairly wide. The model did not perform a sensitivity analysis even though the scenario has enough data to support one.

### Improvements
Explicitly asking for both a conservative and an optimistic scenario in the schema would force the model to show its range calculation more clearly.

---

## Case 3.2 - Chain-of-Thought ML Performance Drop

### Prompt Design Rationale
The system prompt requires the model to distinguish between data drift, concept drift, pipeline failure, and threshold miscalibration. The evidence in the scenario (new payment channel, changed fraud patterns, shifted feature distribution, clean pipeline logs) was designed so the correct answer requires ruling out pipeline failure before attributing the drop to concept drift.

### What Worked
The model correctly identified concept drift and data drift as the most likely causes and did not blame pipeline failure despite the performance drop. It recommended concrete diagnostics like feature distribution analysis before jumping to retraining.

### What Failed
The model listed threshold miscalibration as a possible secondary cause without much evidence, which is borderline correct but could mislead.

### Improvements
Adding a constraint that requires evidence to be cited before listing any cause, even secondary ones, would tighten the analysis.

---

## Case 4.1 - LLM-as-Judge Customer Support

### Prompt Design Rationale
The system prompt defines a five-dimension rubric (empathy, clarity, actionability, policy alignment, tone) and instructs the model to score from 1 to 5. Explicit constraints prevent rewarding length and require penalizing vague or dismissive answers.

### What Worked
The model correctly identified Response B as the winner. It gave Response A low scores on actionability and policy alignment because it did not verify the cancellation before implying a refund was possible. The reasoning summary captured the key difference between the two responses.

### What Failed
Response A received a 3 on empathy, which feels slightly generous given how dismissive the actual text is.

### Improvements
Adding a calibration note to the prompt that shows how to score a response that is polite but unhelpful would help anchor the empathy scores more consistently.

---

## Case 4.2 - LLM-as-Judge (Second Scenario)

### Prompt Design Rationale
Same rubric and schema as Case 4.1. This run tested whether the model would produce consistent scoring across two separate calls with identical prompts and scenarios.

### What Worked
The winner selection and reasoning were consistent with Case 4.1. Response B won for the same structural reasons.

### What Failed
Scores varied slightly between runs, suggesting the judge is not fully stable. At temperature 0.2 there is still some variance.

### Improvements
Running the judge at temperature 0.0 and averaging across two calls would reduce score instability.

---

## Case 5.1 - Self-Consistency Reimbursement

### Prompt Design Rationale
Five independent API calls were made with the same scenario. Each call asked the model to calculate the reimbursable amount based on the policy. Python code then extracted the final_reimbursable_amount from each response and selected the most frequent value.

### What Worked
All five runs returned 37.5, giving a consistency count of 5 out of 5. The calculation logic (international uplift to $75, 50% for same-day travel above 8 hours, minus alcohol) was applied correctly and consistently.

### What Failed
Since all runs agreed, there was nothing to aggregate. A harder scenario where the correct answer is less obvious would better demonstrate the value of self-consistency.

### Improvements
Using a scenario with two defensible answers would show how majority voting corrects for individual run errors.

---

## Case 5.2 - Self-Consistency Security Risk

### Prompt Design Rationale
Five independent runs were made with the security risk scenario. Each run returned a risk level classification. The most common classification across the five runs was selected as the final answer.

### What Worked
The aggregation logic in Python correctly extracted risk levels from each run and applied a Counter to find the majority vote. The model consistently treated Germany as a known country (not a new one) since it appeared in the known countries list.

### What Failed
Some runs may interpret the VPN country rule differently and return MEDIUM where others return CRITICAL. This depends on whether the model applies Rule 3 (both HIGH and MEDIUM conditions true means CRITICAL).

### Improvements
The constraint in the prompt around VPN countries could be stated more directly to reduce ambiguity between runs.

---

## Case 6.1 - Tree-of-Thought Use Case Selection

### Prompt Design Rationale
The model was asked to evaluate four AI use case options across five branches: business value, feasibility, risk, 90-day pilot suitability, and adoption. The system prompt instructs the model to score each dimension separately before arriving at a recommendation.

### What Worked
The model recommended the AI sales proposal generator (Option 2) and clearly explained why the contract risk analyzer (Option 3) was not suitable for a 90-day pilot despite its high business value. The why_not_others field was populated with useful reasoning.

### What Failed
The overall scores appear to weight all five dimensions equally, which may not reflect business priorities. A use case with high business value and low feasibility could end up with a misleadingly low overall score.

### Improvements
Adding an explicit weighting instruction to the prompt (or asking the model to justify its weighting) would make the scoring more defensible.

---

## Case 6.2 - Tree-of-Thought Architecture Selection

### Prompt Design Rationale
Four architecture options for a document QA system were evaluated across accuracy, cost, privacy, timeline, scalability, and citation reliability. The constraints specifically penalize fine-tuning when documents change frequently and require respecting a 6-week MVP timeline.

### What Worked
The model recommended Option A (simple RAG with vector database and hosted LLM API) as the MVP approach and acknowledged that Option D could be used in a later phase. The mvp_plan field provided a phased delivery outline.

### What Failed
The model did not penalize Option A strongly enough for privacy concerns even though documents may contain confidential business data. A hosted LLM API sends data to a third-party service.

### Improvements
Adding a privacy weight or a separate privacy gate to the prompt would force the model to flag Option A's privacy limitation more clearly before recommending it.

---

## Case 7.1 - Rephrase-and-Respond: Vague Operations Request

### Prompt Design Rationale
The stakeholder request was intentionally vague. The model was instructed to first rephrase it into a specific problem statement with measurable outcomes before proposing a solution. This prevents the model from responding to the vague original and forces it to define scope.

### What Worked
The rephrased problem was specific and included measurable targets (20% productivity improvement, 95% data freshness). The proposed solution was scoped to an AI-powered triage engine rather than a broad transformation program.

### What Failed
The implementation steps are detailed but some of them could belong to a later phase. The prompt does not define what counts as MVP scope.

### Improvements
Adding a constraint that limits the proposed solution to what can be delivered in one quarter would force the model to scope more tightly.

---

## Case 7.2 - Rephrase-and-Respond: Vague Technical Requirement

### Prompt Design Rationale
The product manager's requirement used vague language (secure, fast, properly). The model was asked to convert this into testable functional, non-functional, and security requirements before proposing an implementation approach.

### What Worked
The model identified the missing details correctly and produced measurable non-functional requirements with specific latency and accuracy targets. The open questions field called out things the original requirement left undefined.

### What Failed
The model committed to accuracy targets (like 95% factual accuracy) that are difficult to measure without a defined evaluation benchmark. This is a mild version of the overcommitment the prompt was supposed to prevent.

### Improvements
Adding a constraint that requires the model to note when a non-functional requirement needs a defined benchmark before it can be tested would prevent this.

---

## Comparative Summary

This section compares the seven techniques across consistency, prompt effort, and output quality.

Zero-shot prompting worked well when the task had clear decision criteria and a tight schema. The model did not need examples to produce useful output, but it struggled with calibrating open-ended fields like confidence scores. This technique is best suited to classification tasks where the categories and constraints are fully defined.

Few-shot prompting produced the most reliable outputs across the two cases. The examples did real work by teaching the model how to handle boundary cases that would have been ambiguous in a zero-shot setting. The tradeoff is that writing good examples takes time and the examples need to be carefully chosen to avoid anchoring the model too strongly on one pattern.

Chain-of-thought reasoning was the right choice for the numerical and diagnostic tasks. Asking the model to reason privately but output concisely prevented long reasoning chains from cluttering the JSON. The main risk is that the model occasionally leaked confident-sounding but unverified claims into the reasoning summary.

LLM-as-judge worked but is sensitive to prompt calibration. Without anchor examples, scores on dimensions like empathy can drift. The technique is most useful when the rubric is precisely defined and the candidate responses have a clear winner. It becomes less reliable in close comparisons.

Self-consistency added value by confirming answers across multiple independent runs rather than relying on a single call. For the reimbursement case, all five runs agreed, which is useful as a confidence signal. The technique adds API cost and latency, so it is most justified for cases where a wrong answer has downstream consequences.

Tree-of-thought was effective for selection and architecture tasks where there is no single correct answer and trade-offs matter. Breaking the evaluation into branches before synthesizing a recommendation forced the model to address each dimension explicitly rather than jumping to the most obvious choice.

Rephrase-and-respond handled ambiguous inputs better than any of the other techniques would have. By forcing the model to clarify the problem before solving it, the output was more specific and the proposed solution was more defensible. The main limitation is that the rephrased version reflects the model's interpretation, which may not match what the stakeholder actually meant.

Across all seven techniques, schema enforcement and explicit constraints were the most consistent factor in output quality. Prompts that defined exactly what the model should and should not do produced cleaner outputs than prompts that relied on role definition alone.
