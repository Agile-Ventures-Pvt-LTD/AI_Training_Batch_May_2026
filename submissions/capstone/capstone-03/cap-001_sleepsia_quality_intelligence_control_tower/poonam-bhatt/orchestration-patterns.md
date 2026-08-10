# CAP-001 — Orchestration Patterns

## 1. Purpose

This document describes how the CAP-001 Sleepsia Product Quality & Customer Experience Intelligence Control Tower implements the required orchestration patterns:

- Hierarchical orchestration
- Sequential orchestration
- Parallel fan-out
- Fan-in
- Conditional routing
- Selective reassessment
- Retry
- Fallback
- Final action gating

The Quality Supervisor remains the parent orchestrator and final internal quality decision owner.

---

## 2. Hierarchical Orchestration

The solution uses a parent-child agent hierarchy.

```text
Quality Supervisor
│
├── Complaint Pattern Specialist
├── Returns Specialist
├── Product/Batch Specialist
├── Customer Impact Specialist
├── Safety Specialist
├── CAPA Specialist
└── M365 Guidance Specialist

The Supervisor:

Receives the investigation request or trigger.
Determines the investigation intent.
Selects the appropriate topic.
Determines which specialists are required.
Provides current evidence to specialists.
Collects specialist findings.
Makes the final classification through Topic 2.
Controls downstream actions.

Child agents do not own the final classification.

3. Sequential Orchestration

Sequential execution is used whenever a downstream step depends on the result of an earlier step.

Quality Trigger
      ↓
Incident Intake & Validation
      ↓
Required Specialist Analysis
      ↓
Fan-In
      ↓
Quality Investigation Decision
      ↓
CAPA / Closure
      ↓
Supervisor Validation
      ↓
Word Report
      ↓
Excel Update
      ↓
Outlook Notification
Sequential rules
Intake must pass before specialist analysis.
Specialist findings must be available before final decision.
Topic 2 must produce the final classification before CAPA or closure.
CAPA must complete when required before downstream finalization.
Supervisor validation must complete before Word, Excel or Outlook actions.
Downstream actions must not be claimed successful without tool confirmation.
4. Parallel Fan-Out

After successful intake validation, independent evidence domains are analyzed through the appropriate specialists.

Example:

                 Quality Supervisor
                        |
                Intake Validation
                        |
              Valid Investigation
                        |
       +--------+-------+--------+--------+
       |        |       |        |        |
       ↓        ↓       ↓        ↓        ↓
   Complaint Returns Product Customer Safety
   Pattern            /Batch   Impact
   Specialist Specialist Specialist Specialist Specialist
       |        |       |        |        |
       +--------+-------+--------+--------+
                        |
                       FAN-IN

Parallel execution is logical rather than dependent on literal simultaneous infrastructure execution.

Only relevant specialists are called.

For example:

Complaint evidence → Complaint Pattern Specialist
Return evidence → Returns Specialist
SKU/batch evidence → Product/Batch Specialist
Customer exposure → Customer Impact Specialist
Safety evidence → Safety Specialist

The CAPA Specialist is not part of the initial evidence fan-out. It is called conditionally after Topic 2.

5. Fan-In

The Supervisor performs fan-in after the required specialists complete.

Fan-in process:

Collect every required specialist result.
Preserve each specialist's finding.
Identify missing or failed specialist results.
Combine the findings into the current evidence state.
Resolve evidence conflicts using configured/internal evidence.
Pass the consolidated evidence to Topic 2.
Do not independently invent a final classification.

Example consolidated state:

Complaint Pattern:
ClusterCount = 2
RepeatedFailureMode = No

Returns:
ReturnRate = 0.32%
ReturnRateAvailable = Yes

Product/Batch:
SKU = SLP-1001
Batch = B-260701
PreviousIncidentCount = 0

Customer Impact:
AffectedCustomers = 2

Safety:
SafetyIndicator = No
PotentialSafetyCount = 0

The final classification is then produced by Topic 2.

6. Dynamic Specialist Selection

The Supervisor must not call every specialist for every request.

Selection is based on:

User intent
Available evidence
Required decision inputs
Stale evidence
Investigation state
Example

A return-rate question may require:

Returns Specialist

A safety-related complaint may require:

Complaint Pattern Specialist
Safety Specialist
Product/Batch Specialist

A CAPA status request may not require a new complaint investigation.

This prevents duplicate and unnecessary specialist execution.

7. Conditional Routing

The Supervisor uses configured conditions to control workflow branches.

Intake failure
Validation
   |
   +-- Invalid → Stop Specialist Analysis
   |
   +-- Insufficient Evidence → Record Evidence Gap
   |
   +-- Valid → Continue
Safety escalation
SafetyIndicator = Yes
        ↓
Critical Escalation
        ↓
Stop routine investigation path
        ↓
Critical handling
Investigation thresholds
Configured threshold triggered
        ↓
Investigation Required
        ↓
CAPA Planning
Informational path
No configured threshold triggered
        ↓
Informational
        ↓
No CAPA
        ↓
Closure / Monitoring
8. Quality Decision Routing

Topic 2 is the authoritative decision topic.

Configured precedence:

Safety Indicator = Yes
→ Critical Escalation
PotentialSafetyCount >= 2
→ High-Priority Quality Incident
ClusterCount >= 5
→ Investigation Required
ReturnRateAvailable = true AND ReturnRate >= 0.02
→ Investigation Required
PreviousIncidentCount >= 1 AND RepeatedFailureMode = true
→ High-Priority Quality Incident
MissingBatch = true AND ClusterCount >= 2
→ Insufficient Evidence
OverdueCAPA = true
→ High-Priority Quality Incident
No threshold triggered
→ Informational

The Supervisor does not replace this logic with an independently invented classification.

9. Conditional CAPA Routing

CAPA is called only when Topic 2 returns:

Investigation Required
High-Priority Quality Incident
Critical Escalation
Topic 2
   |
   +-- Informational
   |       ↓
   |     Monitor / Close
   |
   +-- Investigation Required
   |       ↓
   +-- High-Priority
   |       ↓
   +-- Critical
           ↓
      CAPA Specialist

CAPA must provide:

Containment
Corrective/preventive actions
OwnerRole
Target date
Validation method
CAPA summary

The CAPA Specialist does not independently change the final classification.

10. Selective Reassessment

When new evidence is received, the Supervisor does not automatically rerun the complete investigation.

Topic 4 determines which evidence became stale.

New Evidence
     ↓
Identify Changed Evidence
     ↓
Identify Stale Specialist
     ↓
Rerun Only Stale Specialist
     ↓
Preserve Unaffected Findings
     ↓
Fan-In
     ↓
Topic 2

Example:

ReturnsStale = true
Returns Specialist → Rerun

ComplaintStale = false
Complaint Pattern → Preserve

SafetyStale = false
Safety Specialist → Preserve

The reassessment count is incremented after the reassessment.

11. Reassessment Limit

Automated reassessment is limited to two cycles.

ReassessmentCount < 2
        ↓
Automated reassessment allowed

ReassessmentCount >= 2
        ↓
Stop automated reassessment
        ↓
Status = Manual Review

The Supervisor must not continuously loop on unresolved evidence.

12. Retry Pattern

A specialist failure follows:

Specialist Call
      ↓
   Success?
   /      \
 Yes       No
 |          |
Continue   Retry Once
              |
           Success?
           /     \
         Yes      No
          |        |
      Continue   Record Failure

Rules:

Retry a failed specialist once.
Do not retry indefinitely.
If the second attempt fails, record the failure.
Do not fabricate the missing result.
Mark affected analysis unavailable or insufficient where appropriate.
13. Tool Failure / Fallback

Configured tools follow the same controlled pattern.

Tool Call
   ↓
Success?
 /     \
Yes      No
 |        |
Continue  Retry/Failure Handling
            |
            ↓
      Record Actual Result

The Supervisor must never report:

Word created
Excel updated
Outlook sent

unless the respective tool confirms the action.

If a tool remains unavailable, preserve the quality decision and report the failed downstream action.

14. MCP Fallback

Microsoft Learn MCP is isolated from the core quality decision workflow.

M365 Guidance Required
        ↓
M365 Guidance Specialist
        ↓
Microsoft Learn MCP
        |
     +--+--+
     |     |
 Success  Failure
     |     |
 Guidance Continue Core
          Quality Flow

If MCP is unavailable:

Do not block quality assessment.
Do not invent Microsoft guidance.
Record the guidance limitation.
Continue the core quality workflow where possible.
15. Final Action Gate

Word, Excel and Outlook are downstream actions.

They can execute only after:

Required Specialist Results
          ↓
       Fan-In
          ↓
     Topic 2 Decision
          ↓
    CAPA if Required
          ↓
 Supervisor Validation
          ↓
   Final Action Gate
      /     |      \
    Word   Excel  Outlook
Word

Create the final report only after validation.

Excel

Update investigation/assessment state only after the final result is validated.

Outlook

Send notification only when the configured notification condition is met and the final status is validated.

16. Interactive vs Autonomous Orchestration
Autonomous
Recurrence/Event
      ↓
Find Processed = No
      ↓
Process Logical SKU/Batch Cluster
      ↓
Intake Validation
      ↓
Specialist Fan-Out
      ↓
Decision
      ↓
Downstream Actions
      ↓
Mark Source Complaints Processed = Yes

Source complaints are marked processed only after the assessment record is successfully created or updated.

Interactive

The Supervisor first identifies user intent.

Supported intents include:

Investigation request
Status request
Evidence update
Selective reassessment
Final decision request
CAPA request
Product care/use question
Internal quality policy question
M365/Copilot/Teams guidance

The Supervisor selects only the topic and specialists required for that intent.

17. End-to-End Control Pattern

The complete implementation follows:

TRIGGER
   ↓
INTAKE
   ↓
VALIDATE
   ↓
DYNAMIC ROUTING
   ↓
PARALLEL FAN-OUT
   ↓
SPECIALIST ANALYSIS
   ↓
FAN-IN
   ↓
QUALITY DECISION
   ↓
CONDITIONAL CAPA
   ↓
SUPERVISOR VALIDATION
   ↓
FINAL ACTION GATE
   ↓
WORD
   ↓
EXCEL
   ↓
OUTLOOK

For changed evidence:

NEW EVIDENCE
   ↓
STALE-DOMAIN DETECTION
   ↓
SELECTIVE RERUN
   ↓
FAN-IN
   ↓
REASSESSMENT
   ↓
DECISION

For failures:

FAILURE
   ↓
ONE RETRY
   ↓
SUCCESS → CONTINUE
   ↓
FAILURE → RECORD / FALLBACK / MANUAL REVIEW
18. Core Principle

The orchestration design is:

Validate → Dynamically Route → Fan-Out → Analyze → Fan-In → Decide → Conditionally Remediate → Validate → Persist → Notify.

This ensures that the Supervisor remains the control point while specialist agents, topics and tools are invoked only when their capabilities are required.