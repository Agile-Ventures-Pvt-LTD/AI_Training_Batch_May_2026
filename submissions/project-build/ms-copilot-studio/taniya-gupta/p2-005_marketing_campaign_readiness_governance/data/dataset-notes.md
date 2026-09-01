# Dataset Notes - P2-005

## Overview
The dataset for **P2-005 (Marketing Campaign Readiness & Governance System)** consists of synthetic enterprise marketing data designed to validate multi-agent launch readiness logic for **NovaSphere Technologies Pvt. Ltd.**

---

## 1. Primary Data Sources

### A. Excel Workbook (`P2-005_Marketing_Campaign_Readiness_Lab_Data.xlsx`)
Contains 7 primary tables queried by the Supervisor and Specialist Child Agents via the Excel Online (Business) connector:

1. **`Campaign_Requests`**: Active campaign intake queue (18 columns: `CampaignID`, `CampaignName`, `Product`, `Objective`, `Geography`, `LaunchDate`, `ProposedBudget_INR`, `ApprovedBudget_INR`, `Channels`, `CampaignOwner`, `CampaignStatus`, etc.).
2. **`Budget_Rules`**: Financial threshold rules and variance limits across geographies and campaign types.
3. **`Approval_Matrix`**: Executive approval hierarchy mapping budget tiers and sensitivity levels to designated approver roles (`VP Marketing`, `Marketing Director`, `Regional Marketing Lead`, `Brand Governance Lead`).
4. **`Channel_Requirements`**: Minimum lead times, mandatory tracking tags (UTM/pixels), and channel prerequisites across Email, LinkedIn, Web, Paid Search, Webinar, and Event channels.
5. **`Asset_Status`**: Asset approval statuses, QA states, and missing asset flags across all campaign collateral.
6. **`Stakeholders`**: Contact information and email addresses for campaign owners and approvers.
7. **`Budget_Allocation`**: Channel-level budget distribution data.

---

## 2. Knowledge Source Documents (OneDrive Attached)

1. **`NovaSphere_Marketing_Governance_Policy.docx`**: Authoritative policy document governing launch readiness criteria, lead times, approval matrices, and decision precedence.
2. **`NovaSphere_Brand_and_Content_Guidelines.docx`**: Authoritative brand guidelines specifying restricted outcome claims, mandatory disclaimers, and regulatory compliance rules.

---

