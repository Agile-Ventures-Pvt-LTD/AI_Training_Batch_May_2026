
# Known Limitations

## Project

NovaWorks Sales Lead Qualification Agent

---

# Purpose

This document describes the known functional, technical, and platform limitations identified during the implementation of the NovaWorks Sales Lead Qualification Agent in Microsoft Copilot Studio.

These limitations are primarily related to connector capabilities, Copilot Studio generative orchestration behaviour, and Microsoft 365 service constraints rather than defects in the business logic.

---

# Functional Limitations

## 1. Duplicate Detection Depends on AI Reasoning

The agent performs duplicate detection by reading the existing Lead Register and comparing the incoming lead against operational records.

Because the Excel Online (Business) connector available in the project environment does not expose server-side filtering (OData Filter or Filter Query), duplicate identification relies on Copilot Studio's reasoning over the retrieved dataset.

Impact:

- Duplicate detection accuracy depends on the quality of extracted lead information.
- Extremely large lead registers may increase processing time.

Mitigation:
The agent instructions explicitly require duplicate verification before creating any new record.

---

## 2. Excel is Not a Relational Database

The operational workbook is used as the authoritative data source as required by the PRD.

However, Excel has several inherent limitations:

- No record locking
- No transaction support
- Limited concurrency
- Sequential row updates
- Performance decreases with large datasets

This implementation is appropriate for demonstration and assessment purposes but would normally be replaced by Dataverse or SQL Server in production.

---

## 3. AI-Based Information Extraction

Lead information is extracted from free-text email content.

If mandatory business information is omitted from the email, the agent cannot reliably infer missing values.

Examples include:

- Estimated Budget
- Purchase Timeline
- Product Interest
- Decision Role

In these cases, the agent requests additional information instead of inventing values.

---

## 4. Qualification Accuracy

Qualification depends on the completeness and accuracy of the incoming enquiry.

The agent follows the business rules defined in the Qualification Rules table and does not generate arbitrary qualification scores.

Incomplete enquiries may receive lower confidence classifications.

---

# Connector Limitations

## Excel Online (Business)

The available connector version supports reading, creating, and updating rows but has limited filtering capabilities within Copilot Studio.

Known constraints include:

- No advanced SQL-like queries
- Limited search optimisation
- Entire table may be retrieved before reasoning

---

## Word Online (Business)

The connector creates Word documents using generated content.

Formatting depends on Microsoft Word rendering and may vary slightly from the reference template.

The generated report remains editable after creation.

---

## Outlook Connector

Automatic email processing depends on:

- Successful Outlook trigger execution
- Mailbox availability
- Microsoft 365 service availability

Connector throttling or temporary service interruptions may delay processing.

---

# Copilot Studio Limitations

## Generative Tool Selection

The agent uses Generative Orchestration.

Although the instructions strongly enforce workflow order, the language model ultimately decides when to invoke tools.

To reduce variability:

- Tool descriptions clearly define responsibilities.
- Instructions specify mandatory execution order.
- Business rules prohibit skipping duplicate detection.

---

## Reasoning Quality

The agent's decisions depend on:

- Email quality
- Extracted business information
- Available operational data
- Microsoft foundation models

Low-quality or ambiguous emails may require human review.

---

# Security Considerations

The solution does not expose:

- API keys
- Authentication tokens
- Microsoft credentials
- Internal connector secrets
- Tenant configuration

Only synthetic business data supplied with the project dataset is processed.

---

# Out of Scope

The following capabilities were intentionally excluded because they are not required by the PRD:

- CRM integration
- Dynamics 365 integration
- Dataverse storage
- External REST APIs
- Machine learning model training
- Predictive analytics
- Real customer information
- Multi-language processing
- Voice interactions
- Teams integration

---

# Future Enhancements

Potential production improvements include:

- Dataverse replacing Excel storage
- Advanced duplicate matching using fuzzy search
- Confidence-based approval workflows
- Microsoft Teams notifications
- Power BI dashboards
- Azure AI Document Intelligence
- CRM integration
- Automated sales pipeline creation
- Calendar meeting scheduling
- Multi-region deployment

---

# Conclusion

The implemented solution satisfies the functional requirements defined in the PRD while operating within the current capabilities of Microsoft Copilot Studio and Microsoft 365 connectors.

The identified limitations are platform constraints rather than implementation defects and are acceptable for the intended assessment environment.
