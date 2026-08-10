# Known Limitations

## Overview

The Sleepsia Quality Intelligence Control Tower was developed as a prototype implementation in Microsoft Copilot Studio and is subject to platform and project constraints.

---

## Data Dependency

Investigation quality depends on the completeness and accuracy of workbook data.

Missing, incomplete, or inaccurate records may affect:

- Specialist findings
- Investigation outcomes
- Reassessment decisions

---

## Knowledge Source Dependency

Policy and guidance responses depend on the quality and completeness of configured knowledge sources.

Outdated or incomplete knowledge content may affect response quality.

---

## Rule-Based Decision Logic

Investigation outcomes are driven by predefined policy rules and configured decision logic.

Changes to business policies require corresponding updates to decision topics and supporting knowledge sources.

---

## Notification Dependency

Notification delivery depends on the availability and correct configuration of Microsoft 365 services.

Failures in external services may prevent notification delivery.

---

## Report Generation Dependency

Investigation reports depend on successful execution of document-generation actions.

Report generation failures may prevent creation of investigation documents.

---

## Prototype Scope

The implementation was designed to demonstrate autonomous quality-investigation orchestration and policy-driven decision support.

Some investigation outcomes may still require human review when evidence is incomplete or ambiguous.