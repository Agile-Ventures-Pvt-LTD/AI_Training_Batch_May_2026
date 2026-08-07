# Specialist Child Agents Design - P2-005

## 1. Budget & Commercial Specialist
- **Role:** Evaluates proposed vs approved budget, CPL targets, financial variance and executive approval thresholds.
- **Tools:** `ListBudgetRules` (Excel), `ListApprovalMatrix` (Excel), `GetCampaignDetails` (Excel).

## 2. Brand & Content Compliance Specialist
- **Role:** Evaluates product naming, restricted claims, regulatory sensitivity, disclaimers and brand approvals.
- **Tools:** `GetBrandCampaignDetails` (Excel), `ListBrandAssetStatus` (Excel).
- **Knowledge:** `NovaSphere_Brand_and_Content_Guidelines.docx`.

## 3. Channel Readiness Specialist
- **Role:** Evaluates minimum lead times, tracking requirements and prerequisites across ALL listed channels.
- **Tools:** `GetChannelCampaignDetails` (Excel), `ListChannelRequirements` (Excel), `ListChannelAssetStatus` (Excel).

## 4. Asset Readiness Specialist
- **Role:** Evaluates asset availability, missing assets, pending QA and <5 days launch timing risk.
- **Tools:** `GetAssetCampaignDetails` (Excel), `ListAssetStatusDetails` (Excel).

## 5. Launch Risk & Decision Specialist
- **Role:** Receives consolidated outputs from 4 specialists, calculates risk level, applies outcome precedence and proposes readiness status.
- **Tools:** None.

## 6. Reporting & Communication Specialist
- **Role:** Generates Word readiness report, updates Excel register and sends conditional Outlook email.
- **Tools:** `CreateWordReadinessReport` (Word Online), `SendOutlookNotificationEmail` (Outlook), `UpdateFinalCampaignStatus` (Excel).
