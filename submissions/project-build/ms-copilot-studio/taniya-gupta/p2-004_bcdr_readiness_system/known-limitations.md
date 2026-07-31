# Known Limitations & Platform Boundaries (`known-limitations.md`)

## System Limitations

1. **Connector Throttling**: Heavy concurrent assessments may experience API rate limits from Power Platform connectors (Excel/Outlook).
2. **MCP Regional Latency**: Calls to `https://learn.microsoft.com/api/mcp` rely on external network availability.
3. **Synthetic Domain Addressing**: External `.example` email domains are automatically routed to active tenant test accounts to prevent delivery failure.

---
