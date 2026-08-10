# Known Limitations

## 1. Data Dependency

The solution depends on the configured Excel tables and their available records. Missing, incomplete, or inconsistent data can affect investigation results.

## 2. Connector Dependency

Excel, Word, and Outlook actions depend on configured Microsoft 365 connectors, permissions, and successful connector execution.

## 3. Evidence Limitation

The agents can only assess evidence available through the configured knowledge sources, tables, and specialist tools. Missing evidence may result in an insufficient-evidence outcome.

## 4. Decision Limitation

Final classification is based on the decision logic configured in Copilot Studio and the information returned by specialist agents. Unexpected or incomplete inputs may require fallback handling.

## 5. CAPA Limitation

CAPA creation depends on valid owner information, required incident/classification data, and successful CAPA_Register updates.

## 6. Reporting Limitation

The Word report depends on successful execution of the configured report-generation tool and availability of the required investigation information.

## 7. Notification Limitation

Outlook notifications depend on valid recipient information and successful execution of the Outlook connector.

## 8. Environment and Permission Limitation

Tool execution can be affected by tenant configuration, connector permissions, authentication, environment settings, and publishing status.

## 9. MCP Limitation

Microsoft Learn MCP guidance depends on the availability and response of the configured MCP server.

## 10. Human Oversight

Critical quality, safety, escalation, and corrective-action decisions should remain subject to appropriate human review and approval according to organizational policy.