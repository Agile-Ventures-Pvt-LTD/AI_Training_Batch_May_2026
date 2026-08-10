# Custom Topics

## Topic 1 — Intake & Validation

**Purpose:** Validate the incident/complaint data before quality investigation.

**Key Variables:**
- IncidentID
- ComplaintID
- OrderID
- SKU
- BatchID
- ComplaintDate
- Category
- Severity
- ValidationStatus
- ValidationReason

**Branches:**
- Required data complete → Continue to Topic 2
- Missing/invalid data → Validation Failed
- Batch/SKU mismatch → Validation Failed

**Outputs:**
- ValidationStatus
- ValidationReason
- IncidentID
- SKU
- BatchID


## Topic 2 — Quality Investigation Decision

**Purpose:** Consolidate specialist findings and apply quality-policy precedence.

**Input Variables:**
- Input_SafetyIndicator
- Input_PotentialSafetyCount
- Input_ComplaintCount
- Input_ReturnRate
- Input_HasPreviousIncident
- Input_IsBatchMissing
- Input_HasOverdueCAPA

**Branches:**
1. Safety Indicator = Yes → Critical Escalation
2. Potential Safety Count ≥ 2 → High-Priority Quality Incident
3. Complaint Count ≥ 5 → Investigation Required
4. Return Rate ≥ 2% → Investigation Required
5. Previous Incident = True → High-Priority Quality Incident
6. Batch Missing + Complaint Count > 1 → Insufficient Evidence
7. Overdue CAPA = True → High-Priority Quality Incident
8. No trigger → Informational

**Outputs:**
- FinalClassification
- DecisionRationale


## Topic 3 — CAPA Planning & Ownership

**Purpose:** Create containment/corrective/preventive actions and assign CAPA ownership.

**Input Variables:**
- IncidentID
- FinalClassification
- SKU
- BatchID

**Branches:**
- Critical Escalation → CAPA required
- High-Priority Quality Incident → CAPA required
- Investigation Required → CAPA required
- Informational → No CAPA / close or monitor
- Invalid incident/classification → Manual handling

**Processing:**
- Create containment action
- Define corrective action
- Define preventive action
- Determine OwnerRole
- Retrieve OwnerName/OwnerEmail from Owners table
- Set TargetDate
- Define ValidationMethod
- Write/update CAPA_Register

**Outputs:**
- CAPA ID
- ContainmentAction
- CorrectiveAction
- PreventiveAction
- OwnerRole
- OwnerName
- OwnerEmail
- TargetDate
- ValidationMethod
- CAPASummary


## Topic 4 — Evidence Update & Selective Reassessment

**Purpose:** Reassess only specialist analyses affected by changed evidence.

**Input Variables:**
- IncidentID
- ChangedEvidence
- ReassessmentCount
- ComplaintFinding
- ReturnFinding
- ProductFinding
- SafetyFinding
- CAPAFinding

**Branches:**
- Complaint evidence changed → Rerun Complaint Specialist
- Return evidence changed → Rerun Return Specialist
- Product/batch evidence changed → Rerun Product Specialist
- Safety evidence changed → Rerun Safety Specialist
- CAPA evidence changed → Rerun CAPA Specialist
- No relevant change → Preserve existing findings
- ReassessmentCount > 2 → Manual Review

**Processing:**
1. Identify changed evidence.
2. Determine stale specialists.
3. Rerun only stale analyses.
4. Preserve unaffected findings.
5. Increment ReassessmentCount.
6. Re-enter Topic 2 for the updated quality decision.

**Outputs:**
- Updated specialist findings
- ReassessmentCount
- Rerun status for each specialist
- ManualReviewRequired
- Updated FinalClassification
- Updated DecisionRationale