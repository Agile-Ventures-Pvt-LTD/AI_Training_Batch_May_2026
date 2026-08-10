# MCP Implementation

## 1. Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control
Tower uses the **Microsoft Learn MCP Server** to provide current
Microsoft product and platform guidance.

The MCP integration is intentionally isolated from the core
quality-decision workflow. It is attached only to the **M365 Guidance
Specialist**, which acts as an operational guidance specialist for
Microsoft Copilot Studio, Teams, Microsoft 365, and connector usage.

The MCP server must **never determine Sleepsia product-quality severity,
incident classification, CAPA requirements, or safety escalation**.

## 2. MCP Objective

The purpose of MCP is to provide current Microsoft guidance for employee
questions such as:

-   How to use Microsoft Copilot Studio.
-   How to configure or publish an agent.
-   How to use Teams with the agent.
-   How Microsoft 365 Copilot works with the solution.
-   How to configure supported Microsoft connectors.
-   How to troubleshoot Microsoft platform configuration issues.

The PRD explicitly requires Microsoft Learn MCP and states that it is
**non-blocking to the core quality workflow**.
fileciteturn12file6L600-L632

## 3. MCP Configuration

Use the following configuration:

  ---------------------------------------------------------------------------
  Setting                             Value
  ----------------------------------- ---------------------------------------
  Server                              Microsoft Learn MCP Server

  Endpoint                            `https://learn.microsoft.com/api/mcp`

  Authentication                      None

  Consumer                            M365 Guidance Specialist only

  Purpose                             Current Microsoft Copilot Studio,
                                      Teams, Microsoft 365 and connector
                                      guidance

  Quality decision impact             None

  Failure impact                      Non-blocking
  ---------------------------------------------------------------------------

The PRD provides these exact MCP configuration requirements.
fileciteturn12file8L818-L828

## 4. Architecture

``` text
Employee Question
       |
       v
Quality Supervisor
       |
       v
M365 Guidance Specialist
       |
       v
Microsoft Learn MCP
       |
       v
Current Microsoft Guidance
       |
       v
Employee Response
```

The MCP path is separate from the quality assessment path:

``` text
Quality Assessment
       |
       +--> Complaint Specialist
       +--> Returns Specialist
       +--> Product/Batch Specialist
       +--> Customer Impact Specialist
       +--> Safety Specialist
       +--> CAPA Specialist
       |
       v
Quality Supervisor
       |
       v
Final Quality Classification
```

MCP must not be inserted between specialist findings and the final
quality decision.

## 5. M365 Guidance Specialist

Create one child agent named:

**M365 Guidance Specialist**

### Purpose

Provide operational Microsoft guidance using the Microsoft Learn MCP
Server.

### Responsibilities

-   Retrieve current Microsoft guidance.
-   Answer Copilot Studio configuration questions.
-   Answer Teams publishing/configuration questions.
-   Answer Microsoft 365 Copilot questions.
-   Answer Microsoft connector/tool configuration questions.
-   Explain relevant Microsoft platform procedures based on retrieved
    documentation.

### Restrictions

The specialist must not:

-   Assign Sleepsia quality severity.
-   Change the final quality classification.
-   Override Sleepsia quality policy.
-   Create or approve CAPA decisions.
-   Determine customer compensation.
-   Replace the Quality Supervisor.
-   Treat Microsoft documentation as Sleepsia quality policy.

The PRD explicitly defines this specialist as operational support and
states that it is not part of the product-quality severity decision.
fileciteturn12file8L818-L820

## 6. Copilot Studio Setup

Configure MCP on the **M365 Guidance Specialist**, not on every child
agent and not as a general-purpose tool for the Quality Supervisor.

Required setup:

