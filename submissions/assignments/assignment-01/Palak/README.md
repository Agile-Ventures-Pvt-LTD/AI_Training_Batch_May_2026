# README.md

## 1. Name: **Palak**

---

## 2. Assignment: **Assignment 1: Foundation of Generative AI**

---

## 3. Short Description 

This assignment presents a comparative study of various prompt engineering techniques using the Groq API to analyze the behavior of Large Language Models (LLMs) across different task categories.

The project evaluates the effectiveness, strengths, limitations, and practical applications of the following prompting techniques:

* Zero-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought (CoT) Reasoning
* LLM-as-Judge
* Self-Consistency
* Tree-of-Thought (ToT) Reasoning
* Rephrase-and-Respond

The analysis focuses on factors such as output quality, reasoning capabilities, consistency, reliability, ambiguity handling, and structured response generation.

---

## 4. Steps to Run the Code

### Prerequisites

* Python 3.9 or higher
* Groq API Key

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your Groq API Key

4. Run the main.ipynb: cells to see how each technique works!


---

## 5. Libraries or Packages Required

Typical dependencies include:

```txt
groq
python-dotenv
ipykernel
```

Install using:

```bash
pip install groq python-dotenv ipykernel
```


---

## 7. Output Explanation

The assignment generates responses using different prompting strategies and compares their effectiveness across various use cases.

### Key Observations

* Structured prompts produce more reliable outputs.
* Few-shot prompting improves classification consistency.
* Chain-of-Thought reasoning enhances analytical problem-solving.
* Self-consistency improves stability by aggregating multiple outputs.
* Tree-of-Thought reasoning supports better decision-making for complex problems.
* Rephrase-and-Respond reduces ambiguity and improves specification quality.
* LLM-as-Judge can effectively evaluate responses when guided by a clear rubric.

### Technique Suitability Summary

| Technique            | Best Suited For                                            |
| -------------------- | ---------------------------------------------------------- |
| Zero-Shot            | Simple tasks with clear rules and structured outputs       |
| Few-Shot             | Classification tasks requiring consistent labeling         |
| Chain-of-Thought     | Multi-step reasoning and analytical problems               |
| LLM-as-Judge         | Evaluation and qualitative scoring tasks                   |
| Self-Consistency     | Reducing uncertainty and improving reliability             |
| Tree-of-Thought      | Complex decision-making with trade-offs                    |
| Rephrase-and-Respond | Converting ambiguous inputs into structured specifications |

---

## Conclusion

The study demonstrates that effective prompt engineering depends primarily on prompt structure, instruction clarity, and appropriate technique selection. Structured outputs, controlled reasoning, and well-defined constraints consistently improve the quality and reliability of LLM responses.
