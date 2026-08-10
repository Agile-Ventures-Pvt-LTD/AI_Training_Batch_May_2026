# Dataset Notes

## 1. Overview

The P2-005 solution uses a deliberately small synthetic dataset to support autonomous campaign-readiness assessment and testing in Microsoft Copilot Studio.

The supplied dataset contains:

- **6 Campaign Requests**
- **6 Budget Rules**
- **10 Channel Requirements**
- **24 Asset records**
- **7 Approval rules**
- **8 Synthetic stakeholders**
- **12 dataset-oriented test scenarios**
- **2 small knowledge documents**

The PRD states that the dataset is intentionally small and provides sufficient variation to test the required orchestration patterns. fileciteturn12file3L564-L602

---

## 2. Data Sources

The campaign-readiness workflow uses the following operational data sources.

### Campaign Requests

Used to retrieve campaign information and identify campaigns awaiting assessment.

The autonomous trigger filters for:

```text
CampaignStatus = Pending
```

and selects the oldest eligible Pending campaign. fileciteturn12file2L324-L336

The Intake & Validation topic uses campaign information including:

- Campaign ID
- Campaign name
- Product
- Launch date
- Budget values
- Geography
- Channels
- Campaign owner

It also validates uniqueness and campaign state. fileciteturn12file9L1364-L1413

---

## 3. Budget Rules

The Budget & Commercial Specialist uses:

- `Campaign_Requests`
- `Budget_Rules`
- `Approval_Matrix`

The specialist evaluates:

- Proposed budget
- Approved budget
- Budget variance
- Target CPL
- Expected leads
- Required financial approval
- Budget-related blocking conditions

fileciteturn12file0L11-L46

The PRD defines important business rules including:

- Proposed budget above approved budget → Marketing Director approval
- Proposed budget above INR 1,000,000 → VP Marketing approval
- Target CPL above INR 4,000 → VP Marketing approval

fileciteturn12file4L668-L674

---

## 4. Channel Requirements

The Channel Readiness Specialist uses:

- `Campaign Requests`
- `Channel Requirements`
- `Asset Status`

It evaluates **every channel listed for the campaign**.

The assessment includes:

- Mandatory channel assets
- Minimum lead time
- Tracking requirement
- Channel owner
- Brand approval requirement
- Missing channel prerequisites
- Channel-specific launch blockers

fileciteturn12file7L1022-L1039

The dataset contains **10 Channel Requirements** records. fileciteturn12file3L564-L573

---

## 5. Asset Status

The Asset Readiness Specialist evaluates:

- Mandatory assets
- Asset availability
- Asset approval status
- Missing assets
- Pending QA
- Pending approval
- Assets requiring changes
- Responsible owner

Each asset is classified as:

```text
Ready
Condition
Blocking
Missing
```

The specialist returns aggregate counts to the Supervisor. fileciteturn12file0L122-L139

The supplied dataset contains **24 Asset records**. fileciteturn12file3L564-L573

The PRD also defines these asset rules:

- Missing mandatory asset = blocking
- Needs Changes = blocking
- Pending Approval = blocking
- Pending QA may be a condition only where the policy permits it

fileciteturn12file4L674-L680

---

## 6. Approval Matrix

Approval information is used to determine when human approval is mandatory.

The Approval & Finalisation topic evaluates conditions including:

- Proposed budget > approved budget
- Proposed budget > INR 1,000,000
- Target CPL > INR 4,000
- High regulatory sensitivity
- Multi-market geography
- Restricted/quantified claims
- Urgent launch with unresolved approval

fileciteturn12file9L1453-L1474

The supplied dataset contains **7 Approval rules**. fileciteturn12file3L564-L573

The system must never fabricate a human approval.

---

## 7. Stakeholders

The dataset contains **8 synthetic stakeholders**. fileciteturn12file3L564-L573

Stakeholder information supports the identification of the appropriate owner or approver during campaign assessment.

The PRD also requires the Excel integration to retrieve stakeholders when required by the workflow. fileciteturn12file4L698-L710

---

## 8. Knowledge Documents

The PRD identifies two supplied knowledge documents:

### NovaSphere Marketing Governance Policy

Authoritative for:

- Readiness statuses
- Budget approval
- Timing
- Asset controls
- Geography
- Sensitivity
- Autonomous-processing rules
- Reassessment

### NovaSphere Brand & Content Guidelines

Authoritative for:

- Brand terminology
- Product naming
- Claims
- Evidence requirements
- Channel-content rules
- Brand review classification

fileciteturn12file8L1227-L1263

The Brand & Content Compliance Specialist must use the Brand & Content Guidelines as its mandatory knowledge source. fileciteturn12file0L84-L91

---

## 9. Dataset Scenario Coverage

The dataset intentionally contains variation for orchestration testing.

The PRD identifies:

1. **One near-ready campaign**
2. **One over-budget campaign**
3. **One remediation case**
4. **One high-sensitivity/high-budget case**
5. **One urgent campaign with missing assets**
6. **One multi-region approval case**

