# Known Limitations

## Overview

The NovaSphere BC/DR Readiness System is designed to automate BC/DR assessments using Microsoft Copilot Studio. The following limitations apply to the current implementation.

---

## 1. Dependency on Input Data Quality

The accuracy of assessment results depends on the completeness and correctness of:

- Application inventory data.
- Recovery information.
- Ownership details.
- Technical configuration details.

Missing or incorrect information may result in an **Insufficient Evidence** classification.

---

## 2. MCP Availability Dependency

The Technical Recovery Specialist depends on the Microsoft Learn MCP Server for technical guidance.

If MCP is unavailable:

- Technical evidence cannot be retrieved.
- The system does not generate unsupported Microsoft recommendations.
- Manual technical review may be required.

---

## 3. Synthetic Data Usage

The system uses synthetic BC/DR application data for assessment and testing purposes.

Production deployment would require integration with actual enterprise application inventories and recovery systems.

---

## 4. AI-Based Assessment Limitations

Specialist agents provide analysis and recommendations based on available information.

Final decisions should be reviewed by responsible BC/DR stakeholders before implementation.

---

## 5. No Automatic Remediation Execution

The Remediation Planning Specialist generates recommended actions only.

The system does not:

- Apply configuration changes.
- Modify Azure resources.
- Execute recovery procedures.

---

## 6. External System Integration Limitations

The current implementation uses Copilot Studio tools and configured integrations.

Additional enterprise integrations may be required for:

- CMDB systems.
- Monitoring platforms.
- Ticketing systems.
- Real-time infrastructure validation.

---

## 7. Notification Limitations

Outlook notifications are generated based on the final Supervisor-approved readiness classification.

Additional approval workflows may be required for production environments with strict communication policies.