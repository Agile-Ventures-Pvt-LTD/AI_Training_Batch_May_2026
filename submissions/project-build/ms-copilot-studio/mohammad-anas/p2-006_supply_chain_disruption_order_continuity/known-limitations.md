# Known Limitations

## Overview

The Supply Chain Disruption Order Continuity solution has been successfully implemented using Microsoft Copilot Studio and Microsoft 365 services. While the solution demonstrates autonomous orchestration, specialist coordination, report generation, stakeholder communication, and lifecycle management, several limitations remain due to platform capabilities, project scope, and the laboratory environment.

These limitations do not prevent the successful execution of the primary business workflow but should be considered before deploying the solution in a production enterprise environment.

---

# Current Implementation Limitations

## 1. Microsoft Excel as Operational Datastore

The solution uses Microsoft Excel Online (Business) as the operational datastore.

Although Excel is suitable for demonstration and laboratory environments, it is not intended for high-volume transactional workloads.

Potential limitations include:

- Limited concurrent updates.
- File locking during simultaneous access.
- Reduced scalability.
- Performance degradation with very large datasets.

A production implementation should replace Excel with Dataverse, SQL Server, or Microsoft Fabric.

---

## 2. Recurrence-Based Processing

Workflow execution depends on a Recurrence Trigger.

Disruption requests are processed only when the scheduled trigger executes.

Real-time event detection is not currently implemented.

Future implementations may use:

- Power Automate Event Triggers
- Microsoft Graph Event Notifications
- Dataverse Triggers
- ERP Event Integration

---

## 3. Single Disruption Processing

Each workflow execution processes only one pending disruption request.

This approach simplifies orchestration and lifecycle management but limits throughput when multiple disruption requests exist simultaneously.

Future enhancements could support controlled batch processing.

---

## 4. Microsoft Word Template Dependency

Report generation depends on Microsoft Word Online (Business).

Changes to the Word template structure or placeholders may require updates to the report generation configuration.

Template version management is not currently automated.

---

## 5. Outlook Notification Dependency

Stakeholder communication depends on Microsoft Outlook.

Notification delivery may fail due to:

- Invalid recipients.
- Mailbox restrictions.
- Connector authentication issues.
- Organizational mail policies.

The current implementation records notification status but does not implement automatic retry logic.

---

## 6. Knowledge Source Coverage

Recovery recommendations rely on the NovaSphere Supply Continuity Policy provided as the project knowledge source.

The solution does not integrate with:

- ERP documentation
- Supplier contracts
- Live procurement systems
- External logistics providers
- Transportation systems

Recommendations are therefore limited to the information available within the configured knowledge source and operational datasets.

---

## 7. Rule-Based Recovery Recommendations

The Recovery Planning Specialist generates recommendations using specialist findings and organizational policy.

The implementation does not perform:

- Predictive analytics
- Demand forecasting
- Machine learning optimisation
- Supply chain simulation
- Risk probability modelling

Future implementations may integrate Azure AI Foundry or Microsoft Fabric AI capabilities.

---

## 8. Manual Approval Simulation

Executive approval routing is represented within the workflow but does not currently integrate with enterprise approval platforms such as:

- Microsoft Teams Approvals
- Power Automate Approval Flows
- ServiceNow
- SAP Workflow
- Oracle Approval Management

Approval decisions remain workflow-based within the current implementation.

---

## 9. Limited Retry Strategy

The Supervisor supports basic retry and Manual Review handling.

Advanced capabilities such as:

- Exponential retry
- Intelligent recovery
- Dynamic workflow compensation
- Automatic rollback

have not been implemented.

---

## 10. Laboratory Dataset

The supplied workbook contains a predefined laboratory dataset.

The implementation has not been validated against:

- Large enterprise datasets
- High-frequency disruption events
- Multi-region operational environments
- Real supplier master data

Performance characteristics therefore reflect laboratory-scale testing.

---

# Microsoft Copilot Studio Limitations

Several implementation decisions were influenced by current Microsoft Copilot Studio capabilities.

These include:

- Limited orchestration visibility during execution.
- Limited debugging for child-agent interactions.
- Topic execution trace limitations.
- Connector response formatting constraints.
- Limited structured variable handling between topics and child agents.

These constraints required additional workflow design considerations during implementation.

---

# Assumptions

The solution assumes:

- Operational Excel tables contain valid data.
- Required Microsoft 365 connectors are authenticated.
- Users have appropriate permissions.
- The Word template remains available.
- Outlook services are operational.
- Knowledge sources remain accessible.
- Required specialist agents are successfully deployed.

---

# Production Recommendations

For enterprise deployment, the following improvements are recommended:

- Replace Excel with Dataverse or SQL Server.
- Implement real-time event-driven triggers.
- Integrate enterprise approval workflows.
- Support batch disruption processing.
- Add predictive supply chain analytics.
- Integrate ERP and procurement platforms.
- Implement advanced monitoring and telemetry.
- Add automated retry and compensation workflows.
- Introduce centralized audit logging.
- Integrate Power BI dashboards for operational reporting.

---

# Conclusion

The implemented solution successfully demonstrates the autonomous orchestration capabilities required by the project while operating within the constraints of Microsoft Copilot Studio and the supplied laboratory environment.

The identified limitations primarily relate to platform scalability, enterprise integration, and advanced governance capabilities rather than the core workflow itself. The current implementation is suitable for academic evaluation, proof-of-concept demonstrations, and functional validation, while future enhancements can extend the solution for production-scale enterprise deployments.