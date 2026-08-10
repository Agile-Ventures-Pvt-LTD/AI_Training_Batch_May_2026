# AI Usage Declaration

This document declares the AI tools, methodologies, validation steps, and manual adjustments applied during the design, development, and testing of the **Sleepsia Quality Control Tower**.

---

## 1. AI Tools Utilized

- **Use Cases:**
  - Structuring system instructions and behavioral boundaries for the parent agent and specialist child agents.
  - Designing multi-agent orchestration flows, variable lists, and branching conditions.
  - Drafting test scenarios and validating logic boundary constraints.

---

## 2. Assisted Activities and Generated Content

| Activity | AI Contribution | Validation Method |
| :--- | :--- | :--- |
| **System Prompt Engineering** | Assisted in drafting specialized behavioral rules for the Complaint, Returns, Product/Batch, Customer Impact, Safety, and CAPA specialists. | Reviewed prompts to ensure compliance with the non-overlapping boundaries specified in the PRD. |
| **Orchestration Architecture** | Assisted in mapping the Power Automate calling structures for parallel specialist fan-out/fan-in and sequential actions. | Verified flow diagrams and logic paths against Copilot Studio execution capabilities. |
| **Custom Topic Branching** | Assisted in defining the 8 levels of rule precedence for the Quality Investigation Decision engine. | Confirmed that rules are executed sequentially without averaging, with the highest-priority rule overriding all others. |

---

## 3. Human Validation and Corrections

While AI tools were utilized to accelerate design and documentation, all outputs were strictly validated by the participant:
1. **Rule Precedence Enforcement:** Manually verified that `SafetyIndicator = Yes` (Priority 1) overrides all other rules, halting routine flows immediately, and that return rate triggers (Priority 4) correctly route to investigation.
2. **Selective Reassessment Logic:** Corrected the reassessment flow to ensure only stale specialists are rerun when new data arrives, and validated that a third reassessment attempt correctly triggers a `Manual Review` status.
3. **No Fabricated Evidence:** All test cases documented in the test report represent actual paths verified in Microsoft Copilot Studio. No screenshots, URLs, or test outcomes were fabricated.
4. **Error Handling Integrity:** Ensured that Excel update failures do not mark complaints as processed, and that Word or Outlook failures do not cause the entire quality flow to fail.

---

## 4. Manual Work Performed

The following activities were performed entirely manually:
- Setting up the Microsoft Copilot Studio environment and creating the Quality Supervisor agent.
- Uploading the internal policy documents (`Sleepsia_Product_Quality_Policy.docx`, `Sleepsia_Product_Care_and_Usage_Guide.docx`, and `Sleepsia_Customer_Resolution_Policy.docx`) and configuring public URLs as knowledge sources.
- Creating the six specialist child agents and defining their non-overlapping scopes.
- Constructing the custom topics, triggers, variables, nested conditions, and Power Automate flows within the Copilot Studio canvas.
- Configuring the MCP connection parameters to the Microsoft Learn MCP server.
- Running the 20 test cases step-by-step, recording execution outcomes, and validating the final publishing settings for Microsoft Teams.
