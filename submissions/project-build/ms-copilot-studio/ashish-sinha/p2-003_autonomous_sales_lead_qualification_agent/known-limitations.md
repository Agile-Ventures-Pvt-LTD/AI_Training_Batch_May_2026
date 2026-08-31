# Known Limitations

## Document Information

| Item | Details |
|------|---------|
| **Project Name** | NovaWorks Autonomous Sales Lead Qualification Agent |
| **Project ID** | P2-003 |
| **Platform** | Microsoft Copilot Studio |
| **Document Version** | 1.0 |
| **Prepared By** | Ashish Sinha |
| **Last Updated** | 31 July 2026 |

---

# 1. Purpose

This document identifies the known functional, technical, connector, and Microsoft 365 tenant limitations associated with the **NovaWorks Autonomous Sales Lead Qualification Agent**.

The purpose of documenting these limitations is to provide transparency regarding the current implementation, identify operational constraints, and establish expectations for users and reviewers.

---

# 2. Functional Limitations

The current implementation is designed specifically for automated sales lead qualification and therefore has the following functional limitations.

| Limitation | Description |
|------------|-------------|
| Email-based processing only | The agent processes leads received through Outlook email only. |
| Structured workflow | The workflow follows predefined business rules and does not dynamically create new business processes. |
| Single business domain | The solution is designed for sales lead qualification and is not intended for other business workflows. |
| Rule-based qualification | Lead qualification depends on configured business rules rather than predictive AI models. |
| Human review required | Certain scenarios require manual review before processing can continue. |

---

# 3. Connector Limitations

The solution relies on Microsoft 365 connectors available within Microsoft Copilot Studio.

### Excel Online (Business)

Current limitations include:

- Performance depends on workbook size.
- Concurrent updates may cause temporary conflicts.
- Table names and column names must remain unchanged.
- The workbook must remain accessible within OneDrive for Business.

---

### Word Online (Business)

Current limitations include:

- Reports must be generated using a predefined template.
- Placeholder names must remain consistent.
- Template formatting should not be modified after deployment.
- Large or complex templates may increase document generation time.

---

### Office 365 Outlook

Current limitations include:

- Requires an active Outlook connection.
- Depends on Microsoft 365 availability.
- Email delivery is subject to organizational mail policies.
- External delivery restrictions may apply depending on tenant configuration.

---

# 4. Microsoft Copilot Studio Limitations

The current implementation inherits several platform limitations.

| Limitation | Description |
|------------|-------------|
| Connector dependency | The agent depends on configured Microsoft 365 connectors. |
| Environment dependency | The solution runs only within the configured Microsoft environment. |
| Published version | Changes require republishing before becoming available to users. |
| Authentication | Users must authenticate using Microsoft Entra ID. |

---

# 5. Microsoft 365 Tenant Limitations

The agent operates within the organization's Microsoft 365 tenant.

Current constraints include:

- Access is restricted to authorized tenant users.
- Connector permissions are controlled by tenant administrators.
- OneDrive resources must remain accessible.
- Outlook mailbox permissions must remain valid.
- Organizational security policies may restrict connector functionality.

---

# 6. Data Limitations

The operational workbook is the primary data source for the solution.

The implementation assumes:

- Business rules are maintained correctly.
- Product catalog information is accurate.
- Territory mappings are current.
- Sales owner assignments are maintained.

Incorrect or outdated operational data may affect qualification outcomes.

---

# 7. Qualification Logic Limitations

The qualification process uses predefined business rules.

Current limitations include:

- No predictive lead scoring.
- No machine learning model.
- No historical trend analysis.
- No automatic optimization of business rules.
- No adaptive qualification based on previous outcomes.

---

# 8. Report Generation Limitations

The generated qualification report is template-driven.

Current limitations include:

- Reports follow a fixed structure.
- Dynamic layouts are not supported.
- Images and branding must be managed within the template.
- Template modifications require validation before deployment.

---

# 9. Notification Limitations

Email notifications depend on Microsoft Outlook.

Known limitations include:

- Delivery depends on Microsoft Exchange Online availability.
- Organizational spam filters may affect delivery.
- Notification failures caused by external mail systems are outside the agent's control.

---

# 10. Error Handling Limitations

The solution includes basic exception handling.

However:

- Unexpected connector outages require manual intervention.
- Workbook corruption cannot be automatically repaired.
- Invalid connector configurations must be corrected by an administrator.
- Authentication failures require reconnection of Microsoft 365 services.

---

# 11. Security Considerations

The solution intentionally avoids storing confidential information within the agent.

Current security constraints include:

- No secrets stored in instructions.
- No embedded API keys.
- No customer credentials retained.
- Authentication managed through Microsoft Entra ID.
- Access controlled using Microsoft 365 permissions.

---

# 12. Assumptions

The implementation assumes:

- Microsoft 365 services are available.
- Outlook mailbox is correctly configured.
- OneDrive for Business remains accessible.
- Operational workbook structure is unchanged.
- Word template is available.
- Connector permissions remain valid.

Failure to meet these assumptions may impact agent execution.

---

# 13. Operational Risks

Potential operational risks include:

| Risk | Impact |
|------|--------|
| Connector authentication expires | Agent cannot execute actions. |
| Excel workbook modified | Tool execution may fail. |
| Word template deleted | Report generation fails. |
| Outlook mailbox unavailable | Trigger cannot activate. |
| OneDrive storage unavailable | Reports cannot be generated or stored. |

---

# 14. Mitigation Strategies

The following practices help reduce operational risks:

- Maintain connector authentication.
- Restrict changes to the operational workbook.
- Version-control report templates.
- Validate connector configurations after updates.
- Periodically test end-to-end execution.
- Monitor agent execution after publishing.

---

# 15. Conclusion

The NovaWorks Autonomous Sales Lead Qualification Agent is designed to operate reliably within the Microsoft 365 ecosystem using Microsoft Copilot Studio and standard Microsoft connectors.

The limitations described in this document are primarily related to platform capabilities, connector dependencies, and organizational configuration rather than defects in the solution itself. Understanding these constraints helps ensure proper deployment, maintenance, and operational use of the agent.

