# Qualification Logic

## P2-003 Autonomous Sales Lead Qualification Agent

## Purpose

This document defines the qualification methodology used by the **NovaWorks Autonomous Sales Lead Qualification Agent** implemented in **Microsoft Copilot Studio**.

The qualification logic determines whether an incoming email is a valid sales opportunity, calculates a standardized qualification score, assigns a business classification, routes the lead to the appropriate sales owner, and determines the autonomous actions that the agent may perform.

The design follows the P2-003 Product Requirements Document (PRD) and emphasizes deterministic scoring, duplicate-safe processing, auditable decision making, and controlled autonomy.

---

# Qualification objectives

The qualification engine is designed to:

* identify genuine sales opportunities
* normalize extracted business information
* prevent duplicate opportunities
* apply consistent scoring
* assign ownership based on territory
* determine follow-up priority
* protect against low-confidence autonomous decisions

---

# Qualification workflow

```text
Incoming Email
       |
       v
Lead Validation
       |
       v
Duplicate Detection
       |
       v
Information Extraction
       |
       v
Normalization
       |
       v
Reference Table Lookup
       |
       v
Score Calculation
       |
       v
Classification
       |
       v
Override Evaluation
       |
       v
Owner Assignment
       |
       v
Autonomous Decision
```

---

# Lead validation

The email is considered a potential sales lead when it contains evidence of commercial interest in NovaWorks products or services.

Indicators include:

* product inquiries
* solution evaluations
* pricing requests
* procurement discussions
* implementation planning
* enterprise transformation initiatives

The following are not considered sales leads:

* support requests
* recruitment
* internship applications
* academic research
* competitor research
* vendor outreach
* spam
* unrelated communications

---

# Required extracted fields

## Source information

* Source_Message_ID
* Sender_Email
* Received_Date
* Lead_Source

## Contact information

* Contact_Name
* Job_Title
* Decision_Role

## Organization information

* Company_Name
* Country_Region
* Territory
* Company_Size
* Industry

## Opportunity information

* Product_Interest
* Business_Need
* Stated_Budget
* Purchase_Timeline

## Assessment information

* Confidence
* Missing_Fields
* Product_Fit
* Risk_Flags

---

# Data normalization

Before scoring, extracted values are standardized using the operational reference tables.

## Country normalization

Country names are mapped to **TerritoryOwnersTable** values.

Examples:

* USA → United States
* UK → United Kingdom
* UAE → United Arab Emirates

Unknown countries trigger a territory exception.

---

## Product normalization

Product references are mapped to **ProductCatalogTable**.

Examples:

* CRM Suite
* Analytics Platform
* ERP Integration
* Supply Chain Suite

Unknown products trigger human review.

---

## Company size normalization

Allowed values:

* Enterprise
* Mid-Market
* SMB
* Startup/Micro

---

## Decision role normalization

Allowed values:

* Decision Maker
* Strong Influencer
* Researcher/User
* Unknown

---

# Duplicate detection

Duplicate detection occurs before scoring.

## Exact duplicate

Match:

* Source_Message_ID

If matched:

* update existing record
* do not create a new lead
* do not create another Word report
* do not send another acknowledgement

Classification:

* Duplicate

---

## Probable duplicate

Compare:

* Sender_Email
* Company_Name
* Product_Interest
* recent lead records

If a probable duplicate is confirmed:

* update the existing record
* preserve the original Lead_ID
* record the latest activity

---

# Qualification scoring framework

The total qualification score ranges from **0 to 100**.

| Dimension                | Maximum Points |
| ------------------------ | -------------- |
| Product Fit              | 20             |
| Budget Viability         | 20             |
| Purchase Timeline        | 15             |
| Decision Role            | 15             |
| Company Size             | 10             |
| Territory                | 10             |
| Lead Source              | 5              |
| Information Completeness | 5              |
| **Total**                | **100**        |

Scoring values are retrieved from **QualificationRulesTable**.

The agent does not generate scoring values independently.

---

# Dimension evaluation

## Product fit (20)

Evaluates alignment between the prospect's stated need and NovaWorks offerings.

Strong product alignment receives the highest score.

Unknown products receive minimal points.

---

## Budget viability (20)

Evaluates whether the stated budget is commercially viable.

Unknown budgets remain **Unknown** and are not treated as zero.

---

## Purchase timeline (15)

Evaluates urgency.

Typical order:

* Immediate
* 1–3 months
* 3–6 months
* 6–12 months
* Unknown

---

## Decision role (15)

Higher authority increases qualification strength.

Typical weighting:

* Decision Maker
* Strong Influencer
* Researcher/User
* Unknown

---

## Company size (10)

Larger organizations generally receive higher strategic weighting.

Typical order:

* Enterprise
* Mid-Market
* SMB
* Startup/Micro

---

## Territory (10)

Mapped through **TerritoryOwnersTable**.

Supported territories receive higher operational readiness scores.

Unmapped territories trigger human review.

---

## Lead source (5)

Priority sources receive higher weighting.

Examples:

* customer referral
* strategic partner
* direct enterprise inquiry

---

## Information completeness (5)

Rewards complete business information.

Typical factors:

* contact name
* company
* product
* budget
* timeline

---

# Classification thresholds

After scoring, the lead is classified using deterministic thresholds.

| Classification                  | Rule                                   |
| ------------------------------- | -------------------------------------- |
| Hot                             | 85–100                                 |
| Qualified                       | 70–84                                  |
| Nurture                         | 50–69                                  |
| Low Priority                    | Below 50                               |
| Additional Information Required | Three or more mandatory fields missing |
| Human Review Required           | Exception condition                    |
| Duplicate                       | Existing opportunity                   |
| Not a Sales Lead                | Non-sales inquiry                      |

---

# Override rules

Overrides are evaluated after score calculation.

## Additional Information Required

Apply when three or more mandatory fields are missing.

The agent:

* creates an incomplete record
* requests missing information
* does not generate a final report

---

## Human Review Required

Apply when:

* confidence is low
* territory is unmapped
* product is unknown
* extracted information conflicts
* competitor involvement is detected
* tool uncertainty exists

The agent must:

* create or update the record
* notify Sales Operations
* withhold external qualification communication

---

## Startup budget override

If a Startup/Micro lead has a budget significantly below the minimum commercial threshold:

Classification:

* Low Priority

This override applies regardless of the calculated score.

---

# Confidence evaluation

The confidence score reflects extraction reliability.

Factors:

* explicit email evidence
* successful normalization
* reference table matches
* completeness
* consistency

Low confidence prevents autonomous qualification communication.

---

# Owner assignment logic

After classification, the agent assigns ownership using **TerritoryOwnersTable**.

Mapping process:

```text
Country
    |
    v
Territory
    |
    v
Assigned Sales Owner
    |
    v
Sales Owner Email
```

If no owner is available:

* Human Review Required
* notify Sales Operations
* withhold owner notification

---

# Autonomous decision matrix

| Classification                  | Excel         | Word | External Email       | Internal Notification |
| ------------------------------- | ------------- | ---- | -------------------- | --------------------- |
| Hot                             | Create        | Yes  | Yes                  | Owner + Sales Ops     |
| Qualified                       | Create        | Yes  | Yes                  | Owner                 |
| Nurture                         | Create        | No   | Yes                  | No                    |
| Low Priority                    | Create        | No   | Conditional          | No                    |
| Additional Information Required | Create        | No   | Missing Info Request | No                    |
| Human Review Required           | Create/Update | No   | No                   | Sales Ops             |
| Duplicate                       | Update        | No   | No                   | No                    |
| Not a Sales Lead                | No            | No   | No                   | No                    |

---

# Word report eligibility

Generate a report only for:

* Hot
* Qualified

The report includes:

* lead summary
* score breakdown
* classification
* confidence
* owner assignment
* recommended action

---

# Missing information policy

Unknown values remain **Unknown**.

The agent must not:

* invent budgets
* invent timelines
* infer authority without evidence
* fabricate organization information

---

# Audit requirements

Every qualification decision records:

* Lead_ID
* score
* classification
* owner
* confidence
* duplicate result
* rule overrides
* autonomous actions
* withheld actions
* processing status

---

# Failure handling

If required reference data cannot be retrieved:

* retry once
* notify Sales Operations
* stop dependent autonomous actions
* do not report success

---

# Decision examples

## Example 1: Hot

Enterprise organization

Decision Maker

Budget available

Immediate timeline

Strong product fit

Score: 92

Classification: Hot

Actions:

* create record
* generate report
* notify owner
* notify Sales Operations
* send acknowledgement

---

## Example 2: Qualified

Mid-Market

Strong Influencer

Budget available

3-month timeline

Score: 78

Classification: Qualified

Actions:

* create record
* generate report
* notify owner
* send acknowledgement

---

## Example 3: Human Review Required

Unknown product

Unmapped territory

Conflicting budget information

Score: 81

Classification: Human Review Required

Actions:

* create record
* notify Sales Operations
* withhold external qualification

---

## Example 4: Duplicate

Existing Source_Message_ID found.

Actions:

* update existing record
* no new report
* no acknowledgement

---

# Design rationale

The qualification engine combines:

* deterministic Excel-based rules
* structured AI extraction
* normalization
* duplicate prevention
* controlled autonomous execution
* explicit human-review boundaries

This architecture minimizes hallucination risk, improves consistency, supports repeatable testing, and provides enterprise-grade auditability.

---

# PRD compliance

| Requirement               | Status   |
| ------------------------- | -------- |
| Lead extraction           | Complete |
| Normalization             | Complete |
| Duplicate detection       | Complete |
| Qualification scoring     | Complete |
| Classification thresholds | Complete |
| Override rules            | Complete |
| Owner assignment          | Complete |
| Human review routing      | Complete |
| Word report conditions    | Complete |
| Autonomous decision paths | Complete |
| Auditability              | Complete |

---

# Final status

The qualification logic provides a deterministic and auditable scoring and classification framework for the NovaWorks Autonomous Sales Lead Qualification Agent. The implementation satisfies the P2-003 PRD requirements for extraction, normalization, duplicate prevention, qualification scoring, owner assignment, controlled autonomy, and human-in-the-loop governance.
