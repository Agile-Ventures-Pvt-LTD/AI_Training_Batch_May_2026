
# Known Limitations

# Overview

This document describes the current implementation limitations of the Autonomous Supply Chain Disruption & Order Continuity Response System. These limitations primarily arise from Microsoft Copilot Studio platform capabilities, the simplified implementation approach adopted for this project, and the scope defined for the solution.

Understanding these limitations helps distinguish between the current implementation and potential enterprise-scale enhancements.

---

# Platform Limitations

## 1. Sequential Child Agent Execution

### Current Implementation

The Supervisor invokes specialist child agents sequentially.

```
Supervisor
      │
      ▼
Inventory
      │
      ▼
Alternate Supplier
      │
      ▼
Customer
      │
      ▼
Commercial
```

### Ideal Enterprise Implementation

The four specialist agents would execute in parallel (Fan-Out) and return their outputs simultaneously (Fan-In).

### Reason

Microsoft Copilot Studio topics currently execute sequentially, therefore logical parallel execution is represented through sequential orchestration.

---

## 2. Limited Parallel Processing

The platform does not currently support native parallel execution of child agents within a single orchestration flow.

Impact:

- Slightly longer execution time
- Simplified orchestration design

---

## 3. Approval Workflow Simplification

The current implementation models approval as part of the orchestration logic.

Future enhancement:

- Microsoft Teams Approvals
- Power Automate Approval Flows
- Adaptive Cards

---

## 4. Excel as Operational Database

Operational data is stored in Microsoft Excel Online.

Suitable for:

- Demonstrations
- Proof of Concept
- Academic implementation

Enterprise recommendation:

- Microsoft Dataverse
- Azure SQL Database
- Microsoft Fabric
- SAP Integration

---

# AI Limitations

## Knowledge Scope

Only the Supervisor Agent contains the NovaSphere Supply Continuity Policy knowledge base.

Specialist agents rely entirely on structured operational data.

Reason:

Centralized policy interpretation improves consistency and simplifies maintenance.

---

## Deterministic Business Rules

The solution intentionally limits autonomous decision-making.

The AI does not:

- Approve suppliers
- Create purchase orders
- Cancel customer orders
- Commit delivery dates
- Override organizational policy

All recommendations remain subject to business governance.

---

# Data Limitations

## Static Dataset

The implementation uses a predefined Excel workbook.

Limitations:

- No live ERP integration
- No SAP connectivity
- No Dynamics 365 integration
- No real-time supplier feeds

---

## Dataset Size

The workbook is intended for demonstration purposes.

Large-scale production datasets may require:

- Database indexing
- Pagination
- API-based retrieval
- Optimized data pipelines

---

# Reporting Limitations

Reports are generated as Microsoft Word documents.

Future enhancements could include:

- PDF generation
- Power BI dashboards
- Executive scorecards
- SharePoint document management

---

# Notification Limitations

Notifications are sent using Outlook.

Current implementation does not include:

- Microsoft Teams messages
- SMS notifications
- Push notifications
- Mobile alerts

---

# Monitoring Limitations

The implementation provides basic workflow monitoring.

Future improvements:

- Application Insights
- Azure Monitor
- Log Analytics
- Operational dashboards

---

# Security Considerations

The solution assumes authenticated Microsoft 365 access.

Not implemented:

- Role-Based Access Control (RBAC)
- Conditional Access Policies
- Azure Key Vault integration
- Managed Identities

These features should be considered for enterprise deployments.

---

# Scalability Considerations

Current implementation is optimized for:

- Demonstration environments
- Small to medium datasets
- Academic evaluation

Enterprise deployments may require:

- Dataverse
- Azure Functions
- Azure Service Bus
- Event-driven architecture
- Distributed orchestration

---

# Future Enhancements

Potential improvements include:

- Native parallel child-agent execution
- Real-time ERP integration
- Teams approval workflows
- Power BI reporting
- Live supplier APIs
- Predictive disruption analytics
- Machine learning–based recovery recommendations
- Azure OpenAI integration for advanced reasoning
- Enterprise monitoring and telemetry

---

# Summary

The current implementation fulfills the functional objectives of the PRD while remaining within the capabilities of Microsoft Copilot Studio and Microsoft 365. The documented limitations primarily reflect platform constraints and implementation scope rather than design shortcomings. The modular architecture enables future enhancements with minimal changes to the overall orchestration design.
