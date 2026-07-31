# Solution Summary

# P2-003 Autonomous Sales Lead Qualification Agent

---

## 1. Executive Summary & Business Problem

### Business Problem
NovaWorks Technologies receives a high volume of sales inquiries daily through a monitored Microsoft 365 mailbox. The existing sales operations workflow is entirely manual and presents several operational challenges:
- **Inefficiency & Delay:** Sales Operations staff must manually read every email, identify key details, and copy-paste them into an Excel lead register. This causes response delays of several hours to days, risking lead decay.
- **Inconsistent Routing:** Opportunities are manually routed to sales representatives based on territory. Human errors in country-to-territory mapping lead to misassigned accounts.
- **Duplicate Records:** Inquiries submitted multiple times or follow-up emails from the same client create separate records and double-booking, resulting in fragmented communication.
- **Ineffective Scoring:** Leads are not consistently scored or prioritized, making it difficult for sales representatives to identify high-value opportunities (`Hot` or `Qualified`) instantly.
- **Manual Documentation:** Creating briefing documents for qualified leads requires sales ops to copy data from emails into Word templates manually.

### Solution Overview
The **Autonomous Sales Lead Qualification Agent** built in **Microsoft Copilot Studio** automates this entire front-line triage. The agent monitors the mailbox, validates if an email is a sales lead, extracts and normalizes information, runs multi-layered duplicate checks, calculates a multi-factor qualification score, classifies the lead, updates the Excel register, generates a Word briefing document, notifies the sales owner, and sends appropriate external communications.

---

## 2. Solution Architecture

The solution uses a fully integrated, event-driven architecture within the Microsoft 365 ecosystem. The complete workflow is built inside Microsoft Copilot Studio, utilizing event triggers, generative orchestration, and direct connector tools.

```mermaid
graph TD
    A[Incoming Email in Outlook] -->|Trigger: When a new email arrives V3| B(Copilot Studio Agent)
    B -->|Subject Filter Check: [P2-003 LEAD]| C{Is in Scope?}
    C -->|No| D[Ignore / Terminate Run]
    C -->|Yes| E[Generative Information Extraction & Normalization]
    E --> F[Duplicate Check: LeadsRegisterTable]
    F -->|Duplicate Found| G[Update Row & Log Action in Excel]
    F -->|New Lead| H[Calculate Qualification Score & Determine Classification]
    H --> I{Apply Overrides & Exceptions}
    I -->|Hot / Qualified| J[Generate Word Report + Add Excel Row + Notify Owner/Ops + Send Client Acknowledgement]
    I -->|Nurture / Low Priority| K[Add Excel Row + Send Client Nurture/Ack + Notify Owner only if Strategic]
    I -->|Human Review / Exception| L[Add Excel Row + Alert Sales Ops + Withhold External Comms]
    I -->|Not a Sales Lead| M[Log Ignored/Non-Sales + No Report + No Owner Assignment]
```

### Key Components:
1. **Event Trigger:** Office 365 Outlook connector listens for new emails.
2. **Generative Orchestrator:** Copilot Studio's AI orchestrator parses the email body, extracts structured metadata, and maps variables.
3. **Data Storage:** Excel Online (Business) hosted on OneDrive/SharePoint storing six tables: `LeadsRegisterTable`, `QualificationRulesTable`, `TerritoryOwnersTable`, `ProductCatalogTable`, `SalesOwnersTable`, and `ActionMatrixTable`.
4. **Document Generation:** Word Online (Business) connector generating structured briefs using custom metadata.
5. **Comms Gateway:** Office 365 Outlook connector sending notifications and alerts.

---

## 3. Core Process Logic

### Step 1: Trigger & Safety Filtering
- **Action:** Triggers automatically.
- **Rule:** Filter on `Subject contains [P2-003 LEAD]`. Non-matching emails are ignored immediately, safeguarding tenant privacy.

### Step 2: Information Extraction & Normalization
- **Extraction:** Captures source metadata (Message ID, email, date), contact details (name, job title, role), organization details (company, country, size, industry), opportunity details (product interest, business need, budget, timeline), and assessments.
- **Normalization:** 
  - Countries must match `TerritoryOwnersTable`.
  - Product names must match `ProductCatalogTable`.
  - Company size mapped to standard tiers (`Enterprise`, `Mid-Market`, `SMB`, `Startup/Micro`).
  - Decision role mapped to standard tiers (`Decision Maker`, `Strong Influencer`, `Researcher/User`, `Unknown`).

### Step 3: Duplicate Detection
- **Level 1 Check:** Scans `LeadsRegisterTable` for exact `Source_Message_ID` match.
- **Level 2 Check:** Compares recent company name, sender email, and product interest.
- **Outcome:** If a duplicate is found, the agent updates the existing row with the latest timestamp and last action, classifies the outcome as `Duplicate`, and suppresses new Word reports or client acknowledgements to maintain data hygiene and professional comms.

### Step 4: Scoring & Classification
- **Scoring:** Points are calculated dynamically across 8 dimensions (max 100 points) based on configured rules in `QualificationRulesTable`.
- **Classification Thresholds:**
  - **Hot:** Score 85–100 (no exception)
  - **Qualified:** Score 70–84 (no exception)
  - **Nurture:** Score 50–69
  - **Low Priority:** Score < 50
- **Exception Overrides:**
  - *Startup/Micro Budget Override:* A startup/micro lead with a budget under 50% of the product's recommended minimum is immediately classified as `Low Priority` regardless of score.
  - *Low Confidence / Security Override:* Competitive risks, unmapped territories, unknown products, or low-confidence assessments are classified as `Human Review Required` to block external leaks of qualification decisions.

### Step 5: Autonomous Action Execution
- **Hot/Qualified:** Create Word report; assign territory owner; email owner (+ Sales Ops if Hot); send external client acknowledgment with Lead ID.
- **Nurture:** Log to Excel; send follow-up request for 1-2 missing fields.
- **Human Review / Low Priority:** Log to Excel; notify Sales Ops; withhold client communication.
- **Not a Sales Lead:** Log as ignored; no owner assignment or notifications.

---

## 4. Expected Business Outcomes

The deployment of the Autonomous Sales Lead Qualification Agent delivers significant operational improvements:

- **100% Automated Triage:** Replaces manual review of inbound emails, freeing up approximately 12-15 hours per week for the sales operations team.
- **95% Lead Response Velocity:** Reduces the average response time for incoming inquiries from 6 hours to under 3 minutes, significantly increasing conversion probabilities.
- **Zero Duplicate Contamination:** Eliminates duplicate data entries in the CRM, preventing multiple sales owners from reaching out to the same contact.
- **Standardized Resource Allocation:** Ensures that high-value (`Hot`) leads are immediately assigned to the correct territory owner and that capacity limits are maintained.
- **Data Compliance and Governance:** Restricts access using Entra ID, prevents external transmission of sensitive qualification data for low-confidence or high-risk leads, and provides audit logs of all actions in the Excel registry.
