# P2-005 --- Autonomous Marketing Campaign Launch Readiness & Governance System

## 1. Project Overview

**Project ID:** P2-005\
**Project:** Autonomous Marketing Campaign Launch Readiness & Governance
System\
**Platform:** Microsoft Copilot Studio\
**Project Type:** Individual Project Build\
**Duration:** 4 Hours\
**Architecture:** Autonomous Multi-Agent System\
**AI Usage:** Permitted\
**PRD Version:** Draft 1.0

This project implements an autonomous campaign-readiness governance
system for NovaSphere Technologies Pvt. Ltd. The system evaluates
whether a marketing campaign is ready for launch by coordinating
campaign validation, independent specialist assessments, governance
checks, remediation, approvals, final readiness classification,
reporting, and conditional stakeholder communication.

The solution is required to operate through Microsoft Copilot Studio and
demonstrate sequential, parallel fan-out/fan-in, hierarchical,
conditional, reassessment-loop, and fallback/escalation orchestration
patterns.

------------------------------------------------------------------------

## 2. Business Scenario

NovaSphere Technologies Pvt. Ltd. runs digital marketing campaigns
across channels such as:

-   Email
-   LinkedIn
-   Web
-   Paid search
-   Webinars
-   Events

Before launch, campaigns must be reviewed for:

-   Budget approval
-   Commercial viability
-   Mandatory assets
-   Brand compliance
-   Content approval
-   Channel readiness
-   Geographic approvals
-   Campaign timing
-   Tracking readiness
-   Claims and disclaimers
-   Stakeholder ownership
-   Required executive approvals

The purpose of this solution is to coordinate these reviews
autonomously, identify blocking and non-blocking findings, determine the
appropriate readiness status, create remediation actions, and
communicate the validated result.

------------------------------------------------------------------------

## 3. Project Objectives

The solution must be capable of:

1.  Identifying a campaign awaiting assessment.
2.  Validating mandatory campaign information.
3.  Preventing duplicate assessments.
4.  Marking a campaign as `In Assessment`.
5.  Delegating independent assessments to specialist agents.
6.  Consolidating specialist results.
7.  Detecting blocking and non-blocking findings.
8.  Applying governance-policy precedence.
9.  Identifying mandatory human approvals.
10. Creating remediation actions.
11. Selectively reassessing corrected domains.
12. Determining the final readiness outcome.
13. Updating operational data in Excel.
14. Creating a Word Campaign Launch Readiness Report.
15. Sending an Outlook notification after Supervisor approval.
16. Handling incomplete, conflicting, or failed specialist outputs
    safely.

------------------------------------------------------------------------

## 4. Required Architecture

The required logical architecture is:

``` text
Recurrence Trigger
       |
       v
Campaign Readiness Supervisor
       |
       v
Campaign Intake & Validation
       |
       v
Campaign Validated?
    /        \
  No          Yes
  |            |
Reject/Hold    Mark "In Assessment"
               |
       +-------+-------+-------+
       |       |       |       |
       v       v       v       v
    Budget   Brand   Channel  Asset
 Specialist Specialist Specialist Specialist
       |       |       |       |
       +-------+-------+-------+
               |
               v
       Supervisor Fan-In
               |
               v
    Launch Risk & Decision
               |
       +-------+-------+
       |       |       |
       v       v       v
     Ready Remediation Approval
              |         |
              v         |
        Reassessment    |
              |         |
              +---------+
                   |
                   v
          Supervisor Validation
                   |
                   v
      Reporting & Communication
             /          \
            v            v
          Word        Outlook
             \          /
              \        /
               v      v
             Excel Register
```

The required orchestration stages must not be removed.

------------------------------------------------------------------------

## 5. Orchestration Patterns

### 5.1 Sequential

Required sequence:

``` text
Trigger
→ Intake Validation
→ Specialist Assessments
→ Fan-In Consolidation
→ Risk Decision
→ Remediation/Approval
→ Final Validation
→ Reporting
→ Notification
```

Later stages must not execute before their required earlier stages have
completed.

Examples:

-   Specialist analysis must not occur before campaign validation.
-   Reporting must not occur before readiness is determined.
-   Outlook notification must not occur before Supervisor validation.

### 5.2 Parallel Fan-Out/Fan-In

