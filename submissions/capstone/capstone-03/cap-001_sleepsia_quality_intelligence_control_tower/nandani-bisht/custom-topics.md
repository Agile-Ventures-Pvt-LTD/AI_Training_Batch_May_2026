# Custom Topic Design and Configuration

This document specifies the design, variables, logic branches, and outputs for the four mandatory custom topics configured in the **Sleepsia Quality Control Tower**.

---

## 1. Topic 1 - Incident Intake & Validation

### Purpose
Deterministic validation of input records to filter out incomplete or invalid complaints before invoking specialist child agents.

### Variables & Inputs
- **Inputs:**
  - `Raw_ComplaintRecord` (Record object from Excel: contains `ComplaintID`, `OrderID`, `SKU`, `BatchID`, `ComplaintDate`, `Category`, `Severity`, `SafetyIndicator`, `Processed`)
- **Internal Variables:**
  - `IsValid` (Boolean)
  - `ValidationStatus` (String: "Valid", "Invalid", "Insufficient Evidence")
  - `ValidationLogs` (String)

### Validation Checks & Branching Logic
1. **ComplaintID & OrderID Existence:**
   - *Check:* `IsBlank(Raw_ComplaintRecord.ComplaintID) || IsBlank(Raw_ComplaintRecord.OrderID)`
   - *Action:* If true, set `ValidationStatus` to "Invalid", log "Missing Core Identifiers", and terminate topic.
2. **SKU Validation:**
   - *Check:* Queries `Product_Master` table to verify if `Raw_ComplaintRecord.SKU` exists.
   - *Action:* If not found, set `ValidationStatus` to "Invalid", log "SKU Not in Product Master", and terminate topic.
3. **BatchID-to-SKU Validation:**
   - *Check:* If `Raw_ComplaintRecord.BatchID` is supplied, queries `Batch_Register` to confirm the batch maps to the provided SKU.
   - *Action:* If batch does not map to SKU, set `ValidationStatus` to "Invalid", log "Batch SKU Mismatch", and terminate. If batch is missing but required (e.g. for repeat clusters), set `ValidationStatus` to "Insufficient Evidence".
4. **Complaint Date Validity:**
   - *Check:* Confirms `Raw_ComplaintRecord.ComplaintDate` is a valid date structure and is not in the future.
   - *Action:* If invalid, set `ValidationStatus` to "Invalid".
5. **Category & Severity Validation:**
   - *Check:* Validates `Category` matches standard categories (e.g., Odour, Shape-Recovery, Stitching, Zipper, Packaging) and `Severity` is within range [1-5].
   - *Action:* If invalid, set `ValidationStatus` to "Invalid".
6. **Duplicate Check:**
   - *Check:* Checks `Quality_Incidents` for an existing record with matching `ComplaintID`.
   - *Action:* If exists and `Processed = Yes`, mark as duplicate and set `ValidationStatus` to "Invalid".

### Outputs
- `ValidationStatus` (String: "Valid" / "Invalid" / "Insufficient Evidence")
- `Validated_Complaint` (Record)

---

## 2. Topic 2 - Quality Investigation Decision

### Purpose
Consolidates findings returned by the five specialist child agents and assigns exactly one quality classification based on explicit policy precedence.

### Variables & Inputs
- **Inputs:**
  - `Specialist_CP_Output` (Complaint Pattern findings)
  - `Specialist_R_Output` (Returns findings)
  - `Specialist_PB_Output` (Product/Batch findings)
  - `Specialist_CI_Output` (Customer Impact findings)
  - `Specialist_S_Output` (Safety findings)
- **Outputs:**
  - `Final_Classification` (String)
  - `Final_Severity` (String: "Low", "Medium", "High", "Critical")
  - `Decision_Rationale` (String)

### Decision Precedence Engine (Highest Priority Wins)
The Supervisor applies the rules sequentially. The first rule that evaluates to `true` determines the classification. No averaging is permitted.

```
       [Evaluate Specialist Outputs]
                     │
                     ▼
  Priority 1: SafetyIndicator = Yes? ────────── Yes ──> [Critical Escalation]
                     │ No
                     ▼
  Priority 2: Two or more Potential safety? ──── Yes ──> [High-Priority Quality Incident]
                     │ No
                     ▼
  Priority 3: 5+ complaints in 7 days? ──────── Yes ──> [Investigation Required]
                     │ No
                     ▼
  Priority 4: Return rate >= 2%? ────────────── Yes ──> [Investigation Required]
                     │ No
                     ▼
  Priority 5: Prev incident + repeat mode? ──── Yes ──> [High-Priority Quality Incident]
                     │ No
                     ▼
  Priority 6: Missing batch for repeat? ──────── Yes ──> [Insufficient Evidence]
                     │ No
                     ▼
  Priority 7: Overdue CAPA? ─────────────────── Yes ──> [High-Priority Quality Incident]
                     │ No
                     ▼
  Priority 8: Single isolated complaint? ────── Yes ──> [Informational]
```

