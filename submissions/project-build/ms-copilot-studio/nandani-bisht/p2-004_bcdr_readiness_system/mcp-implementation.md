# MCP Implementation

## Overview

The **Technical Recovery Specialist** integrates with the **Microsoft Learn Model Context Protocol (MCP) Server** to retrieve official Microsoft documentation related to Business Continuity and Disaster Recovery (BC/DR).

Rather than relying solely on the language model's internal knowledge, the specialist retrieves Microsoft Learn documentation at runtime and uses the retrieved information as supporting evidence for technical recovery recommendations.

This approach ensures that recovery assessments are aligned with Microsoft's published best practices and architecture guidance.

---

# MCP Server Information

| Item | Value |
|------|-------|
| MCP Server Name | Microsoft Learn MCP |
| Purpose | Retrieve official Microsoft technical documentation |
| Endpoint | https://learn.microsoft.com/api/mcp |
| Transport Type | Streamable HTTP |
| Authentication | Public / Unauthenticated |

---

# Purpose of MCP

The Microsoft Learn MCP server enables the Technical Recovery Specialist to retrieve current Microsoft guidance related to:

- Azure Backup
- Azure Site Recovery
- Disaster Recovery
- Business Continuity
- Azure SQL Recovery
- Azure Virtual Machines
- High Availability
- Recovery Best Practices
- Infrastructure Resilience

Using MCP allows recommendations to be supported by official Microsoft documentation rather than relying only on general AI knowledge.

---

# Specialist Agent Using MCP

The MCP server is attached to the:

**Technical Recovery Specialist**

The specialist is responsible for:

- Searching Microsoft documentation
- Retrieving relevant recovery guidance
- Evaluating technical recovery configurations
- Returning evidence-based findings to the Supervisor Agent

---

# MCP Configuration

The MCP server was manually configured in Microsoft Copilot Studio.

Configuration used:

| Property | Value |
|----------|-------|
| Server Name | Microsoft Learn MCP |
| Endpoint | https://learn.microsoft.com/api/mcp |
| Transport | Streamable HTTP |
| Authentication | None (Public Endpoint) |

No credentials, API keys, secrets, or tenant-specific information are required for the Microsoft Learn MCP endpoint.

---

# Copilot Studio Configuration Steps

The following steps were used to configure the MCP server:

1. Open Microsoft Copilot Studio.
2. Navigate to the Technical Recovery Specialist agent.
3. Open **Tools**.
4. Select **Add Tool**.
5. Choose **Model Context Protocol (MCP)**.
6. Enter the endpoint:

```
https://learn.microsoft.com/api/mcp
```

7. Select:

- Transport: **Streamable HTTP**
- Authentication: **Unauthenticated**

8. Save the configuration.
9. Verify that the MCP tools are successfully discovered.
10. Publish the agent.

---

# Tools Discovered

After connecting to the Microsoft Learn MCP server, Copilot Studio discovers the available tools exposed by the server.

Typical tool capabilities include:

- Search Microsoft Learn documentation
- Retrieve documentation pages
- Find Azure recovery guidance
- Retrieve architecture references
- Query Microsoft technical content

> **Note:** The exact list of discovered tools may vary depending on the MCP server version and the Copilot Studio environment.

---

# Tools Invoked

During BC/DR assessments, the Technical Recovery Specialist invokes MCP tools to retrieve Microsoft documentation related to:

- Azure Backup
- Azure Site Recovery
- Recovery planning
- SQL disaster recovery
- Azure Virtual Machine recovery
- Business continuity guidance

The retrieved documentation is incorporated into the technical assessment before being returned to the Supervisor Agent.

---

# Example Technical Scenario

### Scenario

Application:

Customer Commerce Portal

Infrastructure:

- Azure Virtual Machines
- Azure SQL Database

Question:

> What Microsoft guidance is available for protecting Azure Virtual Machines and Azure SQL Database as part of a disaster recovery strategy?

The Technical Recovery Specialist sends the request to the Microsoft Learn MCP server and retrieves the relevant Microsoft documentation.

The findings are then included in the final BC/DR assessment.

---

# Retrieved Microsoft Documentation

Examples of Microsoft documentation that may be retrieved include:

- Azure Backup documentation
- Azure Site Recovery documentation
- Azure SQL disaster recovery guidance
- High availability architecture
- Business continuity planning guidance

These references are used to support technical recommendations made during the assessment.

---

# MCP Evidence in Assessment

The Technical Recovery Specialist includes Microsoft-derived evidence within the assessment report where applicable.

Example:

- Microsoft recommends enabling Azure Site Recovery for critical virtual machines.
- Azure Backup should be configured with appropriate retention policies.
- Recovery testing should be performed regularly.

These recommendations are based on information retrieved through the MCP server.

---

# Failure Handling

If the MCP server is unavailable because of network, tenant, or policy restrictions:

1. Record the MCP failure.
2. Continue the assessment using available application data.
3. Clearly indicate that Microsoft documentation could not be retrieved.
4. Do **not** fabricate Microsoft evidence.
5. Recommend manual verification against Microsoft Learn.

This approach complies with the project requirements and maintains assessment integrity.

---

# Known Limitations

Current limitations include:

- MCP availability depends on network connectivity.
- Retrieved documentation depends on Microsoft Learn availability.
- Search quality depends on the query provided.
- Documentation availability may change over time.
- MCP cannot replace organization-specific recovery procedures.

---

# Security Considerations

- No credentials are stored in the solution.
- No tenant-sensitive information is exposed.
- The Microsoft Learn MCP endpoint is publicly accessible.
- Retrieved documentation is limited to publicly available Microsoft Learn content.

---

# Screenshot References

The repository includes the following screenshots related to MCP implementation:

- `mcp-configuration.png`
- `mcp-tools.png`
- `mcp-successful-call.png`

These screenshots demonstrate:

- MCP server configuration
- Tool discovery
- Successful documentation retrieval

---

# Evaluation Mapping

| Evaluation Criterion | Implementation |
|----------------------|----------------|
| MCP configured manually | ✔ |
| Correct Microsoft Learn endpoint | ✔ |
| Attached to Technical Recovery Specialist | ✔ |
| Documentation retrieval | ✔ |
| Technical assessment uses MCP evidence | ✔ |
| Failure handling documented | ✔ |

---

# Conclusion

The Microsoft Learn MCP integration enables the Technical Recovery Specialist to retrieve authoritative Microsoft documentation during BC/DR assessments. By incorporating evidence-based technical guidance into the assessment workflow, the solution improves the quality, consistency, and reliability of recovery recommendations while aligning with Microsoft Copilot Studio best practices.