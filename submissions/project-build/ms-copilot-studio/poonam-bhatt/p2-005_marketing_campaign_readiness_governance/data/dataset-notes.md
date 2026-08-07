# Dataset Notes & Schemas

The system reads and writes to an Excel workbook stored in OneDrive for Business. Below are the table definitions:

---

## 1. Campaign Requests Table
Main operational register logging incoming campaign details.
*   `CampaignID` (String - Key) — Unique campaign identifier.
*   `CampaignName` (String) — Marketing campaign title.
*   `Product` (String) — Associated product.
*   `LaunchDate` (String) — Planned launch date.
*   `DaysToLaunch` (Number) — Calculation: LaunchDate - Today().
*   `ProposedBudget` (Number) — Proposed budget.
*   `ApprovedBudget` (Number) — Approved budget.
*   `TargetCPL` (Number) — Target Cost Per Lead.
*   `Geography` (String) — Market region (e.g., Multi-Market, Domestic).
*   `Channels` (String) — Target marketing channels (e.g., Email, LinkedIn).
*   `Sensitivity` (String) — Regulatory sensitivity (e.g., High, Normal).
*   `CampaignOwner` (String) — Campaign manager name.
*   `CampaignStatus` (String) — Lifecycle status (`Pending`, `In Assessment`, `Awaiting Remediation`, `Awaiting Approval`, `Completed`).

---

## 2. Budget Rules Table
Defines corporate financial audit variance rules.
*   Variance = ProposedBudget - ApprovedBudget.
*   If Variance > 0 $ightarrow$ Marketing Director approval required.
*   If ProposedBudget > 1,000,000 INR $ightarrow$ VP Marketing approval required.
*   If TargetCPL > 4,000 INR $ightarrow$ VP Marketing approval required.

---

## 3. Channel Requirements Table
Maps lead times and tracking configurations per channel:
*   Email $ightarrow$ Lead time: 2 days. Tracking pixel: Optional.
*   LinkedIn $ightarrow$ Lead time: 5 days. Tracking pixel: Mandatory.
*   Web $ightarrow$ Lead time: 3 days. Tracking pixel: Mandatory.

---

## 4. Asset Status Table
List of creative assets linked by `CampaignID`:
*   `AssetID` (String - Key)
*   `CampaignID` (String - Foreign Key)
*   `AssetName` (String)
*   `AssetType` (String - e.g., Landing Page, Banner)
*   `AssetStatus` (String - `Ready`, `QA`, `Missing`, `Needs Changes`)

---

## 5. Summary of the 6 Campaign Dataset Records

1.  **CP-001 (NovaReady):** Near-ready campaign. Satisfies all baseline rules. Sets status to `Ready`.
2.  **CP-002 (NovaBudget):** Over-budget campaign. Exceeds approved budget and target CPL limits. Requires VP Marketing approval.
3.  **CP-003 (NovaRemedy):** Remediation case. Missing landing page asset. Triggers remediation loop and selective reassessment.
4.  **CP-004 (NovaSensitive):** High-sensitivity/high-budget case. Exceeds INR 1M and is marked High Sensitivity. Requires Compliance Committee approval.
5.  **CP-005 (NovaUrgent):** Urgent campaign with missing assets. Launch date is in less than 5 days with missing assets. Triggers `Not Ready` outcome.
6.  **CP-006 (NovaGlobal):** Multi-region approval case. Multi-market geography. Requires Regional Marketing Lead approval.
