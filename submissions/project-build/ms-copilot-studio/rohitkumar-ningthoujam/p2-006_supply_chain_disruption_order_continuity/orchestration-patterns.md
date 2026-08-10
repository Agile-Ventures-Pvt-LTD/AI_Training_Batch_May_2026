# P2-006 — Orchestration Patterns

## Overview

The solution uses multiple orchestration patterns required by the PRD to coordinate disruption processing, specialist analysis, recovery decisions, approvals, reassessment, and final outputs.

## 1. Sequential Processing

Sequential processing is used where each stage depends on the successful completion of the previous stage.

Autonomous Trigger
        ↓
Disruption Intake & Validation
        ↓
Scope Identification
        ↓
Recovery Planning
        ↓
Recovery Strategy Resolution
        ↓
Approval / Reassessment
        ↓
Final Validation
        ↓
Reporting

The workflow must not proceed to dependent stages when mandatory validation fails.

## 2. Parallel Fan-Out / Fan-In

Independent specialist analyses are performed in parallel.

                 Supervisor
                     ↓
                  Fan-Out
                     ↓
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
   Inventory     Alternate      Customer /
   Specialist    Supplier       Order
                 Specialist      Specialist
       ↓             ↓             ↓
       └─────────────┼─────────────┘
                     ↓
                   Fan-In
                     ↓
              Recovery Planning

The Supervisor consolidates specialist results before recovery strategy resolution.

## 3. Hierarchical Orchestration

The Supply Continuity Supervisor is the parent orchestration layer.

Supply Continuity Supervisor
        ├── Inventory Specialist
        ├── Alternate Supplier Specialist
        ├── Customer & Order Specialist
        ├── Commercial Specialist
        └── Recovery Planning Specialist

The Supervisor coordinates child-agent execution and controls the overall workflow.

## 4. Conditional Routing

The solution uses conditions to select the correct recovery path.

Examples include:

- Existing inventory is sufficient.
- Inventory is partially sufficient.
- Approved alternate supplier is available.
- Only an unapproved alternate is available.
- No viable recovery route exists.
- Approval is required.
- Reassessment is required.

## 5. Conflict Resolution

Specialist outputs may conflict.

The system resolves conflicts using mandatory business precedence rather than averaging scores.

The precedence is:

1. Safety or quality restriction
2. Strategic/SLA-protected customer commitment
3. Supplier approval restriction
4. Inventory availability and timing
5. Commercial approval requirement
6. Cost optimisation
7. Lower-priority customer convenience

Higher-priority restrictions override lower-priority optimisation.

## 6. Selective Reassessment

Selective reassessment is used when a relevant input changes after specialist analysis.

Examples:

- Alternate supplier capacity changes.
- Inventory availability changes.
- Customer priority changes.
- Supplier approval status changes.
- Commercial conditions change.

Only affected specialist analysis should be rerun where possible.

## 7. Retry / Fallback

Specialist failure is handled through controlled retry.

Specialist Failure
        ↓
      Retry
        ↓
   ┌────┴────┐
   ↓         ↓
Success    Failure
   ↓         ↓
Continue  Insufficient
          Evidence
              ↓
        Manual Review

A specialist is retried once.

If the second attempt fails, the system must not fabricate a result.

## 8. Loop Control

Reassessment is bounded by a reassessment-cycle limit.

Condition Changed
        ↓
Reassessment Required
        ↓
Affected Specialist(s)
        ↓
Updated Findings
        ↓
Recovery Resolution
        ↓
Resolved?
   ┌────┴────┐
   ↓         ↓
  Yes        No
   ↓         ↓
Continue   Cycle Limit
             ↓
        Manual Review

The system must prevent uncontrolled reassessment loops.

## 9. Approval Routing

When a decision requires authorization, the workflow routes the case to the appropriate approval boundary.

Examples include:

- Finance approval
- Commercial approval
- Supplier qualification
- Supplier approval
- Customer commitment exception
- Management escalation

The system may prepare and route the recommendation but must not fabricate approval.

## 10. Reporting and Notification

After final validation:

Final Recovery Plan
        ↓
   ┌────┼────┐
   ↓    ↓    ↓
 Word Excel Outlook
Report Update Notification

Reporting and notification occur only after the appropriate validation and authorization conditions are satisfied.

## Pattern Summary

| Pattern | Primary Use |
|---|---|
| Sequential | Ordered workflow stages |
| Parallel Fan-Out/Fan-In | Independent specialist analysis |
| Hierarchical | Supervisor and child-agent coordination |
| Conditional | Recovery-path selection |
| Conflict Resolution | Competing specialist recommendations |
| Selective Reassessment | Changed conditions |
| Retry/Fallback | Specialist failures |
| Loop Control | Bounded reassessment |
| Approval Routing | Human authorization |
| Finalization | Reporting and notification |