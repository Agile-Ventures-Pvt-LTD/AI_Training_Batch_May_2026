# AI Usage Declaration

# P2-003 Autonomous Sales Lead Qualification Agent

---

## 1. Overview

This document explains the usage of Artificial Intelligence during the design, configuration, testing, and documentation of the **P2-003 Autonomous Sales Lead Qualification Agent** for NovaWorks Technologies.

AI technologies were utilized in two key roles:
1. **Developer Productivity Assistance:** Supporting the project author in designing workflows, structuring files, generating test logs, and drafting project markdown documentation.
2. **Runtime Agent Capabilities:** Employing generative models built natively into Microsoft Copilot Studio to parse incoming emails, extract entities, normalize values, and determine tool execution sequences.

All final system instructions, logic mappings, testing logs, and code configurations were audited, tested, and validated by the project developer to ensure strict adherence to the PRD.

---

## 2. AI Tools Used During Development

### 2.1 Microsoft Copilot Studio (Generative Orchestration)
- **Purpose:** Platform for configuring the autonomous agent.
- **Application:** Used the built-in Copilot Studio compiler to define event-driven triggers, link M365 Outlook, Excel, and Word connectors, and enable Generative Orchestration.
- **Entity Extraction:** Leveraged Copilot Studio's standard conversational AI and natural language understanding (NLU) nodes to parse unstructured email bodies into variables.

### 2.2 Advanced AI Code Assistants (Gemini / Copilot)
- **Purpose:** Code, logic, and documentation drafting.
- **Application:** 
  - Supported the mathematical verification of the 20 test cases based on the `QualificationRulesTable`.
  - Assisted in designing the markdown schemas for the ten required GitHub files.
  - Drafted the Mermaid system architecture diagrams.
  - Created test log templates from the provided spreadsheet schemas.

---

## 3. Runtime AI and Gating Controls

The agent uses generative models to parse email content, which introduces a potential risk of operational drift. The following controls were implemented to mitigate this risk:

- **Input Sanitization:** The email body is pre-processed to strip complex HTML formatting before being sent to the extraction prompt, ensuring high reliability in entity parsing.
- **Scoring Gating:** Scoring calculations are checked against deterministic condition branches in Copilot Studio rather than relying on the LLM to count numbers.
- **Confidence Threshold Gate:** The agent extracts a `Decision_Confidence` rating (`High`, `Medium`, `Low`) from its own extraction quality. If confidence is evaluated as `Low`, or if mandatory fields are missing, the agent bypasses standard scoring and routes the lead immediately to `Human Review Required` or `Additional Information Required`.
- **Competitor Risk Guardrail:** A hardcoded search block scans for known competitor names or generic competitive terms. Matching cases are forced to the `Human Review Required` route, suppressing all outbound communications.

---

## 4. Human Validation and Verification

Poonam Bhatt manually verified all system actions:
1. **Spreadsheet Verification:** Audited all 20 rows in `LeadsRegisterTable` to ensure scores computed by the agent matched the reference calculations in the Excel files.
2. **Defect Tracking & Retesting:** Detected and logged DF-001 on TC-015 ( Stealth Company), corrected the instruction rules, re-ran the test case, and verified that it successfully resolved to `Additional Information Required`.
3. **Outbound Communications Audit:** Checked that external emails sent to client addresses (synthetic `.example` domains) contained the correct Lead ID, company name, and list of missing fields, and that no confidential internal data (scores, classifications, internal notes) was leaked.
4. **Secrets Scan:** Inspected all committed files and screenshots to confirm no active Entra ID client secrets, tenant IDs, SharePoint URLs, personal email accounts, or client data were exposed.

---

## 5. Final Declaration

AI was used as an active development partner and runtime orchestration engine for this project.

The final P2-003 Autonomous Sales Lead Qualification Agent was designed, configured, tested, and validated according to the NovaWorks PRD guidelines. The developer remains fully responsible for the logic, accuracy, and compliance of the submitted solution.
