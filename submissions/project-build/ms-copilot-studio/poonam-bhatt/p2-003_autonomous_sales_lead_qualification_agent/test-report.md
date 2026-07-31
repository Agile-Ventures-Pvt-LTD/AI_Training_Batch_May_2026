# Test Execution Report

# P2-003 Autonomous Sales Lead Qualification Agent

---

## 1. Test Summary

The Autonomous Sales Lead Qualification Agent has been tested against the mandatory 20 test cases representing various lead qualities, organizational sizes, geographical territories, duplicate inquiries, exceptions, and non-sales requests.

- **Total Test Cases Executed:** 21 (including 1 failed test case that was corrected and retested, and 1 idempotency test)
- **Passed:** 21
- **Failed:** 0 (after correction)
- **Defects Corrected:** 1
- **Execution Date:** July 31, 2026
- **Test Environment:** Microsoft Copilot Studio (Sandbox environment linked to a synthetic Office 365 tenant and OneDrive storage)

---

## 2. Test Execution Log

The following table summarizes the execution outcomes for all test scenarios:

| Case ID | Contact / Company | Score | Classification | Assigned Owner | Excel Result | Word Result | Outlook Result | Status | Screenshot Path |
|---|---|---|---|---|---|---|---|---|---|
| **TC-001** | Neha Sharma / Orbital Finance | 98 | Hot | Priya Nair | Row Added (LD-2026-0009) | Report Created | Client Ack + Owner/Ops Notification | **Pass** | `screenshots/tc-001-success.png` |
| **TC-002** | Ben Hughes / Acme Logistics | 88 | Hot | Emma Clarke | Row Added (LD-2026-0010) | Report Created | Client Ack + Owner/Ops Notification | **Pass** | `screenshots/tc-002-success.png` |
| **TC-003** | Aarav Student / City University | N/A | Not a Sales Lead | Sales Operations | Logged (Ignored) | Not Created | Suppressed | **Pass** | `screenshots/tc-003-nonsales.png` |
| **TC-004** | Arjun Mehta / Apex Bank | N/A | Duplicate | Priya Nair | Row Updated (LD-2026-0001) | Suppressed | Suppressed | **Pass** | `screenshots/tc-004-duplicate.png` |
| **TC-005** | Fatima Al Noor / Desert Retail | 81 | Qualified | Omar Rahman | Row Added (LD-2026-0011) | Report Created | Client Ack + Owner Notification | **Pass** | `screenshots/tc-005-success.png` |
| **TC-006** | Mina Lee / SmallStartup | 74* | Low Priority | Daniel Tan | Row Added (LD-2026-0012) | Not Created | Client Ack (Polite follow-up) | **Pass** | `screenshots/tc-006-override.png` |
| **TC-007** | Carlos Reyes / Global Mining | 90* | Human Review Required | Sales Operations | Row Added (LD-2026-0013) | Not Created | Ops Review Alert (Unmapped Territory) | **Pass** | `screenshots/tc-007-unmapped.png` |
| **TC-008** | Name missing / Unknown | N/A | Additional Info Required| Sales Operations | Row Added (LD-2026-0014) | Not Created | Client Info Request Sent | **Pass** | `screenshots/tc-008-missing.png` |
| **TC-009** | Daniel Moore / Existing Client | N/A | Not a Sales Lead | Sales Operations | Logged (Support) | Not Created | Internal Support Route | **Pass** | `screenshots/tc-009-support.png` |
| **TC-010** | Oliver King / Public Agency | 78 | Qualified | Emma Clarke | Row Added (LD-2026-0015) | Report Created | Client Ack + Owner Notification | **Pass** | `screenshots/tc-010-success.png` |
| **TC-011** | Sara Jones / MedCare | 94 | Hot | Sophia Carter | Row Added (LD-2026-0016) | Report Created | Client Ack + Owner/Ops Notification | **Pass** | `screenshots/tc-011-success.png` |
| **TC-012** | Kenji Mori / Factory Intl | 81* | Human Review Required | Sales Operations | Row Added (LD-2026-0017) | Not Created | Ops Review Alert (Unmapped Territory) | **Pass** | `screenshots/tc-012-unmapped.png` |
| **TC-013** | Lucy Adams / RetailCo | 97 | Hot | Olivia Bennett | Row Added (LD-2026-0018) | Report Created | Client Ack + Owner/Ops Notification | **Pass** | `screenshots/tc-013-success.png` |
| **TC-014** | Mark Evans / Boutique Advisory | 79 | Qualified | Emma Clarke | Row Added (LD-2026-0019) | Report Created | Client Ack + Owner Notification | **Pass** | `screenshots/tc-014-success.png` |
| **TC-015** | Name missing / Stealth Co | 67 | Additional Info Required| Sales Operations | Row Added (LD-2026-0020) | Not Created | Client Info Request Sent | **Pass** | `screenshots/tc-015-retest.png` |
| **TC-016** | Rival Analyst / Rival AI | N/A | Human Review Required | Sales Operations | Row Added (LD-2026-0021) | Not Created | Ops Review Alert (Competitor Risk) | **Pass** | `screenshots/tc-016-competitor.png`|
| **TC-017** | Mia Wong / SEA Retail Group | 82 | Qualified | Daniel Tan | Row Added (LD-2026-0022) | Report Created | Client Ack + Owner Notification | **Pass** | `screenshots/tc-017-success.png` |
| **TC-018** | Thabo Mokoena / Industry Holdings| 71 | Qualified | Amina Mensah | Row Added (LD-2026-0023) | Report Created | Client Ack + Owner Notification | **Pass** | `screenshots/tc-018-success.png` |
| **TC-019** | Nora Schmidt / EuroBank | 100 | Hot | Lucas Martin | Row Added (LD-2026-0024) | Report Created | Client Ack + Owner/Ops Notification | **Pass** | `screenshots/tc-019-success.png` |
| **TC-020** | Peter Hill / Hill Trading | N/A* | Human Review Required | Sales Operations | Row Added (LD-2026-0025) | Not Created | Ops Review Alert (Unknown Product) | **Pass** | `screenshots/tc-020-unknown.png` |
| **TC-021** | Repeated Trigger (TC-001 replay)| N/A | Duplicate | Priya Nair | Row Updated (LD-2026-0009) | Suppressed | Suppressed | **Pass** | `screenshots/tc-021-idempotency.png`|

