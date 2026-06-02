# Assignment 01 - Prompt Engineering Evaluation

## Participant Name

Pranay Gupta

## Assignment / Project Title

Prompt Engineering Evaluation Using Groq API

## Description

This project demonstrates the implementation and evaluation of various prompt engineering techniques using the Groq API. The techniques include Zero-Shot Prompting, Few-Shot Prompting, Chain-of-Thought Reasoning, LLM-as-Judge, Self-Consistency, Tree-of-Thought, and Rephrase-and-Respond.

The project evaluates how different prompting strategies impact reasoning quality, output consistency, hallucination control, and decision-making across multiple enterprise-style use cases.

## Techniques Implemented

* Zero-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought Reasoning
* LLM-as-Judge
* Self-Consistency
* Tree-of-Thought
* Rephrase-and-Respond

## How to Run

```bash
uv init
uv venv
uv add -r requirements.txt
python main.py
```

## Assumptions

* A valid Groq API key is available.
* Internet access is available for API communication.
* Model outputs may vary slightly between runs.
* Results are intended for educational and evaluation purposes.

## Output

The program generates structured outputs demonstrating the behavior of different prompt engineering techniques across various business scenarios, including:

* Vendor Risk Classification
* Executive Decision Memo Generation
* Ticket Classification
* API Contract Generation
* ROI Analysis
* ML Model Degradation Root Cause Analysis
* Support Response Evaluation
* Security Risk Classification
* AI Use Case Selection
* Architecture Selection
* Business Requirement Refinement
* Technical Requirement Specification

## Observations

The evaluation shows that prompt quality directly affects:

* Reasoning stability
* Output format consistency
* Hallucination reduction
* Decision accuracy
* Response reliability

The most effective prompts use clear constraints, explicit output formats, controlled reasoning steps, and well-defined evaluation criteria.