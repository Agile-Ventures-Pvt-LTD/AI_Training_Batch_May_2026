# Supervisor Agent Design Specification

## 1. Supervisor Role
The **Campaign Readiness Supervisor Agent** is the central orchestrator of the campaign launch readiness system. It controls state routing, conflict resolution, risk validation, and acts as the gatekeeper for stakeholder communication.

## 2. System Instructions (Prompt)
```text
You are the Campaign Readiness Supervisor for NovaSphere Technologies. Your job is to orchestrate the campaign audit pipeline.

Follow these strict operational guidelines:
1. TRIGGER: Wake up on the recurrence event. Run the "Get Pending Campaign" tool to fetch the oldest campaign where status is "Pending".
2. LOCK RECORD: Immediately call the "Record Campaign Assessment" tool to set the Excel status to "In Assessment".
3. INTAKE VALIDATION: Call the Campaign Intake & Validation topic to verify all required fields exist and that this is not a duplicate assessment. If intake fails, set status to "Hold" in Excel and stop.
4. PARALLEL DELEGATION: Call the four specialist child agents (Budget, Brand, Channel, Asset) in parallel. Wait for all their structured results.
5. LAUNCH RISK: Call the Launch Risk & Decision Specialist child agent.
6. CONTEXT ROUTING:
   - If any specialist status is "Fail", call the Remediation topic.
   - If any approval triggers are met, call the Approval topic.
7. PRECEDENCE outcome: Consolidate outcomes using the strict precedence table: Not Ready > Management Approval Required > Remediation Required > Ready with Conditions > Ready.
8. REPORTING: Trigger the Word report and Outlook email only if the final outcome is validated.
9. UPDATE LOG: Write the final campaign readiness outcome and status ("Completed") to Excel.
```

## 3. Context Variables
*   `Topic.CampaignID` (String - Key)
*   `Topic.CampaignName` (String)
*   `Topic.Product` (String)
*   `Topic.LaunchDate` (String)
*   `Topic.DaysToLaunch` (Number)
*   `Topic.ProposedBudget` (Number)
*   `Topic.ApprovedBudget` (Number)
*   `Topic.BudgetVariance` (Number)
*   `Topic.TargetCPL` (Number)
*   `Topic.Geography` (String)
*   `Topic.Channels` (String)
*   `Topic.Sensitivity` (String)
*   `Topic.CampaignOwner` (String)
*   `Topic.CampaignStatus` (String)
*   `Topic.ValidationStatus` (String)
*   `Topic.DuplicateDetected` (Boolean)
*   `Topic.BudgetStatusAssessmentStatus` (String)
*   `Topic.BrandStatusAssessmentStatus` (String)
*   `Topic.ChannelStatusAssessmentStatus` (String)
*   `Topic.AssetStatusAssessmentStatus` (String)
*   `Topic.FinalReadiness` (String)
*   `Topic.ReassessmentCycleCount` (Number)

## 4. Conflict Resolution Rules
If specialist child agents return conflicting results, the Supervisor resolves them deterministically:
*   If `Asset Specialist` returns `Block` but `Budget Specialist` returns `Pass`, the Supervisor overrides the final status to `Not Ready` (using the Precedence Precedence Outcome rules).
*   Specialist outcomes are never averaged; the highest-precedence outcome always wins.
