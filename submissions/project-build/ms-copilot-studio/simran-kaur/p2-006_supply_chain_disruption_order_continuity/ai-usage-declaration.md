# AI Usage Declaration

This document discloses how generative AI was utilized during the planning, design, and documentation of the **Autonomous Supply Chain Disruption & Order Continuity Response System** (Project P2-006).

---

## 1. AI Usage Scope & Guidelines
Generative AI was used in accordance with the project's AI Usage Policy:
* **Orchestration Architecture Design**: Formulating the hierarchical relationships between the Supervisor and child specialists.
* **Agent System Prompts**: Generating system instructions and domain-specific roles for the specialist child agents.
* **Topic Variables Structure**: Structuring the inputs and outputs for custom topics.
* **Test Case Scenarios**: Designing the 24 test cases to cover all mandatory patterns.
* **Documentation Formatting**: Improving readability, markdown structure, and formatting.

---

## 2. Strict Guardrail Compliance
In compliance with NovaSphere policy and the evaluation rubric, **zero AI-generated fabrications** were introduced:
* **No Fabricated Supplier Approvals**: Supplier status calculations are strictly read from the Excel database.
* **No Fabricated Customer Agreements**: Orders and delivery dates were never adjusted without human authorization.
* **No Fabricated Test Evidence**: The test outcomes recorded in the `test-report.md` reflect real validation runs.
* **No Fabricated Screenshots**: The screenshots folder matches the actual Copilot Studio workspace components.
* **No Fabricated Emails**: The notification outputs logged in the test report are actual system-generated notifications.

---

## 3. Sample Prompting History
Below are representative prompts used during the design phase:

### Prompt 1: Specialist Output Contract
> *“Design a JSON schema representing a standard specialist output contract for Copilot Studio child agents. The contract must contain SpecialistName, AssessmentStatus, EvidenceSummary, QuantitativeFindings, BlockingIssues, Constraints, RecommendedAction, ApprovalRequired, RequiredApprover, and Confidence.”*

### Prompt 2: Precedence Logic
> *“Create a deterministic priority list for resolving supply chain disruptions when multiple child agents return conflicting recommendations. The priorities must put quality holds first, followed by strategic SLA protections, supplier approvals, stock timing, commercial spend, and cost optimization.”*

### Prompt 3: Selective Reassessment Loop
> *“Explain how to implement a selective reassessment pattern in Copilot Studio. If an alternate supplier's capacity changes, how can we rerun only the sourcing and commercial specialists while keeping the inventory and customer impact findings intact?”*
