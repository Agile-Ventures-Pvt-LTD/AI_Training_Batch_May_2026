# Orchestration Patterns

## 1. Overview

The P2-005 solution uses an autonomous multi-agent architecture in Microsoft Copilot Studio.

The PRD requires the following orchestration patterns:

- Sequential
- Parallel Fan-Out / Fan-In
- Hierarchical
- Conditional Routing
- Loop / Reassessment
- Fallback / Escalation

These patterns are implemented under the control of the **Campaign Readiness Supervisor**. The PRD explicitly requires the Supervisor to orchestrate the child agents and retain ownership of the final readiness classification, conflict resolution, reassessment decision, and final communication authorization. fileciteturn9file1L150-L174

---

## 2. End-to-End Orchestration

```text
Recurrence Trigger
        |
        v
Campaign Retrieval
        |
        v
Campaign Intake & Validation
        |
        v
Mark Campaign "In Assessment"
        |
        v
Parallel Specialist Fan-Out
   +----+----+----+
   |    |    |    |
   v    v    v    v
Budget Brand Channel Asset
   |    |    |    |
   +----+----+----+
        |
        v
Fan-In Consolidation
        |
        v
Launch Risk & Decision
        |
        v
Conditional Routing
   +----+--------+---------+
   |             |         |
   v             v         v
Ready       Remediation  Approval
               |           |
               v           v
          Selective     Human Approval
          Reassessment       |
               |             |
               +------+------+
                      |
                      v
             Supervisor Validation
                      |
                      v
             Word Report Generation
                      |
                      v
             Outlook Communication
```

The architecture must not allow a child agent to independently issue the final readiness decision. fileciteturn9file6L899-L906

---

# 3. Sequential Pattern

## Purpose

Sequential orchestration is used where one stage depends on the successful completion of a previous stage.

The PRD requires clearly defined sequential stages. fileciteturn9file1L157-L170

## Implementation

The primary sequence is:

```text
Trigger
   ↓
Retrieve Campaign
   ↓
Validate Campaign
   ↓
Mark In Assessment
   ↓
Run Specialist Assessments
   ↓
Consolidate Results
   ↓
Launch Risk & Decision
   ↓
Supervisor Validation
   ↓
Generate Word Report
   ↓
Prepare/Send Outlook Notification
```

The **Launch Risk & Decision Specialist** specifically runs after the first four specialists, making it part of the sequential stage following parallel fan-in. fileciteturn9file5L715-L759

## Required Behaviour

The system must not:

- Generate the final report before final readiness validation.
- Send the final communication before Supervisor approval.
- Move a campaign directly from `Pending` to `Ready`.

The campaign state model explicitly prohibits invalid state progression. fileciteturn9file6L872-L898

---

# 4. Parallel Fan-Out / Fan-In Pattern

## Purpose

The first four specialist agents perform independent domain assessments.

The required specialists are:

1. Budget & Commercial
2. Brand & Content Compliance
3. Channel Readiness
4. Asset Readiness

The PRD requires four independent specialist assessments and fan-in consolidation. fileciteturn9file0L11-L28

## Fan-Out

```text
                  Supervisor
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
     Budget          Brand         Channel
        |              |              |
        +--------------+--------------+
                       |
                       v
                     Asset
```

Conceptually, these are independent assessments. The PRD states that parallel means independent fan-out/fan-in orchestration and does not require proof that Copilot Studio executed calls simultaneously at the infrastructure level. fileciteturn9file7L1029-L1032

## Fan-In

The Supervisor waits until all mandatory specialist results are returned before final consolidation.

```text
Budget Result
Brand Result
Channel Result
Asset Result
      |
      v
Fan-In
      |
      v
Supervisor Consolidation
```

The results must use a consistent semantic output structure including:

- SpecialistName
- AssessmentStatus
- EvidenceSummary
- BlockingIssues
- Conditions
- RequiredActions
- RequiredApprover
- Confidence
- Completed

fileciteturn9file5L810-L822

---

# 5. Hierarchical Pattern

## Purpose

The architecture uses a Supervisor-to-specialist hierarchy.

```text
                 Campaign Readiness
                    Supervisor
                         |
       +-----------------+-----------------+
       |        |        |        |        |
       v        v        v        v        v
    Budget    Brand    Channel   Asset    Risk
   Specialist Specialist Specialist Specialist Specialist
                                           |
                                           v
                                  Reporting & Communication
```

The required hierarchy is:

**Supervisor Agent → Specialist Child Agents**

fileciteturn9file7L1033-L1051

