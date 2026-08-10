# Supervisor Agent Design

## Project

**Marketing Campaign Readiness Governance**

---

# Agent Overview

The **Campaign Readiness Supervisor** is the primary orchestration agent within the Marketing Campaign Readiness Governance solution.

It coordinates the complete campaign readiness lifecycle by validating campaign information, invoking specialist agents, managing remediation and approval workflows, consolidating assessment results, and determining the final readiness status.

The Supervisor acts as the central decision-making component while delegating domain-specific analysis to specialist agents.

---

# Purpose

The Campaign Readiness Supervisor is responsible for:

- Receiving campaign assessment requests.
- Performing deterministic campaign validation.
- Coordinating specialist AI agents.
- Managing campaign remediation.
- Managing approval workflows.
- Determining campaign readiness.
- Updating campaign records.
- Returning the final readiness decision.

---

# Responsibilities

The Supervisor performs the following business functions.

## Campaign Intake

- Receive campaign request.
- Load campaign information from Excel.
- Verify campaign exists.

---

## Validation

Execute Topic 1:

Campaign Intake & Validation

Validation includes:

- Campaign ID
- Campaign Status
- Campaign Name
- Product
- Launch Date
- Budget
- Geography
- Channels
- Campaign Owner

Only validated campaigns continue.

---

## Specialist Coordination

The Supervisor sequentially invokes six specialist agents.

Execution order:

1. Budget & Commercial Specialist
2. Brand & Content Compliance Specialist
3. Asset Readiness Specialist
4. Channel Readiness Specialist
5. Launch Risk & Decision Specialist
6. Reporting & Communication Specialist

The Supervisor waits for each specialist to complete before invoking the next.

---

## Remediation Management

When specialist failures occur:

Execute:

Topic 2

Remediation & Selective Reassessment

The Supervisor:

- Preserves successful specialist assessments.
- Reruns only failed specialist domains.
- Tracks reassessment cycles.
- Escalates to Manual Review after two unsuccessful reassessments.

---

## Approval Management

When approval rules are triggered:

Execute:

Topic 3

Approval & Finalisation

The Supervisor:

- Blocks Ready status.
- Assigns Awaiting Approval.
- Waits for human approval.
- Prevents fabricated approvals.

---

## Final Readiness

After all assessments complete, the Supervisor determines the campaign readiness outcome.

Possible outcomes:

- Ready
- Ready with Conditions
- Remediation Required
- Management Approval Required
- Not Ready

The highest-priority outcome always wins.

---

# Inputs

The Supervisor receives the following campaign information.

| Input | Description |
|---------|-------------|
| CampaignID | Unique campaign identifier |
| CampaignName | Campaign name |
| Product | Product being marketed |
| CampaignStatus | Current workflow state |
| ProposedBudget | Requested campaign budget |
| ApprovedBudget | Approved campaign budget |
| TargetCPL | Target Cost Per Lead |
| Geography | Target region |
| RegulatorySensitivity | Regulatory classification |
| CampaignOwner | Campaign owner |

---

# Outputs

The Supervisor produces:

| Output | Description |
|----------|-------------|
| Validation Result | Pass or Fail |
| Specialist Results | Individual assessment results |
| Approval Status | Required or Not Required |
| Remediation Status | Required or Not Required |
| Final Readiness | Final campaign decision |
| Updated Campaign Status | Updated Excel record |

---

# Tools Used

The Supervisor uses the following Microsoft connectors.

## Excel Online (Business)

### List Rows

Retrieve campaign requests.

---

### Get Row

Retrieve campaign details.

---

### Update Row

Update campaign status.

Examples:

- Pending
- In Assessment
- Awaiting Approval
- Awaiting Remediation
- Manual Review
- Ready

---

# Custom Topics

The Supervisor executes three custom topics.

---

## Topic 1

Campaign Intake & Validation

Purpose:

Validate campaign information before assessment.

---

## Topic 2

Remediation & Selective Reassessment

Purpose:

Coordinate remediation and selective reassessment.

---

## Topic 3

Approval & Finalisation

Purpose:

Handle mandatory management approval.

---

# Orchestration Flow

```
Campaign Request

↓

Topic 1

↓

Budget Specialist

↓

Brand Specialist

↓

Asset Specialist

↓

Channel Specialist

↓

Launch Risk Specialist

↓

Reporting Specialist

↓

Topic 2 (If Required)

↓

Topic 3 (If Required)

↓

Final Readiness Decision

↓

Update Campaign Status

↓

End
```

---

# Decision Logic

The Supervisor follows mandatory precedence.

Priority:

1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready with Conditions
5. Ready

The Supervisor never averages specialist assessments.

Example:

Budget

Pass

Brand

Blocked

Assets

Pass

Final Result

Not Ready

---

# Error Handling

The Supervisor immediately terminates processing when:

- Campaign does not exist.
- Validation fails.
- Campaign status is invalid.
- Mandatory data is missing.

Campaigns requiring remediation or approval follow their respective workflow topics.

---

# State Management

Campaign lifecycle:

```
Pending

↓

In Assessment

↓

Awaiting Approval

OR

Awaiting Remediation

↓

Manual Review

↓

Ready
```

Campaign status updates are persisted to Excel after every major workflow transition.

---

# Benefits

The Supervisor provides:

- Centralized orchestration
- Deterministic execution
- Modular workflow management
- Enterprise governance
- Human approval integration
- Scalable architecture
- Reduced manual intervention

---

# Conclusion

The Campaign Readiness Supervisor serves as the central orchestration engine of the Marketing Campaign Readiness Governance solution. By coordinating specialist agents, executing governance topics, and enforcing business rules, it ensures campaigns are consistently evaluated before launch while maintaining transparency, scalability, and compliance.