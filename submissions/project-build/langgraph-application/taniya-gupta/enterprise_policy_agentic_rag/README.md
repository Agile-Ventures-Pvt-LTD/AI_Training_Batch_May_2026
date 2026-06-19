# Enterprise Policy agent - Project 003

## Name
Taniya Gupta

This project implements a custom state agent that classifies user queries, retrieves relevant context from multiple policy documents, grades the quality of retrieved data, generates answers and performs a reflection check.

---

## Getting Started

### 1. Installation
install the dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Copy the `.env.example` file to `.env` and add your Groq API Key

### 3. Run the app
```bash
python app.py
```

---

## File Structure
```
enterprise_policy_agentic_rag/
│
├── app.py
├── config.py
├── loaders.py
├── chunking.py
├── retrievers.py
├── tools.py
├── graph.py
├── prompts.py
├── output_parser.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ └── policies/
│ ├── hr_leave_policy.md
│ ├── travel_policy.md
│ ├── reimbursement_policy.md
│ ├── it_security_policy.md
│ └── ai_usage_policy.md
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json
 ```

---

### Implementation Choice: Custom LangGraph Agent

Why I chose custom langgraph agent over prebuilt agent - Prebuilt agent was not compatible with the parrallel pattern since it relys on llms capability to decide the routing, and even after giving the specific system prompt I could not achieve parrallelization, so for full customization I chose custom langgraph workflow over prebuilt agent. 

### Sequential Pattern
The graph executes a clean sequence:
1. **Query Classifier**
2. **Parallel Retrieval**
3. **Context Grader**
4. **Answer Generator**
5. **Reflection**
6. **Final Response**

### Parallelization Pattern
For multi-policy questions (e.g., "Are there any security guidelines for using ChatGPT or Copilot on company laptops?"), the assistant must give answwers related to both chunks:
We have achieved parralelization through custom state nodes.

### Conditional Pattern
Conditional routing occurs at three key decision splits in the workflow:
* **After Classifier**: If `requires_clarification` is `True`, the graph bypasses retrieval and routes directly to the **Clarification Node**. Otherwise, it routes to **Parallel Retrieval**.
* **After Grader**:
  * `ANSWER` : **Answer Generator**
  * `REWRITE_QUERY` : **Query Rewriter**
  * `ASK_CLARIFICATION` : **Clarification Node**
  * `NOT_FOUND` : **Final Response Node** 
* **After Reflection**:
  * `needs_revision` is `True` : Loops back to **Answer Generator** 
  * `needs_revision` is `False`: Routes to **Final Response Node**.


### Sample user questions
I have tested the agent on 9 questions. These questions showcase that all the functional requirements have been acheieved. 
1. How many annual leave days can an employee carry forward?
2. Can I claim meals for same-day domestic business travel?
3. What documents are needed for hotel reimbursement?
4. Can I use my personal laptop for office work?
5. What approvals are needed for international travel?
6. Can customer data be uploaded to a public AI tool?
7. Will my reimbursement definitely be approved?
8. What should I do if the policy does not mention my scenario?
9. Are there any security guidelines for using ChatGPT or Copilot on company laptops?

Note: I have added an extra question to showcase parralelization of the agent.
---

## Known Limitations and Future Improvements
**API Rate Limits**: Free tier Groq API keys have tight limits. Even after using the model which gives high number of requests the long answer generation and lannggraph rerouting was enabling the rate limit error.
**Hardcoded Retrieval Parameters**: The chunk sizes and `k` values are static. Implementing a hybrid search model would improve chunk selection accuracy.
**Streamlit integration**: Integrating streamlit UI interface for seamless interaction instead of CLI
