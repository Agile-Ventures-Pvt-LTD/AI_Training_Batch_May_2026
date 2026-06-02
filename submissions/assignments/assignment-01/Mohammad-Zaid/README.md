# Assignment 01 - Prompt Engineering

##  Participant Name  
Mohammad Zaid 

## Assignment Title  
Prompt Engineering Evaluation  

## Short Description  
This project demonstrates multiple types of **prompt engineering techniques** including **zero-shot prompting**, **few-shot prompting**, **chain-of-thought prompting**, **LLM-as-Judge**, **self-consistency prompting**, **tree-of-thought prompting**, and **rephrase-and-respond**.  
Each case explores prompt design, schema enforcement, and common failure modes.  

## Steps to Run the Code  
- Clone the repository.  
- Navigate to the project folder.
- Install Requiremnts  
```bash
pip install -r requirements.txt
```
- Run the notebook or script for each case (e.g., `case1_zero_shot.ipynb`).  
- Outputs are saved in the `outputs/` folder.  


## Libraries or Packages Required  
- Python 3.9+  
- groq 1.2+
- python-dotenv 1.2+
- Groq/LLM API client  
- Jupyter Notebook  
- JSON library  
  

## 6. Output Explanation  
Outputs for each case are stored in the `outputs/` folder. Each includes:  
- Structured JSON responses.  
- Example failure modes (e.g., schema drift, overconfidence, misclassification).  
- Reasoning steps for chain-of-thought and tree-of-thought prompts.  


## Case 1.1 – Zero-Shot Risk Classification for Vendor Onboarding

### Prompt Design

- System prompt defines role as risk assessor with schema discipline.  
- User prompt provides vendor details without examples, forcing the model to classify risk level.  
- Schema enforces structured output: risk level, key factors, missing info, recommendation, confidence.

### Failure Modes

- **Generic procurement language** instead of specific risks.  
- **Missed implicit risks** (e.g., vendor maturity, pricing volatility).  
- **Overconfidence** in scoring without justification.  
- **Schema drift** if model outputs text outside **JSON**.

---

## Case 1.2 – Zero-Shot Executive Decision Memo

### Prompt Design

- Prompt enforces decision-oriented output, not summary.  
- Schema requires explicit decision, rationale, financial, operational, people, compliance, conditions.  
- Constraints prevent overpromising automation benefits.

### Failure Modes

- **Summarization instead of decision**.  
- **Ignoring compliance/governance risks**.  
- **Overemphasis on **ROI**** without change management.  
- **Incomplete schema fields**.

---

## Case 2.1 – Few-Shot Customer Ticket Intent Classification

### Prompt Design

- Few-shot examples teach boundaries: billing vs bug, compliance vs feature request.  
- Schema enforces ticket, category, priority, justification.  
- Examples include ambiguity and tone sensitivity.

### Failure Modes

- **Overfitting to examples** (model may misclassify novel tickets).  
- **Tone misinterpretation** (angry tone ≠ escalation risk).  
- **Category confusion** between compliance and technical bug.  
- **Priority inflation** if tone dominates.

---

## Case 2.2 – Few-Shot Transformation from Requirement to API Contract

### Prompt Design

- Examples show valid and incomplete requests.  
- Schema enforces action, parameters, clarification flag, question, confidence.  
- Constraints prevent invention of dates/types.

### Failure Modes

- **Invented payloads** when info missing.  
- **Ignoring clarification flag**.  
- **Ambiguous dates mishandled** (e.g., “next Friday”).  
- **Schema errors** if clarification not properly set.

---

## Case 3.1 – Chain-of-Thought ROI Decision with Hidden Trade-Offs

### Prompt Design

- System prompt enforces numerical reasoning.  
- Schema requires ranges for revenue, profit, net benefit, payback, plus decision and assumptions.  
- Constraints force use of gross margin, not revenue.

### Failure Modes

- **Incorrect payback math** (using revenue instead of profit).  
- **Ignoring implementation time**.  
- **Over-simplified reasoning summary**.  
- **Generic approval language**.

---

## Case 3.2 – Chain-of-Thought Root Cause Analysis for ML Model Performance Drop

### Prompt Design

- Prompt enforces structured reasoning: causes, evidence, diagnostics, actions.  
- Constraints prevent false pipeline failure claims.  
- Schema ensures separation of short vs long-term actions.

### Failure Modes

- **Generic retrain-only answer**.  
- **Confusion between data drift vs concept drift**.  
- **Ignoring promotional campaign impact**.  
- **Overgeneralization** without diagnostics.

