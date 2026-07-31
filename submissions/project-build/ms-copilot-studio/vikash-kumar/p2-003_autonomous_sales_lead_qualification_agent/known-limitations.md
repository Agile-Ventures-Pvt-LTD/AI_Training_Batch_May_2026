# ⚠️ Known Limitations

## 🚀 Project Information

| Property | Details |
|----------|---------|
| **Project ID** | P2-003 – Autonomous Sales Lead Qualification Agent |
| **Participant** | Vikash Kumar |
| **Platform** | Microsoft Copilot Studio |

---

# 🎯 Purpose

This document outlines the known limitations of the current implementation. These limitations do not prevent the solution from meeting the project requirements but identify areas that could be enhanced in future iterations.

---

# ⚠️ Current Limitations

## 📧 Email Format Dependency

The agent performs best when incoming sales enquiries contain clearly structured business information.

Highly unstructured emails may require additional reasoning by the language model, which can reduce extraction accuracy for certain fields.

---

## 📊 Operational Data Maintenance

Qualification rules, territory mappings, product catalog information, sales owner mappings, and action matrix data are maintained within Microsoft Excel.

The accuracy of business decisions depends on these operational tables remaining up to date.

---

## 🌍 Geographic Coverage

Territory assignment is limited to the mappings defined in the operational workbook.

If a new country or region is introduced without updating the reference data, the agent may escalate the enquiry for human review.

---

## 📦 Product Validation

Product validation is performed only against products available in the Product Catalog reference table.

Enquiries mentioning newly introduced products that are not yet present in the catalog will be classified for human review.

---

## 📄 Report Format

The generated qualification report follows a standardized structure.

Advanced formatting, branding customization, or organization-specific templates are outside the scope of the current implementation.

---

## 📧 Email Communication

The acknowledgement email follows a standardized professional format.

Dynamic personalization beyond the extracted lead information is not currently implemented.

---

## 🤖 AI Decision Confidence

Although the agent follows operational policies and reference data, complex or ambiguous enquiries may still require human review.

This behavior is intentional to maintain reliable business decisions.

---

## 🔒 Microsoft 365 Dependency

The solution relies on Microsoft 365 services including:

- Microsoft Outlook
- Excel Online (Business)
- Word Online (Business)
- Microsoft Copilot Studio

If these services are unavailable or connector authentication expires, processing cannot continue until connectivity is restored.

---

## 🔄 Connector Availability

The autonomous workflow depends on successful execution of Microsoft 365 connector actions.

If a connector fails after the configured retry attempt, the agent stops processing and escalates the case instead of making assumptions.

---

# 💡 Future Enhancements

Potential improvements include:

- CRM integration (Dynamics 365, Salesforce, HubSpot)
- Automatic lead enrichment using external business databases
- Multi-language lead qualification
- Sentiment analysis for customer intent
- Attachment content extraction (PDFs, RFPs, specifications)
- Advanced analytics dashboards
- Configurable qualification rules through an administrative interface
- Real-time notifications through Microsoft Teams
- Integration with approval workflows for high-value opportunities

---

# 🎯 Conclusion

The implemented solution successfully satisfies the functional requirements defined for Project P2-003.

The identified limitations primarily relate to future scalability and enterprise enhancements rather than functional gaps. The current implementation provides a complete, autonomous sales lead qualification workflow using Microsoft Copilot Studio and Microsoft 365 connectors.