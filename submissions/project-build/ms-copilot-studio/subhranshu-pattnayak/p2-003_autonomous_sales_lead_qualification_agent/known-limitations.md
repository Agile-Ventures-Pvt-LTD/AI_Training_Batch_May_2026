# Known Limitations

## Purpose

This document outlines the known limitations and operational constraints of the Autonomous Sales Lead Qualification Agent. These limitations are primarily related to external dependencies, connector availability, and the scope of the implemented business process.

---

# Connector Dependencies

The solution depends on Microsoft 365 connectors for Outlook, Excel Online, and Microsoft Word Business.

If any required connector is unavailable or incorrectly configured, the corresponding operation cannot be completed successfully.

---

# Microsoft 365 Permissions

The agent requires appropriate Microsoft 365 permissions to:

- Access the configured Outlook mailbox.
- Read and update the Excel workbook.
- Generate Microsoft Word documents.
- Send Outlook communications.

Insufficient permissions may prevent autonomous execution.

---

# Configuration-Driven Decisions

Lead qualification, classification, and owner assignment are based on the configured operational data.

Changes to qualification rules, territory mappings, product catalogs, or action matrices require updates to the reference data.

---

# Human Review Scenarios

The agent escalates processing instead of making autonomous decisions when:

- Mandatory information is missing.
- Decision confidence is below the configured threshold.
- Conflicting information is identified.
- Unsupported products or territories are encountered.

These scenarios require manual review before further processing.

---

# Email Content Scope

The agent generates communications only within the approved business scope.

It does not provide:

- Pricing commitments
- Contractual agreements
- Legal advice
- Technical implementation guarantees
- Unsupported product claims

---

# Duplicate Detection

Duplicate detection relies on the configured identifiers and operational data available in the Lead Register.

Its effectiveness depends on the completeness and accuracy of previously processed records.

---

# Operational Scope

The implemented solution is designed specifically for autonomous sales lead qualification.

Business processes outside this scope, such as CRM opportunity management, contract generation, invoicing, or customer support ticket resolution, are not included.

---

# Summary

Despite these operational constraints, the solution successfully automates the complete sales lead qualification workflow defined within the project scope while maintaining consistent decision-making through configurable business rules.