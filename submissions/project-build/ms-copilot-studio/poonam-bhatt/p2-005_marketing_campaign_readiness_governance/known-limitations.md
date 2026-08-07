# Known Limitations & Mitigations

During system implementation and stress testing, the following technical limitations were identified:

## 1. Microsoft Word Online Connector Latency
*   **Limitation:** Generating the Word Campaign Readiness Report can take up to 25-35 seconds depending on Power Platform connector load.
*   **Mitigation:** The Supervisor topic displays a warning message to the stakeholder to wait, and handles the flow asynchronously to prevent session timeouts.

## 2. OneDrive Excel Data Syncing Delays
*   **Limitation:** When updating campaign statuses in Excel sheets, there can be a 1-2 second sync lag before other systems see the changes.
*   **Mitigation:** A deterministic status locking mechanism is implemented. The campaign is immediately marked as `In Assessment` upon intake to prevent duplicate triggering before specialist analysis starts.

## 3. Premium Licensing Constraints
*   **Limitation:** Word Online (Business) and Outlook Office 365 connectors are Premium connectors in Microsoft Copilot Studio.
*   **Mitigation:** The system user guide outlines the licensing requirements and suggests using standard SharePoint integration if budget limits exist.

## 4. Reassessment Loop Bound Limit
*   **Limitation:** The selective reassessment loop is capped at a maximum of 2 automated cycles to prevent infinite looping when users upload repeatedly invalid assets.
*   **Mitigation:** Campaigns exceeding this limit are escalated to `Manual Review` status, alerting the Campaign Owner to coordinate remediation manually.

## 5. API Throttle Limits
*   **Limitation:** Excel connector actions are subject to Power Platform request throttle limits.
*   **Mitigation:** The recurrence trigger is configured to poll at a reasonable interval (e.g. hourly) and only processes a single campaign per trigger execution.
