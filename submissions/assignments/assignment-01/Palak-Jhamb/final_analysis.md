# Assignment 1: Foundation of Generative AI

## 1. Overview

This study evaluates multiple prompt engineering strategies using the Groq API to understand how large language models behave across different task types, including reasoning, transformation, classification, and evaluation.

The assessment focuses on:

- Prompt design quality and precision
- Consistency of structured outputs
- Reliability of multi-step reasoning
- Handling of ambiguous or incomplete inputs
- Performance under explicit constraints and formatting rules

---

## 2. Prompting Techniques Evaluated

### 2.1 Zero-Shot Prompting

**Use Cases:**

- Vendor risk assessment
- Executive-level decision summaries

**Summary:**

Zero-shot prompting relies entirely on instruction clarity and schema definition, without examples to guide behavior.

**Key Findings:**

- High sensitivity to ambiguity in instructions
- Strong dependence on well-defined output formats
- Tendency toward overgeneralization when constraints are vague

---

### 2.2 Few-Shot Prompting

**Use Cases:**

- Support ticket classification
- API contract structuring

**Summary:**

Providing examples significantly improves model consistency by establishing clear patterns and category boundaries.

**Key Strengths:**

- Improved classification accuracy in closely related categories (e.g., billing vs. compliance)
- More consistent interpretation of expected outputs

**Limitations:**

- Overfitting to provided examples or formats
- Reduced adaptability to unseen patterns

---

### 2.3 Chain-of-Thought Reasoning

**Use Cases:**

- ROI and financial decision analysis
- Root-cause analysis in ML systems

**Summary:**

Step-by-step reasoning improves performance in multi-stage logical and analytical tasks.

**Key Strengths:**

- Better handling of multi-step dependencies
- Improved logical coherence in structured reasoning tasks

**Observed Failure Modes:**

- Accumulation of errors from early incorrect assumptions
- Potential reasoning drift in long chains

---

### 2.4 LLM-as-Judge

**Use Cases:**

- Evaluation of customer support responses
- Scoring of code explanations

**Summary:**

With a well-defined rubric, LLMs can act as consistent evaluators of qualitative outputs.

**Key Strengths:**

- Stable comparative scoring across responses
- Effective evaluation of clarity, tone, and usefulness

**Limitations:**

- Bias toward verbosity when scoring criteria are not strict
- Subjectivity when rubrics are loosely defined

---

### 2.5 Self-Consistency

**Use Cases:**

- Policy interpretation tasks
- Security risk classification

**Summary:**

Aggregating multiple independent outputs improves reliability and reduces stochastic variation.

**Key Strengths:**

- Increased stability through majority agreement
- Reduced impact of single-run hallucinations

**Limitations:**

- Systematic errors persist if shared across all samples
- Requires a well-defined aggregation strategy

---

### 2.6 Tree-of-Thought Reasoning

**Use Cases:**

- Solution selection for AI systems
- Architecture and system design decisions

**Summary:**

Exploring multiple reasoning paths improves decision quality in complex, trade-off-heavy problems.

**Key Strengths:**

- Enables structured comparison of alternatives
- Improves multi-criteria evaluation quality

**Limitations:**

- Can become computationally and cognitively complex
- Risk of inconsistent evaluation across branches without strict scoring rules

---

### 2.7 Rephrase-and-Respond

**Use Cases:**

- Converting business requirements into technical specifications
- Transforming vague inputs into structured documentation

**Summary:**

Rewriting ambiguous inputs into structured forms significantly improves downstream output quality.

**Key Strengths:**

- Reduces ambiguity in user inputs
- Produces clearer, implementation-ready specifications

**Risks:**

- May introduce unintended assumptions
- Risk of over-specification beyond original intent

---

## 3. Cross-Method Observations

Across all techniques, several consistent patterns were observed:

- Prompt structure is the primary determinant of output quality
- Strict schemas significantly improve reliability and consistency
- Few-shot prompting is most effective for classification tasks
- Reasoning-based approaches improve accuracy but require control to prevent drift

---

## 4. Key Learnings

- Structured output formats (e.g., JSON schemas) significantly improve reliability
- Few-shot examples should be used selectively when category boundaries are unclear
- Complex reasoning should be separated from final output when possible
- Self-consistency improves reliability in high-uncertainty scenarios
- Rewriting inputs improves clarity but must avoid introducing external assumptions

---

## 5. Conclusion

Effective prompt engineering is driven less by prompt length and more by design discipline, structure, and control.

The most critical success factors are:

- Precision in instruction design
- Strong structural constraints
- Appropriate selection of prompting strategy per task
- Controlled reasoning flow and output formatting

---

## Technique Suitability Summary

| Technique | Best Suited For |
|------------|----------------|
| Zero-Shot | Simple tasks with clear rules and structured outputs |
| Few-Shot | Classification tasks requiring consistent labeling |
| Chain-of-Thought | Multi-step reasoning and analytical problems |
| LLM-as-Judge | Evaluation and qualitative scoring tasks |
| Self-Consistency | Reducing uncertainty and improving reliability |
| Tree-of-Thought | Complex decision-making with trade-offs |
| Rephrase-and-Respond | Converting ambiguous inputs into structured specifications |

---