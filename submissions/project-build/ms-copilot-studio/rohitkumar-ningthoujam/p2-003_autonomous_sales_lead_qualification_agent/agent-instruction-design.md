# Agent Instructions Design

## Purpose

The Autonomous Sales Lead Qualification Agent is designed to autonomously process incoming sales inquiry emails for NovaWorks Technologies. The instructions guide the agent to consistently qualify leads, apply business rules, update operational records, generate reports when required, and communicate with internal and external stakeholders while maintaining controlled autonomy.

---

## Design Principles

The instructions were designed using the following principles:

* Process only authorised project emails.
* Apply deterministic business rules before autonomous actions.
* Use Microsoft 365 connector tools for operational tasks.
* Prevent duplicate processing.
* Maintain data accuracy and consistency.
* Route uncertain cases for human review.
* Avoid unsupported commitments or assumptions.
* Maintain transparency and auditability.

---

## Trigger Scope

The instructions restrict processing to Outlook emails whose subject contains:

**[P2-003 LEAD]**

Emails outside this scope are ignored.

---

## Information Extraction

The instructions direct the agent to extract and normalize:

* Message ID
* Sender information
* Contact details
* Company information
* Country and territory
* Product interest
* Business need
* Budget
* Purchase timeline
* Decision role
* Confidence and missing information

Unknown values are retained as **Unknown** rather than inferred.

---

## Operational Logic

The instructions guide the agent to:

1. Validate the trigger scope.
2. Extract lead information.
3. Check for duplicate opportunities.
4. Read qualification rules and reference tables.
5. Calculate the qualification score.
6. Apply business override rules.
7. Determine the lead classification.
8. Assign the appropriate sales owner.
9. Create or update the Lead Register.
10. Generate a Microsoft Word qualification report when required.
11. Send Outlook communications according to the processing outcome.
12. Record completed and withheld actions.

---

## Duplicate Prevention

The instruction design requires duplicate detection by comparing:

* Source Message ID
* Sender Email
* Company Name
* Product Interest

When a duplicate is detected, the existing Lead Register record is updated, duplicate reports are prevented, and duplicate acknowledgements are not sent.

---

## Qualification Strategy

The instructions direct the agent to evaluate leads using qualification rules stored in the operational reference tables. Classification is based on qualification score together with business override rules.

Supported classifications include:

* Hot
* Qualified
* Nurture
* Low Priority
* Additional Information Required
* Human Review Required
* Duplicate
* Not a Sales Lead

---

## Human Review Strategy

The instructions require Human Review for:

* Low-confidence assessments
* Unknown products
* Unmapped territories
* Conflicting information
* Academic research requests
* Support requests
* Recruitment enquiries
* Competitor-related enquiries
* Tool uncertainty

External qualification decisions are withheld for these cases.

---

## Communication Strategy

The instructions define when to:

* Send lead acknowledgements.
* Request missing information.
* Notify the assigned sales owner.
* Notify Sales Operations.
* Withhold external communication when required by policy.

---

## Privacy and Security

The instructions require the agent to:

* Process only synthetic project data.
* Avoid requesting sensitive personal information.
* Avoid exposing internal classifications or business rules.
* Avoid unsupported claims, pricing commitments, contractual promises, or delivery guarantees.

---

## Error Handling

The instructions include controlled handling for connector failures, missing data, malformed emails, duplicate deliveries, and other operational exceptions.

A single retry is permitted for transient failures. If the retry is unsuccessful, the failure is recorded where possible, appropriate internal notifications are generated, and unsuccessful actions are not represented as completed.

---

## Security Considerations

This document intentionally excludes:

* Connection references
* Authentication credentials
* Microsoft 365 tenant information
* Connector secrets
* API keys
* Internal identifiers

Only the instruction design is documented to support reproducibility while protecting operational security.
