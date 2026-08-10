# Known Limitations

## Project Information

| Field | Details |
|-------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Nandani Bisht |

---

# Overview

This document describes the known functional, connector, and platform limitations observed during the development and testing of the Autonomous Sales Lead Qualification Agent.

These limitations are related to Microsoft 365 services and Microsoft Copilot Studio rather than the business logic of the solution.

---

# Functional Limitations

## 1. Subject-Based Trigger

The Outlook trigger processes only emails containing the configured subject prefix:

```
[P2-003 LEAD]
```

Emails without the required subject format are ignored.

---

## 2. Excel Synchronization Delay

Updates to the operational workbook may not appear immediately due to synchronization delays in Excel Online (Business).

During testing, records were successfully written to the connected workbook after synchronization.

---

## 3. Connector Availability

The solution depends on Microsoft 365 connectors.

If Outlook, Excel Online (Business), Word Online (Business), or OneDrive connectors are unavailable or disconnected, the corresponding actions cannot be completed.

---

## 4. Authentication Requirement

The solution requires authenticated Microsoft 365 connections.

Without valid authentication, connector actions cannot execute successfully.

---

## 5. Human Review Scenarios

Certain scenarios intentionally require manual review instead of fully autonomous processing.

Examples include:

- Incomplete lead information
- Competitor-related enquiries
- Unsupported product requests
- Low-confidence extraction

---

## 6. Word Report Generation

Qualification reports are generated only for applicable lead scenarios.

Not every processed email results in a Word document.

---

# Testing Observations

During testing, the following behaviour was observed:

- Outlook trigger executed successfully.
- Excel records were created successfully.
- Outlook notifications were generated successfully.
- Excel updates became visible after synchronization.

No unresolved functional defects remained after verification.

---

# Future Improvements

Possible enhancements include:

- Automatic retry for temporary connector failures.
- More advanced duplicate detection logic.
- Support for attachment-based lead extraction.
- Dashboard for lead analytics and reporting.
- Integration with Microsoft Dynamics 365 CRM.

---

# Conclusion

The identified limitations are primarily related to Microsoft platform behaviour and connector dependencies. They do not prevent the autonomous lead qualification workflow from operating successfully within the intended project scope.