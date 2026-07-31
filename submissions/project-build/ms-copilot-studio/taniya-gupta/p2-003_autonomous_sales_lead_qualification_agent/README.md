# P2-003 — Autonomous Sales Lead Qualification Agent

**Platform:** Microsoft Copilot Studio
**Project Phase:** Phase 2 Project Build
**Status:** Complete — Published and Tested

---

## Project Summary

The P2-003 agent autonomously processes incoming sales lead emails for NovaWorks. It watches a shared Outlook inbox, reads emails tagged `[P2-003 LEAD]`, scores each lead across 8 dimensions, classifies it and takes fully autonomous action - creating Word reports, logging Excel rows, and sending Outlook notifications.

## Agent URL

See [agent-url.md](agent-url.md) for the published agent URL.

## Configuration Status

| Component | Status |
|---|---|
| Copilot Studio agent created | Complete |
| Generative orchestration enabled | Complete |
| Knowledge source uploaded | Complete |
| Outlook trigger configured | Complete |
| Excel tools configured | Complete |
| Word Online tool configured | Complete |
| Outlook Send email tool configured | Complete |
| Agent published | Complete |
| Evaluation: 23 of 23 test cases passed | Complete |

## Completion Status

All PRD requirements are implemented and verified. The agent correctly handles Hot, Qualified, Nurture, Low Priority, Human Review Required, Additional Information Required, Duplicate, and Not-a-Sales-Lead classification paths. All mandatory test cases from the PRD have been executed and passed.

## Repository Contents

| File / Folder | Purpose |
|---|---|
| README.md | This file |
| agent-url.md | Published URL and access details |
| solution-summary.md | Business problem, architecture, and outcomes |
| agent-instructions-design.md | Instruction design reference |
| trigger-design.md | Outlook trigger configuration and evidence |
| tool-design.md | Tool configuration details |
| qualification-logic.md | Scoring model, overrides, and classification |
| test-report.md | Full test execution evidence |
| known-limitations.md | Known constraints and workarounds |
| ai-usage-declaration.md | AI tools used and validation approach |

---

## 📷 Screenshots & Visual Evidence References

The following screenshots are available in the [`screenshots/`](screenshots/) directory as visual evidence of implementation and testing:

### 1. Agent Overview
![Agent Overview](screenshots/01_agent_overview.png)

### 2. Generative Orchestration Settings
![Generative Orchestration](screenshots/02_generative_orchestration.png)

### 3. Office 365 Outlook Event Trigger (`[P2-003 LEAD]`)
![Outlook Trigger Configuration](screenshots/03_outlook_trigger.png)

### 4. Copilot Studio Connected Tools Overview
![Connected Tools List](screenshots/04_tools_list.png)

### 5. Excel Online Connector Configuration
![Excel Tool Configuration](screenshots/05_excel_configuration.png)

### 6. Word Online Connector Configuration
![Word Tool Configuration](screenshots/06_word_configuration.png)

### 7. Office 365 Outlook Send Email Configuration
![Outlook Send Tool Configuration](screenshots/07_outlook_configuration.png)

### 8. Successful End-to-End Lead Processing Run
![Successful Run Evidence](screenshots/08_successful_run.png)

## Successful acknowledgement mail
![Successful Run Evidence](screenshots/08_successful_run_mail.png)

### 9. Excel Lead Register & Duplicate Prevention Log
![Duplicate Prevention Log](screenshots/09_duplicate_prevention.png)

### 10. Generated Word Qualification Report in OneDrive
![Generated Word Report](screenshots/10_generated_word_report.png)

### 11. Published Agent Confirmation State
![Published Agent Status](screenshots/11_published_agent.png)

### 12. Evaluation with 1 failed testcase that was corrected and retested
![Evaluation](screenshots/12_evaluation_with_1_fail.png)

### 11. Final evaluation result
![Evaluation](screenshots/12_final_evaluation.png)

---

> All data in this repository is 100% synthetic. No real customer data, real email addresses or real company information is present.
