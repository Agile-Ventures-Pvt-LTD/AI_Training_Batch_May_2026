# Custom topics

## Sleepsia product quality & customer experience intelligence control tower

This document defines the mandatory workflow topics implemented in the Sleepsia Product Quality & Customer Experience Intelligence Control Tower.

The PRD requires four core operational topics:

1. Incident Intake & Validation
2. Quality Investigation Decision
3. CAPA Planning & Ownership
4. Evidence Update & Selective Reassessment

In this implementation, each topic is implemented as a **dedicated child agent** coordinated by the **Quality Supervisor** through hierarchical orchestration.

The child-agent architecture provides:

* modularity,
* deterministic execution,
* reusable analytical components,
* structured outputs,
* auditable orchestration,
* enterprise-grade maintainability.

---

# Topic architecture

| PRD topic                                | Implemented child agent                             | Trigger                         | Output                        |
| ---------------------------------------- | --------------------------------------------------- | ------------------------------- | ----------------------------- |
| Incident Intake & Validation             | Incident Intake & Validation Specialist             | Recurrence Trigger / Supervisor | Validation result             |
| Quality Investigation Decision           | Quality Investigation Decision Specialist           | After specialist analysis       | Classification recommendation |
| CAPA Planning & Ownership                | CAPA Planning & Ownership Specialist                | After supervisor classification | CAPA plan                     |
| Evidence Update & Selective Reassessment | Evidence Update & Selective Reassessment Specialist | New evidence                    | Reassessment plan             |

---

# Topic 1: Incident intake & validation

## Implemented component

**Incident Intake & Validation Specialist**

## Purpose

Validate incoming complaint records before any quality analysis begins.

This topic acts as the **mandatory validation gate**.

No specialist analysis may begin until validation succeeds.

---

## Trigger

Invoked by:

* Recurrence Trigger
* Quality Supervisor
* Manual investigation request

---

## Required inputs

* ComplaintID
* OrderID
* SKU
* BatchID
* ComplaintDate
* Category
* Severity

---

## Excel tables used

Read-only:

* tblCustomerComplaints
* tblProductMaster
* tblBatchRegister

---

## Validation rules

### Complaint validation

* ComplaintID must exist.
* Complaint must exist in tblCustomerComplaints.
* Complaint must not already be processed.

### Order validation

* OrderID must exist.

### SKU validation

* SKU must exist in tblProductMaster.

### Batch validation

* BatchID must exist in tblBatchRegister.
* Batch must map to the supplied SKU.

### Data validation

* ComplaintDate must be valid.
* Category must be recognized.
* Severity must be recognized.

---

## Validation outcomes

### Valid

* ValidationStatus = Valid
* CanProceed = True

### Invalid

* ValidationStatus = Invalid
* CanProceed = False

### Insufficient Evidence

* ValidationStatus = Insufficient Evidence
* CanProceed = False

---

## Output schema

```json
{
  "ValidationStatus": "Valid",
  "ValidationReason": "All mandatory identifiers validated successfully",
  "ValidatedSKU": "SLP-1002",
  "ValidatedBatchID": "B-260705",
  "CanProceed": true
}
```

---

## Supervisor routing

### Valid

Proceed to:

* Complaint Pattern Specialist
* Returns Specialist
* Product/Batch Specialist
* Customer Impact Specialist
* Safety Specialist

### Invalid

Stop workflow.

### Insufficient Evidence

Stop workflow and record missing evidence.

---

# Topic 2: Quality investigation decision

## Implemented component

**Quality Investigation Decision Specialist**

## Purpose

Evaluate consolidated specialist findings using deterministic quality policy rules and recommend a quality classification.

The recommendation is advisory.

The **Quality Supervisor assigns the final classification**.

---

## Trigger

Invoked after:

* Complaint Pattern Specialist
* Returns Specialist
* Product/Batch Specialist
* Customer Impact Specialist
* Safety Specialist

have completed.

---

## Required inputs

* Validation findings
* Complaint findings
* Return findings
* Product/Batch findings
* Customer Impact findings
* Safety findings
* Existing CAPA information

---

## Rule precedence

Rules are evaluated in this exact order.

### Rule 1

CriticalEscalation = True

→ Critical Escalation

### Rule 2

HighPrioritySafetyConcern = True

→ High-Priority Quality Incident

### Rule 3

ComplaintCount ≥ 5 similar complaints within 7 days

→ Investigation Required

### Rule 4

ReturnRate ≥ 2%

→ Investigation Required

### Rule 5

PreviousIncidentCount ≥ 1 AND repeated batch pattern detected

→ High-Priority Quality Incident

### Rule 6

Critical manufacturing evidence missing

→ Insufficient Evidence

### Rule 7

Overdue CAPA exists

→ High-Priority Quality Incident

### Rule 8

Single isolated complaint

→ Informational

---

## Output schema

```json
{
  "RecommendedClassification": "Investigation Required",
  "AppliedRule": "Complaint Cluster Threshold",
  "DecisionRationale": "Multiple complaint and return thresholds exceeded",
  "Confidence": "High",
  "CAPARecommended": true
}
```

---

## Supervisor routing

The supervisor reviews:

* recommendation,
* evidence,
* confidence,
* policy context.

The supervisor may:

* confirm,
* modify,
* override

the recommendation.

---

# Topic 3: CAPA planning & ownership

## Implemented component

**CAPA Planning & Ownership Specialist**

## Purpose

