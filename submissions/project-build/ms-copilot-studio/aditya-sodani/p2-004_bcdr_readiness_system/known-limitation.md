# Known Limitations

## 1. Microsoft Learn MCP Dependency

The Technical Recovery Specialist depends on Microsoft Learn MCP to retrieve current Microsoft documentation and best practices. If the MCP service is unavailable or returns no relevant information, technical recommendations may be limited and require manual review.

---

## 2. Knowledge Source Coverage

The quality of the assessment depends on the completeness and accuracy of the configured knowledge source. Missing or outdated organizational policies may affect assessment results.

---

## 3. Excel Data Quality

The solution relies on data stored in the Excel workbook. Incomplete, inconsistent, or incorrect application and assessment records may impact the accuracy of the final readiness assessment.

---

## 4. Manual Data Maintenance

Application inventory, assessment requests, and assessment register data must be maintained manually. The system does not automatically synchronize with enterprise CMDB or asset management platforms.

---

## 5. Limited Scope of Technical Validation

The Technical Recovery Specialist validates recovery capabilities based on available Microsoft guidance and provided application information. It does not perform live infrastructure validation or configuration verification.

---

## 6. No Real-Time Infrastructure Monitoring

The solution does not continuously monitor Azure resources, backup status, disaster recovery health, or application availability. Assessments are based on the information available at the time of execution.

---

## 7. External System Integration

The implementation integrates with Microsoft 365 services but does not include direct integration with enterprise platforms such as ServiceNow, Azure Monitor, Microsoft Defender, or third-party CMDB systems.

---

## 8. Duplicate Assessment Handling

Duplicate assessment detection is based on available assessment records. Advanced duplicate detection using historical trends or intelligent matching is not implemented.

---

## 9. Human Review for Exceptional Cases

Complex recovery scenarios, conflicting assessment results, or insufficient evidence may require manual review before a final BC/DR readiness decision is made.

---

## 10. Scalability

The current implementation is designed for assessment workflows using Microsoft Copilot Studio and Microsoft 365 integrations. Large-scale enterprise deployments may require additional optimization, governance, and monitoring capabilities.