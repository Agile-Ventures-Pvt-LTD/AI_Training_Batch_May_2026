# Architecture

## Logical architecture

```text
Recurrence
   |
   v
Supervisor
   |
   v
Intake & Validation
   |
   v
Mark In Assessment
   |
   +-------------------+-------------------+-------------------+
   |                   |                   |                   |
   v                   v                   v                   v
Budget              Brand               Channel              Asset
Specialist          Specialist          Specialist           Specialist
   |                   |                   |                   |
   +-------------------+-------------------+-------------------+
                           |
                           v
                    Supervisor Fan-In
                           |
                           v
                  Launch Risk & Decision
                           |
              +------------+-------------+
              |            |             |
              v            v             v
            Ready     Remediation      Approval
                         |                |
                         v                v
                   Selective loop   Human approval
                         |                |
                         +-------+--------+
                                 |
                                 v
                       Supervisor Validation
                                 |
                                 v
                    Reporting & Communication
                                 |
                         +-------+-------+
                         |               |
                         v               v
                       Word           Outlook
                         \               /
                          +------v------+
                                 |
                                 v
                           Excel Register
```

## Ownership
| Component | Responsibility |
|---|---|
| Supervisor | Overall orchestration and final readiness |
| Budget Specialist | Financial/commercial assessment |
| Brand Specialist | Brand/content/regulatory assessment |
| Channel Specialist | Channel requirements and readiness |
| Asset Specialist | Asset readiness |
| Risk Specialist | Consolidated risk and proposed outcome |
| Reporting Specialist | Word report and Outlook communication |

## Data flow
Campaign data is retrieved from Excel. Validated campaign information is passed to specialists. Specialist findings are returned to the Supervisor, which performs fan-in and downstream decision logic. Final validated state is persisted to Excel.

## Knowledge
The Marketing Governance Policy is authoritative for readiness statuses, budget approval, timing, asset controls, geography, sensitivity, autonomous-processing rules, and reassessment. Brand & Content Guidelines are authoritative for brand terminology, product naming, claims, evidence requirements, channel-content rules, and brand review classification.
