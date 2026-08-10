# Multi-Agent Orchestration Patterns

This document details the implementation of the six mandatory orchestration patterns for the **Sleepsia Quality Control Tower** within Microsoft Copilot Studio.

---

## 1. Sequential Orchestration Pattern

The core assessment workflow executes in a strict sequential timeline to ensure data integrity and proper validation checkpoints.

### Flow Timeline
```
[Recurrence Trigger] 
       │
       ▼
[Intake Validation (Topic 1)] ──(If Invalid/Insufficient)──> [Request Evidence / Exit]
       │
       ▼ (If Valid)
[Parallel Specialist Fan-Out] 
       │
       ▼ (All Specialists Return)
[Quality Decision Logic (Topic 2)]
       │
       ▼ (Critical / Investigation Required / High-Priority)
[CAPA Planning (Topic 3)] 
       │
       ▼
[Supervisor Validation & Authorization]
       │
       ▼
[Word Quality Report Generation]
       │
       ▼
[Excel Operational Dataset Update]
       │
       ▼
[Outlook Notification Alert]
```

---

## 2. Parallel Fan-Out / Fan-In Pattern

Once input identifiers are validated, the system triggers parallel evaluation processes for the four primary analytical domains.

### Implementation Details
- **Parallel Dispatch:** The Quality Supervisor invokes child agents via concurrent asynchronous threads. Microsoft Copilot Studio maps these calls using parallel Power Automate sub-flows.
- **Independent Scopes:**
  - **Complaint Pattern Specialist** queries the `Customer_Complaints` sheet.
  - **Returns Specialist** queries `Returns` and `Sales_Summary`.
  - **Product/Batch Specialist** queries `Batch_Register` and `Quality_Incidents`.
  - **Customer Impact Specialist** cross-references complaints and returns.
- **Fan-In Synchronisation:** The Supervisor remains in a "Waiting" state and utilizes a validation block to confirm all four specialist return structures are populated (e.g., `IsBlank(CP_Output) = false && IsBlank(R_Output) = false && ...`) before moving to the decision phase.

---

## 3. Hierarchical Pattern

The Quality Supervisor acts as the master parent agent, maintaining centralized authority over all operational actions and outcomes.

### Control Hierarchy
- **Delegation:** Child agents process specific Excel rows, calculate specific ratios, and extract batch histories. They return raw scores and confidence values.
- **Central Authority:** Specialists *never* write directly to `Quality_Incidents`, generate Word documents, or send Outlook emails. They submit their structured findings to the Supervisor.
- **Severity Decoupling:** The final severity and incident classification are calculated inside the Supervisor’s **Quality Investigation Decision (Topic 2)** based on combined specialist evidence.

---

## 4. Conditional Routing

The Supervisor evaluates specialist outputs against a set of predefined corporate quality thresholds and routes execution along specific branches.

| Condition Trigger | Evaluated Variables | Routing Target |
| :--- | :--- | :--- |
| **Safety Indicator = Yes** | `Safety_Specialist.ConfirmedSafetyHazard` | **Critical Escalation Path:** Halts routine troubleshooting, triggers immediate incident creation, and initiates high-priority alerts. |
| **Threshold Exceeded** | `Complaint_Specialist.ComplaintCount >= 5` within 7 days | **Investigation Path:** Initiates CAPA planning. |
| **High Return Rate** | `Returns_Specialist.ReturnRate >= 0.02` (2%) | **Investigation Path:** Triggers detailed product line audit. |
| **Repeat Incident** | `Product_Specialist.PreviousIncidentCount > 0` | **High-Priority Path:** Bypasses informational status, forcing formal tracking. |
| **Missing Evidence** | `Product_Specialist.BatchIDExists = false` or missing data | **Evidence Request Path:** Updates state to `Awaiting Evidence` and exits. |
| **Overdue CAPA** | `CAPA_Specialist.OverdueCAPA = true` | **Critical Escalation Path:** Escalates ownership level. |
| **MCP Server Error** | `M365_Guidance.Status = "Error"` | **Bypass Path:** Logs error, sets status to "Microsoft guidance unavailable - manual review", and proceeds with core quality assessment. |

---

## 5. Selective Reassessment Loop

When new evidence or updated data is submitted for an existing incident, the system triggers a bounded reassessment loop.

```
       [New Evidence Received]
                  │
                  ▼
      [Identify Changed Fields]
                  │
                  ▼
     [Determine Stale Specialists]
                  │
                  ▼
      [Rerun Stale Specialists] ──(Unchanged Specialists Preserved)
                  │
                  ▼
       [Increment Reassessment]
                  │
                  ▼
       [Is Reassessment > 2?]
          ├── Yes ──> [Set state to Manual Review & Halt]
          └── No  ──> [Re-evaluate Quality Decision (Topic 2)]
```

### Loop Guard
- **Stale Tracking:** If only the return data changes, the system reruns the **Returns Specialist** and **Customer Impact Specialist**. The findings of the **Product/Batch Specialist** and **Complaint Pattern Specialist** are preserved to save API usage and token overhead.
- **Cycles Guard:** The counter `ReassessmentCount` is incremented on every entry. If `ReassessmentCount > 2`, the system marks the incident state as `Manual Review` and suspends automation to prevent infinite routing loops.

---

## 6. Retry / Fallback Logic

To ensure system reliability in production, transient failures are caught and handled systematically.

- **Specialist Call Failure:** If a call to a specialist child agent fails or times out, the Quality Supervisor retries the call exactly once. If the second call fails, the Supervisor records a status of `Insufficient Evidence` for that specialist and continues the workflow instead of crashing.
- **Excel Read Failure:** If the system fails to read the operational dataset, the assessment process is halted, and the failure is logged.
- **Excel Update Failure:** If an incident assessment succeeds but the Excel status update fails, the complaint record remains marked `Processed = No` to ensure it is re-evaluated during the next schedule.
- **Word / Outlook Failure:** If the report generation or email notification fails, the incident decision is preserved. The system updates the incident record with `ReportGeneration = Failed` or `Notification = Failed` and proceeds.
- **No Fabricated Evidence:** If an integration point fails, the system logs the actual failure. It never fabricates placeholder data or claims a success when a step has failed.