1.  Open **M365 Guidance Specialist**.
2.  Open **Tools**.
3.  Select **Add a tool**.
4.  Select **New tool**.
5.  Select **Model Context Protocol**.
6.  Provide a meaningful server name.
7.  Provide a meaningful server description.
8.  Enter: `https://learn.microsoft.com/api/mcp`
9.  Select **No authentication**.
10. Create/add the connection.
11. Test a Microsoft documentation lookup.
12. Confirm that the specialist can return useful Microsoft guidance.

These setup steps are specified in the PRD.
fileciteturn12file8L829-L835

## 7. Recommended Server Description

Use a concise description such as:

> Provides current Microsoft Learn guidance for Microsoft Copilot
> Studio, Teams, Microsoft 365 Copilot, connectors, agent configuration,
> publishing, and related Microsoft platform operations. Use only for
> Microsoft operational guidance. Do not use this server for Sleepsia
> product-quality decisions, severity classification, CAPA decisions, or
> safety escalation.

## 8. When MCP Should Be Invoked

MCP should be used when an employee asks for current Microsoft
operational guidance.

Examples:

-   "How do I publish this agent to Teams?"
-   "How can I configure Microsoft 365 Copilot for this agent?"
-   "How do I add a connector in Copilot Studio?"
-   "What is the Microsoft-supported way to configure this feature?"
-   "Where can I find the current Microsoft documentation for this
    Copilot Studio capability?"

The M365 Guidance Specialist should be selected for these requests.

## 9. When MCP Should NOT Be Invoked

Do not use MCP for:

-   Complaint analysis.
-   Return-rate calculation.
-   Product/batch analysis.
-   Customer-impact analysis.
-   Safety assessment.
-   Quality classification.
-   CAPA classification.
-   Sleepsia quality policy interpretation.
-   Incident severity.
-   Recall decisions.
-   Customer compensation decisions.

Those activities belong to the Sleepsia quality workflow and approved
internal sources.

## 10. MCP and Autonomous Quality Workflow

MCP is **not required** for the normal autonomous quality assessment.

The autonomous workflow remains:

``` text
Recurrence Trigger
       |
       v
Incident Intake & Validation
       |
       v
Specialist Fan-Out
       |
       v
Specialist Fan-In
       |
       v
Quality Investigation Decision
       |
       v
CAPA when required
       |
       v
Supervisor Validation
       |
       v
Word / Excel / Outlook
```

The Microsoft Learn MCP path remains independent:

``` text
Employee Microsoft Question
       |
       v
M365 Guidance Specialist
       |
       v
Microsoft Learn MCP
```

The PRD requires MCP to remain non-blocking to the core quality
workflow. fileciteturn12file6L631-L632

## 11. MCP Failure Handling

If the Microsoft Learn MCP Server fails or is unavailable:

1.  Do not stop the core Sleepsia quality workflow.
2.  Do not fabricate Microsoft guidance.
3.  Record or surface the MCP availability problem.
4.  For a Microsoft guidance request, return exactly:

**`Microsoft guidance unavailable - manual review`**

The PRD explicitly defines this MCP fallback.
fileciteturn12file8L836-L837

## 12. Example Failure Flow

``` text
Employee asks Microsoft question
          |
          v
M365 Guidance Specialist
          |
          v
MCP unavailable
          |
          +----> Microsoft guidance unavailable - manual review
```

For an unrelated quality assessment:

``` text
Quality Assessment
       |
       v
MCP unavailable
       |
       v
Continue quality workflow normally
```

MCP availability must never cause an otherwise valid quality assessment
to fail.

## 13. MCP and Knowledge Precedence

Microsoft Learn MCP is not part of the Sleepsia quality-policy
precedence.

For Sleepsia quality decisions, the required precedence remains:

1.  `Sleepsia_Product_Quality_Policy.docx`
2.  Other approved internal policy documents
3.  Operational Excel data
4.  Approved Sleepsia public product URLs

Microsoft Learn MCP is used for **Microsoft operational guidance**, not
Sleepsia quality decisions.

Therefore, an MCP response must never override:

