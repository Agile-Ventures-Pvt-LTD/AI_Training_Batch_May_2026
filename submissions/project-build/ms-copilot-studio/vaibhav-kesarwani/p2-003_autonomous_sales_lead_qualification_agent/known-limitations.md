# Known Limitations

## P2-003 Autonomous Sales Lead Qualification Agent

## Purpose

This document summarizes the known limitations of the NovaWorks Autonomous Sales Lead Qualification Agent implemented in Microsoft Copilot Studio.

## Current limitations

### Attachment processing

The agent primarily analyzes the email body and metadata. PDF, Word, image, and scanned document attachments are not fully parsed.

### AI extraction

Classification accuracy depends on the clarity of the incoming email. Incomplete or ambiguous emails may be routed to **Human Review Required**.

### Excel dependency

The agent relies on the availability and structure of the Excel workbook and reference tables. Missing tables, renamed columns, or connector failures may affect processing.

### Territory and product mapping

Unknown products or unmapped countries cannot be qualified automatically and are escalated for human review.

### External communication

The agent does not provide pricing approvals, discounts, contractual commitments, delivery guarantees, or legal confirmations.

### Scalability

The current implementation uses Excel Online (Business) for storage, which is suitable for project-scale processing but not optimized for high-volume enterprise workloads.

## Future improvements

Potential enhancements include:

* attachment content extraction
* multilingual email processing
* CRM integration
* advanced duplicate detection
* Dataverse or SQL-based storage
* operational dashboards and analytics

## Conclusion

These limitations do not affect the core P2-003 requirements. The agent successfully supports autonomous Outlook-triggered processing, lead qualification, duplicate prevention, Excel updates, Word report generation, Outlook communications, and human-review routing within the Microsoft Copilot Studio implementation boundary.
