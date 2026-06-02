# Prompt Engineering Evaluation Using the Groq API

## Overview

This project evaluates multiple prompt engineering techniques using the Groq API and Large Language Models (LLMs). The objective is to compare how different prompting strategies perform in realistic and ambiguous scenarios while assessing their strengths, limitations, and practical applications.

The evaluation covers:

* Zero-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought (CoT)
* LLM-as-Judge
* Self-Consistency
* Tree-of-Thought (ToT)
* Rephrase-and-Respond

The project provides a reusable framework for executing prompts, extracting structured outputs, storing results, and comparing prompting strategies.

---

# Project Structure

```text
project/
│
├── prompts.py                 # Prompt templates
├── groq_client.py             # Groq API wrapper
├── evaluation.py             # Main evaluation script
├── outputs/                  # Generated JSON outputs
│
├── README.md
└── requirements.txt
```

---

# Prerequisites

* Python 3.9+
* Groq API Key

---

# Installation

Clone the repository:

```bash
git clone https://github.com/your-username/prompt-engineering-evaluation.git

cd prompt-engineering-evaluation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Or export the key directly:

```bash
export GROQ_API_KEY=your_groq_api_key
```

---

# Dependencies

Example `requirements.txt`:

```txt
groq
python-dotenv
```

---

# Groq Client Setup

`groq_client.py`

```python
import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def call_llm(prompt, temperature=0.2):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content
```

---

# Evaluation Framework

The framework performs the following tasks:

1. Sends prompts to the Groq-hosted LLM.
2. Receives model responses.
3. Extracts structured JSON.
4. Stores outputs for analysis.
5. Compares prompt engineering techniques.

---

# Evaluation Script

```python
import json
import os
import re

from groq_client import call_llm
from prompts import Few_Shot_Transformation


def extract_json(response_text):
    """
    Robust JSON extraction with regex fallback.
    """
    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        try:
            match = re.search(
                r'\{.*\}',
                response_text,
                re.DOTALL
            )

            if match:
                return json.loads(match.group())

            return {
                "error": "No JSON found"
            }

        except Exception as e:
            return {
                "error": f"JSON extraction failed: {e}"
            }


def save_output(filename, data):
    """
    Save structured output.
    """
    try:
        os.makedirs(
            "outputs",
            exist_ok=True
        )

        with open(
            os.path.join(
                "outputs",
                filename
            ),
            "w"
        ) as f:
            json.dump(
                data,
                f,
                indent=2
            )

    except Exception as e:
        print(
            f"Save failed: {e}"
        )


def run_case(
    case_name,
    prompt,
    temperature=0.2
):
    """
    Execute prompt evaluation.
    """
    try:
        response = call_llm(
            prompt,
            temperature=temperature
        )

        print(
            f"RAW RESPONSE for {case_name}:"
        )
        print(response)

        parsed = extract_json(
            response
        )

        save_output(
            f"{case_name}.json",
            parsed
        )

        return parsed

    except Exception as e:
        print(
            f"Execution failed: {e}"
        )

        return {
            "error": str(e)
        }


# Example Run

result = run_case(
    "Few_Shot_Transformation_1",
    Few_Shot_Transformation
)

