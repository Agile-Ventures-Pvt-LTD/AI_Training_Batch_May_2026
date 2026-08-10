# CAP-001 — Architecture

## 1. Architecture Overview

The CAP-001 Sleepsia Product Quality & Customer Experience Intelligence Control Tower is designed as a hierarchical, autonomous, multi-agent quality assessment system implemented in Microsoft Copilot Studio.

The architecture separates:

- Autonomous triggering
- Incident intake and deterministic validation
- Specialist analysis
- Specialist result consolidation
- Quality decision making
- CAPA planning
- Supervisor validation
- Reporting
- Notification
- Operational state updates
- Evidence-based reassessment
- Interactive employee assistance

The **Quality Supervisor** is the parent orchestrator and the sole final decision owner.

Specialist agents perform narrow, independent analyses and return findings to the Supervisor. They do not independently determine final incident severity or external/internal actions.

---

# 2. High-Level Architecture

```text
                         +----------------------+
                         |   Recurrence Trigger |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |   Quality Supervisor |
                         |  Parent Orchestrator |
                         +----------+-----------+
                                    |
                                    v
                 +--------------------------------------+
                 | Topic 1: Incident Intake & Validation|
                 +------------------+-------------------+
                                    |
                          Validation Outcome
                           /              \
                          /                \
                    INVALID              VALID
                      |                    |
                      v                    v
                 STOP FLOW         Product / Batch
                                  Context Identified
                                           |
                                           v
                           +-----------------------------+
                           |      Specialist Fan-Out     |
                           +-----------------------------+
                              |      |      |      |      |
                              v      v      v      v      v
                         Complaint Returns Product Customer Safety
                         Pattern   Specialist /Batch  Impact  Specialist
                         Specialist          Specialist Specialist
                              \      |      |      |      /
                               \     |      |      |     /
                                +----+------+------+----+
                                           |
                                           v
                              +-----------------------+
                              |   Supervisor Fan-In   |
                              +-----------+-----------+
                                          |
                                          v
                          +-------------------------------+
                          | Topic 2: Quality Investigation|
                          |          Decision             |
                          +---------------+---------------+
                                          |
                         +----------------+----------------+
                         |                |                |
                         v                v                v
                    Informational    Investigation   Critical /
                    / Monitoring      Required       High Priority
                         |                |                |
                         +----------------+----------------+
                                          |
                                          v
                          +-------------------------------+
                          | Topic 3: CAPA Planning &       |
                          | Ownership / Closure Path       |
                          +---------------+---------------+
                                          |
                                          v
                              +-----------------------+
                              | Supervisor Validation |
                              +-----------+-----------+
                                          |
                             +------------+------------+
                             |                         |
                             v                         v
                       Word Report              Outlook Notification
                             |                         |
                             +------------+------------+
                                          |
                                          v
                                  Excel State Update