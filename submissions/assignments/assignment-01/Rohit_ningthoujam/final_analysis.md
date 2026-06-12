
# 1. Zero-Shot Prompting


## Case 1.1 - Vendor Risk Classification

### Prompt Design Analysis
The prompt used clear instructions and a strict JSON schema...

### Why the Prompt Worked
- Clear constraints improved structured reasoning
- Risk categories guided the model properly

### Failure Modes
- Confidence scores were inconsistent
- Some responses were too verbose

### Improvements
- Add stricter formatting rules
- Improve risk prioritization instructions

### Conclusion
The zero-shot prompt successfully classified vendor risks...


## Case 1.2 – Zero-Shot Executive Decision Memo

### Prompt Design Analysis
The prompt was designed to make the model behave like an executive advisor instead of a summarizer. It included business constraints related to ROI, governance, compliance, operational impact, and workforce concerns. A structured schema ensured decision-focused outputs.

### Why the Prompt Worked
- The model generated actionable recommendations instead of summaries.
- Instructions encouraged balanced evaluation of:
  - financial ROI
  - compliance risks
  - people impact
  - AI governance gaps
- The schema improved output organization and readability.
- Constraints prevented unrealistic automation promises.

### Failure Modes
- Some outputs focused too heavily on cost savings.
- The model occasionally underexplored governance risks.
- Certain responses became overly optimistic about chatbot adoption.
- Conditions for approval were sometimes too generic.

### Improvement Suggestions
- Add stronger governance evaluation instructions.
- Include explicit change-management considerations.
- Require measurable ROI assumptions.
- Add constraints against unsupported productivity claims.




# 2.  Few-Shot Prompting


## Case 2.1 – Few-Shot Customer Ticket Intent Classification
The few-shot prompt was designed using multiple labeled examples to teach the model how to classify customer support tickets into predefined categories. The examples included both straightforward and ambiguous cases so the model could learn category boundaries, urgency handling, and expected output structure.

The prompt demonstrated:
- billing complaints
- technical issues
- account access problems
- compliance concerns
- feature requests
- escalation scenarios

It also clarified that emotional tone increases priority but does not automatically change the category.

### Why the Prompt Worked
- Examples improved the model’s understanding of classification boundaries.
- Ambiguous examples helped the model generalize better to real-world tickets.
- The prompt separated issue category from urgency level.
- JSON schema instructions improved structured output consistency.
- The model learned to distinguish compliance concerns from technical bugs.

### Failure Modes
- Some billing complaints with angry tone were incorrectly classified as escalation risks.
- Multi-intent tickets occasionally confused the model.
- Priority levels were sometimes inconsistent across similar tickets.
- Certain justifications became unnecessarily verbose.

### Improvement Suggestions
- Add more edge-case examples with overlapping intents.
- Include stricter instructions for selecting the primary category.
- Add output validation for allowed labels.
- Limit justification length for cleaner responses.


# 3. COT

## Case 1.1 – Chain-of-Thought Customer Ticket Classification

The CoT prompt guided the model to reason step-by-step before classifying customer tickets by analyzing intent, urgency, and emotional tone.

### Why it worked
- Improved handling of ambiguous tickets
- Better separation of emotion vs intent
- Reduced random guessing
- Improved generalization

### Failure Modes
- Overly verbose reasoning
- Occasional overthinking simple cases
- Format drift in structured output
- Bias toward escalation in emotional tickets

### Improvements
- Enforce strict JSON final output
- Limit reasoning steps (3–5)
- Separate reasoning and final answer clearly
- Add few-shot CoT examples
## Case 3.2 – Root Cause Analysis (ML Performance Drop)

The prompt enabled structured diagnosis of fraud model degradation using drift types, operational changes, and system signals.

### Why it worked
- Clear drift categorization improved reasoning
- Structured JSON ensured consistency
- Strong constraints prevented naive retraining responses
- Multi-factor inputs improved system-level thinking

### Failure Modes
- Overuse of retraining suggestion
- Drift type confusion
- Generic diagnostics
- Underweighted key features (payment channel shift)

### Improvements
- Add few-shot RCA examples
- Prioritize evidence weighting
- Limit number of causes
- Add channel-wise performance analysis


