# ⚠️ Known Limitations

> **P2-004 | NovaSphere BC/DR Readiness System**

---

# 🎯 Purpose

This document identifies the current limitations of the NovaSphere BC/DR Readiness System at the time of submission.

The solution demonstrates a complete autonomous multi-agent architecture using Microsoft Copilot Studio. The limitations listed below primarily relate to implementation maturity and platform capabilities rather than architectural design.

---

# 📋 Summary

| ID | Limitation | Impact | Status |
|----|------------|--------|--------|
| LIM-001 | Word report generation requires additional refinement | Medium | Open |
| LIM-002 | Outlook email workflow not fully validated end-to-end | Low | Open |
| LIM-003 | OneDrive trigger operates at file level | Low | Platform Limitation |
| LIM-004 | Assessment data stored in Excel | Medium | Enhancement Opportunity |
| LIM-005 | Microsoft Learn MCP availability depends on service connectivity | Low | External Dependency |

---

# 📝 LIM-001 — Word Report Generation

## Description

The Reporting & Communication Specialist includes a Microsoft Word connector for report generation. During implementation, the report generation workflow reached the reporting stage, but the generated document workflow requires further refinement before production deployment.

## Impact

- Assessment execution is not blocked.
- Assessment findings remain available through the Supervisor Agent.
- Report automation can be enhanced in a future iteration.

## Recommendation

Evaluate alternative Word Online actions or a template-based reporting approach compatible with the target Microsoft 365 environment.

---

# 📧 LIM-002 — Outlook Notification Validation

## Description

The Outlook connector has been configured within the Reporting & Communication Specialist. However, complete end-to-end validation of email delivery was not completed because it depends on the successful completion of the report generation workflow.

## Impact

- Notification preparation is available.
- Final production validation is still required.

## Recommendation

Perform end-to-end validation in a Microsoft 365 environment after finalizing the report generation workflow.

---

# 📂 LIM-003 — File-Level Trigger

## Description

The autonomous trigger monitors modifications to the assessment workbook stored in OneDrive.

Current implementation:

```
When a file is modified
```

The trigger activates whenever the monitored workbook changes.

## Impact

Updates unrelated to assessment requests may also activate the workflow. The Supervisor validates the data before continuing, preventing incorrect assessments.

## Recommendation

For enterprise deployments, consider event sources that support row-level changes, such as Microsoft Dataverse.

---

# 📊 LIM-004 — Excel as Operational Data Store

## Description

Assessment Requests, Application Inventory, and Assessment Register are maintained in Excel Online.

## Impact

Excel is appropriate for demonstrations and small-scale deployments but is less suitable for environments with high transaction volumes or concurrent updates.

## Recommendation

Migrate operational data to Microsoft Dataverse or SQL Server for larger enterprise implementations.

---

# 🌐 LIM-005 — External MCP Dependency

## Description

The Technical Recovery Specialist relies on Microsoft Learn MCP to retrieve current Microsoft documentation.

## Impact

If the external service is temporarily unavailable, live documentation cannot be retrieved.

The Supervisor continues the assessment using the available information and records that Microsoft guidance was unavailable.

## Recommendation

Continue using graceful error handling and monitor service availability in production.

---

# 🔒 Security Considerations

The current implementation:

- Uses Microsoft 365 authentication.
- Restricts access through Copilot Studio and Microsoft connectors.
- Does not modify Azure resources.
- Retrieves Microsoft documentation in a read-only manner through MCP.

No security issues were identified during functional testing.

---

# 🚀 Future Enhancements

Potential improvements include:

- Dataverse-based assessment storage
- Row-level event triggers
- Enhanced Word report formatting
- Full Outlook workflow validation
- Integration with Azure Resource Graph
- Azure Advisor recommendations
- Azure Monitor insights
- Power BI reporting dashboards
- Historical assessment analytics

---

# 📈 Overall Assessment

Despite the identified limitations, the solution successfully demonstrates:

- ✅ Supervisor–Specialist Multi-Agent Architecture
- ✅ Microsoft Learn MCP Integration
- ✅ Excel Online Integration
- ✅ Organizational Knowledge Base
- ✅ Autonomous Trigger
- ✅ Assessment Register Management
- ✅ Risk Assessment Workflow
- ✅ Remediation Planning
- ✅ End-to-End BC/DR Assessment Orchestration

The remaining limitations are implementation refinements and do not affect the overall architectural approach or the demonstration of the required capabilities.

---

# 🏁 Conclusion

The NovaSphere BC/DR Readiness System meets the primary objectives of the project by delivering an autonomous, multi-agent BC/DR assessment platform within Microsoft Copilot Studio.

The identified limitations represent opportunities for future enhancement rather than fundamental design issues, providing a clear roadmap toward a production-ready enterprise solution.