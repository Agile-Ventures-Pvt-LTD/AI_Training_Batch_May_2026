# Custom Topics Design & YAML Specifications

## Overview
Three mandatory custom topics implement deterministic business logic, conflict resolution and approval routing within the Supervisor agent.

---

## Custom Topic 1: Disruption Intake & Validation
- **Purpose:** Rule-based validation of disruption requests before triggering specialist agents.

---

## Custom Topic 2: Recovery Strategy Resolution
- **Purpose:** Resolves competing specialist recommendations after fan-in using PRD decision precedence.

---

## Custom Topic 3: Approval Exception & Selective Reassessment
- **Purpose:** Controls human approvals, specialist retries, and bounds automated reassessment loops.
