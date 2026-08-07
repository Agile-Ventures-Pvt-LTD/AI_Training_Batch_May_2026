# Known Limitations

## Project
P2-005 — Marketing Campaign Readiness & Governance

## Overview

The Campaign Readiness Supervisor provides automated campaign readiness assessment using Microsoft Copilot Studio, specialist agents, custom topics, structured campaign data, and Microsoft connectors.

The following limitations were identified during implementation and testing.

## 1. Connector Dependency

The solution depends on external Microsoft connectors for accessing campaign data and performing workflow actions.

If a required connector is unavailable or unauthenticated, the readiness assessment may fail before the business logic is executed.

## 2. Authentication During Evaluation

Some automated evaluation test cases failed because the evaluation environment required connector authentication.

A workflow that operates correctly in the Copilot Studio interactive test environment may still fail during automated evaluation if the required connections are unavailable in that execution context.

## 3. Excel Data Dependency

Campaign assessment depends on the accuracy and availability of data stored in the configured Excel tables.

Missing, incorrectly formatted, or inconsistent values may affect:

- Campaign validation
- Launch-date calculation
- Budget assessment
- Channel assessment
- Asset assessment
- Approval determination

## 4. Launch Date Format

LaunchDate is handled using the expected `YYYY-MM-DD` format.

The current implementation converts this string format during the DaysToLaunch calculation.

Unexpected date formats may require additional validation or conversion logic.

## 5. Specialist Agent Dependency

The Supervisor requires usable results from mandatory specialist agents.

If a specialist fails, the Supervisor retries that specialist once.

If the retry also fails:

- The domain is classified as Insufficient Evidence.
- A Ready outcome is prevented.
- The campaign is routed to Manual Review.

## 6. Human Approval Dependency

Some campaign scenarios require human approval.

The solution cannot autonomously create or assume an approval decision.

If mandatory approval is unavailable, the campaign cannot be treated as fully approved.

## 7. Limited Automated Reassessment

The solution permits a maximum of two automated reassessment cycles.

If blocking issues remain unresolved after the allowed cycles, further autonomous reassessment is stopped and the applicable governance/manual-review process is followed.

## 8. Selective Reassessment Dependency

The solution attempts to reassess only the specialist domain affected by remediation.

If a correction affects multiple readiness domains, additional specialist assessments may be required.

## 9. Knowledge Source Dependency

Specialist reasoning depends on the configured governance and brand/content knowledge sources.

Missing, outdated, or incomplete governance documentation may reduce the quality or completeness of specialist findings.

## 10. Generative AI Variability

Specialist agents use generative AI reasoning.

Although agent instructions and governance controls are used to constrain behavior, generated explanations and wording may vary between executions.

Deterministic custom topics are therefore used for important structured validation wherever practical.

## 11. Automated Evaluation Limitations

Some test failures may represent environment or connector failures rather than incorrect campaign-readiness logic.

Failed cases caused by unavailable connections should be rerun after connector authentication is restored.

## 12. Reporting Dependency

Final reporting and stakeholder communication depend on the successful completion of the readiness workflow and the availability of the required Microsoft 365 connectors.

Reporting must not occur before final Supervisor validation.

## 13. Manual Review Requirement

Certain conditions cannot be safely resolved autonomously.

Manual Review may be required when:

- Mandatory specialist evidence remains unavailable.
- Automated reassessment limits are reached.
- Required operational updates fail.
- Governance requirements cannot be conclusively resolved.

## 14. No Campaign Launch Capability

The most important system boundary is that the solution assesses campaign readiness only.

The solution does not:

- Activate campaign channels.
- Publish campaign content.
- Start paid advertising.
- Deploy campaign assets.
- Launch a marketing campaign.

A Ready outcome indicates that the campaign satisfies the applicable readiness requirements; it does not mean that the campaign has been launched.

## 15. Current Test Status

The implemented solution was evaluated using 16 selected test cases.

- Total Test Cases: 16
- Passed: 10
- Failed: 6
- Pass Rate: 62.5%
- Overall Status: Partially Passed

Several failed cases were associated with connector/authentication availability and require regression testing after the relevant connections are restored.

## Conclusion

The current implementation demonstrates the required campaign readiness orchestration and governance workflow but remains dependent on data quality, connector availability, specialist execution, human approvals, and the configured Microsoft Copilot Studio environment.

These limitations should be considered when interpreting automated assessment and evaluation results.