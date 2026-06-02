# 1. Name

**Prompt Engineering Evaluation – Comparative Analysis of Prompting Techniques**

---

# 2. Assignment / Project Title

**Evaluation of Prompt Engineering Techniques Across Multiple AI Use Cases**

---

# 3. Short Description of What You Have Built

This project evaluates the effectiveness of seven prompt engineering techniques across multiple real-world business and technical scenarios. The goal was to analyze how different prompting strategies influence output quality, consistency, reasoning ability, and decision-making.

The techniques evaluated include:

* Zero-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought (CoT)
* LLM-as-Judge
* Self-Consistency
* Tree-of-Thought (ToT)
* Rephrase-and-Respond

For each technique, multiple test cases were designed, executed, and analyzed to identify strengths, weaknesses, and potential improvements.

---

# 4. Steps to Run the Code

### Prerequisites

* Python 3.10+
* OpenAI API Key
* Required Python packages installed

### Installation

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

### Execute Individual Cases

Run the corresponding Python script:

```bash
python case_1_1_vendor_risk.py
python case_1_2_executive_memo.py
python case_2_1_ticket_classification.py
...
```

### Run Complete Evaluation

```bash
python main.py
```

### Generate Final Results

Outputs are generated as structured JSON responses and summarized in the final analysis report.

---

# 5. Libraries or Packages Required

Required Python libraries:

```txt
openai
python-dotenv
pydantic
json
collections
statistics
```

Example installation:

```bash
pip install openai python-dotenv pydantic
```

Additional libraries may be required depending on implementation details.

---

# 6. Assumptions Made

### General Assumptions

* GPT-based models follow instructions accurately when schema constraints are clearly defined.
* Lower temperature settings improve consistency for evaluation tasks.
* Structured JSON outputs are easier to validate than free-form text responses.
* Prompt quality significantly affects output reliability.

### Technique-Specific Assumptions

#### Zero-Shot Prompting

* Categories and decision criteria are sufficiently defined in the prompt.
* The model can infer implicit risks without examples.

#### Few-Shot Prompting

* Examples represent the desired output format accurately.
* Boundary cases improve classification performance.

#### Chain-of-Thought

* Internal reasoning improves calculation and diagnostic accuracy.
* Reasoning remains hidden while concise summaries are returned.

#### LLM-as-Judge

* Rubric definitions are sufficient for scoring.
* Consistency improves with lower temperature settings.

#### Self-Consistency

* Majority voting reduces random reasoning errors.
* Multiple independent runs provide a stronger confidence signal.

#### Tree-of-Thought

* Breaking decisions into evaluation branches improves recommendation quality.
* All evaluation dimensions contribute meaningfully to the final decision.

#### Rephrase-and-Respond

* Clarifying ambiguous requirements before solving them improves solution quality.
* The model's interpretation reasonably matches stakeholder intent.

---

# 7. Output Explanation

## Case 1.1 – Zero-Shot Vendor Risk Classification

**Output:** HIGH Risk Classification

**Key Findings:**

* Missing SOC 2 Type II controls
* Multi-tenant architecture concerns
* Usage-based pricing risks
* Limited operating history

---

## Case 1.2 – Zero-Shot Executive Decision Memo

**Output:** APPROVE_WITH_CONDITIONS

**Key Findings:**

* Missing AI governance policy
* People-impact concerns identified
* Financial and operational risks highlighted


## Case 2.1 – Few-Shot Customer Ticket Classification

**Output:**

* Correct classification across all test cases
* Proper handling of escalation and compliance edge cases

---

## Case 2.2 – Few-Shot Leave Request Parsing

**Output:**

* Ambiguous requests correctly flagged
* Confidence scores reflected request specificity

---

## Case 3.1 – Chain-of-Thought ROI Decision

**Output:** APPROVE

**Key Findings:**

* Correct payback calculations
* Net benefit properly computed
* Decision supported by financial analysis

---

## Case 3.2 – Chain-of-Thought ML Performance Drop

**Output:**

* Data drift and concept drift identified
* Pipeline failure correctly ruled out
* Diagnostic recommendations provided

---

## Case 4.1 & 4.2 – LLM-as-Judge

**Output:**

* Response B selected as winner in both evaluations
* Rubric-based scoring applied consistently
* Minor score variance observed between runs

---

## Case 5.1 – Self-Consistency Reimbursement

**Output:**

* Final reimbursable amount: $37.50
* Agreement across all five independent runs

---

## Case 5.2 – Self-Consistency Security Risk

**Output:**

* Majority voting used for final risk classification
* Consistent interpretation of policy rules

---

## Case 6.1 – Tree-of-Thought Use Case Selection

**Output:**

* AI Sales Proposal Generator selected as best pilot candidate
* Multi-dimensional evaluation performed

---

## Case 6.2 – Tree-of-Thought Architecture Selection

**Output:**

* Simple RAG architecture recommended for MVP
* Trade-offs documented across cost, privacy, and scalability

---

## Case 7.1 – Rephrase-and-Respond Operations Request

**Output:**

* Ambiguous request transformed into measurable objectives
* Solution scoped around AI-powered triage

---

## Case 7.2 – Rephrase-and-Respond Technical Requirement

**Output:**

* Vague requirements converted into testable specifications
* Functional, non-functional, and security requirements defined

---

# Comparative Summary

### Most Reliable Technique

**Few-Shot Prompting**

### Best for Reasoning

**Chain-of-Thought**

### Best for Ambiguous Requirements

**Rephrase-and-Respond**

### Best for Complex Decision Making

**Tree-of-Thought**

### Best for Evaluation Tasks

**LLM-as-Judge**

### Best for High-Confidence Outputs

**Self-Consistency**