# LLM AS JUDGE 
## Case 4.1 – LLM-as-Judge: Customer Support 
This case evaluates two AI-generated customer support responses using a structured LLM-as-judge rubric across empathy, clarity, actionability, and policy correctness.

---

### Why the Prompt Worked
- Multi-dimensional scoring improved evaluation quality
- Structured rubric reduced subjective bias
- Policy constraints prevented incorrect refund decisions
- Forced comparison ensured fair ranking
- JSON output ensured consistency

---

### Failure Modes
- Bias toward longer responses
- Score inconsistency across runs
- Difficulty balancing empathy and policy correctness
- Occasional generic reasoning summaries
- Minor randomness in evaluation

---

### Improvements
- Add few-shot judge examples
- Define strict scoring anchors
- Normalize metric weights
- Add calibration step
- Require evidence-based scoring justification


## Case .2 – LLM-as-Judge: Code Explanation Quality Evaluation

This case evaluates two explanations of shallow copy vs deep copy in Python using an LLM-as-judge approach. The goal is to assess technical correctness, clarity, beginner usefulness, and completeness.

---

### Why the Prompt Worked
- Focused on educational evaluation rather than preference
- Clear scoring dimensions reduced subjectivity
- Explicit constraint prevented misleading simplifications
- Forced detection of incorrect claims (especially deep copy misunderstanding)
- Schema structure ensured consistent evaluation

---

### Failure Modes
- Model may still slightly favor simpler explanations
- Risk of under-penalizing partially correct but misleading statements
- Some variability in scoring across runs
- Difficulty balancing clarity vs technical depth
- Occasional generic justification in reasoning summary

---

### Improvements
- Add few-shot correct vs incorrect explanation examples
- Define strict scoring anchors for each metric
- Add penalty rules for misleading simplifications
- Require explicit correction notes in issues field
- Improve consistency via calibration examples



# 5. SELF CONSISTENCY 

## Case 5.1 – Self-Consistency: Policy Reimbursement Calculation

This case applies self-consistency prompting to a complex reimbursement policy involving multiple interacting rules such as international travel uplift, same-day travel reduction, and non-reimbursable alcohol expenses.

The model was executed multiple times independently to reduce reasoning variance and improve reliability of final numerical output.

---

### Why the Prompt Worked
- Multiple independent runs reduced reasoning randomness
- Majority voting improved numerical stability
- Forced short output reduced explanation noise
- Captured different interpretations of rule ordering
- Improved robustness for multi-rule policy reasoning

---

### Failure Modes
- Variation in rule ordering (uplift vs 50% rule)
- Occasional misinterpretation of alcohol exclusion timing
- Some runs ignored international uplift
- Minor numeric inconsistencies across generations
- Sensitivity to rule prioritization

---

### Improvements
- Add explicit rule precedence hierarchy
- Force step-by-step intermediate structured reasoning before final number
- Increase number of runs (5 → 7 or 9)
- Add validation rules for alcohol exclusion enforcement
- Normalize calculation order across prompts


## Case 5.2 – Self-Consistency for Security Risk Classification

Self-consistency was used to classify security risk based on login behavior, MFA failures, VPN detection, and file download activity. Multiple independent runs helped reduce inconsistent rule interpretation.

### Why the Prompt Worked
- Reduced over-triggering of HIGH risk through majority voting  
- VPN exclusion rule became more stable across runs  
- Improved separation of MEDIUM vs HIGH classification  
- Reduced single-run reasoning bias  
- Aggregation improved final decision stability  

### Failure Modes
- Overestimation of HIGH risk due to file downloads  
- Confusion between VPN country and new country rule  
- Inconsistent rule prioritization (MFA vs downloads vs time)  
- Occasional ignoring of VPN exclusion rule  
- Threshold sensitivity caused variation in outputs  

### Improvements
- Define strict rule hierarchy (VPN → MFA → downloads → time)  
- Evaluate conditions separately before final classification  
- Use structured reasoning template per run  
- Penalize ignoring VPN rule  
- Increase number of runs for stability  

# 6. Tree of thoughts
## Case 6.1 – Tree-of-Thought: Selecting AI Automation Use Case

The Tree-of-Thought approach was used to evaluate multiple AI automation options by branching reasoning across business value, feasibility, risk, pilot suitability, and adoption. Each option was independently scored before synthesizing a final decision.