This variation is intended to provide sufficient coverage for the required orchestration patterns without requiring a large dataset. fileciteturn12file3L594-L602

---

## 10. Dataset and Autonomous Trigger

The Recurrence event trigger uses the Campaign Requests data to autonomously identify work.

The required logic is:

```text
Recurrence Trigger
       ↓
Retrieve Campaign Requests
       ↓
Find CampaignStatus = Pending
       ↓
Select Oldest Eligible Campaign
       ↓
Process One Campaign
       ↓
Update Status
       ↓
Begin Intake & Validation
```

The trigger must process only one campaign per execution and update its status before specialist analysis begins. fileciteturn12file2L324-L336

---

## 11. Dataset and Specialist Agents

### Budget & Commercial Specialist

Uses:

```text
Campaign_Requests
Budget_Rules
Approval_Matrix
```

fileciteturn12file0L30-L34

### Brand & Content Compliance Specialist

Uses:

```text
Campaign Requests
Asset Status
NovaSphere Brand & Content Guidelines
```

fileciteturn12file0L84-L91

### Channel Readiness Specialist

Uses:

```text
Campaign Requests
Channel Requirements
Asset Status
```

fileciteturn12file7L1034-L1039

### Asset Readiness Specialist

Uses the campaign asset information and evaluates asset readiness and classification. fileciteturn12file0L122-L139

### Launch Risk & Decision Specialist

Receives the consolidated outputs of the first four specialists together with:

- Days until launch
- Geography
- Sensitivity
- Pending approvals

fileciteturn12file0L140-L184

---

## 12. Dataset and Campaign States

The campaign state model includes:

```text
Pending
In Assessment
Awaiting Remediation
Awaiting Approval
Ready with Conditions
Ready
Not Ready
Manual Review
Completed
```

The system must prevent invalid state progression, such as:

```text
Pending → Ready
```

without completing the required assessment. fileciteturn12file2L337-L363

---

## 13. Dataset and Testing

The dataset is designed to support the required orchestration and business-logic tests.

Examples from the mandatory test coverage include:

- Valid Pending campaign
- Completed campaign / duplicate prevention
- Four independent specialist assessments
- Budget above approved budget
- Budget above INR 1,000,000
- High-sensitivity content
- Multiple channels

fileciteturn12file8L1340-L1353

The PRD requires at least **16 documented tests** overall. fileciteturn12file5L770-L790

---

## 14. Excel Storage Requirements

The operational workbook must be stored in:

- OneDrive for Business, or
- SharePoint

so that Copilot Studio can access the Excel tables through **Excel Online (Business)**. fileciteturn12file4L698-L710

Required Excel capabilities include:

- List campaign rows
- Retrieve relevant rules
- Retrieve assets
- Retrieve channel requirements
- Retrieve stakeholders
- Update campaign status

The PRD identifies the available Excel Online (Business) actions as:

- List rows present in a table
- Get a row
- Add a row into a table
- Update a row

`CampaignID` should be used as the primary logical key where applicable. fileciteturn12file4L698-L710

---

## 15. Data Integrity and Failure Handling

The implementation must handle:

- No Pending campaigns
- Duplicate CampaignID
- Missing campaign information
- Missing Excel row
- Specialist failure
- Conflicting specialist results
- Excel update delay/failure
- Missing approver
- Reassessment limit reached

The agent must not fabricate successful completion. fileciteturn12file8L1285-L1298

If data required for an assessment is unavailable, the system must not convert the missing evidence into an unsupported `Ready` result.

---

## 16. Synthetic Data Requirement

The PRD specifies that **only synthetic data must be used**. fileciteturn12file8L1331-L1339

The dataset is therefore intended for project development, testing, demonstration, and evaluation rather than production campaign processing.

---

## 17. Dataset Limitations

The dataset is intentionally small.

It contains only:

```text
6 Campaign Requests
6 Budget Rules
10 Channel Requirements
24 Asset Records
7 Approval Rules
8 Synthetic Stakeholders
12 Dataset-Oriented Test Scenarios
2 Knowledge Documents
```

Therefore, it is designed primarily to demonstrate the required orchestration patterns and business rules rather than large-scale performance.

The PRD explicitly states that the dataset is sufficient for testing the required patterns without requiring a large dataset. fileciteturn12file3L564-L602

---

## 18. Important Dataset Rules

1. Treat the supplied dataset as the operational source for campaign assessment.
2. Use `CampaignID` as the logical campaign identifier where applicable.
3. Do not invent missing campaign information.
4. Do not invent approvals.
5. Do not treat missing evidence as a successful assessment.
6. Evaluate every channel listed for a campaign.
7. Preserve specialist findings for traceability.
8. Respect the defined campaign-state model.
9. Apply governance rules to the supplied data.
10. Use only synthetic data.

These rules ensure that the dataset remains consistent with the P2-005 PRD and supports deterministic, traceable campaign-readiness assessment.