After successful campaign validation, four independent specialist agents
assess the same campaign:

1.  Budget & Commercial Specialist
2.  Brand & Content Compliance Specialist
3.  Channel Readiness Specialist
4.  Asset Readiness Specialist

The Supervisor must wait for all mandatory specialist results before
final consolidation.

### 5.3 Hierarchical

The architecture is:

``` text
Supervisor Agent
       |
       +-- Budget Specialist
       +-- Brand Specialist
       +-- Channel Specialist
       +-- Asset Specialist
       +-- Risk & Decision Specialist
       +-- Reporting & Communication Specialist
```

The Supervisor owns:

-   Overall orchestration
-   Final readiness classification
-   Conflict resolution
-   Reassessment decisions
-   Final Word generation authorization
-   Outlook communication authorization

Child agents return findings and must not independently issue the final
readiness decision.

### 5.4 Conditional Routing

Examples include:

-   High-sensitivity campaign → additional brand/content and management
    review.
-   Budget above approved amount → approval path.
-   Multi-region campaign → regional approval.
-   Missing mandatory asset → remediation.
-   No blocking findings → final readiness.
-   Specialist failure → retry/fallback path.

### 5.5 Reassessment Loop

The required pattern is:

``` text
Failure
   ↓
Remediation
   ↓
Data Correction
   ↓
Selective Specialist Reassessment
   ↓
Supervisor Recalculation
```

Only affected domains should be reassessed.

A maximum of **two automated reassessment cycles** is permitted. After
two unsuccessful cycles, the campaign must enter `Manual Review`.

### 5.6 Fallback and Escalation

If a specialist:

-   Does not respond,
-   Returns unusable information,
-   Cannot access required data, or
-   Produces insufficient evidence,

the Supervisor must:

1.  Retry the specialist once.
2.  If unsuccessful, mark that domain as insufficient evidence.
3.  Prevent an unsupported `Ready` classification.
4.  Route the campaign for manual review.

------------------------------------------------------------------------

## 6. Autonomous Recurrence Trigger

The solution must use a **Recurrence event trigger directly in Microsoft
Copilot Studio**.

A separate Power Automate workflow is not required for the core
solution.

On every recurrence:

1.  Retrieve Campaign Requests from Excel.
2.  Identify campaigns where `CampaignStatus = Pending`.
3.  Select the oldest eligible Pending campaign.
4.  Process only one campaign per trigger execution.
5.  Update its status before specialist analysis begins.

During development, a short testing interval may be used.

This mechanism is intended to prevent duplicate concurrent assessment.

------------------------------------------------------------------------

## 7. Campaign State Model

The solution must use these campaign states:

  -----------------------------------------------------------------------
  State                               Meaning
  ----------------------------------- -----------------------------------
  `Pending`                           Awaiting assessment

  `In Assessment`                     Autonomous assessment currently
                                      active

  `Awaiting Remediation`              Blocking issues require correction

  `Awaiting Approval`                 Mandatory human approval is
                                      outstanding

  `Ready with Conditions`             Only permitted non-blocking
                                      conditions remain

  `Ready`                             All mandatory requirements are
                                      satisfied

  `Not Ready`                         Launch cannot proceed

  `Manual Review`                     Insufficient evidence or unresolved
                                      system failure

  `Completed`                         Final assessment and communication
                                      completed
  -----------------------------------------------------------------------

Invalid state progression must be prevented. For example, a campaign
must not move directly from `Pending` to `Ready` without assessment.

------------------------------------------------------------------------

## 8. Campaign Readiness Supervisor

The Supervisor is the central orchestration component.

### Responsibilities

-   Receive the campaign selected by the recurrence trigger.
-   Coordinate intake validation.
-   Prevent duplicate processing.
-   Mark the campaign as `In Assessment`.
-   Invoke the four domain specialists.
-   Wait for required specialist results.
-   Consolidate results.
-   Invoke Launch Risk & Decision.
-   Resolve conflicts between specialist findings.
-   Decide whether remediation or approval is required.
-   Control selective reassessment.
-   Validate the final readiness classification.
-   Authorize Word report generation.
-   Authorize Outlook communication.

The Supervisor is the **only component permitted to assign the final
readiness classification**.

