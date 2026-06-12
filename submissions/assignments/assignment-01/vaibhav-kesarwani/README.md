# Assignment 01 - Prompt Engineering Techniques Using Groq API

## Participant Name

Vaibhav Kesarwani

## Assignment Title

Prompt Engineering Techniques Using Groq API

## Description

This assignment demonstrates the implementation and evaluation of multiple prompt engineering techniques using the Groq API. The project explores how different prompting strategies influence Large Language Model (LLM) behavior across realistic business and reasoning tasks.

The techniques implemented include:

* Zero-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought (CoT) Reasoning
* LLM-as-Judge
* Self-Consistency
* Tree-of-Thought (ToT)
* Rephrase-and-Respond

A unified execution framework was developed to ensure consistent evaluation, structured outputs, reproducibility, and easy comparison across techniques.

---

## Features

### Helper Functions

* `run_case()` – Standardized LLM execution using Groq API
* `extract_json()` – Robust JSON extraction with fallback handling
* `save_output()` – Structured output persistence

### Prompting Techniques Implemented

#### 1. Zero-Shot Prompting

Used for:

* Vendor Risk Classification
* Executive Decision Memo Generation

#### 2. Few-Shot Prompting

Used for:

* Customer Ticket Classification
* Natural Language to API Contract Transformation

#### 3. Chain-of-Thought (CoT)

Used for:

* ROI Calculation
* ML Performance Degradation Analysis

#### 4. LLM-as-Judge

Used for:

* Customer Support Response Evaluation
* Code Explanation Quality Assessment

#### 5. Self-Consistency

Used for:

* Reimbursement Calculation
* Security Risk Classification

#### 6. Tree-of-Thought (ToT)

Used for:

* AI Use Case Selection
* RAG Architecture Selection

#### 7. Rephrase-and-Respond

Used for:

* Business Requirement Clarification
* Technical Specification Generation

---

## How to Run

### Intialise the virtual environment

```bash
uv venv
```
### Install Dependencies

```bash
uv pip install -r requirements.txt
```

### Execute the Assignment

```bash
main.ipynb
```

---

## Required Libraries

* groq
* python-dotenv
* json
* re
* pathlib

Install all dependencies using:

```bash
uv pip install -r requirements.txt
```

---

## Assumptions Made

* A valid Groq API key is available and configured in the environment.
* The selected Groq model supports JSON-style structured responses.
* Prompt templates are designed to encourage deterministic outputs.
* Self-consistency experiments may require multiple model calls with controlled temperature settings.
* Output files are stored locally for evaluation and comparison.

---

## Comparative Summary

| Technique            | Strength                 | Best Use Case                    |
| -------------------- | ------------------------ | -------------------------------- |
| Zero-Shot            | Fast structured baseline | Classification, extraction       |
| Few-Shot             | Learns from examples     | Intent classification, mapping   |
| Chain-of-Thought     | Strong reasoning         | Math, diagnostics                |
| LLM-as-Judge         | Reliable evaluation      | Benchmarking, scoring            |
| Self-Consistency     | Improved reliability     | Risk assessment, calculations    |
| Tree-of-Thought      | Trade-off analysis       | Strategy, architecture decisions |
| Rephrase-and-Respond | Handles ambiguity        | Requirement engineering          |

---

## Output

The system generates structured JSON outputs for each prompting technique, allowing easy comparison of:

* Accuracy
* Consistency
* Reasoning Quality
* Decision-Making Behavior

Outputs are saved automatically and can be reviewed for comparative evaluation across prompting strategies.

---

## Conclusion

This assignment demonstrates that prompt engineering is a systematic design discipline rather than simple prompt writing. Different prompting techniques provide unique advantages depending on the task:

* Zero-Shot → Instruction Following
* Few-Shot → Behavior Shaping
* Chain-of-Thought → Reasoning Enhancement
* LLM-as-Judge → Evaluation Framework
* Self-Consistency → Reliability Improvement
* Tree-of-Thought → Decision Optimization
* Rephrase-and-Respond → Ambiguity Resolution

Together, these techniques form a strong foundation for building robust, production-ready LLM applications.
