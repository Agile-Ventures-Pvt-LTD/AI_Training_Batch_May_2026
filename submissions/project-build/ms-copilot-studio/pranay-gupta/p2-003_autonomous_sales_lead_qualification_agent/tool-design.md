# Tool Design

## Project Information

| Field                | Details              |
| -------------------- | -------------------- |
| **Project ID**       | P2-003           |
| **Participant Name** | Pranay Gupta |
| **Agent Name**       | Pranay NovaWorks Sales Lead Agent      |

---

# Overview

The agent uses Microsoft 365 connectors to automate lead qualification. Each tool has a specific responsibility within the workflow, ensuring consistent and reliable processing.

---

# Configured Tools

| Tool                    | Purpose                                         | Action |
| ----------------------- | ----------------------------------------------- | ------ |
| Office 365 Outlook      | Trigger agent when a new lead email is received | Read   |
| Excel Online (Business) | Read qualification rules and reference data     | Read   |
| Excel Online (Business) | Create new lead records                         | Create |
| Excel Online (Business) | Update existing lead records                    | Update |
| Word Online (Business)  | Generate lead qualification reports             | Create |
| Office 365 Outlook      | Send acknowledgement emails                     | Send   |
| Office 365 Outlook      | Request missing information                     | Send   |
| Office 365 Outlook      | Notify Sales Owner                              | Send   |
| Office 365 Outlook      | Notify Sales Operations                         | Send   |

---

# Tool Workflow

```text id="dnm9f3"
Outlook Trigger
      │
      ▼
Read Excel Reference Tables
      │
      ▼
Create / Update Lead Record
      │
      ▼
Generate Word Report
      │
      ▼
Send Outlook Notifications
```

---

# Tool Usage Logic

### Outlook

Used to:

* Receive incoming lead emails.
* Send customer acknowledgements.
* Request additional information.
* Notify internal stakeholders.

---

### Excel Online (Business)

Used to:

* Read operational reference tables.
* Detect duplicate opportunities.
* Store lead information.
* Update processing status.

---

### Word Online (Business)

Used to:

* Generate qualification reports for eligible leads.
* Save reports in OneDrive or SharePoint.

---

# Error Handling

If a tool fails:

* Retry once for temporary failures.
* Record the error if it persists.
* Notify Sales Operations.
* Stop external communication when processing is incomplete.

---

# Benefits

* Automated business processing
* Consistent operational records
* Reduced manual effort
* Standardized document generation
* Reliable stakeholder communication

---

# Conclusion

The selected Microsoft 365 tools work together to support the complete autonomous lead qualification process. Each connector has a clearly defined role, enabling the agent to process sales inquiries efficiently while maintaining data consistency and operational reliability.
