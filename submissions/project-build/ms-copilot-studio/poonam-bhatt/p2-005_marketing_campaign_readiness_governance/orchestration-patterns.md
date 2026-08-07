# Orchestration Patterns

## 1. Sequential Orchestration
The system executes a strictly sequential pipeline to ensure governance gates cannot be bypassed:
`Recurrence Trigger` $ightarrow$ `Intake Validation` $ightarrow$ `Specialist Assessments` $ightarrow$ `Launch Risk Decision` $ightarrow$ `Remediation/Approval routing` $ightarrow$ `Final Validation` $ightarrow$ `Word Reporting` $ightarrow$ `Outlook Notification` $ightarrow$ `Excel Status Update`.

*   **Dependencies:** Later stages are blocked until earlier steps succeed (e.g. reporting and emails cannot be triggered until supervisor validation succeeds).

## 2. Parallel Fan-Out/Fan-In
*   **Fan-Out:** Immediately after campaign validation passes, the Supervisor invokes the four specialist child agents (`Budget`, `Brand`, `Channel`, `Asset`) in parallel.
*   **Fan-In:** The Supervisor pauses and waits for all four specialists to return their structured outputs before passing the consolidated findings to the Risk Specialist.

## 3. Hierarchical Orchestration
*   **Supervisor Agent:** Acts as the central executive decision-maker. It is the only component permitted to assign the final readiness classification, resolve conflicts, decide on reassessments, and authorize Word and Outlook integrations.
*   **Child Specialists:** Scoped to their specific domains. They return structured findings (Pass, Fail, Condition, Block, Insufficient Evidence) rather than independently issuing final decisions.

## 4. Conditional Routing
The Supervisor routes the campaign through different validation branches based on fanned-in variables:
*   Proposed budget > approved budget $ightarrow$ Routes to `Approval & Finalisation`.
*   High-Sensitivity Campaign $ightarrow$ Requires brand compliance sign-off.
*   Missing mandatory asset $ightarrow$ Routes to `Remediation & Selective Reassessment`.
*   Specialist failure $ightarrow$ Routes to retry/fallback path.

## 5. Reassessment Loop (Selective Reassessment)
When a campaign fails due to correctable issues:
1.  Sets status to `Awaiting Remediation`.
2.  Preserves already-passed specialist results (e.g. keeping Budget as "Pass").
3.  Once the owner corrects the data, it triggers a selective reassessment, **rerunning only the affected specialists** (e.g. rerunning Asset, but skipping Budget).
4.  Capped at a maximum of **two automated cycles**. If the second reassessment fails, the campaign is routed to `Manual Review`.

## 6. Fallback and Escalation
If a child specialist fails to respond or returns unusable data:
1.  The Supervisor retries the specialist once.
2.  If the retry fails, the Supervisor marks that domain as "Insufficient Evidence" in the variables.
3.  The campaign's readiness outcome is set to `Manual Review` to prevent unsafe `Ready` classifications.