------------------------------------------------------------------------

## 9. Specialist Agents

### 9.1 Budget & Commercial Specialist

#### Responsibilities

Evaluate:

-   Proposed budget
-   Approved budget
-   Budget variance
-   Target CPL
-   Expected leads
-   Required financial approval
-   Budget-related blocking conditions

#### Data Sources

-   `Campaign_Requests`
-   `Budget_Rules`
-   `Approval_Matrix`

#### Required Output

-   Assessment status
-   Proposed budget
-   Approved budget
-   Variance
-   CPL assessment
-   Approval required
-   Required approver
-   Blocking issues
-   Recommended action
-   Evidence used

------------------------------------------------------------------------

### 9.2 Brand & Content Compliance Specialist

#### Responsibilities

Evaluate:

-   Product naming
-   Campaign claims
-   Regulatory sensitivity
-   Required disclaimers
-   Brand approval
-   Restricted or unsupported claims
-   CTA consistency
-   External agency implications

#### Knowledge Source

-   `NovaSphere Brand & Content Guidelines`

#### Data Sources

-   Campaign Requests
-   Asset Status

This specialist must not perform budget or channel-operational analysis.

------------------------------------------------------------------------

### 9.3 Channel Readiness Specialist

#### Responsibilities

Evaluate **every channel** listed for the campaign.

Determine:

-   Mandatory channel assets
-   Minimum lead time
-   Tracking requirement
-   Channel owner
-   Brand approval requirement
-   Missing channel prerequisite
-   Channel-specific launch blocker

#### Data Sources

-   Campaign Requests
-   Channel Requirements
-   Asset Status

The specialist must evaluate all campaign channels, not only the first
channel.

------------------------------------------------------------------------

### 9.4 Asset Readiness Specialist

#### Responsibilities

Evaluate:

-   Mandatory assets
-   Asset availability
-   Asset approval status
-   Missing assets
-   Pending QA
-   Pending approval
-   Assets requiring changes
-   Responsible owner

Each asset must be classified as:

-   `Ready`
-   `Condition`
-   `Blocking`
-   `Missing`

The specialist must return aggregate counts to the Supervisor.

------------------------------------------------------------------------

### 9.5 Launch Risk & Decision Specialist

This specialist runs after the first four specialists and therefore
belongs to the sequential stage following parallel fan-in.

#### Inputs

-   Budget result
-   Brand result
-   Channel result
-   Asset result
-   Days until launch
-   Geography
-   Sensitivity
-   Pending approvals

#### Responsibilities

Identify:

-   Blocking issues
-   Non-blocking conditions
-   Approval requirements
-   Timing risk
-   Unresolved evidence
-   Campaign risk level

Risk levels:

-   Low
-   Medium
-   High
-   Critical

The specialist proposes a readiness outcome, but the Supervisor must
validate it.

------------------------------------------------------------------------

### 9.6 Reporting & Communication Specialist

This specialist executes only after Supervisor validation.

#### Word Report

The Campaign Launch Readiness Report must contain:

-   Campaign ID
-   Campaign name
-   Objective
-   Launch date
-   Days to launch
-   Budget assessment
-   Brand assessment
-   Channel assessment
-   Asset assessment
-   Blocking gaps
-   Conditions
-   Required approvals
-   Risk classification
-   Final readiness status
-   Remediation actions
-   Recommended next steps

#### Outlook

After Supervisor approval, send the appropriate stakeholder
notification.

The notification must differ according to the final outcome.

------------------------------------------------------------------------

## 10. Standard Specialist Output Contract

All specialists should return equivalent semantic information:

  -----------------------------------------------------------------------
  Output                              Requirement
  ----------------------------------- -----------------------------------
  `SpecialistName`                    Name of specialist

  `AssessmentStatus`                  Pass / Condition / Block /
                                      Insufficient Evidence

  `EvidenceSummary`                   Information used

  `BlockingIssues`                    Blocking findings

  `Conditions`                        Non-blocking findings

  `RequiredActions`                   Required remediation

  `RequiredApprover`                  Human approver where applicable

  `Confidence`                        High / Medium / Low

  `Completed`                         Yes / No
  -----------------------------------------------------------------------

Different variable names may be used, but the semantic structure should
remain consistent.

