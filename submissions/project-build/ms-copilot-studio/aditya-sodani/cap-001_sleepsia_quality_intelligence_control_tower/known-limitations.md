# Known Limitations

## 1. Tenant Limitations

- Copilot Studio functionality depends on the Microsoft 365 / Power Platform tenant configuration.
- Availability of Teams, Word, Outlook, Excel and MCP capabilities may depend on tenant permissions and administrator policies.
- Publishing and channel availability may vary according to tenant configuration.
- Some connectors or capabilities may require administrator approval or additional permissions.

## 2. Connector Limitations

### Excel

- Excel-based operations depend on the workbook being available through the configured Microsoft 365 connection.
- Table structure, column names and permissions must remain consistent for reliable tool execution.
- Changes to workbook schema may require corresponding tool or topic updates.

### Word

- Word report generation depends on the configured Word Online (Business) connector and document/template configuration.
- Report generation may fail if the template, connection or required permissions are unavailable.
- A Word connector failure does not change the underlying quality decision.

### Outlook

- Outlook notifications depend on a valid Office 365 Outlook connection and recipient information.
- Notification delivery can fail because of connector, permission or mailbox issues.
- An Outlook failure must not invalidate an already completed quality decision or CAPA record.

## 3. MCP Limitations

- Microsoft Learn MCP is used for M365/Copilot Studio guidance and is not a dependency for core quality classification.
- MCP availability depends on the configured MCP connection and tenant/network access.
- If MCP is unavailable, the M365 Guidance Specialist returns a manual-review/unavailable-guidance response.
- MCP failure must not affect quality severity, classification or CAPA decisions.

## 4. Data Limitations

- The solution depends on the accuracy and completeness of operational Excel data.
- Missing SKU, BatchID, complaint, return, incident or CAPA evidence can limit automated decision-making.
- The agent must not invent missing operational evidence.
- Missing required evidence may result in an `Insufficient Evidence` classification or manual handling.

## 5. Reassessment Limitation

- Automatic selective reassessment is limited to two reassessment cycles.
- When `ReassessmentCount > 2`, the case is routed to Manual Review.
- Unaffected specialist findings are preserved during selective reassessment.

## 6. Automation Limitations

- Specialist findings depend on the availability and successful execution of their configured tools and data sources.
- Tool failures may require manual intervention.
- The Supervisor remains responsible for the final quality classification and does not delegate final decision authority to individual specialists.

## 7. Mitigation

Where tenant, connector, MCP or data limitations prevent automated execution, the case should be surfaced for manual review rather than producing an unsupported or fabricated result.