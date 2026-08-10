# Supervisor Agent Design

## 1. Purpose

The **Campaign Readiness Supervisor** is the central orchestration agent for the P2-005 Autonomous Marketing Campaign Launch Readiness & Governance System.

Its primary responsibility is to coordinate the complete campaign-readiness lifecycle while ensuring that specialist agents perform only their assigned domain assessments.

The Supervisor controls:

- Campaign intake
- Validation
- Specialist delegation
- Parallel assessment
- Result consolidation
- Risk and decision processing
- Remediation
- Approval routing
- Selective reassessment
- Final readiness validation
- Reporting and communication authorization

---

## 2. Agent Role

**Agent Name:** Campaign Readiness Supervisor

**Role:** Central Campaign Governance and Orchestration Agent

**Primary Objective:**

> Coordinate the autonomous campaign launch-readiness assessment, enforce governance rules, delegate domain-specific assessments to specialist agents, consolidate their findings, control remediation and approvals, and determine the final campaign readiness status.

The Supervisor is the **only component authorized to assign the final readiness classification**.

---

## 3. Responsibilities

The Supervisor must:

1. Receive a campaign selected by the recurrence trigger.
2. Retrieve and validate campaign information.
3. Prevent duplicate campaign processing.
4. Set a valid campaign to `In Assessment`.
5. Invoke the four independent specialist agents.
6. Wait for required specialist results.
7. Consolidate specialist findings.
8. Invoke the Launch Risk & Decision Specialist.
9. Resolve conflicting findings according to governance precedence.
10. Determine whether remediation or approval is required.
11. Coordinate selective reassessment.
12. Enforce the reassessment limit.
13. Handle specialist failures and insufficient evidence.
14. Validate the final readiness result.
15. Authorize readiness-report generation.
16. Authorize stakeholder communication.
17. Ensure the campaign state is updated correctly.

---

## 4. High-Level Flow

```text
Recurrence Trigger
       ↓
Supervisor
       ↓
Campaign Intake & Validation
       ↓
Validation Passed?
    /       \
  No         Yes
  ↓           ↓
Stop       In Assessment
              ↓
       Parallel Specialists
       ┌──────┼──────┬──────┐
       ↓      ↓      ↓      ↓
    Budget  Brand  Channel  Asset
       └──────┼──────┴──────┘
              ↓
       Fan-In Consolidation
              ↓
       Risk & Decision
              ↓
      Final Outcome Required?
        /       |        \
       ↓        ↓         ↓
    Ready   Remediation  Approval
       \        |         /
        \       ↓        /
         Reassessment
              ↓
       Supervisor Validation
              ↓
        Reporting & Communication
```

---

## 5. Campaign Intake

When the Supervisor receives a campaign, it must ensure that the campaign contains sufficient information for assessment.

The validation stage checks information such as:

- Campaign ID
- Campaign name
- Product
- Objective
- Launch date
- Proposed budget
- Approved budget
- Geography
- Channels
- Campaign owner
- Campaign status

The Supervisor must not continue with specialist assessment when mandatory campaign information is unavailable or invalid.

---

## 6. Duplicate Prevention

Before starting a new assessment, the Supervisor must check the campaign state.

A campaign should not be assessed again when it is already in a state such as:

- `In Assessment`
- `Awaiting Remediation`
- `Awaiting Approval`
- `Completed`

The Supervisor must prevent duplicate processing.

---

## 7. Campaign State Management

The Supervisor controls campaign-state transitions.

Typical progression:

```text
Pending
   ↓
In Assessment
   ↓
Assessment
   ↓
Ready / Ready with Conditions
```

Alternative paths include:

```text
In Assessment
      ↓
Awaiting Remediation
      ↓
Reassessment
      ↓
In Assessment
```

or:

```text
In Assessment
      ↓
Awaiting Approval
      ↓
Approval Received
      ↓
Final Assessment
```

Unresolved failures may result in:

```text
Manual Review
```

---

