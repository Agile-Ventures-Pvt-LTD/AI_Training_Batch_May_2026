# Known limitations

## Sleepsia product quality & customer experience intelligence control tower

This project is fully functional and deployed in **Microsoft 365 Copilot** and **Microsoft Teams**, but there are a few practical limitations that I identified during development and testing.

## Current limitations

### Excel-based data source

The system currently uses **Excel Online (Business)** as the primary data source. This works well for the capstone project, but it is not ideal for large-scale production environments with high transaction volumes.

### CAPA workflow

The CAPA plan is generated automatically, but the implementation does not include a complete approval workflow, reminder system, or escalation tracking for overdue CAPA actions.

### Report generation

The investigation report is generated in a form of Word Documents. Advanced report customization, dashboards, and analytics are not included in the current implementation.

### MCP dependency

The M365 Guidance Specialist depends on **Microsoft Learn MCP** for Microsoft documentation. If the MCP service is unavailable, the agent cannot retrieve the latest Microsoft guidance.

### Manual review

The system escalates unresolved cases to **Manual Review** after the reassessment limit is reached. The manual investigation process itself is outside the scope of this project.

## Future improvements

Some improvements I would consider in a future version include:

* migrating data from Excel to Dataverse or SQL,
* adding predictive quality analytics,
* implementing automated CAPA reminders,
* creating Power BI dashboards,
* adding audit logs and approval workflows,
* improving trend analysis and forecasting,
* integrating supplier and manufacturing systems.

These limitations do not affect the core objective of the project, which is to demonstrate a **Microsoft Copilot Studio multi-agent quality investigation system with hierarchical orchestration, child agents, Microsoft 365 integration, and autonomous quality decision support**.