------------------------------------------------------------------------

## 11. Custom Topics

### Topic 1 --- Campaign Intake & Validation

The topic performs deterministic pre-assessment validation before child
agents are invoked.

It must validate:

-   Campaign ID exists
-   Campaign ID is unique
-   Campaign status is Pending
-   Campaign name exists
-   Product exists
-   Launch date exists
-   Launch date is not in the past
-   Budget values exist
-   Geography exists
-   At least one channel exists
-   Campaign owner exists

Required equivalent variables include:

-   CampaignID
-   CampaignName
-   Product
-   LaunchDate
-   DaysToLaunch
-   ProposedBudget
-   ApprovedBudget
-   BudgetVariance
-   TargetCPL
-   Geography
-   Channels
-   Sensitivity
-   CampaignOwner
-   ValidationStatus
-   DuplicateDetected

If a campaign is already `In Assessment`, `Awaiting Remediation`,
`Awaiting Approval`, or `Completed`, a fresh assessment must not be
created.

### Topic 2 --- Remediation & Selective Reassessment

This topic:

1.  Receives failed specialist domains.
2.  Creates remediation actions.
3.  Identifies the responsible owner.
4.  Sets `CampaignStatus` to `Awaiting Remediation`.
5.  Preserves already-passed specialist results.
6.  Detects corrected underlying data.
7.  Identifies stale specialist results.
8.  Reruns only affected specialists.
9.  Returns to Supervisor consolidation.
10. Recalculates final readiness.

Example: if only a missing landing page is corrected, reassess the
relevant Channel/Asset domain rather than automatically rerunning
Budget.

Maximum automated reassessment cycles: **2**.

After two unsuccessful cycles:

``` text
Manual Review
```

### Topic 3 --- Approval & Finalisation

The topic evaluates:

-   Proposed budget \> approved budget
-   Proposed budget \> INR 1,000,000
-   Target CPL \> INR 4,000
-   High regulatory sensitivity
-   Multi-market geography
-   Restricted/quantified claims
-   Urgent launch with unresolved approval

It must:

-   Determine the required approver.
-   Prevent `Ready` while approval is outstanding.
-   Record the approval reason.
-   Set the state to `Awaiting Approval`.
-   Allow reassessment when approval data changes.
-   Return to the Supervisor.
-   Never fabricate a human approval.

------------------------------------------------------------------------

## 12. Final Readiness Precedence

The mandatory precedence is:

1.  `Not Ready`
2.  `Management Approval Required`
3.  `Remediation Required`
4.  `Ready with Conditions`
5.  `Ready`

If multiple conditions apply, the highest-precedence outcome wins.

The system must not average specialist outcomes.

Example:

``` text
Budget  = Pass
Channel = Pass
Assets  = Pass
Brand   = Block
```

The final result cannot be `Ready`.

------------------------------------------------------------------------

## 13. Mandatory Business Rules

### Budget

-   Proposed budget above approved budget → Marketing Director approval.
-   Proposed budget above INR 1,000,000 → VP Marketing approval.
-   CPL above INR 4,000 → VP Marketing approval.

### Timing

-   Missing blocking assets with fewer than 5 calendar days to launch →
    `Not Ready`.
-   Pending QA may be a condition only when the policy permits it.

### Assets

The following are blocking:

-   Missing mandatory asset
-   Needs Changes
-   Pending Approval

### Geography

Multi-market campaigns require Regional Marketing Lead approval.

### Sensitivity

High-sensitivity campaigns require additional brand/content and
management review.

The supplied governance document is authoritative for exact policy
interpretation.

------------------------------------------------------------------------

## 14. Excel Integration

The operational workbook must be stored in OneDrive for Business or
SharePoint so that Copilot Studio can access it through Excel Online
(Business).

The solution must use appropriate Excel actions to:

-   List campaign rows
-   Retrieve relevant rules
-   Retrieve assets
-   Retrieve channel requirements
-   Retrieve stakeholders
-   Update campaign status

Available Excel Online (Business) operations specified by the PRD
include:

-   List rows present in a table
-   Get a row
-   Add a row into a table
-   Update a row

`CampaignID` should be used as the primary logical key where applicable.

------------------------------------------------------------------------

## 15. Knowledge Sources

