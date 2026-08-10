# Architecture

## Sleepsia product quality & customer experience intelligence control tower

This document describes the enterprise architecture for the **Sleepsia Product Quality & Customer Experience Intelligence Control Tower**, a hierarchical multi-agent quality investigation system built with **Microsoft Copilot Studio**, **Excel Online (Business)**, **Word Online (Business)**, **Office 365 Outlook**, and **Microsoft Learn MCP**.

The architecture follows a **parent-supervisor orchestration model** where a single supervisory agent coordinates specialized analytical agents, consolidates evidence, applies deterministic quality rules, and authorizes enterprise actions.

---

# Architecture overview

The system is designed around **hierarchical orchestration**.

A **Quality Supervisor** acts as the parent agent and delegates analytical responsibilities to specialized child agents.

The supervisor is responsible for:

* workflow orchestration,
* evidence consolidation,
* policy evaluation,
* final quality classification,
* CAPA authorization,
* report authorization,
* notification authorization,
* reassessment control.

Child agents never assign the final quality classification.

---

# High-level architecture

```text
                   Recurrence Trigger
                          |
                          v
               Quality Supervisor (Parent)
                          |
                          v
        Incident Intake & Validation Specialist
                          |
                Validation Gate (Pass/Fail)
                          |
        -----------------------------------------
        |        |         |        |          |
        v        v         v        v          v
 Complaint   Returns   Product/   Customer   Safety
 Pattern    Specialist  Batch      Impact   Specialist
 Specialist              Specialist Specialist
        \        |         |        |          /
         \       |         |        |         /
          ------------------------------------
                          |
                          v
       Quality Investigation Decision Specialist
                          |
                          v
                Quality Supervisor Decision
                          |
                          v
      CAPA Planning & Ownership Specialist
                          |
                          v
     -------------------------------------------
     |                  |                     |
     v                  v                     v
 Word Report       Excel Updates       Outlook Notification
                          |
                          v
 Evidence Update & Selective Reassessment
                          |
                          v
                Quality Supervisor
```

---

# Parent agent

## Quality Supervisor

The Quality Supervisor is the **single orchestration authority**.

### Responsibilities

* receive autonomous triggers,
* coordinate child agents,
* enforce workflow sequencing,
* consolidate evidence,
* apply quality rule precedence,
* assign final classification,
* authorize CAPA,
* authorize report generation,
* authorize Excel updates,
* authorize notifications,
* manage reassessment cycles.

The supervisor maintains the complete incident state.

---

# Child-agent architecture

## Incident Intake & Validation Specialist

### Purpose

Validate incoming complaint records before analysis.

### Data sources

* tblCustomerComplaints
* tblProductMaster
* tblBatchRegister

### Outputs

* ValidationStatus
* ValidationReason
* ValidatedSKU
* ValidatedBatchID
* CanProceed

---

## Complaint Pattern Specialist

### Purpose

Analyze complaint clustering and repeated failure patterns.

### Data source

* tblCustomerComplaints

### Outputs

* ComplaintCount
* DominantCategories
* ClusterStatus
* RepeatedFailureModes
* Confidence

---

## Returns Specialist

### Purpose

Evaluate return trends and return-rate risk.

### Data sources

* tblReturns
* tblSalesSummary

### Outputs

* ReturnCount
* ReturnRate
* ThresholdStatus
* RefundExposure
* Confidence

---

## Product/Batch Specialist

### Purpose

Evaluate manufacturing and batch-level evidence.

### Data sources

* tblProductMaster
* tblBatchRegister
* tblQualityIncidents

### Outputs

* ManufactureDate
* SupplierLot
* PreviousIncidentCount
* RepeatedBatchPattern
* ManufacturingAssessment

---

## Customer Impact Specialist

### Purpose

Measure customer exposure and operational impact.

### Data sources

* tblCustomerComplaints
* tblReturns

### Outputs

* CustomersAffected
* UnresolvedCases
* CustomerExposureLevel
* OperationalImpact

---

## Safety Specialist

### Purpose

Evaluate safety risk and escalation conditions.

### Data source

* tblCustomerComplaints

### Outputs

* CriticalEscalation
* HighPrioritySafetyConcern
* SafetyAssessment
* HazardEvidence

---

## Quality Investigation Decision Specialist

### Purpose

Apply deterministic quality rules and recommend a classification.

### Inputs

All specialist findings.

### Outputs

* RecommendedClassification
* AppliedRule
* DecisionRationale
* CAPARecommended

---

## CAPA Planning & Ownership Specialist

### Purpose

Create containment, corrective, and preventive actions.

### Data sources

* tblOwners
* tblCAPARegister

### Outputs

* ContainmentActions
* CorrectiveActions
* PreventiveActions
* OwnerAssignments
* TargetDates

---

## Evidence Update & Selective Reassessment Specialist

