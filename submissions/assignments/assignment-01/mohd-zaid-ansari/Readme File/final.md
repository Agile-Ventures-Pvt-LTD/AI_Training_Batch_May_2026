# Assignment 01 - Prompt Engineering

## Participant Name

Mohd Zaid Ansari

## 2. Assignment 

**Advanced Prompt Engineering Techniques using LLMs**

## 3. Short Description

This project demonstrates multiple prompt engineering techniques using LLMs for structured reasoning, decision-making, classification, evaluation, and AI workflow analysis. Techniques implemented include Zero-Shot, Few-Shot, Chain-of-Thought, LLM-as-Judge, Self-Consistency, Tree-of-Thought, and Rephrase-and-Respond prompting.

## 4. Steps to Run the Code

```bash
uv init
uv venv
uv add -r requirements.txt
```

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Run files:

```bash
python groq_cleint.py
python prompts.py
```

Finally run:

```bash
main.ipynb
```

## 5. Libraries / Packages Required

* Python 3.x
* groq
* python-dotenv
* jupyter
* uv

## 6. Assumptions Made

* Python and uv are installed
* Valid Groq API key is available
* Internet connection is required
* Prompts are evaluated using structured JSON outputs
* Notebook cells are executed sequentially

## 7. Output Explanation

The project generates structured JSON outputs for:

* Risk assessment
* Ticket classification
* API transformation
* Financial reasoning
* ML debugging
* AI solution evaluation
* Multi-option decision analysis

---

# Prompting Technique Summaries

### Case 1 — Zero-Shot Prompting

Uses strong role definition and evaluation criteria without examples. Focuses on ROI, governance, privacy, scalability, vendor risk, and structured JSON outputs. Helps reduce vague or hallucinated responses.

### Case 2 — Few-Shot Prompting

Uses labeled examples to teach category boundaries, API transformation logic, ambiguity handling, and clarification requests. Improves classification consistency and schema accuracy.

### Case 3 — Chain-of-Thought Prompting

Applies stepwise reasoning for financial calculations and ML debugging tasks. Separates assumptions, calculations, and decisions to improve analytical accuracy.

### Case 4 — LLM-as-Judge Prompting

Evaluates candidate outputs using scoring rubrics across accuracy, clarity, empathy, actionability, and policy compliance. Produces structured comparison results.

### Case 5 — Self-Consistency Prompting

Runs multiple independent reasoning passes and aggregates results using majority consistency. Improves reliability for logical and rule-based tasks.

### Case 6 — Tree-of-Thought Prompting

Explores multiple reasoning branches before selecting the best solution. Balances feasibility, business value, risk, adoption likelihood, and deployment constraints.

### Case 7 — Rephrase-and-Respond Prompting

First converts vague requirements into precise problem statements, then generates realistic AI solutions. Helps reduce ambiguity and over-engineered responses.

---

# Final Conclusion

This project demonstrates how advanced prompt engineering techniques improve reasoning quality, consistency, structured decision-making, hallucination control, and enterprise AI reliability across multiple real-world use cases.
