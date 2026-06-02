# Assignment 01 - Prompt Engineering

## Participant Name
Taniya Gupta

## Description

This document accompanies the code submission for the Prompt Engineering Evaluation. For each technique and each case, it provides a short introduction and a brief analysis of what worked, what could go wrong, and how to improve it.

## How to Run

1. Configure .env with your GROQ_API_KEY.
2. Run the cells related to each case in main.ipynb file.

## Libraries and frameworks
Please refer to requirements.txt for libraries and frameworks required.

---

## Section 1 — Zero-Shot Prompting

### What Zero-Shot Prompting Is

Zero-shot prompting means giving the model a task with no worked examples. The model has to rely entirely on the instructions, the role it is given, and any criteria or schemas you embed in the prompt.


---

### Case 1.1 — Zero-Shot Risk Classification for Vendor Onboarding

**The Problem**
A procurement team has collected an unstructured note about a new AI vendor called DocuMind AI. The model needs to classify the vendor as LOW, MEDIUM, HIGH, or CRITICAL risk and explain why, without being shown any examples of how to do it.

**The Prompt Design**
The body of the prompt structures risk across five dimensions-privacy and data governance, compliance and certification, operational and technical risk, pricing and commercial risk, and vendor maturity. Each dimension includes specific signals to look for. 

The prompt also instructs the model to find **implicit** risks — risks that are not directly stated in the vendor note. 

**What to Expect from the Output**
The expected risk level is HIGH. The vendor has SOC 2 Type I but not Type II, does not offer data residency, uses customer data for product improvement unless manually opted out, has undocumented API rate limits, has only been operating for 18 months, and has 12 enterprise customers.

---

### Case 1.2 — Zero-Shot Executive Decision Memo

**The Problem**
A COO needs a decision memo about whether to deploy a GenAI chatbot for first-level customer support. The situation involves financial trade-offs, compliance concerns, change management risks, and a missing AI governance policy. The model must reach a clear decision.

**The Prompt Design**
The most important instruction in this prompt is the model is told it is an executive advisor. Without it, models describe all sides of the issue and leave the decision to the reader. With it, they commit to a recommendation.

**What to Expect from the Output**
The expected decision is APPROVE_WITH_CONDITIONS. The financial case is plausible at the high end of the estimate, but the compliance risk, the governance gap, and the change management challenge all require specific conditions to be met before go-live.

**What Could Go Wrong**
Without the financial math cues, models often produce ROI statements that are vague or directionally wrong. Without framing governance as a blocker, models may acknowledge it as a concern but still issue an unconditional approval. The persona instruction does most of the heavy lifting here.

**How to Improve It**
Provide an assumed agent cost (for example, $35 per hour and five hours per ticket handled) so the payback calculation is grounded in real inputs rather than model estimation. Adding a `"payback_analysis"` field to the output schema would also force the model to show its arithmetic.

---

## Section 2 — Few-Shot Prompting

### What Few-Shot Prompting Is

Few-shot prompting means giving the model examples before asking it to handle new inputs. The examples teach the model how to label things, where to draw boundaries, and what edge cases look like. 

---

### Case 2.1 — Few-Shot Customer Ticket Intent Classification

**The Problem**
A company receives support tickets and needs each one classified into one of six categories: BILLING_ISSUE, TECHNICAL_BUG, ACCOUNT_ACCESS, FEATURE_REQUEST, COMPLIANCE_CONCERN, or ESCALATION_RISK. Each ticket also needs a priority level: LOW, MEDIUM, HIGH, or URGENT.

**The Prompt Design**
The prompt provides seven examples. The first few cover straightforward cases, a billing dispute, a performance bug, a feature request. The later examples target the boundaries that matter most.

**What to Expect from the Output**
Ticket 1 should be ESCALATION_RISK / URGENT. Ticket 2 should be TECHNICAL_BUG / HIGH. Ticket 3 should be FEATURE_REQUEST / LOW. Ticket 4 should be COMPLIANCE_CONCERN / HIGH. Ticket 5 should be ACCOUNT_ACCESS / HIGH.

