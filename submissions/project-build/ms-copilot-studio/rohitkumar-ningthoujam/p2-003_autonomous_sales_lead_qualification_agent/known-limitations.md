# Known Limitations

## Purpose

This document describes the known functional, Microsoft 365 connector, and tenant limitations of the **P2-003 Autonomous Sales Lead Qualification Agent** implemented in Microsoft Copilot Studio. These limitations are documented for transparency and do not prevent the agent from demonstrating the required project functionality.

---

# Functional Limitations

## Attachment Processing

The agent processes information contained within the email subject and body. Email attachments are detected through Outlook metadata but their contents are not parsed or analyzed as part of this implementation.

---

## Rule-Based Qualification

Lead qualification is based on the operational reference tables and business rules provided in the project dataset. The agent does not learn from previous executions or modify qualification rules automatically.

---

## Unknown or Incomplete Information

When mandatory information such as budget, purchase timeline, or product details is unavailable, the agent retains these values as **Unknown** and routes the lead according to the defined business rules instead of making assumptions.

---

## Human Review Dependency

Cases involving low confidence, unknown products, unmapped territories, conflicting information, competitor enquiries, academic research, recruitment, or support requests require manual review by Sales Operations before any qualification decision can be communicated externally.

---

# Outlook Connector Limitations

* Autonomous processing depends on the successful execution of the **Office 365 Outlook – When a new email arrives (V3)** trigger.
* Only emails with the subject containing **[P2-003 LEAD]** are processed.
* Outlook connector availability depends on Microsoft 365 service availability and valid connector authentication.
* Email delivery may be affected by tenant policies, mailbox permissions, or connector availability.

---

# Excel Online (Business) Limitations

* The Excel workbook must be stored in **OneDrive for Business** or **SharePoint Online**.
* All required tables must exist and maintain the expected schema.
* Changes to table names, column names, or workbook location may prevent successful execution.
* Concurrent edits to the workbook may temporarily affect read or update operations.

---

# Word Online (Business) Limitations

* Microsoft Word qualification reports are generated only for classifications defined by the business rules.
* Document creation depends on Word Online (Business) connector availability.
* Report generation may fail if the destination location is unavailable or required permissions are missing.

---

# Microsoft 365 Tenant Limitations

* The solution requires valid Microsoft 365 licenses and connector permissions.
* Some autonomous capabilities may vary depending on tenant configuration, security policies, and administrator settings.
* Publishing, sharing, and trigger execution require appropriate tenant permissions.

---

# Error Handling Limitations

The agent performs one controlled retry for transient connector failures. Persistent failures are recorded where possible, and the affected action is not reported as successful. Recovery from infrastructure or tenant-level issues requires manual intervention.

---

# Project Assumptions

The implementation assumes that:

* Only synthetic project data is processed.
* Operational reference tables contain valid and consistent data.
* Outlook, Excel Online (Business), and Word Online (Business) connectors are correctly configured.
* Required Microsoft 365 storage locations remain accessible throughout execution.

---

# Future Improvements

The solution could be enhanced with:

* Email attachment content extraction.
* Advanced AI-based confidence scoring.
* CRM integration for opportunity management.
* Automated follow-up reminders.
* Analytics dashboards for lead qualification trends.
* Enhanced duplicate detection using semantic similarity.
* Additional business rule customization through configurable policies.

---

# Conclusion

The identified limitations primarily relate to Microsoft 365 connector availability, tenant configuration, project scope, and controlled autonomy. Within these boundaries, the Autonomous Sales Lead Qualification Agent successfully demonstrates the required functionality defined in the P2-003 Project Requirements Document while maintaining accuracy, auditability, and compliance with the NovaWorks Sales Lead Qualification and Autonomy Policy.