## Supervisor Ownership

The Supervisor owns:

- Overall orchestration
- Final readiness classification
- Conflict resolution
- Reassessment decision
- Final stakeholder communication authorization

Specialists own only their assigned domains. fileciteturn9file7L1043-L1051

## Child-Agent Rule

Child agents return findings.

They must not independently announce the final campaign readiness decision. fileciteturn9file6L899-L906

---

# 6. Conditional Routing Pattern

## Purpose

Different campaign conditions result in different execution paths.

The PRD requires specialists and topics to be conditionally invoked. fileciteturn9file7L1052-L1060

## Routing Rules

### High-Sensitivity Campaign

```text
High Sensitivity
      ↓
Additional Brand Review
```

### Budget Above Approved Amount

```text
Budget > Approved Budget
          ↓
Approval Path
```

### Multi-Region Campaign

```text
Multi-Region
     ↓
Regional Approval
```

### Missing Mandatory Asset

```text
Missing Asset
     ↓
Remediation
```

### No Blocking Findings

```text
No Blocking Findings
        ↓
Final Readiness
```

### Specialist Failure

```text
Specialist Failure
       ↓
Retry / Fallback
```

These conditional paths are explicitly required by the PRD. fileciteturn9file7L1052-L1060

---

# 7. Loop / Reassessment Pattern

## Purpose

The reassessment loop handles correctable campaign-readiness failures.

The required pattern is:

```text
Failure
   ↓
Remediation
   ↓
Data Correction
   ↓
Selective Specialist Reassessment
   ↓
Supervisor Recalculation
```

fileciteturn9file7L1061-L1065

## Selective Reassessment

Only the affected domain should be rerun.

For example:

```text
Asset Issue
    ↓
Asset Corrected
    ↓
Asset Specialist Reassessment
    ↓
Supervisor Recalculation
```

The system must not rerun every specialist when only one domain changed. fileciteturn9file7L1061-L1065

## Reassessment Limit

The PRD requires bounded reassessment. If the second remediation attempt fails, the campaign is routed to `Manual Review`. fileciteturn9file4L519-L540

The mandatory test case for this behaviour is:

**TC-11 — Second remediation fails → Manual Review.** fileciteturn9file4L593-L597

---

# 8. Fallback / Escalation Pattern

## Purpose

The fallback pattern prevents specialist or tool failures from producing unsupported readiness decisions.

A specialist failure may occur when the specialist:

- Does not respond.
- Returns unusable information.
- Cannot access required data.
- Produces insufficient evidence.

fileciteturn9file7L1066-L1085

## Required Flow

```text
Specialist Failure
       ↓
Retry Once
       |
   +---+---+
   |       |
Success   Failure
   |       |
   v       v
Continue  Insufficient Evidence
             |
             v
        Prevent Ready
             |
             v
        Manual Review
```

The Supervisor must retry the specialist once. If unsuccessful, the domain must be marked as insufficient evidence, an unsupported `Ready` classification must be prevented, and the campaign must be routed for manual review. fileciteturn9file7L1085-L1090

---

# 9. Final Decision and Precedence

The orchestration must preserve governance precedence.

A blocking specialist result must not be overridden simply because another specialist passes.

The PRD requires:

- Conflict handling
- Final readiness precedence
- Explicit blocking rules
- Traceability to specialist findings

The mandatory test case **TC-14** specifically verifies that a Brand `Block` plus Budget `Pass` results in the blocking result prevailing. fileciteturn9file4L598-L604

The Supervisor remains responsible for resolving specialist conflicts and assigning final readiness. fileciteturn9file6L899-L906

---

# 10. Autonomous Trigger Orchestration

The process begins with a **Recurrence event trigger** configured directly in Microsoft Copilot Studio.

For each trigger execution:

1. Retrieve `Campaign Requests` from Excel.
2. Identify campaigns where `CampaignStatus = Pending`.
3. Select the oldest eligible Pending campaign.
4. Process only one campaign.
5. Update its status before specialist analysis begins.

fileciteturn9file6L859-L871

This prevents duplicate concurrent assessment.

A separate Power Automate workflow is not required for the core solution. fileciteturn9file6L859-L871

---

# 11. Reporting and Communication Sequence

Reporting and communication occur only after the Supervisor validates the final readiness.

```text
Final Assessment
       ↓
Supervisor Validation
       ↓
Word Readiness Report
       ↓
Excel Update
       ↓
Supervisor-approved Communication
       ↓
Outlook Notification
```

