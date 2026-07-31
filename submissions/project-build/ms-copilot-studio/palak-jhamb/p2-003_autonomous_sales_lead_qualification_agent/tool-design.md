# tool-design.md

# Tool Design

## Outlook Tools

### Get emails (V3)

**Purpose**

Retrieve incoming sales enquiry emails.

**Input**

- Inbox
- Subject

**Output**

- Email content
- Sender information
- Message ID

**Dependency**

Outlook

---

### Send External Acknowledgement

**Purpose**

Send acknowledgement emails for qualified leads.

**Input**

Recipient, Subject, Email Body

**Output**

Customer acknowledgement

---

### Send Missing Information Request

**Purpose**

Request mandatory missing information.

**Input**

Recipient, Missing Fields

**Output**

Information request email

---

### Send Internal Owner Notification

**Purpose**

Notify assigned Sales Owner.

**Input**

Lead Summary

**Output**

Internal notification

---

### Send Sales Operations Review Alert

**Purpose**

Notify Sales Operations for Human Review.

**Input**

Lead Details

**Output**

Review notification

---

# Excel Tools

### Read Leads Register

Purpose:

Duplicate detection and existing lead lookup.

---

### Read Qualification Rules

Purpose:

Retrieve qualification scoring rules.

---

### Read Product Catalog

Purpose:

Validate products and determine Product Fit.

---

### Read Territory Owners

Purpose:

Determine sales territory.

---

### Read Sales Owners

Purpose:

Retrieve assigned Sales Owner.

---

### Read Action Matrix

Purpose:

Determine reports, communications, and review actions.

---

### Add Lead to Register

Purpose:

Create new lead records.

---

### Update Lead Register

Purpose:

Update existing lead records.

---

# Word Tool

### Generate Lead Qualification Report

Purpose:

Generate Microsoft Word qualification reports.

---

## Execution Dependencies

Outlook

↓

Information Extraction

↓

Excel Reference Tables

↓

Qualification

↓

Lead Register

↓

Word Report

↓

Email Communication