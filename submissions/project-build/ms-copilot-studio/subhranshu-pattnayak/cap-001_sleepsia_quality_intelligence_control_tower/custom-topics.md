# Custom Topics

## Overview

The Sleepsia Quality Intelligence Control Tower uses custom topics to implement investigation logic, policy-driven decision making, CAPA processing, and reassessment management.

These topics are orchestrated by the Quality Supervisor during autonomous investigations and provide structured outputs used throughout the workflow.

---

## 1. Incident Intake & Validation

### Purpose

Validates complaint records before specialist investigation begins.

### Inputs

- ComplaintID
- OrderID
- SKU
- Category
- Severity
- ComplaintDate
- BatchID

### Outputs

- ValidationStatus

### Possible Outcomes

- Valid
- Invalid
- Insufficient Evidence

### Usage

Executed immediately after a complaint is retrieved from the Customer Complaints table.

Only complaints with a status of **Valid** proceed to specialist investigation.

---

## 2. Quality Investigation Decision

### Purpose

Applies quality policy rules and determines the investigation outcome.

### Inputs

Investigation metrics collected from specialist findings and workbook data, including:

- ComplaintCount
- ReturnRate
- PreviousIncidentCount
- SafetyIndicatorDetected
- CriticalEscalationRequired
- MissingEvidence
- RepeatIncidentDetected
- CAPAOverdue
- PotentialSafetyCount

### Outputs

- Classification
- AppliedRuleID
- CAPARequired

### Allowed Classifications

- Informational
- Monitor
- Investigation Required
- High-Priority Quality Incident
- Critical Escalation
- Insufficient Evidence
- Manual Review

### Usage

Executed after specialist analysis is completed and investigation metrics have been assembled.

---

## 3. CAPA Planning & Ownership

### Purpose

Processes CAPA recommendations and determines ownership information for corrective actions.

### Inputs

- CAPARequired

### Outputs

- CAPAStatus

### Usage

Executed only when the Quality Investigation Decision determines that CAPA action is required.

---

## 4. Evidence Update & Selective Reassessment

### Purpose

Determines whether new evidence requires reassessment of an existing incident.

### Inputs

- Existing incident information
- ReassessmentCount
- Updated investigation evidence

### Outputs

- ReassessmentRequired
- ManualReviewRequired
- ReassessmentStatus

### Usage

Executed during incident reassessment processing.

When reassessment is required, affected specialists may be re-invoked and the Quality Investigation Decision topic is executed again using updated evidence.

---

## Topic Orchestration

The topics are executed in the following sequence during autonomous investigations:

1. Incident Intake & Validation
2. Specialist Analysis
3. Quality Investigation Decision
4. CAPA Planning & Ownership (when required)
5. Evidence Update & Selective Reassessment (when required)

The Quality Supervisor remains responsible for orchestrating topic execution and acting on topic outputs.