The Reporting & Communication Specialist executes only after Supervisor validation. It creates the Campaign Launch Readiness Report and sends the appropriate stakeholder notification after approval. fileciteturn9file5L760-L809

---

# 12. Failure Handling for External Tools

The orchestration must also handle external tool failures.

Required failure scenarios include:

- Missing Excel row
- Excel update failure
- Word creation failure
- Outlook failure
- Missing approver

If Word generation fails:

```text
Final Readiness
      ↓
Preserve Readiness in Excel
      ↓
Mark Report Generation Failed
      ↓
Do Not Claim Report Exists
```

If Outlook fails:

```text
Final Assessment
      ↓
Preserve Assessment Result
      ↓
Mark Notification Failed
      ↓
Do Not Claim Stakeholders Were Notified
```

These behaviours are explicitly required by the PRD. fileciteturn9file4L519-L540

---

# 13. Campaign State Orchestration

The supported campaign states are:

| State | Meaning |
|---|---|
| `Pending` | Awaiting assessment |
| `In Assessment` | Autonomous assessment currently active |
| `Awaiting Remediation` | Blocking issues require correction |
| `Awaiting Approval` | Mandatory human approval is outstanding |
| `Ready with Conditions` | Only permitted non-blocking conditions remain |
| `Ready` | All mandatory requirements satisfied |
| `Not Ready` | Launch cannot proceed |
| `Manual Review` | Insufficient evidence or unresolved system failure |
| `Completed` | Final assessment and communication completed |

fileciteturn9file6L872-L895

Invalid state transitions must be prevented.

---

# 14. Pattern-to-Component Mapping

| Pattern | Main Component | Implementation |
|---|---|---|
| Sequential | Supervisor | Validation → assessment → decision → reporting |
| Parallel Fan-Out | Supervisor | Four independent specialist assessments |
| Fan-In | Supervisor | Wait and consolidate specialist results |
| Hierarchical | Supervisor + child agents | Supervisor controls specialists |
| Conditional | Supervisor / Topics | Approval, remediation, review, and readiness routing |
| Loop / Reassessment | Supervisor + Remediation Topic | Selective reassessment of corrected domains |
| Fallback | Supervisor | Retry once → insufficient evidence → Manual Review |
| Autonomous Trigger | Recurrence Trigger | Select oldest Pending campaign |

The PRD explicitly requires documentation of these patterns. fileciteturn9file0L99-L113

---

# 15. Pattern Evidence

The implementation should provide evidence for each orchestration pattern.

Recommended screenshots include:

- `recurrence-trigger.png`
- `intake-topic.png`
- `parallel-specialists.png`
- `fan-in-consolidation.png`
- `remediation-topic.png`
- `approval-topic.png`
- `final-assessment.png`

These are part of the PRD's required GitHub screenshot structure. fileciteturn9file0L82-L97

The test report should additionally record:

- Test Case ID
- Campaign ID
- Trigger execution
- Topic invoked
- Child agents invoked
- Pattern demonstrated
- Specialist outputs
- Expected result
- Actual result
- Final status
- Pass/Fail
- Failure reason
- Remediation
- Retest result
- Screenshot reference

fileciteturn9file4L612-L628

---

# 16. Mandatory Pattern Coverage

The PRD requires the following minimum testing coverage:

- **3 sequential-pattern tests**
- **3 parallel fan-out/fan-in tests**
- **3 hierarchical tests**
- **2 conditional-routing tests**
- **2 reassessment-loop tests**
- **2 failure/fallback tests**
- **1 end-to-end autonomous test**

At least one failed test must be corrected and retested. fileciteturn9file4L644-L652

---

# 17. Summary

The P2-005 orchestration is built around a controlled Supervisor hierarchy:

```text
                    Recurrence
                        ↓
                    Supervisor
                        ↓
                 Intake & Validation
                        ↓
               Parallel Fan-Out
              /      |       |               Budget     Brand   Channel  Asset
              \      |       |      /
                        ↓
                    Fan-In
                        ↓
              Risk & Decision
                        ↓
               Conditional Route
                 /      |                    Ready  Remediate Approval
                       ↓          ↓
                  Reassessment  Approval
                       \          /
                        ↓
                Supervisor Validation
                        ↓
                 Word + Outlook
```

The key architectural rule is that **specialists provide domain findings, while the Supervisor controls orchestration and owns the final decision**. The implementation must also demonstrate bounded reassessment, controlled fallback, conditional routing, and traceable evidence without fabricating results. fileciteturn9file7L1033-L1090
