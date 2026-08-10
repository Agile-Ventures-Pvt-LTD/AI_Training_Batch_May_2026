# Custom Topics & Adaptive Card UI Documentation

## 1. Incident State Model 

| Incident State | Trigger / Condition | Responsible Topic / Node | Output Action |
|---|---|---|---|
| **New** | Autonomous trigger detects unprocessed complaint row (`Processed = No`). | Recurrence Trigger | Creates intake record context. |
| **In Assessment** | Topic 1 validates identifiers as `Valid`. Specialist fan-out initiated. | Topic 1 (Intake Validation) | Invokes 5 specialist child agents. Renders Intake Card. |
| **Monitoring** | Single isolated complaint. No threshold met (Rule 8). | Topic 2 (Decision Topic) | Classifies as `Informational`. Renders Summary Card. |
| **Investigation Open** | Complaint cluster ≥ 5 (Rule 3) OR Return rate ≥ 2% (Rule 4). | Topic 2 (Decision Topic) | Classifies as `Investigation Required`. Renders Summary Card. |
| **CAPA Open** | Topic 3 generates CAPA plan for Investigation, High-Priority, or Critical cases. | Topic 3 (CAPA Planning) | Writes to `CAPA_Register`. Renders CAPA Card. |
| **Awaiting Evidence** | Missing BatchID for repeated cluster (Rule 6) OR specialist retry pending. | Topic 1 & Topic 2 | Sets status `Awaiting Evidence` / `Insufficient Evidence`. |
| **Critical Escalation** | `SafetyIndicator = Yes` confirmed (Rule 1). | Topic 2 & Safety Specialist | Halts routine troubleshooting. Alerts Safety Officer in 24h. |
| **Manual Review** | Automated reassessment loop count exceeds 2 cycles (`ReassessmentCount > 2`). | Topic 4 (Reassessment) | Sets status `Manual Review`. Halts automation. |
| **Closed** | Human Quality Supervisor approves investigation and CAPA validation. | Quality Supervisor | Updates `Quality_Incidents` status to `Closed`. |

---

## 2. Topic 1: Incident Intake & Validation
- **Model Description:** Deterministic intake validation before specialist analysis.
- **Inputs:** `ComplaintID`, `OrderID`, `SKU`, `BatchID`, `IsRepeatedCluster`
- **Outputs:** `ValidationResult` (`Valid`, `Invalid`, `Insufficient Evidence`), `ValidationReason`

---

## 3. Topic 2: Quality Investigation Decision
- **Model Description:** Consolidate specialist findings and assign quality classification based on 8 explicit priority rules.
- **Inputs:** `SafetyIndicatorConfirmed`, `PotentialSafetyCount`, `TotalComplaintCount`, `ReturnRatePercent`, `PreviousIncidentCount`, `RepeatedFailureMode`, `BatchID`, `HasOverdueCAPA`
- **Outputs:** `IncidentClassification`, `ClassificationRationale`
- **Rule Precedence:**
  1. Priority 1: `SafetyIndicator = Yes` → Critical Escalation
  2. Priority 2: 2+ Potential safety complaints → High-Priority Quality Incident
  3. Priority 3: 5+ complaints within 7 days → Investigation Required
  4. Priority 4: Return rate ≥ 2% → Investigation Required
  5. Priority 5: Previous incident + repeated failure → High-Priority Quality Incident
  6. Priority 6: Missing batch for repeated cluster → Insufficient Evidence
  7. Priority 7: Overdue CAPA → High-Priority Quality Incident
  8. Priority 8: Single isolated complaint → Informational

---

## 4. Topic 3: CAPA Planning & Ownership
- **Model Description:** Generate CAPA recommendations and assign owner role for Investigation, High-Priority or Critical incidents
- **Inputs:** `IncidentID`, `IncidentClassification`, `SKU`, `BatchID`, `DominantFailureMode`
- **Outputs:** `CAPAStatus`, `OwnerRole`, `ContainmentAction`, `CorrectiveAction`, `PreventiveAction`, `ValidationMethod`, `TargetDate`
- **Owner Roles & SLAs:**
  - `Critical Escalation` → Safety Officer (SLA: 24 Hours)
  - `High-Priority Quality Incident` → Quality Manager (SLA: 3 Days)
  - `Investigation Required` → Quality Analyst (SLA: 7 Days)

---

## 5. Topic 4: Evidence Update & Selective Reassessment
- **Model Description:** Handle evidence updates, increment cycle count, enforce max 2 reassessment limit
- **Inputs:** `IncidentID`, `ReassessmentCount`, `NewEvidenceDetails`, `PreviousClassification`
- **Outputs:** `ReassessmentCount`, `ReassessmentStatus`, `RequiresManualReview`