### Purpose

Control selective reassessment after new evidence arrives.

### Outputs

* StaleSpecialists
* SpecialistsToRerun
* UpdatedReassessmentCount
* ManualReviewRequired

---

## M365 Guidance Specialist

### Purpose

Provide Microsoft operational guidance.

### Tool

Microsoft Learn MCP

### Outputs

* Microsoft guidance
* configuration recommendations
* deployment guidance

This agent does not influence quality severity.

---

# Orchestration model

## Sequential stages

### Stage 1: Trigger

The recurrence trigger retrieves the oldest unprocessed complaint cluster.

### Stage 2: Validation

The supervisor invokes the Incident Intake & Validation Specialist.

### Stage 3: Validation gate

If validation fails, the workflow terminates.

If validation succeeds, specialist analysis begins.

### Stage 4: Parallel execution

The supervisor invokes in parallel:

* Complaint Pattern Specialist
* Returns Specialist
* Product/Batch Specialist
* Customer Impact Specialist
* Safety Specialist

### Stage 5: Fan-in

The supervisor waits for all required specialist findings.

### Stage 6: Decision recommendation

The supervisor invokes the Quality Investigation Decision Specialist.

### Stage 7: Final classification

The supervisor assigns the final quality classification.

### Stage 8: CAPA

The supervisor invokes CAPA Planning & Ownership Specialist when required.

### Stage 9: Operational execution

The supervisor:

* generates the report,
* updates Excel,
* sends notifications.

### Stage 10: Reassessment

New evidence is processed through selective reassessment.

---

# Parallel fan-out / fan-in

The architecture intentionally separates **parallel evidence collection** from **centralized decision making**.

## Fan-out

Independent specialists analyze different evidence domains simultaneously.

## Fan-in

The supervisor consolidates:

* complaint evidence,
* return evidence,
* manufacturing evidence,
* customer evidence,
* safety evidence.

This reduces investigation latency while preserving deterministic governance.

---

# Decision authority

## Child agents

Child agents provide:

* evidence,
* analysis,
* recommendations,
* confidence,
* data gaps.

## Quality Supervisor

The supervisor assigns:

* Informational
* Monitoring
* Investigation Required
* High-Priority Quality Incident
* Critical Escalation
* Insufficient Evidence
* Manual Review

Only the supervisor may assign the final classification.

---

# Quality rule precedence

Rules are evaluated in this order.

## Rule 1: Safety override

CriticalEscalation = True

## Rule 2: High-priority safety pattern

Repeated safety concerns.

## Rule 3: Complaint threshold

Five or more similar complaints within seven days.

## Rule 4: Return-rate threshold

Return rate greater than or equal to 2%.

## Rule 5: Previous incident recurrence

Historical repeated batch failure.

## Rule 6: Missing evidence

Critical manufacturing or batch data missing.

## Rule 7: Overdue CAPA

Existing overdue corrective action.

The highest-priority applicable rule wins.

---

# Data architecture

## Read-only tables

* tblProductMaster
* tblBatchRegister
* tblSalesSummary
* tblReturns
* tblOwners
* tblQualityRules

## Operational tables

* tblCustomerComplaints
* tblQualityIncidents
* tblCAPARegister

Only the Quality Supervisor writes to operational tables.

---

# State management

Each incident maintains:

* IncidentID
* ComplaintID
* SKU
* BatchID
* FinalClassification
* DecisionRationale
* AppliedRule
* ReassessmentCount
* CAPAStatus
* ReportStatus
* NotificationStatus

State is preserved across reassessment cycles.

---

# Failure isolation

Specialist failures do not automatically terminate the workflow.

The supervisor:

1. retries once,
2. records the failure,
3. continues with available evidence when permitted.

MCP failures are isolated from quality investigations.

---

# Reassessment architecture

When new evidence arrives:

1. identify changed evidence,
2. determine stale specialists,
3. rerun only affected specialists,
4. preserve unaffected findings,
5. increment ReassessmentCount,
6. re-enter decision evaluation.

Maximum automated reassessment cycles:

**2**

After the second unresolved cycle:

**Manual Review**

---

# Security model

## Quality Supervisor

Read/write operational authority.

## Specialists

Read-only analytical authority.

## M365 Guidance Specialist

External documentation authority only.

This separation supports auditability and controlled enterprise governance.

---

# Enterprise design principles

The architecture is built around:

* hierarchical supervision,
* single decision authority,
* deterministic policy enforcement,
* parallel evidence collection,
* bounded autonomous execution,
* selective reassessment,
* auditable decision making,
* Microsoft 365 native integration,
* enterprise operational governance.

This architecture satisfies the PRD requirement for a **multi-agent autonomous quality investigation control tower** with **parallel orchestration, deterministic decision logic, and enterprise-grade operational governance**.