---

### Why the Prompt Worked
- Forced comparison across multiple decision dimensions instead of single-factor thinking  
- Encouraged structured scoring for each branch (option)  
- Improved trade-off reasoning between value, risk, and feasibility  
- Reduced bias toward only high business value solutions  
- Enabled systematic evaluation for 90-day pilot constraints  

---

### Failure Modes
- Risk scoring interpretation inconsistencies (high risk vs high score inversion)  
- Some branches overemphasized business value over feasibility  
- Occasional underweighting of implementation complexity  
- Trade-offs not always explicitly balanced across all dimensions  
- Slight inconsistency in normalization of scores across options  

---

### Improvements
- Enforce strict scoring rubric with clear anchors for each score (1–5)  
- Normalize risk scoring explicitly before aggregation  
- Add weighted scoring system for pilot suitability constraints  
- Require explicit comparison matrix between all options  
- Improve consistency in trade-off justification format  

## Case 6.2 – Tree-of-Thought: AI Document QA Architecture Selection

The Tree-of-Thought technique was used to evaluate multiple system architectures for building an AI document question-answering system. The evaluation focused on balancing accuracy, cost, privacy, scalability, and MVP delivery constraints.

The system must support:
- PDF document uploads
- Question answering with citations
- Confidential business data handling
- Fast MVP delivery within 6 weeks
- Scaling from 500 to 20,000 users

---

### Why the Prompt Worked
- Forced structured comparison across multiple architecture strategies  
- Encouraged trade-off analysis instead of “best model bias”  
- Balanced real-world constraints like cost, privacy, and timeline  
- Penalized over-complex solutions not suitable for MVP  
- Included phased deployment thinking for scalability  

---

### Failure Modes
- Tendency to over-rank complex agentic systems  
- Occasional underestimation of MVP timeline constraints  
- Confusion between scalability and accuracy trade-offs  
- Fine-tuning option sometimes overvalued despite data volatility  
- Inconsistent weighting of citation reliability  

---

### Improvements
- Add stricter weighting rules for MVP feasibility  
- Explicit penalty for over-engineering in early stages  
- Enforce timeline-first decision constraint  
- Add structured scoring justification per criterion  
- Improve clarity between retrieval vs training-based approaches  

## 7. REPHRASE AND RESPONSE

## Case 7.1 – Rephrase-and-Respond: Ambiguous Business Request Clarification

The Rephrase-and-Respond technique was used to transform a vague business request into a structured and actionable AI problem definition. The focus was on converting abstract goals like “improve operations” and “increase productivity” into measurable and implementable requirements.

---

### Why the Prompt Worked
- Forced clarification before solution generation  
- Converted vague business language into measurable objectives  
- Reduced hallucination by grounding assumptions  
- Encouraged structured thinking (problem → assumptions → solution)  
- Improved relevance of proposed AI use case  

---

### Failure Modes
- Risk of over-assuming organizational context  
- Potential variation in defining "productivity" metrics  
- Some responses may still be too broad without strict constraints  
- Occasional generic AI solution proposals instead of system-level design  
- Ambiguity in selecting target users if not tightly constrained  

---

### Improvements
- Add stricter definition of measurable KPIs  
- Force domain selection (e.g., HR, finance, operations)  
- Require concrete workflow mapping  
- Include constraint on solution scope (MVP-level system only)  
- Improve separation between assumptions and requirements  

## Case 7.2 – Rephrase-and-Respond Technical Requirement Conversion

The prompt successfully converts a vague product requirement into a structured engineering specification by forcing the model to define functional, non-functional, and security requirements separately. This improves clarity and ensures the output is suitable for system design.

### Why the Prompt Worked
- Forced decomposition of vague terms like "fast" and "secure"
- Encouraged measurable acceptance criteria
- Separated functional vs non-functional concerns
- Prevented unrealistic guarantees like “no wrong answers”

### Failure Modes
- Some outputs may still over-assume system design details
- Security requirements may become generic without constraints
- Non-functional metrics (latency, scale) may vary across runs

### Improvement Suggestions
- Add explicit latency and throughput targets if domain is known
- Include example architecture constraints (RAG, API, vector DB)
- Require justification for each requirement category