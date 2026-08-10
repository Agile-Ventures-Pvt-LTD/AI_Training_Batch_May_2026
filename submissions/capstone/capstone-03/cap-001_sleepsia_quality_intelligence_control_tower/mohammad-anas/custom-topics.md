# Custom Topics

## Standard specialist output contract
Every specialist returns: domain-specific quantitative findings. Insufficient Evidence is returned explicitly rather than a fabricated value when data cannot be retrieved.

---

## Topic 1 — Incident Intake & Validation

**Purpose:** Deterministic validation before any specialist analysis begins; also routes new evidence on existing incidents to reassessment instead of a fresh fan-out.

**Inputs:** the next unprocessed complaint record's fields (ComplaintID, OrderID, SKU, BatchID, ComplaintDate, Category, Severity, Description, SafetyIndicator) read via List rows on Customer_Complaints filtered `Processed eq 'No'`.

**Validation checks (per-record, not schema-level):**
- ComplaintID, OrderID non-blank
- SKU exists as a row in Product_Master
- BatchID (if supplied) exists in Batch_Register and maps to the same SKU
- ComplaintDate non-blank/valid
- Category and Severity are non-blank / within expected value sets
- Duplicate check: complaint not already Processed

**Branches:**
- Any check fails → ValidationStatus = Invalid or Insufficient Evidence, ValidationReason recorded, complaint not marked Processed, no specialists invoked.
- All checks pass → check Quality_Incidents for an existing Open record on this SKU/BatchID:
  - Found → set ChangedDataSource = "New complaint added", capture IncidentID and ReassessmentCount → call Topic 4.
  - Not found → proceed to fan-out (five specialists) → fan-in → call Topic 2.

**Outputs:** ValidationStatus, ValidationReason, SKU, BatchID, and (if applicable) IncidentID/ReassessmentCount for the Topic 4 branch.

---

## Topic 2 — Quality Investigation Decision

**Purpose:** Consolidate specialist findings into exactly one FinalClassification using strict rule precedence — never averaged.

**Inputs:** SafetyIndicatorFlag, PotentialSafetyComplaintCount (Safety Specialist); SimilarComplaintCount7Days (Complaint Pattern Specialist); ReturnRatePct (Returns Specialist); PreviousIncidentExists, RepeatedFailureMode, BatchMissingForRepeatedCluster, OverdueCAPAExists (Product/Batch Specialist); IncidentID.

**Branches, in priority order (first match wins):**
1. SafetyIndicatorFlag = true → Critical Escalation
2. PotentialSafetyComplaintCount >= 2 → High-Priority Quality Incident
3. SimilarComplaintCount7Days >= 5 → Investigation Required
4. ReturnRatePct >= 2 → Investigation Required
5. PreviousIncidentExists AND RepeatedFailureMode → High-Priority Quality Incident
6. BatchMissingForRepeatedCluster → Insufficient Evidence
7. OverdueCAPAExists → High-Priority Quality Incident
8. None of the above → Informational

**Outputs:** FinalClassification, Rationale (references which rule/finding fired), IncidentID (pass-through).

---

## Topic 3 — CAPA Planning & Ownership

**Purpose:** Gate and delegate CAPA creation to cases that require it.

**Inputs:** IncidentID, FinalClassification, SKU, BatchID (from Topic 2).

**Branches:**
- FinalClassification in {Investigation Required, High-Priority Quality Incident, Critical Escalation} → call CAPA Specialist, capture CAPAID/ActionType/ActionDescription/OwnerRole/TargetDate/ValidationMethod, set CAPACreated = Yes.
- Otherwise (Monitor/Informational) → set CAPACreated = No, no agent call.

**Outputs:** CAPACreated, and CAPA fields where created.

---

## Topic 4 — Evidence Update & Selective Reassessment

**Purpose:** Bounded reassessment when new evidence arrives on an already-open incident.

**Inputs:** IncidentID, SKU, BatchID, ChangedDataSource, ReassessmentCount.

**Logic:**
1. ReassessmentCount > 2 → set Quality_Incidents.Status = Manual Review, end (no further reassessment).
2. Otherwise, determine stale specialists from ChangedDataSource (e.g. new complaint → re-run Complaint Pattern + Safety; new return → re-run Returns; batch/quality-hold change → re-run Product/Batch). Unaffected specialists' prior outputs are preserved, not re-fetched.
3. Call only the stale specialist(s).
4. Increment and persist ReassessmentCount to Quality_Incidents.
5. Re-enter Topic 2 with the mix of fresh and preserved specialist outputs.

**Outputs:** updated FinalClassification (via Topic 2 re-entry), updated ReassessmentCount.