### Rule Rules Definition

1. **Priority 1 (Critical Escalation):**
   - *Condition:* `Specialist_S_Output.SafetyIndicator = "Yes"` (e.g. fire/smoke complaints).
   - *Classification:* `Critical Escalation`
2. **Priority 2 (High-Priority Quality Incident):**
   - *Condition:* `Specialist_S_Output.PotentialSafetyCount >= 2` for same SKU/batch without a confirmed safety override.
   - *Classification:* `High-Priority Quality Incident`
3. **Priority 3 (Investigation Required):**
   - *Condition:* `Specialist_CP_Output.ComplaintCount >= 5` for same SKU/batch within 7 days.
   - *Classification:* `Investigation Required`
4. **Priority 4 (Investigation Required):**
   - *Condition:* `Specialist_R_Output.ReturnRate >= 0.02` for the target SKU.
   - *Classification:* `Investigation Required`
5. **Priority 5 (High-Priority Quality Incident):**
   - *Condition:* `Specialist_PB_Output.PreviousIncidentCount > 0` AND `Specialist_CP_Output.HasRepeatedFailureMode = true`.
   - *Classification:* `High-Priority Quality Incident`
6. **Priority 6 (Insufficient Evidence):**
   - *Condition:* Repeated failure mode cluster detected but `Raw_ComplaintRecord.BatchID` is missing/null.
   - *Classification:* `Insufficient Evidence`
7. **Priority 7 (High-Priority Quality Incident):**
   - *Condition:* `Specialist_PB_Output.HasOverdueCAPA = true`.
   - *Classification:* `High-Priority Quality Incident`
8. **Priority 8 (Informational):**
   - *Condition:* Single isolated low-severity complaint (does not trigger any higher rules).
   - *Classification:* `Informational`

---

## 3. Topic 3 - CAPA Planning & Ownership

### Purpose
Executes only after Topic 2 assigns a classification of `Investigation Required`, `High-Priority Quality Incident`, or `Critical Escalation`. Generates containment actions and writes to the registry.

### Variables & Inputs
- **Inputs:**
  - `Incident_ID` (String)
  - `Classification` (String)
  - `SKU` (String)
  - `BatchID` (String)
- **Outputs:**
  - `CAPA_Summary` (Record)

### Flow Steps
1. **Containment Plan Generation:**
   - If `Classification` is `Critical Escalation`, set containment to "Immediate quarantine of batch, pause shipping, alert production line".
   - If `Investigation Required` or `High-Priority`, set containment to "Increase inspection rate for incoming inventory, monitor returns daily".
2. **Corrective & Preventive Action Drafting:**
   - Auto-drafts corrective plan (e.g. "Conduct supplier audit for lot, test zipper durability").
3. **Ownership Assignment:**
   - Queries the `Owners` table in Excel matching the product category to assign `OwnerRole` (e.g., Quality Engineer, Sourcing Specialist, Safety Lead).
4. **Target Date Calculation:**
   - Set target date to `Today() + 14` days for Investigations, and `Today() + 3` days for Critical Escalation.
5. **Validation Method Definition:**
   - Defines the validation method (e.g., "100% inspections of next 3 shipments", "Thermal stress test verification").
6. **Database Write:**
   - Writes new row to `CAPA_Register` table containing: `CAPA_ID`, `Incident_ID`, `SKU`, `ContainmentAction`, `CorrectiveAction`, `OwnerRole`, `TargetDate`, `Status = Open`.

---

## 4. Topic 4 - Evidence Update & Selective Reassessment

### Purpose
Controls re-evaluations when new evidence arrives for an active incident. Restricts re-runs to stale specialist outputs to optimize execution.

### Variables & Inputs
- **Inputs:**
  - `Incident_ID` (String)
  - `New_Evidence` (Record containing updated fields)
- **Outputs:**
  - `Reassessment_Status` (String: "Re-assessed", "Manual Review Required")

### Flow Steps
1. **Changed Evidence Identification:**
   - Compare `New_Evidence` against cached values.
2. **Determine Stale Specialists:**
   - If returns data changed: mark `Returns Specialist` and `Customer Impact Specialist` as **Stale**.
   - If batch/manufacturing data changed: mark `Product/Batch Specialist` as **Stale**.
   - If complaint count/texts changed: mark `Complaint Pattern Specialist` as **Stale**.
3. **Rerun Stale Specialists:**
   - Dispatches calls only to the child agents marked as **Stale**.
   - Keeps and reuses the cached outputs of the non-stale specialists.
4. **Increment Loop Counter:**
   - `ReassessmentCount = ReassessmentCount + 1`
5. **Loop Guard Evaluator:**
   - If `ReassessmentCount > 2`:
     - Set status to `Manual Review Required`.
     - Update incident state in Excel to `Manual Review`.
     - Exit topic to prevent infinite execution loops.
   - Else:
     - Re-enter **Topic 2 - Quality Investigation Decision** with updated specialist parameters.