-   Sleepsia quality classification.
-   Safety escalation.
-   Complaint thresholds.
-   Return-rate rules.
-   CAPA requirements.
-   Incident state.
-   Internal quality policy.

## 14. Example Queries

### Query 1 --- Teams

> "How do I publish my Copilot Studio agent to Microsoft Teams?"

Expected routing:

``` text
Quality Supervisor
        |
        v
M365 Guidance Specialist
        |
        v
Microsoft Learn MCP
```

Expected behavior: return current Microsoft guidance.

### Query 2 --- Microsoft 365 Copilot

> "How can I make this agent available in Microsoft 365 Copilot?"

Expected routing: M365 Guidance Specialist -\> MCP.

### Query 3 --- Connector

> "How do I configure an Excel Online connector in Copilot Studio?"

Expected routing: M365 Guidance Specialist -\> MCP.

### Query 4 --- Quality Question

> "Five complaints occurred for the same SKU in seven days. What is the
> Sleepsia classification?"

Expected behavior: **do not use MCP**. Use the Sleepsia quality workflow
and internal quality policy. The applicable rule is Investigation
Required unless a higher-priority rule applies.
fileciteturn12file9L863-L880

### Query 5 --- Safety

> "A complaint has SafetyIndicator = Yes. What should we do?"

Expected behavior: **do not use MCP**. The Sleepsia Safety Specialist
and Quality Supervisor handle the decision. The classification is
Critical Escalation. fileciteturn12file9L863-L880

## 15. Testing Checklist

### Configuration

-   [ ] M365 Guidance Specialist exists.
-   [ ] MCP is attached only to M365 Guidance Specialist.
-   [ ] Server is Microsoft Learn MCP Server.
-   [ ] Endpoint is `https://learn.microsoft.com/api/mcp`.
-   [ ] Authentication is None.
-   [ ] MCP connection succeeds.
-   [ ] A Microsoft documentation lookup succeeds.

### Routing

-   [ ] Microsoft operational questions route to M365 Guidance
    Specialist.
-   [ ] Quality questions do not unnecessarily invoke MCP.
-   [ ] Safety questions do not invoke MCP for classification.
-   [ ] CAPA decisions do not depend on MCP.

### Failure

-   [ ] MCP failure does not stop quality assessment.
-   [ ] Microsoft guidance request returns
    `Microsoft guidance unavailable - manual review`.
-   [ ] No Microsoft response is fabricated.

### Boundary

-   [ ] MCP cannot assign quality severity.
-   [ ] MCP cannot authorize CAPA.
-   [ ] MCP cannot authorize reports.
-   [ ] MCP cannot authorize notifications.
-   [ ] MCP cannot override internal Sleepsia policy.

## 16. PRD Alignment

The MCP implementation satisfies the PRD requirements that:

-   Microsoft Learn MCP is mandatory.
-   It is attached only to the M365 Guidance Specialist.
-   The endpoint is `https://learn.microsoft.com/api/mcp`.
-   Authentication is None.
-   It provides current Microsoft Copilot Studio, Teams, Microsoft 365
    and connector guidance.
-   It is non-blocking to the core quality assessment.
-   Its failure must not block the quality workflow.
-   The specialist must return the defined manual-review response when
    MCP is unavailable. fileciteturn12file8L818-L837

## 17. Final MCP Design

``` text
                         QUALITY DOMAIN
                              |
                  +-----------+-----------+
                  |                       |
                  v                       v
          Quality Specialists       Quality Supervisor
                  |                       |
                  +-----------+-----------+
                              |
                       Final Classification
                              |
                    Excel / Word / Outlook


                      MICROSOFT GUIDANCE DOMAIN
                              |
                              v
                    M365 Guidance Specialist
                              |
                              v
                    Microsoft Learn MCP
                              |
                              v
                    Microsoft Guidance
```

The key architectural rule is:

> **MCP provides Microsoft operational guidance only. It is a
> non-blocking support capability and must never participate in Sleepsia
> product-quality decision ownership.**
