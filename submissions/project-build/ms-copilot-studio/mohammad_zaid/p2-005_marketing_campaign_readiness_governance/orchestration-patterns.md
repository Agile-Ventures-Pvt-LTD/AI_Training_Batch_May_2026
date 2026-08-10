
# Orchestration Patterns

# 1. Introduction

The Autonomous Marketing Campaign Launch Readiness & Governance System is implemented using Microsoft Copilot Studio's multi-agent orchestration capabilities. The solution combines sequential execution, hierarchical delegation, parallel fan-out/fan-in assessment, conditional routing, remediation loops, and controlled failure handling to ensure that every campaign is evaluated consistently and according to the NovaSphere Marketing Governance Policy.

Each orchestration pattern has a specific responsibility within the overall workflow and collectively enables autonomous, explainable, and policy-driven campaign readiness assessment.

---

# 2. Sequential Orchestration

The primary workflow follows a strict sequential execution model.

No stage is allowed to execute until the previous stage has completed successfully.

## Sequential Flow

```text
Recurrence Trigger
        │
        ▼
Campaign Intake & Validation
        │
        ▼
Campaign Validation
        │
        ▼
Specialist Assessments
        │
        ▼
Supervisor Fan-In
        │
        ▼
Launch Risk & Decision
        │
        ▼
Supervisor Validation
        │
        ▼
Approval / Remediation
        │
        ▼
Reporting
        │
        ▼
Outlook Notification
        │
        ▼
Excel Update
```

This sequencing guarantees that:

- Invalid campaigns never reach specialist assessment.
- Reporting never occurs before a final decision.
- Outlook notifications are sent only after Supervisor validation.
- Campaign status is updated only after the appropriate workflow stage.

---

# 3. Parallel Fan-Out / Fan-In

After successful campaign validation, the Supervisor initiates four independent specialist assessments.

## Fan-Out

```text
Campaign Readiness Supervisor
                │
                ├────────► Budget & Commercial Specialist
                │
                ├────────► Brand & Content Compliance Specialist
                │
                ├────────► Channel Readiness Specialist
                │
                └────────► Asset Readiness Specialist
```

Each specialist evaluates a different business domain while using only the knowledge and tools relevant to its responsibility.

The specialists operate independently and return structured findings to the Supervisor.

## Fan-In

Once all mandatory specialist assessments are complete, the Supervisor performs fan-in consolidation.

```text
Budget Result
        │
Brand Result
        │
Channel Result
        │
Asset Result
        │
        ▼
Supervisor Consolidation
        │
        ▼
Launch Risk & Decision Specialist
```

The Supervisor waits for all required assessment results before continuing to the decision stage.

---

# 4. Hierarchical Orchestration

The solution follows Microsoft's recommended parent-child orchestration model.

```text
Campaign Readiness Supervisor
            │
            ├── Budget Specialist
            ├── Brand Specialist
            ├── Channel Specialist
            ├── Asset Specialist
            ├── Launch Risk Specialist
            └── Reporting Specialist
```

## Supervisor Responsibilities

The Supervisor is responsible for:

- Campaign discovery
- Campaign validation
- State management
- Specialist invocation
- Result consolidation
- Conflict resolution
- Governance enforcement
- Final readiness validation
- Approval routing
- Remediation routing
- Reporting authorization

## Child Agent Responsibilities

Each child agent owns a single business domain.

Child agents:

- Perform only their assigned assessment.
- Return structured findings.
- Never assign the final campaign readiness outcome.

Only the Supervisor can assign the final readiness status.

---

# 5. Conditional Routing

The solution uses conditional routing to direct campaigns into the appropriate workflow.

Examples include:

| Condition                     | Routing Decision                 |
| ----------------------------- | -------------------------------- |
| Campaign validation fails     | Reject / Hold                    |
| Budget exceeds approved value | Approval workflow                |
| High regulatory sensitivity   | Additional approval              |
| Missing mandatory assets      | Remediation workflow             |
| Blocking findings             | Not Ready or Remediation         |
| No blocking findings          | Continue to readiness evaluation |
| Specialist failure            | Retry / Manual Review            |

Conditional routing ensures that each campaign follows the appropriate governance path without unnecessary processing.

---

# 6. Remediation and Selective Reassessment

When blocking findings can be corrected, the solution enters the remediation workflow.

```text
Blocking Finding
        │
        ▼
Remediation Topic
        │
        ▼
Correct Campaign Data
        │
        ▼
Selective Specialist Reassessment
        │
        ▼
Supervisor Consolidation
        │
        ▼
Updated Readiness Decision
```

Only the affected specialist domains are reassessed.

Previously successful specialist results are preserved to reduce unnecessary processing.

A maximum of two automated reassessment cycles are permitted before routing the campaign for Manual Review.

---

# 7. Approval Workflow

Campaigns requiring mandatory human approval follow a dedicated approval path.

```text
Launch Risk & Decision
        │
        ▼
Management Approval Required
        │
        ▼
Approval & Finalisation Topic
        │
        ▼
Awaiting Approval
        │
        ▼
Supervisor Validation
```

The approval workflow:

- Determines the required approver.
- Records approval reasons.
- Prevents Ready status while approval is outstanding.
- Returns control to the Supervisor after approval processing.

---

# 8. Reporting Workflow

Reporting is executed only after the Supervisor validates the final readiness outcome.

```text
Supervisor Validation
        │
        ▼
Reporting & Communication Specialist
        │
        ├── Microsoft Word Report
        ├── Outlook Notification
        └── Excel Status Update
```

This guarantees that no report or notification is generated before the final campaign decision has been approved.

---

# 9. Failure and Fallback Pattern

The architecture includes controlled failure handling for specialists and Microsoft 365 connectors.

## Specialist Failure

If a specialist:

- Fails to respond.
- Returns unusable information.
- Returns insufficient evidence.

The Supervisor:

1. Retries the specialist once.
2. Marks the affected domain as Insufficient Evidence if the retry fails.
3. Prevents unsupported Ready classifications.
4. Routes the campaign to Manual Review when necessary.

---

## Connector Failure

The solution also handles failures involving:

- Microsoft Excel
- Microsoft Word
- Microsoft Outlook

Failures are recorded without fabricating successful completion.

Campaign readiness decisions remain traceable even when reporting or communication cannot be completed.

---

# 10. Orchestration Summary

| Pattern             | Purpose                                                |
| ------------------- | ------------------------------------------------------ |
| Sequential          | Controls execution order                               |
| Parallel Fan-Out    | Executes independent specialist assessments            |
| Fan-In              | Consolidates specialist findings                       |
| Hierarchical        | Supervisor controls all child agents                   |
| Conditional Routing | Selects the appropriate workflow                       |
| Remediation Loop    | Supports corrective action and reassessment            |
| Approval Workflow   | Handles mandatory human approvals                      |
| Failure Handling    | Ensures safe recovery and Manual Review where required |

---

# Conclusion

The orchestration strategy combines autonomous event triggering, hierarchical supervision, independent specialist analysis, structured consolidation, conditional workflow execution, remediation, approval management, and failure recovery to create a scalable and governance-compliant campaign launch readiness solution using Microsoft Copilot Studio.
