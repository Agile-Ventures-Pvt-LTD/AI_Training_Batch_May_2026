# Dataset Notes

## 1. Data Type

All project data is synthetic and intended for the Microsoft Copilot Studio P2-005 project build.

## 2. Participant Files

### P2-005_Marketing_Campaign_Readiness_Lab_Data.xlsx

Primary operational dataset containing the campaign and supporting tables.

The workbook should be stored in OneDrive for Business or SharePoint so that Excel Online (Business) can access its tables.

### Campaign_Requests.csv

Lightweight copy of campaign intake records.

### NovaSphere_Marketing_Governance_Policy.docx

Authoritative knowledge source for:

- Readiness statuses
- Budget approval
- Timing
- Asset controls
- Geography
- Sensitivity
- Autonomous processing
- Reassessment

### NovaSphere_Brand_and_Content_Guidelines.docx

Authoritative knowledge source for:

- Brand terminology
- Product naming
- Claims
- Evidence requirements
- Channel-content rules
- Brand review classification

## 3. Trainer-Only File

`P2-005_Evaluator_Expected_Outcomes.csv` is identified as trainer-only in the supplied dataset manifest.

It should not be distributed when participants are expected to derive outcomes independently.

## 4. Knowledge and Tool Scoping

Knowledge and tools should be scoped narrowly to each agent.

Recommended mapping:

| Agent | Primary Data / Knowledge |
|---|---|
| Supervisor | Governance Policy + orchestration/state data |
| Budget Specialist | Campaign Requests + Budget Rules + Approval Matrix |
| Brand Specialist | Brand Guidelines + Campaign Requests + Asset Status |
| Channel Specialist | Campaign Requests + Channel Requirements + Asset Status |
| Asset Specialist | Asset Status + relevant campaign data |
| Risk Specialist | Specialist outputs + governance context |
| Reporting Specialist | Validated Supervisor results + Word/Outlook |

## 5. Dataset Handling

The trainer-supplied dataset does not need to be copied into the GitHub repository unless explicitly instructed.
