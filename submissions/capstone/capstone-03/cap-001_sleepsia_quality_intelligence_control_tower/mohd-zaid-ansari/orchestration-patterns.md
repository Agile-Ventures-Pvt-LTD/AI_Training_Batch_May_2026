# Orchestration Patterns

## Overview

The Sleepsia solution uses a **Supervisor–Specialist** orchestration model in Microsoft Copilot Studio. The **Quality Supervisor** controls the investigation workflow, while specialist agents perform independent domain-specific analysis.

---

# 1. Sequential Orchestration

The workflow follows a fixed execution order:

1. Incident Intake & Validation
2. Specialist Investigation
3. Quality Investigation Decision
4. CAPA Planning (if required)
5. Evidence Reassessment (if required)
6. Report Generation
7. Excel Updates
8. Email Notification

---

# 2. Parallel Orchestration (Fan-Out)

After successful validation, the Supervisor executes the following agents simultaneously:

- Complaint Pattern Specialist
- Returns Specialist
- Product/Batch Specialist
- Customer Impact Specialist
- Safety Specialist

This reduces investigation time by running independent analyses in parallel.

---

# 3. Fan-In Consolidation

The Supervisor waits for all specialist responses before continuing.

It consolidates the returned evidence and passes it to the **Quality Investigation Decision** topic for deterministic classification.

---

# 4. Hierarchical Orchestration

The Quality Supervisor acts as the parent orchestrator.

Child agents perform only their assigned responsibilities and return findings to the Supervisor. Child agents never communicate directly with each other.

---

# 5. Conditional Orchestration

Workflow branches are determined by business rules.

Examples:

- Invalid complaint → Stop investigation.
- Investigation Required → Start CAPA Planning.
- No Investigation Required → Generate report and close.
- New evidence received → Execute Selective Reassessment.

---

# 6. Loop / Selective Reassessment

If additional evidence is submitted, only the affected specialist agent is re-executed.

Previously completed specialist analyses are reused to improve efficiency.

---

# 7. Fallback Handling

If a specialist, tool, or knowledge source cannot provide sufficient evidence:

- Record the issue.
- Return **Insufficient Evidence**.
- Stop only the affected investigation.
- Continue processing other complaints.

---

# Workflow Summary

```text
Trigger
   │
   ▼
Incident Intake & Validation
   │
   ▼
Fan-Out Specialist Analysis
   │
   ▼
Fan-In Consolidation
   │
   ▼
Quality Investigation Decision
   │
   ▼
CAPA Planning (if required)
   │
   ▼
Evidence Reassessment (if required)
   │
   ▼
Report Generation
   │
   ▼
Excel Updates
   │
   ▼
Email Notification
   │
   ▼
End Investigation
```

---

# Benefits

- Centralized orchestration
- Parallel specialist execution
- Deterministic decision making
- Clear tool ownership
- Efficient selective reassessment
- Improved scalability and traceability

---

# Conclusion

The orchestration combines **sequential**, **parallel**, **hierarchical**, **conditional**, **loop**, and **fallback** patterns to deliver a governed, scalable, and efficient quality investigation workflow in Microsoft Copilot Studio.