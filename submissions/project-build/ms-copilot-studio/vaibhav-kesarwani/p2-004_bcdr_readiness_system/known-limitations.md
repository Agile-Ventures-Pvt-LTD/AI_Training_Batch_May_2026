# Known limitations

## P2-004 Autonomous Multi-Agent BC/DR Readiness System

The current implementation has the following limitations:

* The system depends on the accuracy and completeness of the Excel application inventory.
* The Technical Recovery Specialist cannot directly inspect Azure resources and relies on available operational data and Microsoft Learn MCP documentation.
* Microsoft Learn MCP availability depends on network connectivity and Microsoft service availability.
* Child agents do not maintain long-term memory across assessments.
* The system generates remediation recommendations but does not implement Azure or infrastructure changes.
* Report generation and notifications depend on Microsoft 365 connector availability.
* High-risk assessments and unresolved evidence limitations require human review and approval.

These limitations are intentional to ensure evidence-based assessments, governance compliance, and safe autonomous operation within Microsoft Copilot Studio.
