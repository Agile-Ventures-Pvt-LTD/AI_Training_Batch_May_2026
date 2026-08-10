# Architecture

## High-Level Architecture

```text
Complaint
   |
   v
Incident Intake & Validation
   |
   +---- Invalid ------------------> STOP
   |
   +---- Insufficient Evidence ----> STOP
   |
   +---- Valid
          |
          v
   Supervisor Fan-Out
     |    |    |    |    |
     v    v    v    v    v
  Pattern Returns Product Customer Safety
     |    |    |    |    |
     +----+----+----+----+
                 |
               Fan-In
                 |
                 v
        Supervisor Decision
                 |
       +---------+----------+
       |                    |
   No CAPA                 CAPA
       |                    |
       |              CAPA Specialist
       |                    |
       +---------+----------+
                 |
                 v
       Report / Notification
```

## Agent Boundaries

| Agent | Owns | Does not own |
|---|---|---|
| Supervisor | orchestration and final classification | specialist analysis |
| Complaint Pattern | complaint patterns | final severity |
| Returns | returns/sales analysis | final classification |
| Product/Batch | product and batch evidence | final classification |
| Customer Impact | customer impact | final classification |
| Safety | safety evidence | non-safety quality decision |
| CAPA | CAPA actions | final incident classification |
| M365 Guidance | Microsoft guidance | quality decision |

## Tool Boundaries

Supervisor tools:
- incident retrieval/check/update
- CAPA duplicate check
- Word report generation
- Outlook notification

Specialists should use only the data/tools required for their assigned domain.

## Key Governance
- Missing evidence is not Passed.
- Specialists provide evidence; Supervisor makes the final classification.
- Safety has highest decision priority.
- Duplicate investigation/CAPA creation must be prevented.
- M365 guidance cannot alter the quality decision.
