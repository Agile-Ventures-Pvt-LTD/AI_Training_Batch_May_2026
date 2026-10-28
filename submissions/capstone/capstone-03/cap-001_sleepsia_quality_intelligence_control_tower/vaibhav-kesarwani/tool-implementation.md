# Tool implementation

## Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower uses **Microsoft 365 tools** directly within **Copilot Studio**. The Quality Supervisor and child agents access Excel, Word, Outlook, and Microsoft Learn MCP without using Power Automate.

## Tools used

| Tool                    | Purpose                          |
| ----------------------- | -------------------------------- |
| Excel Online (Business) | Read and update operational data |
| Word Online (Business)  | Generate investigation reports   |
| Office 365 Outlook      | Send investigation notifications |
| Microsoft Learn MCP     | Microsoft platform guidance      |

## Excel implementation

The system reads operational data from:

* tblCustomerComplaints
* tblProductMaster
* tblBatchRegister
* tblReturns
* tblSalesSummary
* tblOwners
* tblQualityRules

The Quality Supervisor writes to:

* tblQualityIncidents
* tblCAPARegister
* tblCustomerComplaints (Processed status)

## Word implementation

Word Online (Business) generates the **Product Quality Investigation Report** using a predefined template that includes:

* Incident details
* Complaint summary
* Specialist findings
* Final classification
* CAPA summary
* Supervisor approval

## Outlook implementation

Outlook is used for internal notifications after supervisor approval.

Notification routing:

* **Investigation Required** → Quality Manager
* **High-Priority Quality Incident** → Quality Manager, Production Manager
* **Critical Escalation** → Quality Manager, Operations Manager, Leadership

## Microsoft Learn MCP

The **M365 Guidance Specialist** uses Microsoft Learn MCP to retrieve documentation for:

* Copilot Studio
* Microsoft 365
* Teams
* Connectors
* Deployment and governance

MCP is isolated from the quality investigation workflow.

## Tool execution sequence

```text
Validation
      |
      v
Specialist Analysis
      |
      v
Supervisor Decision
      |
      +--> Word Report
      |
      +--> Excel Updates
      |
      +--> Outlook Notification
```

## Failure handling

The Quality Supervisor retries failed tool operations once.

The system never claims that:

* a report was generated,
* an Excel update succeeded,
* an email was sent,
* MCP guidance was retrieved,

unless the corresponding tool confirms success.

This implementation provides a **Microsoft 365 native, enterprise-ready tool architecture** for autonomous quality investigations.
