# Known Limitations

## Overview

The Autonomous Sales Lead Qualification Agent automates lead qualification using Microsoft Copilot Studio and Microsoft 365 services. The following limitations apply to the current implementation.

---

## Functional Limitations

- Processes only emails with the configured subject filter (`[P2-003 LEAD]`).
- Supports Outlook email as the only input channel.
- Qualification is based on predefined business rules stored in Excel.
- Email attachments are not processed.
- Designed only for sales lead qualification.

---

## Connector Limitations

- Depends on Microsoft Outlook, Excel, and Word Online connectors.
- Connector failures or expired authentication may interrupt processing.
- Excel workbook availability and table structure must remain unchanged.

---

## Tenant Limitations

- Requires appropriate Microsoft 365 licensing and permissions.
- Subject to tenant security policies and connector restrictions.

---

## AI Limitations

- Does not guess missing information.
- Does not expose internal qualification logic.
- Cannot negotiate pricing or make business commitments.
- Requires human review for exceptional scenarios.

---

## Future Enhancements

Potential improvements include:

- CRM integration
- Multi-channel lead intake
- Attachment processing
- AI-based predictive lead scoring
- Power BI reporting
- Microsoft Teams notifications

---

## Summary

The solution meets the project requirements for autonomous lead qualification. The identified limitations are mainly related to the current implementation scope and Microsoft 365 platform capabilities, with clear opportunities for future enhancement.