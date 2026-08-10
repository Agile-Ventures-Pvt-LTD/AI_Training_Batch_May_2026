# Assignment 01 – Prompt Engineering Evaluation

## 1. Name
**Simran Kaur**

---

## 2. Assignment / Project Title
**Comparative Evaluation of Prompt Engineering Techniques using Groq API**

---

## 3. Short Description of What You Have Built

This project explores and evaluates multiple Prompt Engineering techniques using Large Language Models (LLMs) through the Groq API. The goal was to understand how different prompting strategies influence model performance, reasoning quality, consistency, and reliability across various business and technical scenarios.

The evaluation covers tasks such as:

- Classification and categorization
- Decision-making and risk assessment
- Root-cause analysis
- Requirement clarification
- Architecture selection
- Quality evaluation and scoring

The following Prompt Engineering techniques were implemented and analyzed:

| Technique | Purpose |
|------------|----------|
| Zero-Shot Prompting | Task completion without examples |
| Few-Shot Prompting | Learning behavior through examples |
| Chain-of-Thought (CoT) | Step-by-step reasoning |
| LLM-as-Judge | Evaluation and scoring of outputs |
| Self-Consistency | Reliability through multiple reasoning paths |
| Tree-of-Thought (ToT) | Exploration of multiple solution branches |
| Rephrase-and-Respond | Converting ambiguous requirements into structured inputs |

### Project Objective

To compare the effectiveness, strengths, and limitations of various prompt engineering approaches and identify the most suitable technique for different categories of AI tasks.

---

## 4. Steps to Run the Code

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
```

### Step 2: Install Required Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Credentials

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_api_key_here
```

### Step 4: Execute the Project

For Python scripts:

```bash
python main.py
```

For Jupyter Notebook:

```bash
jupyter notebook
```

Open the notebook and run all cells sequentially.

---

## 5. Libraries / Packages Required

### Core Libraries

```text
groq
python-dotenv
pandas
numpy
json
jupyter
```

### Installation Command

```bash
pip install -r requirements.txt
```

---

## 6. Assumptions Made

The following assumptions were considered during the evaluation:

1. A valid Groq API key is available and configured correctly.
2. Internet connectivity is available for sending API requests.
3. The selected LLM supports advanced reasoning and structured output generation.
4. Model outputs may vary slightly across executions due to the probabilistic nature of generative AI.
5. Evaluation tasks use predefined schemas and rubrics wherever applicable.
6. Prompt quality directly impacts response quality and consistency.

---

## 7. Output Explanation

The project generates outputs for multiple prompt engineering techniques and evaluates their effectiveness based on consistency, reasoning quality, and task performance.

### A. Zero-Shot Prompting

**Tasks Performed**
- Vendor Risk Classification
- Executive Decision Memo Generation

**Observations**
- Works effectively for straightforward tasks.
- Highly dependent on prompt clarity.
- May produce inconsistent outputs when requirements are ambiguous.

**Key Learning**
> Clear instructions and structured schemas are essential when no examples are provided.

---

### B. Few-Shot Prompting

**Tasks Performed**
- Ticket Classification
- API Contract Generation

**Observations**
- Improves classification accuracy.
- Provides better boundary handling.
- Reduces ambiguity in labels.

**Key Learning**
> Well-designed examples significantly improve output consistency.

---

### C. Chain-of-Thought (CoT) Reasoning

**Tasks Performed**
- ROI Analysis
- ML Model Degradation Investigation

**Observations**
- Improves multi-step reasoning.
- Produces more explainable decisions.
- Better handling of analytical problems.

**Key Learning**
> Explicit reasoning steps help the model arrive at more reliable conclusions.

---

### D. LLM-as-Judge

**Tasks Performed**
- Customer Support Response Evaluation
- Code Explanation Scoring

**Observations**
- Provides structured qualitative assessment.
- Effective when combined with a detailed rubric.
- Enables automated evaluation workflows.

**Key Learning**
> Strong evaluation criteria are necessary to reduce scoring subjectivity.

---

### E. Self-Consistency

**Tasks Performed**
- Policy Interpretation
- Security Risk Classification

**Observations**
- Generates multiple independent reasoning paths.
- Uses consensus-based decision making.
- Improves reliability and stability.

**Key Learning**
> Majority agreement often reduces single-response errors and hallucinations.

---

### F. Tree-of-Thought (ToT)

**Tasks Performed**
- AI Use Case Selection
- Architecture Decision Making

**Observations**
- Explores multiple reasoning branches.
- Enables trade-off comparison.
- Produces more balanced decisions.

**Key Learning**
> Considering alternative solution paths often leads to better final decisions.

---

### G. Rephrase-and-Respond

**Tasks Performed**
- Requirement Clarification
- Technical Specification Generation

**Observations**
- Converts vague requirements into structured inputs.
- Improves downstream output quality.
- Reduces ambiguity before reasoning begins.

**Key Learning**
> Better problem definition often leads to better solutions.

---

## Overall Findings

### Major Observations

- Prompt structure is more important than prompt length.
- Schema enforcement significantly improves consistency.
- Few-shot prompting excels in classification tasks.
- Reasoning-based techniques improve analytical accuracy.
- Self-consistency improves reliability in critical scenarios.
- Rephrasing unclear inputs enhances downstream performance.

---

## Key Learnings

1. Define strict output schemas whenever possible.
2. Use examples when task boundaries are unclear.
3. Separate reasoning from final responses.
4. Apply self-consistency for high-risk decisions.
5. Avoid making assumptions when context is incomplete.
6. Design prompts with clear objectives and constraints.
7. Evaluate prompts iteratively to improve reliability.

---

## Conclusion

This project demonstrates that effective Prompt Engineering is not about creating longer prompts; it is about designing prompts that are:

- **Precise**
- **Structured**
- **Context-Aware**
- **Constraint-Driven**
- **Reliable**

Different prompting techniques serve different purposes:

## Technique Suitability Analysis

The evaluation demonstrated that each prompting technique excels in a specific category of tasks:

🔹 **Zero-Shot Prompting**
- Suitable for straightforward tasks with clearly defined objectives.
- Commonly used for classification, extraction, and summarization.

🔹 **Few-Shot Prompting**
- Effective when task boundaries are unclear.
- Improves consistency by providing representative examples.

🔹 **Chain-of-Thought (CoT)**
- Best suited for analytical and multi-step reasoning problems.
- Enhances transparency of the model's decision-making process.

🔹 **LLM-as-Judge**
- Designed for evaluation and assessment tasks.
- Useful for scoring responses against predefined rubrics.

🔹 **Self-Consistency**
- Improves answer reliability through consensus-based reasoning.
- Particularly valuable in high-stakes decision scenarios.

🔹 **Tree-of-Thought (ToT)**
- Enables exploration of multiple solution paths.
- Ideal for complex decisions involving trade-offs and alternatives.

🔹 **Rephrase-and-Respond**
- Reduces ambiguity by transforming unclear inputs into structured requirements.
- Improves the quality of downstream responses and solutions.

### Final Takeaway

Prompt Engineering is a systematic process of guiding Large Language Models toward reliable, accurate, and explainable outputs through carefully designed instructions, examples, constraints, and reasoning frameworks.