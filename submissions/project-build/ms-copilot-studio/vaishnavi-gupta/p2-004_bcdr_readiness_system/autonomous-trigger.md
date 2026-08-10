# Autonomous Trigger Design

## Overview

The Autonomous Trigger enables the BC/DR Readiness Assessment System to operate without manual user interaction. The solution uses a **When a file is modified** that monitors the folder containing the BC/DR assessment workbook. Whenever the workbook is updated, the trigger automatically starts the Supervisor Agent.

---

## Trigger Type

**When a file is modified**

The trigger monitors the designated OneDrive or SharePoint folder. Any saved modification to the assessment workbook initiates the assessment workflow.

---

## Trigger Workflow

1. A change is detected in the monitored folder.
2. The File Modified Trigger is activated.
3. The BC/DR Supervisor Agent starts automatically.
4. The Supervisor retrieves pending assessment requests.
5. Application details are read from the Excel workbook.
6. Specialist agents perform their respective assessments.
7. The Supervisor consolidates all findings.
8. The Reporting & Communication Specialist generates the assessment report.
9. The Assessment Register is updated.
10. Outlook notifications are sent to the relevant stakeholders.

---

## Trigger Input

- Modified BC/DR assessment workbook
- Assessment requests
- Application inventory data

---

## Trigger Output

- Autonomous execution of the BC/DR assessment workflow
- Updated Assessment Register
- Generated BC/DR Readiness Assessment Report
- Stakeholder notification

---

## Design Considerations

- No manual chat interaction is required.
- The trigger starts the assessment automatically after a file modification.
- The Supervisor Agent validates available assessment requests before processing.
- If no pending requests are found, the workflow ends without generating reports or notifications.
- The trigger only initiates the workflow; all assessment logic is handled by the Supervisor Agent and specialist agents.

---

## Benefits

- Fully automated assessment initiation.
- Reduces manual effort.
- Supports continuous monitoring of assessment requests.
- Ensures consistent and repeatable execution of the BC/DR readiness assessment process.