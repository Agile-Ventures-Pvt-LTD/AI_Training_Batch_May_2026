# Solution Summary

## Business Problem

NovaWorks Technologies receives many sales emails every day.
The sales team checks every email by hand. They copy information into Excel, check for duplicate leads, decide the lead type, assign a sales owner, create reports, and send reply emails.
This process takes time and can lead to mistakes.

---

## Solution

This project uses Microsoft Copilot Studio to automate the lead qualification process.

When a new email with the subject **[P2-003 LEAD]** arrives, the agent starts automatically.

The agent:

- Reads the email.
- Checks if it is a sales lead.
- Gets lead details.
- Checks for duplicate leads.
- Reads business rules from Excel.
- Calculates the lead score.
- Assigns a lead classification.
- Assigns a sales owner.
- Adds or updates the lead in Excel.
- Creates a Word report for Hot and Qualified leads.
- Sends the correct reply email.
- Sends difficult cases for human review.

---

## Solution Architecture

```
Outlook Email Trigger
          │
          ▼
Read Email
          │
          ▼
Extract Lead Details
          │
          ▼
Check Duplicate
          │
          ▼
Read Excel Reference Tables
          │
          ▼
Score and Classify Lead
          │
          ▼
Assign Sales Owner
          │
          ▼
Update Excel
          │
          ▼
Create Word Report (Hot/Qualified)
          │
          ▼
Send Reply Email
```

---

## Business Logic

The agent follows these steps:

1. Process only emails with **[P2-003 LEAD]** in the subject.
2. Check if the email is a sales lead.
3. Extract lead information.
4. Check for duplicate leads.
5. Read business rules from Excel.
6. Calculate the lead score.
7. Assign the correct classification.
8. Assign the sales owner.
9. Add or update the Excel record.
10. Create a Word report for Hot and Qualified leads.
11. Send the correct email reply.
12. Send difficult cases for human review.

---

## Project Outcomes

The solution helps by:

- Saving time.
- Reducing manual work.
- Keeping lead records up to date.
- Preventing duplicate leads.
- Giving the same qualification process for every lead.
- Creating reports automatically.
- Sending reply emails automatically.
- Sending difficult cases to human review.

---

## Technologies Used

- Microsoft Copilot Studio
- Office 365 Outlook
- Excel Online (Business)
- Microsoft Word Online
- OneDrive for Business