Generate structured corrective and preventive action plans for confirmed quality incidents.

---

## Trigger

Invoked only when the final classification is:

* Investigation Required
* High-Priority Quality Incident
* Critical Escalation

---

## Required inputs

* IncidentID
* FinalClassification
* SKU
* BatchID
* Specialist findings
* SupervisorDecisionRationale

---

## Excel tables used

Read:

* tblOwners
* tblCAPARegister

Write:

* tblCAPARegister

---

## Containment actions

Examples:

* batch review,
* shipment hold,
* inventory inspection,
* supplier notification,
* complaint monitoring.

---

## Corrective actions

Examples:

* manufacturing investigation,
* supplier investigation,
* material inspection,
* process review,
* batch testing.

---

## Preventive actions

Examples:

* inspection improvements,
* process control updates,
* supplier audits,
* operator training,
* monitoring enhancements.

---

## Owner assignment

Owners are resolved using **tblOwners**.

Typical assignments:

* Quality Manager
* Production Manager
* Supplier Quality Engineer
* Operations Manager
* Product Engineering

---

## Target date rules

### Critical Escalation

* Containment: Immediate
* Corrective: 3 days
* Preventive: 7 days

### High-Priority Quality Incident

* Containment: 1 day
* Corrective: 5 days
* Preventive: 10 days

### Investigation Required

* Containment: 2 days
* Corrective: 7 days
* Preventive: 14 days

---

## Validation methods

Every CAPA includes validation methods such as:

* batch inspection,
* complaint reduction,
* return-rate verification,
* supplier verification,
* process audit.

---

## Output schema

```json
{
  "CAPARequired": true,
  "ContainmentActions": [],
  "CorrectiveActions": [],
  "PreventiveActions": [],
  "OwnerAssignments": {},
  "TargetDates": {},
  "ValidationMethods": [],
  "CAPASummary": "Structured CAPA plan generated"
}
```

---

## Excel update

After supervisor approval:

Create or update **tblCAPARegister**.

---

# Topic 4: Evidence update & selective reassessment

## Implemented component

**Evidence Update & Selective Reassessment Specialist**

## Purpose

Manage new evidence and selectively rerun only affected specialists.

---

## Trigger

Invoked when:

* new complaint,
* complaint correction,
* return update,
* batch update,
* safety update,
* customer resolution update,
* incident history update,
* CAPA update

is received.

---

## Required inputs

* IncidentID
* CurrentClassification
* ReassessmentCount
* NewEvidenceType
* ExistingSpecialistFindings

---

## Stale specialist mapping

### New complaint

Rerun:

* Complaint Pattern Specialist
* Customer Impact Specialist
* Safety Specialist

### Return update

Rerun:

* Returns Specialist
* Customer Impact Specialist

### Batch update

Rerun:

* Product/Batch Specialist
* Complaint Pattern Specialist

### Safety update

Rerun:

* Safety Specialist
* Complaint Pattern Specialist

### Customer update

Rerun:

* Customer Impact Specialist

### Incident history update

Rerun:

* Product/Batch Specialist

### CAPA update

Rerun:

* CAPA Planning & Ownership Specialist

---

## Preservation policy

Preserve unaffected findings.

Do not rerun specialists whose inputs have not changed.

---

## Reassessment rules

Increment **ReassessmentCount** after each automated reassessment.

### ReassessmentCount < 2

Continue automation.

### ReassessmentCount = 2

Perform final automated reassessment.

### ReassessmentCount > 2

Assign **Manual Review**.

Stop automated reassessment.

---

## Output schema

```json
{
  "StaleSpecialists": [],
  "SpecialistsToRerun": [],
  "PreservedFindings": [],
  "UpdatedReassessmentCount": 1,
  "ReassessmentAllowed": true,
  "ManualReviewRequired": false
}
```

---

# Supervisor orchestration

## Stage 1

Incident Intake & Validation Specialist

## Stage 2

Parallel execution:

* Complaint Pattern Specialist
* Returns Specialist
* Product/Batch Specialist
* Customer Impact Specialist
* Safety Specialist

## Stage 3

Quality Investigation Decision Specialist

## Stage 4

Quality Supervisor final classification

## Stage 5

CAPA Planning & Ownership Specialist

## Stage 6

Operational execution:

* Word report,
* Excel updates,
* Outlook notification.

## Stage 7

Evidence Update & Selective Reassessment Specialist

---

# State transitions

## New complaint

Open

↓

Validation

↓

Under Investigation

↓

Decision

↓

CAPA (if required)

↓

Monitoring / Closed

## Reassessment

Monitoring

↓

New Evidence

↓

Selective Reassessment

↓

Decision Re-evaluation

↓

Monitoring / Manual Review

---

# Data ownership

## Read-only

* Validation
* Complaint Pattern
* Returns
* Product/Batch
* Customer Impact
* Safety
* Decision

## Write-enabled

* CAPA Planning & Ownership
* Quality Supervisor

Operational updates:

* tblQualityIncidents
* tblCAPARegister
* tblCustomerComplaints

are performed only after supervisor authorization.

---

# Enterprise compliance

The implemented child-agent architecture satisfies all mandatory PRD custom topics while providing:

* deterministic validation,
* parallel specialist analysis,
* structured evidence collection,
* policy-driven decision support,
* controlled CAPA generation,
* bounded reassessment,
* auditable workflow execution,
* enterprise-grade orchestration,
* Microsoft 365 native integration.
