# Prompt Engineering Evaluation – Final Analysis

## 1. Objective
In this experiment, I tested different prompt engineering techniques using the Groq API to understand how prompt design affects LLM responses in terms of reasoning quality, accuracy, and consistency.

The main focus was not just generating answers, but comparing how different prompting styles change the output behavior.

---

## 2. What I Actually Observed in My Runs

Across all experiments stored in the `/outputs` folder, I noticed clear differences in how the model behaves depending on the prompting method.

Some techniques gave short but direct answers, while others forced deeper reasoning or multiple perspectives.

---

## 3. Technique-wise Observations

### 3.1 Zero-shot Prompting
In my outputs, zero-shot responses were the fastest and most direct.

However, I noticed:
- Some answers were too brief
- In reasoning-heavy questions, the model sometimes skipped steps
- Works fine for simple factual queries but not for complex tasks

Overall, it felt like a baseline behavior of the model.

---

### 3.2 Few-shot Prompting
Few-shot prompting clearly improved structure.

From my results:
- Outputs followed patterns from examples
- Better formatting and more controlled responses
- Accuracy improved slightly compared to zero-shot

This technique helped the model “understand expectations” better.

---

### 3.3 Chain-of-Thought (CoT)
This was one of the most noticeable improvements.

Observations:
- Answers became more step-by-step
- Even when final answers were wrong, reasoning was still visible
- Helped in debugging logic

In my runs, CoT performed best for reasoning-based questions.

---

### 3.4 Self-Consistency
I generated multiple outputs and compared them.

What I saw:
- Different reasoning paths sometimes led to different answers
- Final majority answer was usually more stable
- Reduced randomness compared to single CoT

But it increased computation and response time.

---

### 3.5 Tree of Thought (ToT)
This technique produced the most structured reasoning.

From my outputs:
- The model explored multiple possible paths
- Better for complex decision-style problems
- However, it felt slower and more verbose

In some cases, outputs were better than CoT, but not always necessary.

---

### 3.6 LLM-as-a-Judge
Here I used one model output to evaluate others.

What I noticed:
- It was helpful for ranking responses
- But sometimes the judge also showed bias toward longer answers
- Quality depends heavily on how well the judge prompt is written

So evaluation is useful, but not fully reliable alone.

---

### 3.7 Rephrase-and-Respond
This technique was surprisingly effective.

Observations:
- When the question was unclear, rephrasing helped a lot
- Final answers became more relevant and focused
- Reduced misinterpretation issues

This worked best for ambiguous or messy inputs.

---

## 4. Overall Comparison (Based on My Outputs)

From my experiment:

- Best for reasoning → Chain-of-Thought / Tree of Thought  
- Best for stability → Self-Consistency  
- Best for speed → Zero-shot  
- Best for clarity improvement → Rephrase-and-Respond  
- Best for structured evaluation → LLM-as-a-Judge  

---

## 5. Key Learnings

- Prompt design heavily changes output quality, even with the same model
- More complex prompting ≠ always better (ToT is powerful but heavy)
- Simple techniques still work well for basic tasks
- The biggest improvement comes from guiding the model’s reasoning process

---

## 6. Conclusion

This experiment showed that prompt engineering is less about “getting the model to answer” and more about “controlling how it thinks.”

Different techniques serve different purposes, and in real applications, a hybrid approach works best.