### NovaSphere Marketing Governance Policy

Authoritative for:

-   Readiness statuses
-   Budget approval
-   Timing
-   Asset controls
-   Geography
-   Sensitivity
-   Autonomous-processing rules
-   Reassessment

### NovaSphere Brand & Content Guidelines

Authoritative for:

-   Brand terminology
-   Product naming
-   Claims
-   Evidence requirements
-   Channel-content rules
-   Brand review classification

Knowledge and tools should be scoped narrowly to the agents that need
them.

------------------------------------------------------------------------

## 16. Tool and Knowledge Scoping

Recommended ownership:

  Agent                  Primary capability
  ---------------------- --------------------------------------------------
  Supervisor             Overall orchestration and campaign-state control
  Budget Specialist      Excel financial/rule data
  Brand Specialist       Brand knowledge + campaign/asset data
  Channel Specialist     Excel channel requirements
  Asset Specialist       Excel asset status
  Risk Specialist        Consolidated specialist outputs
  Reporting Specialist   Word + Outlook

Every child agent should receive only the tools and knowledge required
for its assigned domain.

------------------------------------------------------------------------

## 17. Failure and Exception Handling

The implementation must handle:

-   No Pending campaigns
-   Duplicate CampaignID
-   Missing campaign information
-   Missing Excel row
-   Specialist failure
-   Conflicting specialist results
-   Word creation failure
-   Outlook failure
-   Excel update delay/failure
-   Missing approver
-   Reassessment limit reached

The system must never fabricate successful completion.

### Word Failure

If Word generation fails:

1.  Preserve final readiness in Excel.
2.  Mark report generation as failed.
3.  Do not claim that a report exists.

### Outlook Failure

If Outlook fails:

1.  Preserve the assessment result.
2.  Mark notification as failed.
3.  Do not claim that stakeholders were notified.

------------------------------------------------------------------------

## 18. Safety, Privacy and Explainability

### Safety

No autonomous campaign launch action is permitted.

The agent evaluates readiness; it does not launch campaigns.

### Privacy

Only synthetic data must be used.

### Explainability

Every non-Ready result must identify the reason.

### Reliability

A specialist failure must not result in an unsupported `Ready`
classification.

------------------------------------------------------------------------

## 19. Mandatory Test Cases

The PRD defines 22 test cases:

  -------------------------------------------------------------------------
  ID                Scenario            Pattern           Expected
                                                          Behaviour
  ----------------- ------------------- ----------------- -----------------
  TC-01             Valid Pending       Sequential        Validate and
                    campaign                              proceed to
                                                          specialist stage

  TC-02             Campaign already    Conditional       Prevent duplicate
                    Completed                             assessment

  TC-03             Four independent    Parallel          Fan-out then wait
                    specialist                            for all results
                    assessments                           

  TC-04             Budget exceeds      Conditional       Route to approval
                    approved budget                       

  TC-05             Budget exceeds INR  Conditional       Require VP
                    1M                                    Marketing
                                                          approval

  TC-06             High-sensitivity    Hierarchical      Brand specialist
                    content                               identifies
                                                          required review

  TC-07             Multiple channels   Parallel          Channel
                                                          specialist
                                                          evaluates every
                                                          channel

  TC-08             Mandatory asset     Sequential        Route to
                    missing                               remediation

  TC-09             Launch \<5 days     Decision          Final result Not
                    with missing asset  precedence        Ready

  TC-10             Only landing page   Selective loop    Rerun affected
                    corrected                             assessment only

  TC-11             Second remediation  Loop limit        Manual Review
                    fails                                 

  TC-12             Specialist produces Fallback          Retry once
                    no result                             

  TC-13             Specialist retry    Fallback          Insufficient
                    fails                                 evidence/manual
                                                          review

  TC-14             Brand Block +       Fan-in            Blocking result
                    Budget Pass                           prevails

  TC-15             APAC/multi-market   Conditional       Regional approval
                    review missing                        required

  TC-16             All controls pass   Sequential        Ready

  TC-17             Only permitted QA   Conditional       Ready with
                    remains                               Conditions

  TC-18             Final readiness     Sequential        Generate Word
                    validated                             report

  TC-19             Word succeeds       Sequential        Update Excel then
                                                          prepare
                                                          notification

  TC-20             Supervisor approves Hierarchical      Send Outlook
                    communication                         notification

  TC-21             Outlook fails       Failure           Record
                                                          notification
                                                          failure

  TC-22             No Pending campaign Trigger           Exit safely
                    exists                                without
                                                          processing
  -------------------------------------------------------------------------

