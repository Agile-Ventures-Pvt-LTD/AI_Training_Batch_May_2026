# Known Limitations

During integration and stress testing, the following technical limits and boundaries were identified:

---

## 1. Excel Online Sync Delays
*   **Limitation:** Updates to the Excel database tables take 5 to 10 seconds to sync globally.
*   **Mitigation:** The primary Quality Supervisor writes `Status = "In Assessment"` back to the row immediately *before* calling specialists to lock the row and prevent concurrent trigger runs.

---

## 2. API Throttling Limits
*   **Limitation:** Microsoft Graph API limits Excel Online sheet updates to 100 requests per minute.
*   **Mitigation:** The supervisor schedules the recurrence interval to 1 hour, batching evaluations to avoid hitting API limits.

---

## 3. Parallel Execution Limits
*   **Limitation:** Copilot Studio limits parallel branch execution to 5 concurrent branches.
*   **Mitigation:** The specialist child agent roster is locked at exactly 5 concurrent agents.

---

## 4. Word Report Generation Time
*   **Limitation:** Populating the Word report template and generating the PDF takes up to 30 seconds.
*   **Mitigation:** The supervisor executes the report generation asynchronously at the end of the pipeline.

---

## 5. Teams & M365 Copilot Publishing Restrictions
*   **Limitation:** Tenant publishing depends on organization policies. If admin consent is blocked, the agent remains restricted to development testing.
*   **Mitigation:** Sideloading the app manifest directly in Microsoft Teams for local validation.
