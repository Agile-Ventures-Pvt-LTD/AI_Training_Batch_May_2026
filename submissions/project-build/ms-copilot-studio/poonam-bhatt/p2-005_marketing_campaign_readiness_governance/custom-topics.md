# Custom Topics & Precedence Rules

## 1. Campaign Intake & Validation (Topic 1)
Acts as a deterministic pre-assessment check to ensure campaign data is valid and prevents duplicate assessment runs.
*   **Input Parameters:** `CampaignID`, `CampaignName`, `Product`, `LaunchDate`, `DaysToLaunch`, `ProposedBudget`, `ApprovedBudget`, `TargetCPL`, `Geography`, `Channels`, `Sensitivity`, `CampaignOwner`, `CampaignStatus`.
*   **Output Parameters:** `ValidationStatus`, `DuplicateDetected`, `CampaignStatus`, `BudgetVariance`.
*   **Duplicate Handling:** If `CampaignStatus` is already `"In Assessment"`, `"Awaiting Remediation"`, `"Awaiting Approval"`, or `"Completed"`, it sets `DuplicateDetected = true` and `ValidationStatus = "Failed: Duplicate assessment detected"`, halting the intake immediately.
*   **Validations:** Checks that mandatory fields exist, and verifies `DaysToLaunch >= 0`.

---

## 2. Remediation & Selective Reassessment (Topic 2)
Coordinates corrective actions when specialist reviews fail, keeping track of loop limits and selective reassessments.
*   **Input Parameters:** `BudgetStatusAssessmentStatus`, `BrandStatusAssessmentStatus`, `ChannelStatusAssessmentStatus`, `AssetStatusAssessmentStatus`, `ReassessmentCycleCount`, `CampaignOwner`, `BudgetCorrected`, `BrandCorrected`, `ChannelCorrected`, `AssetCorrected`.
*   **Output Parameters:** `CampaignStatus`, `ReassessmentCycleCount`, `RemediationActions`, `ResponsibleOwner`, `BudgetStatusAssessmentStatus`, `BrandStatusAssessmentStatus`, `ChannelStatusAssessmentStatus`, `AssetStatusAssessmentStatus`.
*   **Loop Control:** Checks if `ReassessmentCycleCount >= 2`. If yes, it aborts the loop, sets status to `Manual Review`, and alerts the supervisor.
*   **Selective Reassessment:** Marks failed domains as `Stale`. Once corrections are detected (e.g. `BudgetCorrected = true`), it resets only that specific specialist to `Pending` for reassessment, preserving already passed results.

---

## 3. Approval & Finalisation (Topic 3)
Evaluates if a campaign meets governance thresholds requiring manual human sign-off.
*   **Input Parameters:** `ProposedBudget`, `ApprovedBudget`, `TargetCPL`, `Sensitivity`, `Geography`, `DaysToLaunch`, `HasClaims`.
*   **Output Parameters:** `CampaignStatus`, `FinalReadiness`, `ApprovalRequired`, `RequiredApprover`, `ApprovalReason`.
*   **Governance Rules:**
    *   Proposed budget > approved budget $ightarrow$ Requires "Marketing Director" approval.
    *   Proposed budget > 1,000,000 INR $ightarrow$ Requires "VP Marketing" approval.
    *   Target CPL > 4,000 INR $ightarrow$ Requires "VP Marketing" approval.
    *   High regulatory sensitivity $ightarrow$ Requires "Brand & Compliance Committee" approval.
    *   Multi-market geography $ightarrow$ Requires "Regional Marketing Lead" approval.
    *   DaysToLaunch < 5 $ightarrow$ Requires "VP Marketing & Executive Sponsor" approval.
*   **Policy Enforcements:** Prevents setting final status to `Ready` while approval is outstanding; logs the reason, sets status to `Awaiting Approval`, and restricts the AI agent from auto-approving.

---

## 4. Final Readiness Precedence Rules
When specialists return conflicting results, the Supervisor applies this strict outcome hierarchy (no averaging):

| Precedence | Outcome | Condition |
| :--- | :--- | :--- |
| **1** | **Not Ready** | Any specialist returns `Block`, launch date is in the past, or reassessment loop failed. |
| **2** | **Management Approval Required** | Campaign meets any human approval triggers and approvals are outstanding. |
| **3** | **Remediation Required** | Any specialist returns `Fail` or is marked as `Stale`. |
| **4** | **Ready with Conditions** | Only non-blocking conditions remain (e.g., pending QA). |
| **5** | **Ready** | All specialists return `Pass` / `Ready` and all criteria are satisfied. |
