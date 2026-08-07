# Known Limitations

## Overview

The Autonomous Multi-Agent Supply Chain Disruption & Order Continuity System was developed as a proof-of-concept using Microsoft Copilot Studio, Power Automate, and Microsoft 365 connectors. While the solution demonstrates autonomous multi-agent orchestration and policy-driven decision making, several limitations exist due to project scope, platform capabilities, and the use of simulated business data.

---

# 1. Excel-Based Data Storage

The solution uses Microsoft Excel Online as the primary data source.

### Limitation

Excel is suitable for demonstration purposes but is not designed for high-volume transactional enterprise workloads.

### Impact

- Limited concurrent updates
- Potential record locking
- Reduced scalability for large datasets

### Future Improvement

Replace Excel with enterprise databases such as:

- Microsoft Dataverse
- SQL Server
- Azure SQL Database
- SAP
- Dynamics 365

---

# 2. Static Sample Data

The project operates on a predefined sample dataset.

### Limitation

The system does not consume live operational supply chain data.

### Impact

- Results are limited to available sample records.
- Real-time supply chain events cannot be evaluated.

### Future Improvement

Integrate live ERP systems and operational databases.

---

# 3. Simulated Approval Workflow

Commercial and management approvals are simulated according to project requirements.

### Limitation

Approvals are not routed to actual business users.

### Impact

- No real approval lifecycle.
- No approval history outside the demonstration workflow.

### Future Improvement

Integrate:

- Microsoft Teams Approvals
- Power Automate Approval Actions
- Microsoft Approvals
- Dynamics 365 Approval workflows

---

# 4. External ERP Integration

The current implementation operates independently of enterprise ERP systems.

### Limitation

Systems such as SAP, Oracle ERP, or Dynamics 365 are not connected.

### Impact

The solution cannot automatically:

- Create purchase orders
- Update ERP inventory
- Modify supplier records
- Update production schedules

### Future Improvement

Implement secure ERP connectors and APIs.

---

# 5. Limited Supplier Intelligence

Supplier evaluation relies on structured business data stored in Excel.

### Limitation

Supplier risk is not dynamically calculated.

### Impact

The solution cannot consider:

- Live supplier performance
- Current geopolitical risks
- Financial stability
- Weather disruptions
- Transportation issues

### Future Improvement

Integrate external supplier risk intelligence services.

---

# 6. No Predictive Analytics

The solution evaluates only existing disruptions.

### Limitation

It cannot predict future supply disruptions.

### Impact

Recovery planning begins only after a disruption is reported.

### Future Improvement

Implement predictive AI models using:

- Historical disruption data
- Machine learning
- Demand forecasting
- Supplier performance trends

---

# 7. Manual Knowledge Maintenance

Business policies are maintained manually within the knowledge source.

### Limitation

Policy updates require manual synchronization.

### Impact

Outdated knowledge may affect recommendations if not maintained.

### Future Improvement

Automate synchronization from enterprise policy repositories.

---

# 8. Microsoft 365 Dependency

The solution depends on Microsoft 365 services.

### Limitation

Successful execution requires properly configured connectors and permissions.

### Impact

Workflow execution may fail if:

- Excel connectors are unavailable.
- Outlook permissions are revoked.
- Word connector is inaccessible.

### Future Improvement

Implement connector health monitoring and automated recovery.

---

# 9. Recovery Recommendation Scope

The Recovery Planning Specialist recommends recovery strategies but does not execute operational actions.

### Limitation

The system does not automatically:

- Place purchase orders
- Reallocate warehouse inventory
- Modify customer orders
- Update supplier contracts

### Reason

Business-critical operational actions require human approval and ERP integration.

---

# 10. Human Oversight

Although the workflow is autonomous, certain business decisions require organizational approval.

### Examples

- Commercial approvals
- Executive escalation
- Manual supplier qualification
- Exception handling

These activities remain outside the autonomous scope of the current implementation.

---

# 11. Limited Communication Channels

The project supports Microsoft Outlook for stakeholder notifications.

### Limitation

Other enterprise communication channels are not included.

### Future Improvement

Support additional channels such as:

- Microsoft Teams
- SMS
- ServiceNow
- Slack
- Webhooks

---

# 12. Performance Considerations

The solution executes multiple specialist agents during each disruption assessment.

### Limitation

Execution time depends on:

- Connector response times
- Excel query performance
- Child agent execution
- Power Automate latency

For very large datasets or high request volumes, response times may increase.

---

# 13. Generative AI Variability

The system uses Large Language Models through Microsoft Copilot Studio.

### Limitation

Responses may vary slightly between executions even with identical inputs.

### Mitigation

The solution minimizes variability by:

- Using deterministic Excel data
- Restricting tool access
- Applying structured business rules
- Limiting knowledge sources to policy-driven agents

---

# Summary

Despite these limitations, the solution successfully demonstrates:

- Autonomous multi-agent orchestration
- Hierarchical AI architecture
- Policy-driven decision making
- Parallel specialist assessment
- Recovery planning
- Automated reporting
- Enterprise workflow automation

The current implementation provides a strong foundation that can be extended with enterprise data sources, ERP integrations, predictive analytics, and advanced governance capabilities for production-scale deployment.