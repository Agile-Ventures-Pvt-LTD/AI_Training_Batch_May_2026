# Orchestration Patterns — Sleepsia Quality Intelligence Control Tower

## Overview

The Sleepsia Quality Intelligence Control Tower uses multiple orchestration patterns within Microsoft Copilot Studio.

The primary patterns implemented or planned in the solution are:

1. Sequential orchestration
2. Parallel specialist analysis
3. Hierarchical orchestration
4. Conditional orchestration
5. Loop / reassessment orchestration
6. Fallback and manual-review handling

These patterns allow the Quality Supervisor to coordinate specialist agents while maintaining clear decision ownership and policy precedence.

---

# Orchestration Patterns

## Sequential Implementation

The workflow executes mandatory topics in sequence:

User Request → Topic 1: Intake & Validation → Topic 2: Quality Investigation Decision → Topic 3: CAPA Planning & Ownership → Final Response.

Topic 4 is invoked when evidence changes and reassessment is required.

---

## Parallel Implementation

The Quality Supervisor coordinates independent specialist analyses:

- Complaint Specialist
- Returns Specialist
- Product/Batch Specialist
- Safety Specialist
- CAPA Specialist

The specialist findings are consolidated by Topic 2. Each specialist is responsible only for its assigned domain and does not determine the final classification independently.

---

## Hierarchical Implementation

The solution follows a Supervisor–Specialist hierarchy:

Quality Supervisor  
→ Mandatory Topics  
→ Specialist Agents  
→ Tools / Data Sources

The Supervisor manages orchestration and final decision-making, while specialist agents retrieve and analyze domain-specific evidence.

---

## Conditional Implementation

Topic 2 applies quality-policy rules in explicit precedence order:

1. Confirmed Safety Indicator → Critical Escalation
2. Potential Safety Cluster → High-Priority Quality Incident
3. Complaint Cluster → Investigation Required
4. Return-Rate Threshold → Investigation Required
5. Previous Incident → High-Priority Quality Incident
6. Missing Evidence → Insufficient Evidence
7. Overdue CAPA → High-Priority Quality Incident
8. No trigger → Informational

The first applicable condition determines the final classification, ensuring exactly one classification is assigned.

---

## Loop / Reassessment Implementation

Topic 4 implements selective reassessment.

When evidence changes:

1. Identify changed evidence.
2. Determine which specialist findings are stale.
3. Rerun only the affected specialists.
4. Preserve unaffected findings.
5. Increment `ReassessmentCount`.
6. Re-enter Topic 2 for the updated quality decision.

Example:

Changed Return Evidence:
- Complaint → Preserve
- Returns → Rerun
- Product → Preserve
- Safety → Preserve
- CAPA → Preserve

If `ReassessmentCount > 2`, automatic reassessment stops and the case is routed to Manual Review.

---

## Fallback Implementation

Fallback handling is implemented for exceptional cases:

- Invalid complaint/input → Return validation failure and stop processing.
- Missing evidence → Return Insufficient Evidence or route for investigation/manual handling.
- Reassessment count greater than 2 → Manual Review.
- Tool failure → [ADD ACTUAL IMPLEMENTED TOOL FAILURE BEHAVIOR].

This prevents invalid or repeatedly failing cases from continuing through the automated workflow.