print(result)
```

---

# Prompt Engineering Techniques Evaluated

## 1. Zero-Shot Prompting

### Description

Provides instructions without examples and relies entirely on the model's prior knowledge.

### Strengths

* Fast implementation
* Minimal prompt design effort
* Effective for simple tasks

### Weaknesses

* Sensitive to ambiguity
* May miss hidden constraints

### Best Use Cases

* Classification
* Extraction
* Formatting tasks

---

## 2. Few-Shot Prompting

### Description

Provides examples that guide the model toward desired behavior.

### Strengths

* Improved consistency
* Better understanding of boundaries
* More predictable outputs

### Weaknesses

* Requires curated examples
* Potential example bias

### Best Use Cases

* Ambiguous classifications
* Policy enforcement
* Structured outputs

---

## 3. Chain-of-Thought (CoT)

### Description

Encourages the model to reason step-by-step before producing an answer.

### Strengths

* Better logical reasoning
* Improved analytical performance
* Useful for calculations

### Weaknesses

* Longer outputs
* Higher token consumption

### Best Use Cases

* Mathematics
* Diagnostics
* Multi-step reasoning

---

## 4. LLM-as-Judge

### Description

Uses an LLM to evaluate responses against a rubric.

### Strengths

* Automated evaluation
* Consistent assessment
* Scalable review process

### Weaknesses

* Rubric-dependent
* Potential scoring inconsistency

### Best Use Cases

* Content evaluation
* Benchmarking
* Response comparison

---

## 5. Self-Consistency

### Description

Generates multiple reasoning paths and selects the most common answer.

### Strengths

* Higher reliability
* Reduced variance
* Better accuracy

### Weaknesses

* Increased computational cost
* Longer execution time

### Best Use Cases

* Critical reasoning tasks
* High-stakes decisions

---

## 6. Tree-of-Thought (ToT)

### Description

Explores multiple solution branches before selecting the best option.

### Strengths

* Evaluates alternatives
* Supports strategic decisions
* Considers trade-offs

### Weaknesses

* Computationally expensive
* More complex prompting

### Best Use Cases

* Planning
* Strategy
* Multi-criteria decisions

---

## 7. Rephrase-and-Respond

### Description

Clarifies ambiguous instructions before solving the task.

### Strengths

* Improved clarity
* Better requirement understanding
* More actionable responses

### Weaknesses

* Can oversimplify assumptions

### Best Use Cases

* Ambiguous requests
* Requirement gathering
* User support

---

# Comparative Summary

| Technique            | Accuracy    | Cost   | Complexity | Best For            |
| -------------------- | ----------- | ------ | ---------- | ------------------- |
| Zero-Shot            | Medium      | Low    | Low        | Simple Tasks        |
| Few-Shot             | High        | Medium | Medium     | Boundary Learning   |
| Chain-of-Thought     | High        | Medium | Medium     | Reasoning           |
| LLM-as-Judge         | Medium-High | Medium | Medium     | Evaluation          |
| Self-Consistency     | Very High   | High   | High       | Reliability         |
| Tree-of-Thought      | Very High   | High   | High       | Strategic Decisions |
| Rephrase-and-Respond | High        | Low    | Low        | Ambiguous Requests  |

---

# Key Findings

### Most Efficient

**Zero-Shot Prompting**

Suitable when requirements are well-defined and execution speed is important.

### Most Reliable

**Self-Consistency**

Produced the most stable outputs across repeated runs.

### Best for Complex Decisions

**Tree-of-Thought**

Handled trade-offs and multi-criteria reasoning effectively.

### Best General-Purpose Technique

**Few-Shot Prompting**

Balanced accuracy, consistency, and implementation effort.

---

# Recommendations

### Use Zero-Shot When

* Tasks are simple.
* Output schema is well-defined.

### Use Few-Shot When

* Boundaries need to be demonstrated.
* Consistency is important.

### Use Chain-of-Thought When

* Solving analytical problems.
* Performing calculations.

### Use LLM-as-Judge When

* Evaluating content quality.
* Comparing model outputs.

### Use Self-Consistency When

* Reliability matters more than cost.

### Use Tree-of-Thought When

* Multiple alternatives must be explored.

### Use Rephrase-and-Respond When

* Requirements are vague or incomplete.

---

# Conclusion

Prompt engineering is the process of selecting and adapting prompting strategies based on task requirements rather than relying on a single technique. Each approach offers distinct trade-offs between simplicity, accuracy, interpretability, and computational cost.

The evaluation demonstrates that combining techniques often produces the strongest results. For example:

* Few-Shot + Chain-of-Thought for structured reasoning.
* Tree-of-Thought + Self-Consistency for strategic decisions.
* Rephrase-and-Respond + Few-Shot for ambiguous requirements.

Understanding when and how to apply these techniques is critical for building reliable, scalable, and high-performing AI systems.

## Copyright

© 2026 Vikash Kumar. All Rights Reserved.

---

## Author

**Vikash Kumar**

Prompt Engineering Evaluation Project using the Groq API

---