**What Could Go Wrong**
Ticket 4 is the most likely to be misclassified. The question about AI model training sits at the boundary between compliance and technical interpretation. Without Example 7 acting as a precedent, many models default to TECHNICAL_BUG.

**How to Improve It**
Add a `secondary_category` field for borderline cases.

---

### Case 2.2 — Few-Shot Transformation from Requirement to API Contract

**The Problem**
An AI-powered leave management assistant must convert natural language requests into structured API contracts. Some requests are complete; others are missing required information and must trigger clarification.

**The Prompt Design**
The model is explicitly told never to invent dates, never to assume leave types, and never to mark `requires_clarification` as false unless all required fields are present.

Seven examples cover full coverage: complete requests, partial requests, ambiguous requests, and policy queries. Roughly half require clarification, teaching the model that incompleteness is normal.

**What to Expect from the Output**
Fully specified requests should return API. Incomplete requests should return `requires_clarification: true` with a question.

**What Could Go Wrong**
Models may still infer dates despite explicit instructions, especially without a reference “today” date.

**How to Improve It**
Inject a runtime “current date” and allow safe relative date resolution only when explicitly unambiguous.

---

## Section 3 — Chain-of-Thought Style Reasoning

### What Chain-of-Thought Reasoning Is

Chain-of-thought prompting structures multi-step reasoning so the model explicitly follows intermediate steps before producing a final answer. This reduces skipped logic and improves reliability for decision tasks.

---

### Case 3.1 — Business ROI Decision with Hidden Trade-Offs

**The Problem**
A retail company evaluates an AI recommendation engine under a 12-month payback constraint.

**The Prompt Design**
The prompt enforces step-by-step computation:

- Convert revenue → gross profit
- Subtract operating costs
- Compute net benefit
- Account for implementation delay correctly
- Apply decision thresholds explicitly


**What to Expect**
Likely outcome: APPROVE_WITH_CONDITIONS due to strong high-case ROI but weak low-case performance.

**What Could Go Wrong**
Models may still use revenue instead of profit.

**How to Improve It**
Enforce temperature = 0 for deterministic result.

---

### Case 3.2 — Root Cause Analysis for ML Model Performance Drop

**The Problem**
A fraud model shows degraded precision and recall.

**The Prompt Design**
The prompt forces evaluation across predefined hypotheses.

**What Could Go Wrong**
Models may default to “retrain model” instead of diagnosing root cause.

**How to Improve It**
Add time-to-fix estimates for each mitigation strategy.

---

## Section 4 — LLM-as-Judge

### What LLM-as-Judge Is

LLMs evaluate outputs using structured rubrics. Quality depends on rubrics.

---

### Case 4.1 — Customer Support Response Evaluation

**What Works**
Rubric penalises deflection, rewards empathy and ownership, and prevents unconditional refund promises.

**Risk**
Model may overvalue politeness.

**Improvement**
Add calibration examples before scoring.

---

### Case 4.2 — Code Explanation Evaluation

**What Works**
Technical correctness explicitly weighted.

**Risk**
Simpler but incorrect explanations may be over-scored.

**Improvement**
Require quoted evidence for penalties.

---

## Section 5 — Self-Consistency

### What It Is

Multiple runs with aggregation to reduce randomness.

---

### Case 5.1 — Policy Interpretation

Correct answer depends on strict rule ordering.

**Risk**
All runs converge on wrong logic → amplified error.

---

### Case 5.2 — Logical Deduction

Tests rule precedence (VPN override).

**Risk**
Numeric anchors bias results.

---

## Section 6 — Tree-of-Thought

### What It Is

Branch-by-branch evaluation before final decision.

---

### Case 6.1 — Use Case Selection

**Best option:** HR assistant due to low risk and high feasibility.

---

### Case 6.2 — Architecture Selection

**Best option:** RAG system.

---

## Section 7 — Rephrase-and-Respond

### What It Is

Clarify vague input before solving.

---

### Case 7.1 — Business Request

Turns vague operational goal into measurable system.

---

### Case 7.2 — Technical Requirement

Transforms vague PM request into engineering spec.

---

## Final Summary

### Key Principles

- Role assignment drives reasoning style
- Embed domain knowledge explicitly
- Design for failure modes