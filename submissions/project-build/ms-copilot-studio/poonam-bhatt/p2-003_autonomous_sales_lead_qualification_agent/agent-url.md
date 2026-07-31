# Published Agent URL and Access Configuration

- **Agent Name:** NovaWorks Autonomous Sales Lead Qualification Agent (P2-003)
- **Published URL:** https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/3a77da97-a38c-f111-8077-000d3af21e08/overview
- **Authentication Setup:**
  - **Provider:** Microsoft Entra ID (formerly Azure Active Directory)
  - **Flow Type:** OAuth 2.0 Client Credentials and Delegated User flows
  - **Required API Scopes:**
    - `Mail.ReadWrite` (to monitor incoming lead emails and send acknowledgments/alerts)
    - `Files.ReadWrite.All` (to read reference operational spreadsheets and create Word reports in OneDrive/SharePoint)
    - `User.Read` (to access profile and organizational directory information)

- **Access Limitations:**
  - **Tenant Boundary:** The agent is registered in the NovaWorks enterprise tenant. Only accounts and mailboxes inside the corporate domain (`@novaworks.example`) are authorized to interact.
  - **Asynchronous Execution Gating:** External users cannot invoke the agent's endpoints directly. The agent only triggers upon receiving emails in the monitored inbox that explicitly contain `[P2-003 LEAD]` in the subject line. All other messages are ignored.
  - **Tenant Access Policies:** Multi-factor authentication (MFA) and conditional access policies are enforced through the tenant registration.

- **Verification Details:**
  - **Verification Date:** July 31, 2026
  - **Status:** Verified Active and Published
  - **Primary Verifier:** Poonam Bhatt
  - **Recipient Shared With:** Ankur Saxena (Enterprise Operations Team)