## 8. Specialist Delegation

After successful intake validation, the Supervisor invokes four independent specialist agents:

### Budget & Commercial Specialist

Responsible for budget and commercial assessment.

### Brand & Content Compliance Specialist

Responsible for brand, claims, content, and sensitivity assessment.

### Channel Readiness Specialist

Responsible for evaluating every applicable campaign channel.

### Asset Readiness Specialist

Responsible for evaluating mandatory campaign assets.

The Supervisor must not perform these specialist assessments itself when they belong to a dedicated child agent.

---

## 9. Parallel Fan-Out

The four independent specialist assessments should be executed in parallel.

```text
                 Supervisor
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
    Budget          Brand         Channel
       │              │              │
       └──────────────┼──────────────┘
                      ↓
                    Asset
```

The Supervisor must wait for the required specialist outputs before proceeding to consolidated decision processing.

---

## 10. Fan-In and Consolidation

After specialist execution, the Supervisor consolidates:

- Specialist status
- Evidence
- Blocking issues
- Conditions
- Required actions
- Required approvals
- Confidence/evidence quality

The Supervisor must preserve the distinction between:

- Blocking findings
- Non-blocking conditions
- Approval requirements
- Insufficient evidence

Specialist results must not simply be averaged.

---

## 11. Risk & Decision Delegation

Once the four specialist assessments are available, the Supervisor invokes the **Launch Risk & Decision Specialist**.

The Risk & Decision Specialist evaluates:

- Overall risk
- Blocking issues
- Non-blocking conditions
- Timing
- Approvals
- Unresolved evidence

The Supervisor receives the proposed decision and validates it against the governance rules.

---

## 12. Final Readiness Precedence

The Supervisor applies the required outcome precedence:

```text
Not Ready
     ↓
Management Approval Required
     ↓
Remediation Required
     ↓
Ready with Conditions
     ↓
Ready
```

For example:

```text
Budget  → Pass
Brand   → Block
Channel → Pass
Asset   → Pass
```

The Supervisor must not classify the campaign as `Ready`.

A blocking result takes precedence over a passing result from another specialist.

---

## 13. Conditional Routing

The Supervisor determines the next path based on the consolidated results.

### Ready

If all mandatory controls pass:

```text
Assessment
    ↓
Ready
```

### Ready with Conditions

If only permitted non-blocking conditions remain:

```text
Assessment
    ↓
Ready with Conditions
```

### Remediation

If blocking issues can be corrected:

```text
Assessment
    ↓
Awaiting Remediation
    ↓
Correction
    ↓
Selective Reassessment
```

### Approval

If mandatory human approval is required:

```text
Assessment
    ↓
Awaiting Approval
    ↓
Approval
    ↓
Final Validation
```

### Manual Review

If sufficient evidence cannot be obtained:

```text
Specialist Failure
       ↓
Retry
       ↓
Failure
       ↓
Insufficient Evidence
       ↓
Manual Review
```

---

## 14. Remediation and Selective Reassessment

The Supervisor controls reassessment after remediation.

The process is:

```text
Blocking Finding
       ↓
Remediation
       ↓
Corrected Data
       ↓
Identify Affected Domain
       ↓
Rerun Affected Specialist
       ↓
Consolidate Again
```

The Supervisor should not unnecessarily rerun specialists whose previous results remain valid.

### Reassessment Limit

A maximum of **two automated reassessment cycles** is permitted.

If the second remediation attempt fails:

```text
Manual Review
```

---

## 15. Specialist Failure Handling

If a specialist does not provide a usable result:

### First failure

```text
Specialist
    ↓
Retry Once
```

### Retry failure

```text
Retry
  ↓
Failure
  ↓
Insufficient Evidence
  ↓
Manual Review
```

The Supervisor must never convert missing evidence into a successful assessment.

---

## 16. Human Approval Handling

The Supervisor coordinates approval requirements but must not fabricate approval.

Examples include:

