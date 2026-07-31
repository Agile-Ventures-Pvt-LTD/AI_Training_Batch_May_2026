# Tool Design

## Overview

The Autonomous Sales Lead Qualification Agent uses Microsoft Copilot Studio connector tools to process incoming sales lead emails, retrieve operational reference data, update the lead register, generate qualification reports, and send business communications.

---

# Outlook Trigger

## When a New Email Arrives (V3)

**Purpose**

Automatically starts the lead qualification process when a new Outlook email is received.

**Required Inputs**

* Message ID
* Sender Name
* Sender Email
* Subject
* Email Body
* Received Date and Time
* Attachment Metadata

**Expected Output**

Starts the autonomous processing workflow.

**Action Boundary**

* Processes only emails with the subject **[P2-003 LEAD]**.
* Ignores all other emails.

**Action Type**

Internal

---

# Excel Online (Business) Tools

## List_LeadsRegister

**Purpose**

Searches the Leads Register to detect duplicate opportunities before creating a new lead.

**Required Inputs**

* Message ID
* Sender Email
* Company Name
* Product Interest

**Expected Output**

Returns existing lead records or confirms that no duplicate exists.

**Do Not Use**

* Creating new lead records

**Action Type**

Internal

---

## Update_Lead_Record

**Purpose**

Updates an existing lead record when a duplicate is detected or when lead information changes.

**Required Inputs**

* Existing Lead ID
* Updated lead details
* Processing status
* Qualification result

**Expected Output**

Existing Lead Register record updated successfully.

**Do Not Use**

* Creating new lead records

**Action Type**

Internal

---

## Add_Lead_Record

**Purpose**

Creates a new lead record for qualified sales opportunities that do not already exist.

**Required Inputs**

* Lead information
* Qualification score
* Classification
* Assigned owner
* Processing status

**Expected Output**

New record added to the Leads Register.

**Do Not Use**

* Duplicate opportunities

**Action Type**

Internal

---

## List_ProductCatalog

**Purpose**

Validates and normalizes the product requested in the email.

**Required Inputs**

* Product Interest

**Expected Output**

Returns the matching product from the Product Catalog.

**Do Not Use**

* Unknown or unsupported products without Human Review.

**Action Type**

Internal

---

## List_QualificationRules

**Purpose**

Retrieves the qualification scoring rules used to evaluate sales leads.

**Required Inputs**

* Lead attributes
* Product information

**Expected Output**

Returns the applicable scoring rules and qualification criteria.

**Action Type**

Internal

---

## List_TerritoryOwners

**Purpose**

Determines the correct sales territory based on the lead's country.

**Required Inputs**

* Country

**Expected Output**

Returns the mapped sales territory.

**Action Type**

Internal

---

## List_SalesOwners

**Purpose**

Retrieves the assigned sales representative for the identified territory.

**Required Inputs**

* Territory

**Expected Output**

Returns the assigned sales owner.

**Action Type**

Internal

---

## List_ActionMatrix

**Purpose**

Determines the appropriate business action based on the lead classification.

**Required Inputs**

* Lead classification

**Expected Output**

Returns the required autonomous processing action.

**Action Type**

Internal

---

# Word Online (Business)

## Create a Microsoft Word document with the given content

**Purpose**

Generates a Lead Qualification Report for Hot and Qualified opportunities.

**Required Inputs**

* Lead Information
* Qualification Score
* Lead Classification
* Assigned Territory
* Assigned Sales Owner
* Duplicate Detection Result
* Recommended Action
* Processing Summary

**Expected Output**

Microsoft Word qualification report stored in Microsoft 365.

**Do Not Use**

* Duplicate
* Human Review Required
* Additional Information Required
* Low Priority
* Not a Sales Lead

**Action Type**

Internal

---

# Outlook Communication Tools

## Send_Acknowledgement

**Purpose**

Sends an acknowledgement email confirming receipt of a valid sales enquiry.

**Required Inputs**

* Recipient Email
* Lead ID
* Contact Name
* Product Interest

**Expected Output**

Acknowledgement email sent successfully.

**Do Not Use**

* Duplicate
* Human Review Required
* Not a Sales Lead

**Action Type**

External

---

## Send_Missing_Information_Request

**Purpose**

Requests mandatory information required to complete lead qualification.

**Required Inputs**

* Recipient Email
* Missing Fields
* Lead ID

**Expected Output**

Missing information request sent successfully.

**Do Not Use**

* Leads with complete information

**Action Type**

External

---

## Send_SalesOps

**Purpose**

Notifies Sales Operations when a lead requires manual review or exception handling.

**Required Inputs**

* Lead ID
* Exception Reason
* Confidence
* Processing Status

**Expected Output**

Sales Operations notification sent successfully.

**Do Not Use**

* Standard autonomous processing

**Action Type**

Internal

---

# Tool Execution Sequence

1. When a New Email Arrives (V3)
2. List_LeadsRegister
3. List_ProductCatalog
4. List_QualificationRules
5. List_TerritoryOwners
6. List_SalesOwners
7. List_ActionMatrix
8. Add_Lead_Record or Update_Lead_Record
9. Create a Microsoft Word document with the given content
10. Send_Acknowledgement or Send_Missing_Information_Request or Send_SalesOps

All tools execute autonomously according to the configured business rules and lead classification.
