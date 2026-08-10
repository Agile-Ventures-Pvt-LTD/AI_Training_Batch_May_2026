# Known Limitations

## Tenant and Connector
- Microsoft connector availability and permissions may vary by tenant.
- Excel Online, Word Online, and Outlook actions depend on connector access and configuration.
- Published-channel behavior may differ from the development canvas.

## Data
- Results depend on the completeness and correctness of the project dataset.
- Missing evidence must not be interpreted as negative evidence.
- Duplicate detection depends on the available processed/status data.

## Multi-Agent Execution
- Actual parallel runtime behavior must be verified in the deployed/test environment.
- Specialist failures require explicit handling and should not be silently treated as Passed.

## Microsoft Learn MCP
- MCP availability depends on server/tenant configuration.
- Retrieved Microsoft guidance must not override Sleepsia quality evidence.
- If MCP is unavailable, manual review is required.

## Reporting
- Word report generation depends on the Word Online connector.
- Outlook notification depends on mailbox/permission configuration.

## Publishing
- Final Teams/M365 publishing status and agent URL are environment-specific and must be recorded after actual publication.