---

## Case 4.1 – LLM-as-Judge: Customer Support Responses

### Prompt Design

- Prompt enforces rubric: clarity, correctness, schema adherence.  
- Schema requires scores, strengths, weaknesses, winner, reasoning summary.  
- Constraints penalize vague/dismissive answers and refund promises without verification.

### Failure Modes

- **Length bias** (preferring longer response).  
- **Ignoring refund verification rule**.  
- **Generic scoring** without justification.  
- **Tie overuse** when model avoids judgment.

---

## Case 4.2 – LLM-as-Judge: Code Explanation Quality

### Prompt Design

- Prompt enforces evaluation of clarity, correctness, usefulness.  
- Schema requires scores, issues, overall score, winner, reasoning summary.  
- Constraints penalize oversimplification and misleading claims.

### Failure Modes

- **Rewarding oversimplification** (“deep copy always better”).  
- **Ignoring beginner usefulness**.  
- **Failure to detect technical inaccuracies**.  
- **Schema drift** if scores not numeric.

---

## Case 5.1 – Self-Consistency for Complex Policy Interpretation

### Prompt Design

- Prompt enforces multiple independent runs (≥5).  
- Schema requires individual answers, final amount, consistency count, decision, reasoning summary.  
- Constraints exclude alcohol, apply international uplift + same-day rule.

### Failure Modes

- **Order of rules misapplied** (uplift before/after 50% rule).  
- **Alcohol not excluded**.  
- **Too few runs** (less than 5).  
- **Consensus failure** if outputs diverge.

---

## Case 5.2 – Self-Consistency for Logical Deduction

### Prompt Design

- Prompt enforces ≥5 runs with majority vote.  
- Schema requires runs, votes, final risk, disagreement analysis, reasoning summary.  
- Constraints clarify Germany is known country/**VPN**, downloads alone ≠ **HIGH** risk.

### Failure Modes

- **Incorrect **HIGH** risk flag** due to file downloads.  
- **Ignoring **VPN** rule**.  
- **Consensus drift** if outputs split.  
- **Weak disagreement analysis**.

---

## Case 6.1 – Tree-of-Thought: Selecting Best AI Automation Use Case

### Prompt Design

- Prompt enforces evaluation across five dimensions with trade-offs.  
- Schema requires scores, trade-offs, recommended option, why not others, final recommendation.  
- Constraints prevent choosing only on business value.

### Failure Modes

- **Single-factor bias** (choosing only on cost or value).  
- **Ignoring risk scoring inversion** (lower risk = higher score).  
- **Weak trade-off explanation**.  
- **Generic recommendation**.

---

## Case 6.2 – Tree-of-Thought: Architecture Selection

### Prompt Design

- Prompt enforces evaluation across accuracy, cost, privacy, timeline, scalability, citation reliability.  
- Schema requires scores, recommended architecture, rationale, risks, mitigations, **MVP** plan.  
- Constraints penalize fine-tuning, enforce 6-week **MVP**, avoid blind complexity.

### Failure Modes

- **Choosing complex option blindly**.  
- **Ignoring **MVP** timeline**.  
- **Overvaluing accuracy without cost/privacy trade-offs**.  
- **Weak phased approach rationale**.

---

## Case 7.1 – Rephrase-and-Respond: Ambiguous Business Request

### Prompt Design

- Prompt enforces rephrasing vague stakeholder input into measurable problem.  
- Schema requires problem, assumptions, solution, users, features, data, metrics, steps, risks.  
- Constraints prevent generic answers and enforce measurable outcomes.

### Failure Modes

- **Generic productivity language**.  
- **Over-scoping transformation program**.  
- **Ambiguity leakage** in rephrased problem.  
- **Invented assumptions**.

---

## Case 7.2 – Rephrase-and-Respond: Poorly Written Technical Requirement

### Prompt Design

- Prompt enforces rephrasing vague requirement into clear technical spec.  
- Schema requires functional, non-functional, security, acceptance criteria, solution approach, open questions.  
- Constraints prevent overcommitment to “never wrong answers.”

### Failure Modes

- **Overcommitment** to unrealistic guarantees.  
- **Unmeasurable definitions** (“fast,” “secure”).  
- **Incomplete clarification** (missing file formats, auth).  
- **Overengineering** beyond **MVP**.

---

## Final Note

Each case includes:  
- Prompt design rationale.  
- Failure mode analysis.  
- Outputs saved in `outputs/` folder per case.