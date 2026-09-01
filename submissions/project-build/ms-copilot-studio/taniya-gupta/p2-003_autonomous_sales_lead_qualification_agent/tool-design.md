# tool-design.md — Tool Design
## P2-003 Autonomous Sales Lead Qualification Agent

---

## Tool Overview

The agent uses **9 tools** configured inside Microsoft Copilot Studio. All tools use the Connector type and are available exclusively to the Sales Lead Qualification Agent. All tools were last modified during the project build session.

The exact tool list as it appears in Copilot Studio:

| Tool Name | Type | Trigger |
|---|---|---|
| Add a row into a table | Connector | By agent |
| List Rows - Territory Owners | Connector | By agent |
| List Rows - Leads Register | Connector | By agent |
| List Rows - Product Catalog | Connector | By agent |
| List Rows - Qualification Rules | Connector | By agent |
| List Rows - Action Matrix | Connector | By agent |
| Update a row | Connector | By agent |
| Send an email (V2) | Connector | By agent |
| Create a Microsoft Word document with the given content | Connector | By agent |

---

## Tool 1 — Add a row into a table

**Connector:** Excel Online (Business)
**Purpose:** Log a new lead record to LeadsRegisterTable after a new, non-duplicate lead is processed.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| Location | Custom value | OneDrive for Business |
| Document Library | Custom value | OneDrive |
| File | Custom value | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table | Custom value | LeadsRegisterTable |
| Row | Dynamically fill with AI | Agent generates the full JSON row |

**Action boundaries:**
- Only called after duplicate check confirms no existing record
- Not called for Duplicate, Not-a-Sales-Lead, or non-sales inquiry paths
- If the tool fails, the agent retries once then records Processing_Status as Failed

---

## Tool 2 — List Rows - Territory Owners

**Connector:** Excel Online (Business)
**Purpose:** Look up the assigned owner and territory status for the lead's country from TerritoryOwnersTable.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| Location | Custom value | OneDrive for Business |
| Document Library | Custom value | OneDrive |
| File | Custom value | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table | Custom value | TerritoryOwnersTable |

**Action boundaries:**
- Called during Step 8 (owner assignment)
- Returns: Territory, Default_Owner, Owner_Email, Territory_Status, Autonomous_Assignment_Allowed
- If Autonomous_Assignment_Allowed = 0, lead is routed to Human Review Required

---

## Tool 3 — List Rows - Leads Register

**Connector:** Excel Online (Business)
**Purpose:** Search LeadsRegisterTable for an existing record to perform duplicate detection before any new record is created.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| Location | Custom value | OneDrive for Business |
| Document Library | Custom value | OneDrive |
| File | Custom value | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table | Custom value | LeadsRegisterTable |
| Filter Query | Dynamically fill with AI | Agent filters by Company_Name and Contact_Name |

**Action boundaries:**
- Called at Step 3 for every sales inquiry before any other action
- Result is used only for duplicate detection — no data sent externally
- Checks for matches within the last 90 days

---

## Tool 4 — List Rows - Product Catalog

**Connector:** Excel Online (Business)
**Purpose:** Look up the product minimum budget and product fit category for the lead's stated product interest from ProductCatalogTable.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| Location | Custom value | OneDrive for Business |
| Document Library | Custom value | OneDrive |
| File | Custom value | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table | Custom value | ProductCatalogTable |

**Action boundaries:**
- Used during scoring to determine Product Fit band and Budget vs Minimum band
- If the product cannot be matched, an Unknown Product flag is raised

---

## Tool 5 — List Rows - Qualification Rules

**Connector:** Excel Online (Business)
**Purpose:** Read the scoring bands from QualificationRulesTable to support accurate dimension-by-dimension scoring.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| Location | Custom value | OneDrive for Business |
| Document Library | Custom value | OneDrive |
| File | Custom value | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table | Custom value | QualificationRulesTable |

**Action boundaries:**
- Referenced during Step 5 (scoring) to apply the correct point values per dimension and band
- Read-only — never writes data

