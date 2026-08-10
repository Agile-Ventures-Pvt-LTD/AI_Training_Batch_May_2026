# AI Usage Declaration

This document declares the AI tools, methodologies, validation steps, and manual adjustments applied during the design, development, and testing of the **NovaRetail Support and Warranty Assistant**.

---

## 1. AI Tools Utilized
- Chatgpt , Microsoft copilot studio
- **Use Cases:** 
  - Authoring system instructions and behavioral boundaries.
  - Designing conversation logic, variable lists, and branching conditions.
---

## 2. Assisted Activities and Generated Content

| Activity | AI Contribution | Validation Method |
| :--- | :--- | :--- |
| **System Instruction Design** | AI assisted in drafting the initial instructions. | Reviewed, refined, and aligned the instructions with the PRD requirements. |
| **Topic Flow Design** | AI assisted in generating the initial topic structure and flow logic. | Modified, validated, and tested the topic flows in Copilot Studio to meet the project requirements. |

---

## 3. Human Validation and Corrections

While AI was utilized to accelerate design and documentation, all outputs were strictly validated by the participant:
1. **Warranty Coverage Period Logic:** AI-generated rules were verified to ensure laptop batteries and accessories are strictly bound to a 6-month limit while laptops and printers have a 12-month limit.
2. **Safety Override Checks:** Manually confirmed that safety checks occur *before* any troubleshooting steps are presented to the user, and that Level 4 safety escalation halts the chat loop.
3. **No Fabricated Evidence:** All test cases documented in the test report represent actual paths verified in Microsoft Copilot Studio. No screenshots or URLs were fabricated.
4. **Correction Handling:** Ensured that variable updates in the correction branch correctly reset prior classifications and re-evaluate dates.

---

## 4. Manual Work Performed

The following activities were performed entirely manually:
- Setting up the Microsoft Copilot Studio environment and creating the agent.
- Uploading the Lenovo and HP User Guide PDFs and configuring the official public websites as knowledge sources.
- Creating the custom topics, triggers, variables, nested conditions, and generative-answers nodes in the Copilot Studio canvas.
- Authoring the reusable subtopics for Product Safety Assessment and Support Case Summary.
- Running the 40 test cases step-by-step in the Copilot Studio test panel, capturing evidence, and taking screenshots.
- Publishing the chatbot and sharing the access URL with the evaluator.

---
