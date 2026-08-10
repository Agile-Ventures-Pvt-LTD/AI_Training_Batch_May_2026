# Enterprise Publishing and Channel Deployment

This document records the publishing status, channel configuration parameters, and the tenant billing constraint encountered during the deployment of the **Sleepsia Quality Control Tower**.

---

## 1. Publishing Process & Tenant Billing Constraint

During the compilation and deployment phase in Copilot Studio, the system encountered an environment billing policy restriction.

### Error Analysis & Evidence
- **Trigger Action:** Clicking the "Publish" button on the **Evaluation** tab.
- **System Warning:** A modal dialog appeared with the following message:
  > **There is a billing issue.**
  > *Please contact your admin to confirm the billing capability for this environment and agent.*
- **System State:** The "Publish" button was completely disabled (greyed out), preventing the latest changes (including custom topics and connector credentials) from being deployed to active channels.
- **Forced Versioning Attempt:** The option "Force newest version" was enabled to clear out active sessions, but the publishing lock remained due to tenant-level subscription limits.

```text
[Environment: Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359]
  └── Bot: 76dac50e-8194-f111-b8dc-000d3af21e08 (Quality Control Tower)
        └── Action: Publish -> BLOCKED (Disabled by Power Platform Billing Check)
```

---

## 2. Root Cause & Administrative Remediation

The billing block is a standard tenant-level limitation inside the Microsoft Power Platform environment:

1. **AI Builder Credits Exhausted:** The agent uses advanced multi-agent triggers and generative orchestration which query LLMs. If the host environment runs out of AI Builder capacity credits, Microsoft blocks publishing.
2. **Missing Trial/Production Licenses:** The environment requires an active Copilot Studio user license or tenant-wide message capacity pass. If the trial expires or the billing subscription is not associated with the environment, publishing is locked.
3. **Required Admin Actions:**
   - The tenant administrator must allocate AI Builder capacity to environment `Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359`.
   - Update billing profiles in the Power Platform Admin Center.

---

## 3. Planned Channel Configurations (Pending Billing Resolution)

Once the administrator resolves the billing block, the following channels are configured for deployment:

### Microsoft Teams Channel
- **Target Status:** **Ready for Sideloading**
- **Configuration Steps:**
  1. Under **Settings** -> **Channels**, select **Microsoft Teams**.
  2. Click **Turn on Teams** to activate the channel interface.
  3. Click **Submit for admin approval** or download the app manifest file (`manifest.zip`).
  4. Sideload the bot package into Teams using the tenant App Sideloading Policy.

### Microsoft 365 Copilot Channel
- **Target Status:** **Extensibility Integration Enabled**
- **Configuration Steps:**
  1. Select **Microsoft 365 Copilot** from the Channels menu.
  2. Toggle the switch **Enable Copilot Integration** to `On`.
  3. Map the agent's trigger phrases to Copilot's extensibility engine, allowing employees to query the quality database using natural language prompts within the broader M365 chat interface.