*\*Note: Scores with asterisks indicate that the final classification was overridden by business rule exceptions (e.g., startup budgets under minimum, unmapped territories, competitor risk, or unidentified products).*

---

## 3. Defect Correction & Retesting

### Defect ID: **DF-001 - Missed Completeness Route on TC-015**
- **Test Case:** TC-015 (Inbound lead from Stealth Company)
- **Scenario:** The incoming message was missing 3 key fields: Contact Name, Job Title, and Decision Role.
- **Expected Outcome:** The agent should classify the lead as `Additional Information Required` and send a missing information request using Outlook, without generating a Word brief.
- **Actual Outcome (First Run):** The agent evaluated the lead with a score of `67` based on the partial parameters extracted and classified it as `Nurture` (status: Received), proceeding to search for a sales owner and attempting to generate a partial Word briefing.
- **Root Cause:** The system prompt and variable checks inside the Copilot Studio orchestration layer did not enforce the completeness check as a primary gating rule. The agent calculated scoring and routed based on the score threshold instead of validating the `Missing_Field_Count` parameter first.
- **Correction Applied:**
  1. Updated the Agent System Prompt inside `agent-instructions-design.md` to establish a priority rule:
     > "If three or more mandatory fields are missing, classify the lead immediately as 'Additional Information Required', regardless of the total score, and skip owner assignment."
  2. Configured a conditional branch node in Copilot Studio: `If Missing_Field_Count >= 3, Route to Additional Information Required path`.
- **Retest Evidence:**
  - **Date:** July 31, 2026
  - **Outcome:** The agent successfully classified the lead as `Additional Information Required`. The database was updated with `Classification = Additional Information Required`, `Processing_Status = Awaiting Information`, no Word document was generated, and the correct outbound email listing the three missing fields was sent to the client. Status: **Pass**.

---

## 4. Duplicate Prevention Verification

- **Case Verified:** TC-004 (Arjun Mehta, Apex Bank) & TC-021 (Repeated Trigger).
- **Execution Log Details:**
  - On receiving the email for TC-004, the agent scanned `LeadsRegisterTable` and matched the name and company to `LD-2026-0001` (Arjun Mehta / Apex Bank - preloaded seed record).
  - The agent updated the existing row (changing `Last_Updated` to `2026-07-31` and setting `Last_Action = Follow-up duplicate email received; recorded`).
  - No new row was written to the spreadsheet.
  - No second Word report was created.
  - The external email acknowledgment was suppressed, protecting the client from receiving duplicate automated receipts.
- **Idempotency Verification:** On re-delivery of the exact email from TC-001 (TC-021), the agent matched the `Source_Message_ID` (`MSG-EX-001`), updated the existing row `LD-2026-0009` with the timestamp and action, and safely terminated.
