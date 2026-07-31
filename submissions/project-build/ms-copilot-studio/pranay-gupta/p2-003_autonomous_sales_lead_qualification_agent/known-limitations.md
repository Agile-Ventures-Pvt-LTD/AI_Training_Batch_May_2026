# Known Limitations

## Project Information

| Field                | Details              |
| -------------------- | -------------------- |
| **Project ID**       | P2-003           |
| **Participant Name** | Pranay Gupta |
| **Agent Name**       | Pranay NovaWorks Sales Lead Agent    |

---

# Overview

The Autonomous Sales Lead Qualification Agent meets the project requirements defined in the PRD. The following limitations reflect the current implementation scope and identify areas for future enhancement.

---

# Current Limitations

| Area              | Limitation                                                                             |
| ----------------- | -------------------------------------------------------------------------------------- |
| Email Processing  | Only emails matching the configured subject filter (`[P2-003 LEAD]`) are processed.    |
| Attachments       | Email attachments are not analyzed as part of the current implementation.              |
| Data Source       | The agent relies only on the provided operational Excel workbook and policy documents. |
| Report Generation | Qualification reports are generated only for eligible lead classifications.            |
| Retry Logic       | Temporary tool failures are retried once before escalation.                            |
| Human Review      | Exceptional or low-confidence scenarios require manual review before further action.   |

---

# Assumptions

The implementation assumes that:

* Microsoft 365 connectors are configured and available.
* The operational Excel workbook is accessible.
* Outlook, Excel, and Word services are functioning correctly.
* Operational reference tables contain valid and up-to-date information.

---

# Future Enhancements

Possible improvements include:

* CRM integration (e.g., Dynamics 365 or Salesforce)
* Email attachment analysis
* Multi-language support
* AI-assisted confidence scoring
* Power BI dashboards for lead analytics
* Automated follow-up scheduling
* Enhanced reporting and monitoring

---

# Conclusion

These limitations are consistent with the current project scope and do not affect the successful operation of the implemented solution. The proposed enhancements provide opportunities for future expansion while maintaining the existing autonomous lead qualification workflow.
