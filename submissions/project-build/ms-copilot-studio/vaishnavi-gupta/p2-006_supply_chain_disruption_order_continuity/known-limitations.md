# Known Limitations

## Scope Limitations
- Designed and tested using a small synthetic dataset.
- Processes only one pending disruption per trigger execution.
- Not optimized for large-scale enterprise workloads.

## Platform Limitations
- Fully dependent on Microsoft Copilot Studio capabilities.
- Requires Excel Online (Business), Outlook, and Word connector availability.
- Functionality may vary based on licensing and environment configuration. 【1-b810d8】

## Data Limitations
- Recommendations are only as accurate as the source data.
- Uses Excel tables instead of enterprise databases.
- Does not validate real-time supplier or inventory information. 【1-b810d8】

## Automation Limitations
The system cannot autonomously:
- Place purchase orders
- Approve suppliers
- Cancel customer orders
- Commit customer delivery dates
- Authorize commercial spending

Human approval is required for governed business decisions. 【1-b810d8】

## Approval Limitations
- Approvals must be provided by authorized stakeholders.
- The system never assumes or fabricates approvals.
- Workflows pause when approval is required. 【1-b810d8】

## Reassessment Limitations
- Maximum automated reassessment cycles: **2**
- Unresolved cases are routed to **Manual Review**. 【1-b810d8】

## Failure Handling Limitations
- Specialist assessments are retried only once.
- Connector failures (Excel, Outlook, Word) may interrupt processing.
- Unsupported recommendations are blocked when evidence is insufficient. 【1-b810d8】

## Testing Limitations
- Tested using synthetic project data.
- Not validated for production-scale volumes or real-world ERP integrations.
- Additional testing would be required before enterprise deployment. 【1-b810d8】