At least **16 of the 22** test cases must be executed.

------------------------------------------------------------------------

## 20. Test Evidence

The test report must capture:

-   Test Case ID
-   Campaign ID
-   Trigger execution
-   Topic invoked
-   Child agents invoked
-   Pattern demonstrated
-   Specialist outputs
-   Expected result
-   Actual result
-   Final status
-   Pass/Fail
-   Failure reason
-   Remediation
-   Retest result
-   Screenshot reference

Mandatory coverage includes:

-   3 sequential-pattern tests
-   3 parallel fan-out/fan-in tests
-   3 hierarchical tests
-   2 conditional-routing tests
-   2 reassessment-loop tests
-   2 failure/fallback tests
-   1 end-to-end autonomous test

At least one failed test must be corrected and retested.

------------------------------------------------------------------------

## 21. Acceptance Criteria

The project is complete when:

-   A main Supervisor Agent exists.
-   At least four domain specialist child agents exist.
-   Specialist responsibilities are non-overlapping.
-   A recurrence event trigger is configured.
-   Campaign data is retrieved autonomously.
-   Duplicate processing is prevented.
-   Intake validation is implemented.
-   Four independent specialist assessments are performed.
-   Fan-in consolidation is implemented.
-   Hierarchical delegation is demonstrated.
-   Sequential processing is demonstrated.
-   Conditional routing is implemented.
-   Selective reassessment is implemented.
-   Reassessment is bounded.
-   Specialist failure is handled.
-   Final outcome precedence is implemented.
-   Excel is updated.
-   Word readiness report is generated.
-   Outlook communication is conditional.
-   Child agents cannot independently issue the final decision.
-   At least 16 tests are documented.
-   The solution is published.
-   Required GitHub artifacts are submitted.

------------------------------------------------------------------------

## 22. GitHub Submission Structure

The PRD requires the artifacts under:

``` text
submissions/project-build/ms-copilot-studio/
firstname-lastname/
p2-005_marketing_campaign_readiness_governance/
```

Required structure:

``` text
p2-005_marketing_campaign_readiness_governance/
│
├── README.md
├── solution-summary.md
├── architecture.md
├── orchestration-patterns.md
├── supervisor-agent-design.md
├── specialist-agent-design.md
├── custom-topics.md
├── autonomous-trigger.md
├── test-report.md
├── known-limitations.md
├── ai-usage-declaration.md
│
├── data/
│   └── dataset-notes.md
│
└── screenshots/
    ├── supervisor-agent.png
    ├── child-agents.png
    ├── recurrence-trigger.png
    ├── intake-topic.png
    ├── parallel-specialists.png
    ├── fan-in-consolidation.png
    ├── remediation-topic.png
    ├── approval-topic.png
    ├── excel-tools.png
    ├── word-tool.png
    ├── outlook-tool.png
    └── final-assessment.png
```

Participants do not need to upload copies of the trainer-supplied
dataset unless instructed.

------------------------------------------------------------------------

## 23. Required Orchestration Documentation

The `orchestration-patterns.md` document must explicitly explain:

### Sequential

Which steps depend on previous stages.

### Parallel

Which child agents perform independent assessments and how their results
are consolidated.

### Hierarchical

How the Supervisor controls child agents.

### Conditional

Which conditions result in different execution paths.

### Loop/Reassessment

How failed domains are selectively reassessed.

### Fallback

How tool and agent failures are handled.

Screenshots should be referenced where useful.

------------------------------------------------------------------------

## 24. Suggested Four-Hour Build Plan

  Time           Activity
  -------------- ------------------------------------------------------
  00:00--00:20   Review PRD, dataset and architecture
  00:20--00:40   Create Supervisor and recurrence trigger
  00:40--01:00   Configure Excel and knowledge sources
  01:00--01:25   Build Intake & Validation topic
  01:25--02:10   Build four parallel specialist agents
  02:10--02:30   Implement Supervisor fan-in and Risk Specialist
  02:30--02:50   Build Remediation/Reassessment topic
  02:50--03:05   Build Approval & Finalisation topic
  03:05--03:20   Configure Word and Outlook tools
  03:20--03:45   Test sequential, parallel and hierarchical behaviour
  03:45--04:00   Fix, retest, publish and document

