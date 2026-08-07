# Specialist Agent Design

## P2-005 — All Specialist Child Agents

This document details the design of all six specialist child agents that operate under the Campaign Readiness Supervisor.

---

## Standard Specialist Output Contract

All specialists return structured information following this common contract:

| Output Field | Requirement |
|-------------|-------------|
| SpecialistName | Name of the specialist |
| AssessmentStatus | Pass / Condition / Block / Insufficient Evidence |
| EvidenceSummary | Information and data points used |
| BlockingIssues | Blocking findings (or "None") |
| Conditions | Non-blocking findings (or "None") |
| RequiredActions | Required remediation steps (or "None") |
| RequiredApprover | Human approver where applicable (or "None") |
| Confidence | High / Medium / Low |
| Completed | Yes / No |

---

## Specialist 1: Budget & Commercial Specialist

### Overview
| Property | Value |
|----------|-------|
| Name | Budget & Commercial Specialist |
| Type | Child Agent |
| Domain | Financial viability and budget compliance |
| Runs In | Parallel (with Brand, Channel, Asset) |

### Responsibilities
- Evaluate proposed vs approved budget and calculate variance
- Assess target CPL reasonableness
- Identify required financial approvals based on thresholds
- Flag budget-related blocking conditions

### Data Sources
| Excel Table | Purpose |
|-------------|---------|
| Campaign_Requests | ProposedBudget, ApprovedBudget, ExpectedLeads, TargetCPL |
| Budget_Rules | Budget approval thresholds |
| Approval_Matrix | Approval requirements by level |

### Knowledge
- NovaSphere Marketing Governance Policy

### Business Rules
| Condition | Result |
|-----------|--------|
| ProposedBudget > ApprovedBudget | Block → Marketing Director approval |
| ProposedBudget > INR 1,000,000 | Block → VP Marketing approval |
| TargetCPL > INR 4,000 | Block → VP Marketing approval |
| Budget = ApprovedBudget, CPL acceptable | Pass |

### Boundary
- Does NOT evaluate brand, channel, or asset domains

---

## Specialist 2: Brand & Content Compliance Specialist

### Overview
| Property | Value |
|----------|-------|
| Name | Brand & Content Compliance Specialist |
| Type | Child Agent |
| Domain | Brand compliance, content quality, regulatory sensitivity |
| Runs In | Parallel (with Budget, Channel, Asset) |

### Responsibilities
- Verify product naming compliance
- Review campaign claims for restrictions
- Assess regulatory sensitivity implications
- Check required disclaimers
- Verify brand approval status
- Check CTA consistency
- Evaluate external agency implications

### Data Sources
| Excel Table | Purpose |
|-------------|---------|
| Campaign_Requests | Product, RegulatorySensitivity, ExternalAgency |
| Asset_Status | Content details, approval status |

### Knowledge
- **NovaSphere Brand & Content Guidelines** (primary)
- NovaSphere Marketing Governance Policy

### Business Rules
| Condition | Result |
|-----------|--------|
| High-sensitivity campaign | Block → Additional review required |
| Missing mandatory disclaimers | Block |
| Non-compliant product naming | Block |
| Unsupported/restricted claims | Block |
| Pending brand approval | Block |
| Minor CTA inconsistencies | Condition |

### Boundary
- Does NOT evaluate budget or channel-operational aspects

---

## Specialist 3: Channel Readiness Specialist

### Overview
| Property | Value |
|----------|-------|
| Name | Channel Readiness Specialist |
| Type | Child Agent |
| Domain | Channel operational readiness |
| Runs In | Parallel (with Budget, Brand, Asset) |

### Responsibilities
- Evaluate EVERY channel listed for the campaign (not just the first)
- Check mandatory channel assets
- Verify minimum lead time compliance
- Check tracking/analytics requirements
- Identify channel owners
- Verify brand approval for channel content
- Identify missing prerequisites

### Data Sources
| Excel Table | Purpose |
|-------------|---------|
| Campaign_Requests | Channels (semicolon-separated) |
| Channel_Requirements | Requirements per channel |
| Asset_Status | Channel-related asset readiness |

### Knowledge
- NovaSphere Marketing Governance Policy

### Business Rules
| Condition | Result |
|-----------|--------|
| Missing mandatory channel asset | Block |
| Lead time violation | Block |
| Missing tracking when required | Condition |
| Missing channel owner | Condition |
| Brand approval pending for channel | Block |
| All prerequisites met for all channels | Pass |

### Key Requirement
Must evaluate **ALL** channels listed in the campaign's Channels field, not only the first channel.

### Boundary
- Does NOT evaluate budget or brand-compliance aspects

---

## Specialist 4: Asset Readiness Specialist

### Overview
| Property | Value |
|----------|-------|
| Name | Asset Readiness Specialist |
| Type | Child Agent |
| Domain | Asset availability, approval, and QA status |
| Runs In | Parallel (with Budget, Brand, Channel) |