---

## Tool 6 — List Rows - Action Matrix

**Connector:** Excel Online (Business)
**Purpose:** Look up the required autonomous actions for each classification outcome from ActionMatrixTable.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| Location | Custom value | OneDrive for Business |
| Document Library | Custom value | OneDrive |
| File | Custom value | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table | Custom value | ActionMatrixTable |

**Action boundaries:**
- Referenced during Step 9 (action execution) to confirm which tools to invoke for each classification
- Read-only — never writes data

---

## Tool 7 — Update a row

**Connector:** Excel Online (Business)
**Purpose:** Update an existing Excel row when a duplicate is detected, or to record a tool failure status.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| Location | Custom value | OneDrive for Business |
| Document Library | Custom value | OneDrive |
| File | Custom value | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table | Custom value | LeadsRegisterTable |
| Key Column | Custom value | Lead_ID |
| Key Value | Dynamically fill with AI | Agent supplies the matching Lead_ID |
| Item Properties | Dynamically fill with AI | Agent supplies the updated field values |

**Action boundaries:**
- Used for duplicate records (updates Last_Action timestamp on existing row)
- Used when a tool failure occurs (updates Processing_Status to Failed)
- Does not create new records — only updates existing ones

---

## Tool 8 — Send an email (V2)

**Connector:** Office 365 Outlook
**Purpose:** Send external acknowledgements to lead senders and internal notifications to assigned owners and Sales Operations.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| To | Dynamically fill with AI | Derived from Sender Email or owner lookup |
| Subject | Dynamically fill with AI | Agent generates contextual subject |
| Body | Dynamically fill with AI | Agent composes appropriate content |

**Email types sent by the agent:**

| Email Type | Recipient | When |
|---|---|---|
| Lead receipt acknowledgement | Sender | Hot and Qualified leads |
| Internal hot lead alert | Assigned Owner + Sales Operations | Hot leads |
| Internal qualified lead notification | Assigned Owner only | Qualified leads |
| Nurture acknowledgement | Sender | Nurture leads |
| Missing information request | Sender | Additional Information Required |
| Human review alert | Sales Operations only | Human Review Required |
| Tool failure notification | Sales Operations | Any tool failure after retry |

**Action boundaries:**
- External emails never contain qualification scores, internal classifications, pricing, or delivery timelines
- The agent never sends a qualification result externally for Human Review Required leads
- If the tool fails, the agent retries once, records the failure in Excel, and notifies Sales Operations

---

## Tool 9 — Create a Microsoft Word document with the given content

**Connector:** Word Online (Business)
**Purpose:** Generate a structured lead qualification report for Hot and Qualified leads.

**Configuration:**
| Input | Setting | Value |
|---|---|---|
| File Name | Dynamically fill with AI | Agent generates e.g. Lead_Qualification_Report_LD-2026-0009.docx |
| File Content | Dynamically fill with AI | Agent writes the full report using the required structure |
| Folder Path | Root OneDrive folder | Reports are saved to root directory |

**Report sections generated:**
1. Report Date and Lead ID
2. Contact and Organisation details
3. Opportunity Summary (product, budget, timeline, business need)
4. Qualification Score Breakdown (all 8 dimensions)
5. Classification and Confidence Level
6. Missing Information and Duplicate Result
7. Risk and Exception Flags
8. Assigned Owner and Territory
9. Recommended Next Action
10. Disclaimer: Preliminary autonomous assessment subject to internal review

**Action boundaries:**
- Only called for Hot and Qualified classifications
- Never called for Nurture, Low Priority, Human Review, Additional Info, Duplicate, or Non-Sales paths
- If the tool fails, the agent retries once, records Processing_Status as Failed in Excel, and notifies Sales Operations
- Word reports are saved to the root OneDrive folder (not a subfolder) due to a connector path limitation

---

Note : Each tool was configured with a description in Copilot Studio to guide the generative orchestrator. The description ensures that the generative model knows when and how to use each tool correctly.