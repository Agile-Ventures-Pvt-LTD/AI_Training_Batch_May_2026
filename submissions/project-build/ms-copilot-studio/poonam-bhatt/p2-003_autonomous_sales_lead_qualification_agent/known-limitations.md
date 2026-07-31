# Known Limitations

# P2-003 Autonomous Sales Lead Qualification Agent

---

## 1. Functional Boundaries

The agent operates strictly on defined inputs and rule matrices. It is not designed to replace professional human sales and operations planning.

- **No Negotiation or Pricing Generation:** The agent cannot negotiate pricing, propose custom discounts, or create bespoke service packages. If a prospect requests pricing (e.g. TC-012), the agent records the request in the registry, alerts Sales Operations, and terminates without sending a price quote.
- **No Attachment Processing:** The agent processes only the plain text/HTML email body. It does not parse attachments such as custom RFPs, pricing sheets, or company overview presentations. All qualification data must reside in the email text.
- **Limited Multi-Factor Reasoning:** The agent cannot make subjective judgements regarding a lead's strategic value. For example, if a company is very small but represents a high-profile brand, the scoring system will evaluate it strictly based on employees (Startup/Micro size = 2 points) and budget.
- **Ambiguity Suppression:** To prevent errors, any high-ambiguity request (such as TC-020 where the product interest is completely unspecified) triggers a `Human Review Required` classification rather than guessing product fit.

---

## 2. Microsoft 365 Connector Limitations

The agent relies on standard cloud connectors, which introduce architectural boundaries:

- **Excel API Performance and Table Search Size:**
  - The Excel Online (Business) connector suffers from latency when performing sequential reads on tables. As the `LeadsRegisterTable` grows beyond 500 rows, duplicate lookup speeds may degrade.
  - Large workbooks can trigger connector timeouts (default 120 seconds).
- **Outlook API Rate Limits:**
  - The Office 365 Outlook connector enforces API call throttling. The standard tenant-wide limit is 300 requests/minute. During lead generation spikes, triggers or notifications might experience queuing.
- **Word Document File Lock Collisions:**
  - The Word Online connector requires exclusive access to the target OneDrive/SharePoint directory when creating files. If a sales operations member has the directory or a template open in write-mode, the agent's file creation node will fail with a `409 Conflict / Locked File` error. One retry is permitted before the agent routes the case as `Failed` and notifies Sales Operations.

---

## 3. Security, Domain and Tenant Constraints

- **Single-Tenant Restriction:**
  - The agent is registered within the NovaWorks Microsoft Entra ID tenant. Cross-tenant authentication is blocked by default.
  - The monitored mailbox must be hosted within the same tenant.
- **Outbound Email Domain Restriction:**
  - To prevent data leaks and spam, tenant security policies block the agent from emailing unverified external domains. For testing purposes, all outbound emails are sent to synthetic `.example` domains, which are caught and redirected to test mailboxes. Production deployment requires explicit tenant whitelisting.
- **Generative Orchestration Drift:**
  - While generative orchestration allows the agent to extract and map variables dynamically, variations in the LLM model's temperature can occasionally cause normalization drift (e.g., classifying a role as `Strong Influencer` instead of `Researcher/User`). Deterministic validation branches are implemented in Copilot Studio to double-check classification outputs before finalizing data entry.
