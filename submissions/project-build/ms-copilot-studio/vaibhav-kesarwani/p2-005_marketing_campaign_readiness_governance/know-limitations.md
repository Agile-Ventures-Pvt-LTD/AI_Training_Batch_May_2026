# Known limitations

## Current implementation limitations

| Area                       | Limitation                                         | Impact                                                |
| -------------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| Excel storage              | Uses Excel Online as the operational data store    | Limited scalability and concurrent write performance  |
| Single-campaign processing | Processes one pending campaign per trigger cycle   | Lower throughput for high campaign volumes            |
| Trigger scheduling         | Depends on recurrence intervals                    | Assessment may not start immediately after submission |
| Approval workflow          | Human approvals are simulated through data updates | No native approval tracking within the agent          |
| Knowledge sources          | Governance knowledge is document-based             | Updates require manual knowledge refresh              |
| Reporting                  | Generates Microsoft Word reports only              | No PDF or dashboard reporting                         |
| Notifications              | Uses Outlook email notifications                   | No Teams or SMS integration                           |
| Reassessment               | Maximum of two automated reassessment cycles       | Complex cases require manual review                   |
| Risk model                 | Rule-based governance evaluation                   | Does not use historical predictive analytics          |
| Monitoring                 | Basic execution monitoring                         | No advanced operational dashboard                     |
| Audit history              | Limited historical assessment tracking             | Full audit trail not implemented                      |
| Concurrency                | Duplicate prevention is state-based                | Not optimized for distributed parallel processing     |
| Performance                | Connector latency may affect execution time        | Large datasets may increase processing duration       |
| Integrations               | Limited to Microsoft 365 services                  | No CRM, ERP, or marketing platform integration        |


## Conclusion

The current implementation focuses on demonstrating the required **multi-agent orchestration architecture, governance decision logic, selective reassessment, and autonomous campaign readiness assessment**. The identified limitations primarily affect scalability, enterprise integrations, and operational monitoring rather than the correctness of the governance workflow.
