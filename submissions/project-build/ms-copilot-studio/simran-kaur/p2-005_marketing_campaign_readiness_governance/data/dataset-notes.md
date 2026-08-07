# Dataset Notes

## Supplied artifacts

### Campaign_Requests.csv
Campaign request records and campaign-level information.

### P2-005_Marketing_Campaign_Readiness_Lab_Data.xlsx
Operational workbook used by the Copilot Studio solution. The project data model includes the following tables:
- Campaign_Requests
- Budget_Rules
- Approval_Matrix
- Asset_Status
- Channel_Requirements
- Stakeholders

### NovaSphere_Marketing_Governance_Policy.docx
Authoritative governance source for readiness statuses, budget approval, timing, asset controls, geography, sensitivity, autonomous-processing rules, and reassessment.

### NovaSphere_Brand_and_Content_Guidelines.docx
Authoritative brand/content source for brand terminology, product naming, claims, evidence requirements, channel-content rules, and brand review classification.

### P2-005_Dataset_Manifest.md
Dataset documentation describing structure, fields, and interpretation.

### P2-005_Evaluator_Expected_Outcomes.csv
Expected evaluation outcomes used to compare actual solution behavior against required results.

## Operational guidance
- Use `CampaignID` as the primary logical key where applicable.
- Excel must be stored in OneDrive for Business or SharePoint for Excel Online (Business) access.
- Keep tools scoped to the specialist that needs them.
- Use synthetic data only.

## Important distinction
The PRD and supplied governance documents are authoritative. This file should be updated with exact field names, representative values, and any dataset-specific mappings after the workbook/manifest is inspected during implementation.
