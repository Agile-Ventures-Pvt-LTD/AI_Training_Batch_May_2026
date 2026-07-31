# Known Limitations

## Functional Limitations

- The agent processes only emails with **[P2-003 LEAD]** in the subject.
- The agent does not process email attachments.
- The agent cannot process emails outside the project scope.
- The agent depends on the information provided in the email.
- Missing or unclear information may require human review.

---

## Connector Limitations

- The agent requires a working Outlook connection.
- The agent requires a working Excel Online (Business) connection.
- The agent requires a working Microsoft Word connection.
- If a connector is unavailable, the agent cannot complete the related action.
- The agent retries a failed tool action only once.

---

## Tenant Limitations

- The agent works only in the Microsoft 365 tenant where it is published.
- Users must have permission to access the agent.
- Users must have permission to access the Excel and Word files.
- The agent uses only Microsoft 365 services.
- The agent uses only synthetic project data.