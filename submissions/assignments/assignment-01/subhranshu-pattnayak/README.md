# Prompt Engineering Evaluation

This project implements multiple prompt engineering strategies for structured reasoning, AI evaluation, business analysis, and requirement interpretation using large language models.

The implementation focuses on:

* structured JSON outputs,
* reasoning-oriented prompting,
* evaluation workflows,
* and prompt reliability analysis.

---

# Implemented Techniques

* Zero-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought Reasoning
* LLM-as-Judge
* Self-Consistency
* Tree-of-Thought Reasoning
* Rephrase-and-Respond

---

# Project Structure

```text
prompt_engineering_evaluation/
│
├── main.ipynb
├── groq_client.py
├── prompts.py
├── utils.py
├── requirements.txt
├── .env
│
├── outputs/
│   ├── zero_shot_outputs.json
│   ├── few_shot_outputs.json
│   ├── cot_outputs.json
│   ├── llm_judge_outputs.json
│   ├── self_consistency_outputs.json
│   ├── tree_of_thought_outputs.json
│   └── rephrase_respond_outputs.json
│
└── final_analysis.md
```

---

# Features

* Structured prompt organization
* JSON schema-constrained outputs
* Output parsing and validation
* Multi-technique reasoning workflows
* Self-consistency aggregation
* Comparative evaluation prompts
* Structured output persistence

---

# Setup Instructions

## 1. Create Environment

Using UV:

```bash
uv venv
```

Activate environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 2. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## 4. Run Notebook

Open:

```text
main.ipynb
```

Run all notebook cells sequentially.

---

# Output Format

Each technique stores outputs as structured JSON files containing:

* prompt,
* raw model response,
* parsed output,
* validation status,
* and case metadata.

---

# Final Analysis

Detailed observations, failure patterns, and prompt engineering insights are documented in:

```text
final_analysis.md
```

---

# Notes

* The project prioritizes reviewer readability and prompt engineering clarity over excessive framework abstraction.
* Outputs may vary slightly across runs depending on model temperature and provider behavior.
