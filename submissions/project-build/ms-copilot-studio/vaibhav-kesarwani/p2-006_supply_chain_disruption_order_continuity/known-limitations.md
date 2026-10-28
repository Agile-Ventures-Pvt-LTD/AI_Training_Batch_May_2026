# Known limitations

## NovaSphere supply continuity autonomous multi-agent system

### Current system limitations

| Area                 | Limitation                                               | Impact                                                  |
| -------------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| Data source          | Uses Excel Online as the operational database            | Limited scalability and concurrent access               |
| Trigger              | Recurrence-based polling                                 | Not real-time event driven                              |
| Processing           | One disruption processed per execution cycle             | High-volume disruptions may create queue delays         |
| Inventory            | ATP calculated from available Excel data only            | No real-time ERP inventory synchronization              |
| Supplier data        | Alternate supplier capacity is static                    | Dynamic supplier capacity changes require reassessment  |
| Customer data        | Revenue and priority depend on Excel records             | External CRM changes are not automatically synchronized |
| Commercial rules     | Fixed approval thresholds (15% and 10%)                  | Thresholds require manual policy updates                |
| Approval workflow    | Approval routing is identified but not fully interactive | External approval portal integration required           |
| Reporting            | Word report generation uses predefined templates         | Limited report customization                            |
| Notifications        | Outlook email notifications only                         | No Teams, SMS, or mobile push notifications             |
| Reassessment         | Maximum two automated reassessment cycles                | Complex disruptions require manual intervention         |
| Integration          | No direct SAP, Dynamics 365, or ERP integration          | Operational data must be synchronized separately        |
| Concurrency          | Single execution concurrency recommended                 | Parallel disruption processing is limited               |
| Predictive analytics | No disruption forecasting or demand prediction           | Reactive rather than predictive recovery planning       |
| Transportation       | Logistics rerouting is not optimized                     | Transportation constraints are evaluated manually       |

## Copilot Studio limitations

| Limitation                                  | Mitigation                                        |
| ------------------------------------------- | ------------------------------------------------- |
| Limited long-running workflow orchestration | Use Power Automate for asynchronous operations    |
| Complex document generation                 | Use Word Online (Business) through Power Automate |
| External approval tracking                  | Integrate with Power Automate approvals           |
| Advanced transaction management             | Use Dataverse or SQL Server in future versions    |
| Large-scale data processing                 | Migrate operational data from Excel to Dataverse  |

## Future enhancements

| Enhancement                 | Expected improvement                     |
| --------------------------- | ---------------------------------------- |
| Dataverse migration         | Better scalability and concurrency       |
| SharePoint integration      | Centralized document management          |
| SAP integration             | Real-time procurement and inventory data |
| Dynamics 365 integration    | Customer and operational synchronization |
| Azure Event Grid            | Real-time disruption detection           |
| Predictive analytics        | Proactive disruption prevention          |
| Transportation optimization | Automated logistics recovery             |
| Teams integration           | Faster stakeholder collaboration         |
| Interactive approval portal | End-to-end approval automation           |

## Overall assessment

The current implementation is suitable for **prototype, demonstration, and controlled enterprise deployment**. The primary limitations are related to **Excel scalability, real-time integration, and external approval automation**, while the core **multi-agent orchestration, deterministic decision engine, approval governance, and reporting workflow** remain fully aligned with the PRD.
