# P2-001: NovaHR Assist — AI Usage & Transparency Declaration

* **Policy Version:** 1.0 (In strict compliance with PRD Section 15.5 & Section 17)
* **Project Name:** P2-001 HR Employee Assistance RAG Chatbot
* **Implementation Period:** July 2026

---

## 15.5.1 Which AI Tools Were Used
* **Microsoft Copilot Studio Generative AI Engine:** Used natively for Retrieval-Augmented Generation (RAG) and conversational parsing.
* **External LLM Assistants:** Google Gemini

---

## 15.5.2 How AI Assisted the Development
Generative AI tools were deployed as productivity enhancers across three specific conceptual activities
1. **Workflow Design & Guidance:** Assisting in conceptualizing the multi-step, deterministic conversational flows for the `Leave Request Advisor` and `Workplace Concern and Escalation` custom topics to ensure a logical user experience.
---

## 15.5.3 What Outputs Were Manually Validated
In strict accordance with the **Section 17 AI Usage Policy**, **zero AI-generated outputs were accepted blindly**. The implementation I maintained full human-in-the-loop responsibility through rigorous manual verification protocols:
---

## 15.5.4 What Corrections Were Made to AI-Generated Suggestions
During the iterative development process, several AI-generated conceptual suggestions required mandatory human correction and overriding to align with the PRD:
1. **Correction of Hallucinated Statutory Leave Entitlements:** Initial generative AI prompts attempted to interpolate general Indian labor law statutory minimums when suggesting responses for leave quotas. These outputs were manually overridden to strictly enforce the **12 Casual Leave days** and **10 Sick Leave days** mandated by the NovaWorks Addendum
2. **Refinement of Escalation Boundaries:** AI initial suggestions for harassment reporting attempted to offer investigative advice. This was manually corrected to ensure the bot strictly acts as a routing tool to the Internal Committee (IC/CMGI) without judging or investigating claims
3. **Variable Initialization Debugging:** During debugging, AI suggestions initially misidentified how variables should be scoped across multiple branching paths. This was manually audited and corrected to ensure clean topic compilation without duplicate variable errors.

---

## 15.5.5 Alternative Tools & Approaches for User Responses
While Microsoft Copilot Studio's native RAG and Adaptive Cards were selected as the primary mechanisms for rendering user responses, several alternative conversational tools and architectural approaches were evaluated during the design phase:
* **Adaptive Cards vs. Standard Text:** I chose to implement JSON-based Adaptive Cards for report summaries because they provide a structured, professional visual layout that standard markdown text blocks cannot replicate effectively in web chat interfaces.
---

## Summary of Responsibility
The implementation team confirms full understanding of all topic flows, RAG precedence hierarchies, and conditional logic implemented in NovaHR Assist. The final published solution represents a fully validated, human-verified implementation that strictly satisfies all functional and non-functional requirements of the NovaWorks PRD.