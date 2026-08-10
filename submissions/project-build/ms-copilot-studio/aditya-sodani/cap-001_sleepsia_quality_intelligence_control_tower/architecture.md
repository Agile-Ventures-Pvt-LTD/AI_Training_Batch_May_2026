# Architecture — Sleepsia Quality Intelligence Control Tower

## 1. Architecture Overview

The Sleepsia Quality Intelligence Control Tower follows a **Supervisor–Specialist architecture** implemented in Microsoft Copilot Studio.

The architecture separates:

- User interaction and orchestration
- Complaint intake and validation
- Specialist quality analysis
- Quality decision-making
- CAPA planning and ownership
- Evidence reassessment
- Enterprise data access
- Reporting and notification

The **Quality Supervisor** acts as the central orchestration layer. Specialist agents perform domain-specific analysis and return findings. The Supervisor consolidates those findings and applies explicit policy precedence.

---

## 2. High-Level Architecture

```text
                         USER
                          |
                          v
              +-----------------------+
              | Quality Supervisor    |
              | Copilot Studio Agent  |
              +-----------+-----------+
                          |
            +-------------+-------------+
            |                           |
            v                           v
   +------------------+       +----------------------+
   | Topic 1          |       | Topic 4              |
   | Intake &         |       | Evidence Update &    |
   | Validation       |       | Selective Reassessment|
   +--------+---------+       +----------+-----------+
            |                            |
            | Valid                      |
            v                            |
   +------------------+                  |
   | Topic 2          |<-----------------+
   | Quality          |
   | Investigation    |
   | Decision         |
   +--------+---------+
            |
            | Classification
            v
   +------------------+
   | Topic 3          |
   | CAPA Planning &  |
   | Ownership        |
   +--------+---------+
            |
      +-----+------+----------------+
      |            |                |
      v            v                v
   Excel         Word           Outlook
   Tools         Tool             Tool
      |            |                |
      v            v                v
Operational    Quality/CAPA     Owner/Quality
Data           Report           Notification