### Responsibilities
- Evaluate all assets for the campaign
- Classify each asset: Ready / Condition / Blocking / Missing
- Check asset approval status
- Identify pending QA items
- Identify assets needing changes
- Return aggregate counts to the Supervisor

### Data Sources
| Excel Table | Purpose |
|-------------|---------|
| Campaign_Requests | CampaignID, LaunchDate |
| Asset_Status | All asset records |

### Knowledge
- NovaSphere Marketing Governance Policy

### Business Rules
| Condition | Result |
|-----------|--------|
| Missing mandatory asset | Block |
| Needs Changes | Block |
| Pending Approval | Block |
| Pending QA (when policy permits) | Condition |
| Missing blocking assets + launch < 5 days | Not Ready (escalate) |

### Additional Output
Returns aggregate counts:
- Total Assets, Ready count, Condition count, Blocking count, Missing count

### Boundary
- Does NOT evaluate budget, brand, or channel aspects

---

## Specialist 5: Launch Risk & Decision Specialist

### Overview
| Property | Value |
|----------|-------|
| Name | Launch Risk & Decision Specialist |
| Type | Child Agent |
| Domain | Consolidated risk analysis and readiness recommendation |
| Runs In | **Sequential** (AFTER the 4 parallel specialists, post fan-in) |

### Responsibilities
- Analyse consolidated results from all four domain specialists
- Identify blocking issues, conditions, and approvals across all domains
- Assess timing risk based on days to launch
- Classify overall campaign risk level
- Propose a readiness outcome (Supervisor validates)

### Inputs
Receives consolidated data from the Supervisor:
- Budget, Brand, Channel, Asset specialist results
- DaysToLaunch, Geography, Sensitivity, Pending approvals

### Risk Classification
| Level | Criteria |
|-------|----------|
| Low | All pass, no conditions, sufficient lead time |
| Medium | Minor conditions, no blockers, adequate lead time |
| High | One+ blocking issues OR tight timeline OR pending approvals |
| Critical | Multiple blocking domains OR launch < 5 days with blocks OR insufficient evidence |

### Tools
- None (receives data from Supervisor, no direct data access)

### Boundary
- **Proposes** an outcome — the Supervisor VALIDATES and OWNS the final decision

---

## Specialist 6: Reporting & Communication Specialist

### Overview
| Property | Value |
|----------|-------|
| Name | Reporting & Communication Specialist |
| Type | Child Agent |
| Domain | Report generation and stakeholder notification |
| Runs In | **Sequential** (ONLY after Supervisor validation) |

### Responsibilities
- Generate a Word Campaign Readiness Report (via Word Online Business)
- Send Outlook stakeholder notification (via Outlook Office 365)
- Handle tool failures gracefully

### Tools
| Tool | Connector | Action |
|------|-----------|--------|
| Word Online (Business) | Premium | Create a Microsoft Word document |
| Outlook (Office 365) | Standard | Send an email |

### Word Report Content
Campaign Overview, Budget/Brand/Channel/Asset assessments, Blocking gaps, Conditions, Required approvals, Risk classification, Final readiness status, Remediation actions, Recommended next steps

### Outlook Notification
Content varies by outcome:
| Outcome | Recipient | Subject Theme |
|---------|-----------|--------------|
| Ready | Campaign Owner | Launch approval |
| Ready with Conditions | Campaign Owner | Conditional approval with conditions |
| Approval Required | Required Approver (CC: Owner) | Approval request |
| Remediation Required | Owner (CC: relevant owners) | Blocking issues and remediation |
| Not Ready | Owner (CC: Marketing Director) | Cannot proceed |
| Manual Review | Marketing Director (CC: Owner) | Requires human review |

### Failure Handling
- Word fails → preserve readiness in Excel, do NOT claim report exists
- Outlook fails → preserve assessment, do NOT claim notification sent

### Boundary
- Does NOT make readiness decisions — executes only after Supervisor validates

---

## Tool and Knowledge Scoping Summary

| Agent | Excel Tables | Knowledge | Other Tools |
|-------|-------------|-----------|-------------|
| Supervisor | Campaign_Requests (status updates) | Governance Policy | — |
| Budget Specialist | Campaign_Requests, Budget_Rules, Approval_Matrix | Governance Policy | — |
| Brand Specialist | Campaign_Requests, Asset_Status | Brand & Content Guidelines | — |
| Channel Specialist | Campaign_Requests, Channel_Requirements, Asset_Status | Governance Policy | — |
| Asset Specialist | Campaign_Requests, Asset_Status | Governance Policy | — |
| Risk Specialist | (none — receives data) | Governance Policy | — |
| Reporting Specialist | (none) | — | Word Online, Outlook |

Tools and knowledge are **scoped narrowly** to each agent's domain, following Microsoft's guidance to reduce orchestrator confusion.

---

## Screenshots

### All Child Agents Overview
![All Child Agents Overview](/screenshots/child_agent.png)

### Parallel Specialist Invocation
![Parallel Specialist Invocation](/screenshots/parlalel_specialist.png)