- Budget above approved amount
- Budget above INR 1,000,000
- High-sensitivity content
- Multi-market campaign
- Other governance-defined approval conditions

When approval is required:

```text
Assessment
    ↓
Approval Required
    ↓
Awaiting Approval
    ↓
Approval Received
    ↓
Supervisor Validation
```

---

## 17. Reporting Authorization

The Supervisor must validate the final readiness classification before authorizing the Reporting & Communication Specialist.

The reporting flow is:

```text
Final Assessment
      ↓
Supervisor Validation
      ↓
Report Generation
```

The Supervisor must not authorize reporting based on incomplete or unsupported assessment results.

---

## 18. Communication Authorization

Outlook communication occurs only after Supervisor approval.

```text
Final Readiness
      ↓
Supervisor Validation
      ↓
Communication Authorization
      ↓
Outlook Notification
```

If Outlook fails, the Supervisor must not claim that communication was successfully sent.

---

## 19. Tools

The Supervisor may require access to tools for:

- Campaign retrieval
- Campaign status updates
- Specialist delegation
- State management
- Final validation
- Report authorization
- Communication authorization

Excel Online (Business) is the primary operational data source.

The Supervisor should use the campaign's **CampaignID as the logical campaign identifier** and should not automatically treat it as the Excel connector's internal row ID.

---

## 20. Knowledge Sources

The Supervisor should have access to the governance information required to coordinate the workflow.

### Marketing Governance Policy

Used for:

- Campaign states
- Readiness rules
- Approval rules
- Timing rules
- Remediation
- Reassessment
- Escalation

The Supervisor should rely on specialist-specific knowledge sources for detailed domain assessment rather than duplicating specialist knowledge.

---

## 21. Output Contract

The Supervisor should produce a structured final result containing information such as:

```text
CampaignID
CampaignName
AssessmentStatus
SpecialistResults
BlockingIssues
Conditions
RequiredApprovals
RemediationActions
RiskClassification
FinalReadinessStatus
NextAction
EvidenceSummary
```

The exact implementation variable names may differ, but the semantic information must be preserved.

---

## 22. Supervisor Decision Example

### Input

```text
CampaignID: CAMP-001

Budget: Pass
Brand: Pass
Channel: Pass
Assets: Blocking
```

### Supervisor processing

```text
Four specialist results
        ↓
Asset blocker identified
        ↓
Risk & Decision
        ↓
Remediation required
```

### Final state

```text
Awaiting Remediation
```

The Supervisor does not mark the campaign `Ready`.

---

## 23. Supervisor Design Principles

The Supervisor follows these principles:

1. **Centralized orchestration** — overall workflow remains under Supervisor control.
2. **Specialization** — domain decisions are delegated to specialist agents.
3. **Evidence-based decisions** — unsupported conclusions are not accepted.
4. **Governance precedence** — blocking rules override passing results.
5. **Controlled autonomy** — human approval remains mandatory where required.
6. **Bounded reassessment** — automated loops are limited.
7. **Failure transparency** — tool or specialist failures are not hidden.
8. **State consistency** — campaign status must reflect the actual workflow stage.
9. **No duplicate assessment** — campaigns already being processed or completed are not reassessed unnecessarily.
10. **Final decision ownership** — only the Supervisor assigns the final readiness classification.

---

## 24. End-to-End Supervisor Responsibility

The complete Supervisor responsibility can be summarized as:

```text
Select Campaign
      ↓
Validate
      ↓
Mark In Assessment
      ↓
Delegate
      ↓
Wait for Specialists
      ↓
Consolidate
      ↓
Evaluate Risk
      ↓
Route
 ┌────┼────────┐
 ↓    ↓        ↓
Ready Remediate Approval
       ↓        ↓
       Reassess │
          \     /
           ↓   ↓
        Validate
           ↓
        Report
           ↓
     Communicate
```

The Supervisor therefore acts as the **governance and orchestration authority**, while specialist agents remain responsible for their individual domains.
