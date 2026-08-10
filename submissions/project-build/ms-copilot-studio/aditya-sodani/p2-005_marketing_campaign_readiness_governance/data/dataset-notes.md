# Dataset Notes

## Project
P2-005 — Marketing Campaign Readiness & Governance

## Dataset Overview

The project uses structured campaign and governance data to support the Campaign Readiness Supervisor and its specialist agents.

The dataset provides the operational information required for campaign intake validation, specialist assessments, approval checks, remediation decisions, and final readiness determination.

## Primary Dataset

The primary project dataset is stored in an Excel workbook:

`P2-005_Marketing_Campaign_Readiness_Lab_Data.xlsx`

The workbook contains structured tables used by the Copilot Studio solution.

## Dataset Tables

The dataset contains the following main data areas:

- Campaign Requests
- Budget Rules
- Channel Requirements
- Asset Status
- Approval Matrix
- Stakeholders
- Test Scenarios

## Campaign Requests

The Campaign Requests data contains the primary campaign information used by the Campaign Readiness Supervisor.

Campaign records are uniquely identified using:

`CampaignID`

Example:

`CMP-001`

Campaign information includes fields such as:

- CampaignID
- CampaignName
- CampaignOwner
- Product
- Objective
- TargetAudience
- Geography
- LaunchDate
- ProposedBudget
- ApprovedBudget
- TargetCPL
- Channels
- RegulatorySensitivity
- CampaignStatus

The Supervisor uses CampaignID to retrieve the correct campaign record.

## Campaign Status

CampaignStatus is used to control the campaign assessment lifecycle.

The solution checks campaign status before beginning a new readiness assessment.

An eligible campaign begins in:

`Pending`

After successful intake validation, the Supervisor changes the campaign status to:

`In Assessment`

This prevents duplicate or uncontrolled campaign processing.

The final status is updated only after the Supervisor validates the final readiness outcome.

## Launch Date

LaunchDate is stored in the dataset using the format:

`YYYY-MM-DD`

Example:

`2026-08-28`

The Campaign Intake & Validation topic calculates `DaysToLaunch` from this value.

A negative DaysToLaunch value indicates that the campaign launch date is already in the past and therefore fails intake validation.

## Budget Rules

Budget Rules provide governance information used by the Budget & Commercial Specialist.

The rules support assessment of:

- Proposed budget
- Approved budget
- Budget thresholds
- Commercial requirements
- Required management approvals

These rules help determine whether the campaign can proceed or requires additional approval.

## Channel Requirements

Channel Requirements define readiness requirements for marketing channels used by campaigns.

Supported campaign channels may include:

- Email
- LinkedIn
- Paid Search
- Web
- Webinar/Event

The Channel Readiness Specialist evaluates the applicable requirements for every channel configured for the campaign.

## Asset Status

Asset Status contains information about campaign assets and their current readiness state.

Asset states may include:

- Approved
- Pending QA
- Pending Approval
- Needs Changes
- Missing / Not Started

The Asset Readiness Specialist uses this information to identify blocking and non-blocking asset gaps.

Missing mandatory assets are treated as blocking findings.

## Approval Matrix

The Approval Matrix contains information used to determine when additional human approval is required.

Approval requirements may depend on conditions such as:

- Campaign budget
- Geography
- Regulatory sensitivity
- Campaign findings
- Governance rules

Possible approvers may include roles such as:

- Marketing Director
- VP Marketing
- Regional Marketing Lead
- Brand & Content Lead

The AI system must never fabricate an approval result.

## Stakeholders

The Stakeholders data provides stakeholder information required for final reporting and communication.

This information may be used by the Reporting & Communication Specialist after the Campaign Readiness Supervisor has validated the final readiness outcome.

## Test Scenarios

The dataset includes test scenarios used to evaluate the Campaign Readiness Supervisor.

The scenarios cover areas such as:

- Campaign intake
- Duplicate assessment prevention
- Budget controls
- Brand/content compliance
- Channel readiness
- Asset readiness
- Approval requirements
- Blocking conditions
- Remediation
- Reassessment
- Specialist failure
- Insufficient evidence
- Manual review
- Ready outcomes
- Ready with Conditions outcomes
- Not Ready outcomes

## Data Access

Microsoft Copilot Studio accesses the dataset through configured Microsoft connectors.

Campaign lookup uses:

`Key Column = CampaignID`

and:

`Key Value = Current CampaignID`

This allows the workflow to retrieve or update the specific campaign being assessed.

## Data Usage by Agent

The dataset is used across the solution as follows:

### Campaign Readiness Supervisor
Uses campaign data to coordinate the overall readiness assessment.

### Campaign Intake & Validation
Uses campaign request data for eligibility, mandatory-field, status, and launch-date validation.

### Budget & Commercial Specialist
Uses campaign financial information and budget rules.

### Brand & Content Compliance Specialist
Uses campaign information together with the configured brand/content knowledge source.

### Channel Readiness Specialist
Uses campaign channels and channel requirements.

### Asset Readiness Specialist
Uses campaign asset records and asset statuses.

### Approval & Finalisation
Uses applicable approval requirements and campaign findings.

### Reporting & Communication Specialist
Uses campaign, assessment, and stakeholder information for final reporting and communication.

## Data Quality Considerations

The readiness assessment depends on accurate and complete source data.

Potential data-quality issues include:

- Missing CampaignID
- Missing mandatory campaign fields
- Invalid LaunchDate format
- Missing budget information
- Incorrect CampaignStatus
- Missing channel requirements
- Missing asset records
- Missing approval information
- Inconsistent campaign identifiers across tables

Such issues may prevent successful automated assessment or require Manual Review.

## Data Modification

The solution performs controlled updates to campaign data.

The campaign may be updated to:

`In Assessment`

after successful intake validation.

After final Supervisor validation, the final CampaignStatus may also be persisted to the dataset.

The solution must not modify campaign data in a way that implies that the campaign itself has been launched.

## Dataset Limitations

The dataset represents the controlled data available for the P2-005 project and evaluation scenarios.

The solution depends on:

- Correct table structure
- Consistent CampaignID values
- Valid connector access
- Accurate source data
- Expected date formatting
- Availability of required governance records

Changes to the workbook schema, table names, column names, or data formats may require corresponding changes in the Copilot Studio implementation.

## Conclusion

The project dataset provides the structured operational foundation for the Campaign Readiness Supervisor.

It enables campaign identification, intake validation, specialist assessment, governance checks, approval determination, remediation, testing, final status persistence, and stakeholder reporting while maintaining CampaignID as the primary link across the readiness workflow.