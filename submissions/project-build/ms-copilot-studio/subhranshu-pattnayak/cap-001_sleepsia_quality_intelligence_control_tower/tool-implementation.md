# Tool Implementation

## Overview

The Sleepsia Quality Intelligence Control Tower uses Microsoft Copilot Studio tools and Microsoft 365 connectors to retrieve data, update records, generate reports, and send notifications.

Tools are invoked by the Quality Supervisor and specialist agents based on workflow requirements.

---

## Customer Complaints Table

Purpose:

- Retrieve unprocessed complaints
- Mark complaints as processed

Used By:

- Quality Supervisor

Operations:

- Get a row
- Update a row

---

## Quality Incidents Table

Purpose:

- Retrieve incident records
- Create incident records
- Update incident records
- Maintain reassessment information

Used By:

- Quality Supervisor
- Product/Batch Specialist (read-only)

Operations:

- List rows
- Add a row
- Update a row

---

## Returns Table

Purpose:

- Retrieve return records for analysis

Used By:

- Returns Specialist

Operations:

- List rows

---

## Sales Summary Table

Purpose:

- Retrieve sales volume information

Used By:

- Returns Specialist

Operations:

- List rows

---

## Product Master Table

Purpose:

- Retrieve product information

Used By:

- Product/Batch Specialist
- Quality Supervisor (Interactive Mode)

Operations:

- List rows

---

## Batch Register Table

Purpose:

- Retrieve batch information

Used By:

- Product/Batch Specialist
- Quality Supervisor (Interactive Mode)

Operations:

- List rows

---

## CAPA Register Table

Purpose:

- Retrieve CAPA information

Used By:

- Quality Supervisor (Interactive Mode)

Operations:

- List rows

---

## Owners Table

Purpose:

- Retrieve stakeholder information for notification processing

Used By:

- Quality Supervisor

Operations:

- List rows

---

## Microsoft Word Connector

Purpose:

- Generate investigation reports

Used By:

- Quality Supervisor

Operations:

- Create document

---

## Outlook Connector

Purpose:

- Send investigation notifications

Used By:

- Quality Supervisor

Operations:

- Send email

---

## MCP Integration

Purpose:

- Retrieve Microsoft 365 information and guidance

Used By:

- M365 Guidance Specialist

Operations:

- MCP tool execution
- MCP information retrieval

---

## Tool Access Controls

### Autonomous Mode

Permitted Operations:

- Read records
- Create records
- Update records
- Generate reports
- Send notifications

### Interactive Mode

Permitted Operations:

- Read records
- Retrieve guidance
- Retrieve information

Interactive Mode does not create records, update records, generate CAPAs, or send notifications.