------------------------------------------------------------------------

## 25. Evaluation Rubric --- 50 Marks

### A. Autonomous Trigger & Intake --- 7 Marks

-   Recurrence trigger configured --- 2
-   Correct Pending campaign selection --- 1
-   Validation topic --- 2
-   Duplicate/state handling --- 2

### B. Multi-Agent Architecture --- 13 Marks

-   Supervisor design --- 2
-   Specialist separation --- 2
-   Hierarchical delegation --- 2
-   Parallel fan-out --- 2
-   Fan-in consolidation --- 2
-   Structured specialist outputs --- 1
-   Conflict handling --- 2

### C. Sequential, Conditional & Loop Logic --- 10 Marks

-   Sequential stage control --- 2
-   Conditional routing --- 2
-   Remediation logic --- 2
-   Selective reassessment --- 2
-   Retry/fallback control --- 2

### D. Business Logic & Tools --- 12 Marks

-   Budget rules --- 2
-   Brand/content rules --- 2
-   Channel and asset logic --- 2
-   Final readiness precedence --- 2
-   Excel integration --- 2
-   Word/Outlook integration --- 2

### E. Testing & Documentation --- 8 Marks

-   Required test coverage --- 2
-   Orchestration-pattern evidence --- 2
-   Defect correction/retest --- 1
-   GitHub documentation --- 2
-   AI usage and limitations --- 1

------------------------------------------------------------------------

## 26. AI Usage Policy

AI may be used for:

-   Understanding the PRD
-   Designing agent instructions
-   Designing child-agent responsibilities
-   Designing topic flows
-   Designing variables
-   Troubleshooting Copilot Studio
-   Generating test ideas
-   Improving documentation

However, the participant remains responsible for the final solution.

AI must not:

-   Fabricate test evidence
-   Fabricate screenshots
-   Fabricate human approvals

The participant must understand and be able to explain the implemented
sequential, parallel, hierarchical, conditional, and reassessment
patterns.

A visually complete solution without working orchestration will not
receive full marks.

------------------------------------------------------------------------

## 27. Implementation Constraints

The orchestration must be built within Microsoft Copilot Studio using:

-   Copilot Studio event triggers
-   Copilot Studio topics
-   Copilot Studio child agents
-   Copilot Studio tools/connectors
-   Generative orchestration

A separate Power Automate workflow is not required and should not be
created for the core solution.

Word Online (Business) is specified as a Premium connector in Copilot
Studio, so connector availability in the training environment should be
validated before implementation.

------------------------------------------------------------------------

## 28. Dataset Summary

The supplied dataset is intentionally small and contains:

-   6 Campaign Requests
-   6 Budget Rules
-   10 Channel Requirements
-   24 Asset records
-   7 Approval rules
-   8 Synthetic stakeholders
-   12 dataset-oriented test scenarios
-   2 small knowledge documents

The scenarios include:

-   One near-ready campaign
-   One over-budget campaign
-   One remediation case
-   One high-sensitivity/high-budget case
-   One urgent campaign with missing assets
-   One multi-region approval case

This variation is intended to support testing of the required
orchestration patterns without requiring a large dataset.

------------------------------------------------------------------------

## 29. Definition of Done

The project can be considered complete only when the Copilot Studio
implementation, testing evidence, documentation, and submission
artifacts collectively demonstrate the PRD requirements.

The most important implementation principle is:

``` text
Recurrence
   ↓
Supervisor
   ↓
Validate
   ↓
Four Specialist Fan-Out
   ↓
Fan-In
   ↓
Risk & Decision
   ↓
Remediation / Approval if required
   ↓
Supervisor Final Validation
   ↓
Word Report
   ↓
Conditional Outlook Notification
   ↓
Excel State Update
```

The Supervisor remains the authority for the final readiness outcome,
while specialist agents provide domain-specific findings and evidence.

## Author name
Vaishnavi Gupta