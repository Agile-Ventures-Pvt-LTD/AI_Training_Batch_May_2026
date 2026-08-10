# Known Limitations

## 1. Purpose

This document records the known implementation, tenant, tool, connector,
data, and automation limitations of the **CAP-001 Sleepsia Product
Quality & Customer Experience Intelligence Control Tower**.

The limitations below are based on the PRD requirements and should be
documented as part of the final GitHub submission. The PRD specifically
requires `known-limitations.md` to capture tenant, tool, and connector
limitations. 

## 2. Microsoft Tenant and Publishing Limitations

### Teams and Microsoft 365 Copilot

Publishing availability depends on:

-   Organization permissions.
-   Microsoft 365 licensing.
-   Teams/Power Platform app policies.
-   Sharing and tenant configuration.

Microsoft 365 Copilot availability may therefore not be controllable by
the participant. If the final channel cannot be enabled because of
tenant policy, the exact limitation and configuration evidence must be
documented. 

**Impact:** The agent may be fully implemented while final channel
validation remains tenant-dependent.

## 3. Microsoft Learn MCP Dependency

The Microsoft Learn MCP Server is required only for the **M365 Guidance
Specialist**.

Known limitations:

-   MCP depends on availability of the Microsoft Learn MCP endpoint.
-   MCP is not a source of Sleepsia quality policy.
-   MCP cannot determine quality severity.
-   MCP cannot authorize CAPA, reports, notifications, or safety
    escalation.
-   MCP failure must not block the core quality workflow.

The PRD defines MCP as non-blocking and requires Microsoft guidance to
be marked unavailable when MCP fails.

**Fallback:**

`Microsoft guidance unavailable - manual review`

## 4. Excel Online Limitations

The operational workflow depends on Excel Online (Business) access to
the supplied workbook.

Known limitations:

-   Workbook access depends on correct OneDrive for Business or
    SharePoint configuration.
-   Tables must be available to the Excel connector.
-   A failed Excel read stops the affected assessment.
-   A failed Excel update prevents complaints from being marked
    `Processed = Yes`.
-   Source evidence must not be silently overwritten.

The PRD explicitly requires these failure behaviors.


**Impact:** Incorrect workbook location, permissions, table
configuration, or connector failure can prevent autonomous processing.

## 5. Synthetic Dataset Limitation

The project uses a compact synthetic dataset rather than live production
quality data.

The PRD specifies:

-   8 products.
-   18 complaints.
-   12 returns.
-   Small supporting tables.

The workbook contains product, batch, complaint, sales, return,
incident, CAPA, owner, rule, and test-scenario data.


**Impact:**

-   Results demonstrate the intended workflow but do not represent
    real-world production quality performance.
-   Complaint and return patterns are limited to the supplied scenarios.
-   The system should not be treated as a production statistical
    quality-monitoring system based solely on this dataset.

## 6. Deterministic Rule Scope

The quality decision engine is constrained by the explicit rules
supplied in the PRD.

The main rules include:

-   Safety indicator -\> Critical Escalation.
-   Two or more potential safety complaints -\> High-Priority Quality
    Incident.
-   Five or more similar complaints within 7 days -\> Investigation
    Required.
-   Return rate \>= 2% -\> Investigation Required.
-   Previous incident + repeated failure mode -\> High-Priority Quality
    Incident.
-   Missing batch for repeated cluster -\> Insufficient Evidence.
-   Overdue CAPA -\> High-Priority Quality Incident.
-   Single isolated low-severity complaint -\> Informational.

When multiple rules apply, the highest-priority rule wins.


**Limitation:** The system should not infer additional business rules
that are not supported by the approved policy or operational data.

## 7. Specialist Failure Limitation

Specialist agents are not guaranteed to succeed on every execution.

The implemented fallback is:

1.  Specialist fails.
2.  Retry once.
3.  If the second attempt fails, record the failure.
4.  Do not fabricate the missing finding.
5.  Treat the affected assessment as Insufficient Evidence where
    appropriate.

The PRD explicitly requires retry-once behavior and no fabricated
evidence. fileciteturn13file3L338-L343

**Impact:** A specialist failure can prevent a fully evidenced automated
classification.

## 8. Selective Reassessment Limitation

The reassessment loop is intentionally bounded.

After new evidence:

-   Only stale specialist analyses should be rerun.
-   Unaffected findings should be preserved.
-   `ReassessmentCount` is incremented.
-   Maximum automated reassessment cycles = 2.
-   After unresolved automation beyond the permitted cycles, the case
    moves to Manual Review.

The PRD specifies this bounded reassessment model.


**Impact:** Cases requiring more than the permitted automated
reassessment cycles require human/manual handling.

## 9. Word Report Limitation

Word Online (Business) is used to generate the Product Quality
Investigation Report after Supervisor validation.

If report generation fails:

-   Preserve the quality decision.
-   Record `ReportGeneration = Failed`.
-   Do not claim that a report was generated.

The PRD explicitly requires this behavior.


**Impact:** A correct quality decision can exist without a successfully
generated Word report.

## 10. Outlook Notification Limitation

Outlook notification is conditional on the final Supervisor decision.

If Outlook fails:

-   Preserve the quality decision.
-   Record `Notification = Failed`.
-   Do not claim that an email was sent.

The PRD explicitly requires this failure behavior.


**Impact:** The internal decision may be completed even when
notification delivery fails.

## 11. No False-Success Guarantee

The system depends on external tools and connectors, so tool execution
cannot always be assumed to succeed.

The agent must distinguish:

-   Action requested.
-   Action attempted.
-   Action succeeded.
-   Action failed.

It must never claim:

-   A report exists when Word generation failed.
-   An email was sent when Outlook failed.
-   An Excel update occurred when the update failed.
-   A specialist finding exists when the specialist failed.
-   Evidence exists when the data is missing.

This is a core PRD requirement. 

## 12. Safety Scope Limitation

The system is an internal product-quality intelligence system, not a
medical or clinical assistant.

It must not:

-   Diagnose medical conditions.
-   Provide medical treatment advice.
-   Approve recalls.
-   Promise refunds.
-   Make customer compensation decisions.
-   Issue public safety announcements.

The project creates internal quality intelligence and controlled
escalation only.

## 13. Public Product Information Limitation

Approved Sleepsia public URLs may be used for product facts.

They must not:

-   Override internal quality policy.
-   Determine internal severity.
-   Override CAPA requirements.
-   Replace operational evidence.

The PRD explicitly states that public marketing claims must not override
internal quality rules. 

## 14. Knowledge Source Limitation

The quality workflow depends on the supplied knowledge documents and
approved public product sources.

If required knowledge is unavailable or ambiguous:

-   Do not invent policy.
-   Do not invent product facts.
-   Identify missing evidence or information.
-   Use the approved escalation/manual-review path where required.

The internal quality policy remains the highest authority for internal
quality decisions. 

## 15. Autonomous Trigger Limitation

The autonomous workflow depends on the recurrence event trigger and the
`Customer_Complaints` data.

The trigger is intended to identify unprocessed complaint records and
start assessment. If no unprocessed complaints exist, the workflow exits
without creating an incident. 

**Impact:** Trigger failures, unavailable data, or incorrect `Processed`
state can prevent autonomous processing.

## 16. Processed-State Limitation

A complaint must only be marked:

`Processed = Yes`

after the assessment record is successfully created or updated.

Therefore, a failed Excel update or incomplete assessment can
intentionally leave records unprocessed for later handling.

**Impact:** Reprocessing may occur if state synchronization is not
completed successfully.

## 17. Final Decision Ownership Limitation

Only the Quality Supervisor can assign the final internal quality
classification.

Specialists provide findings only.

This means the system intentionally does not allow:

-   Complaint Pattern Specialist to assign final severity.
-   Returns Specialist to assign final severity.
-   Product/Batch Specialist to assign final severity.
-   Customer Impact Specialist to assign final severity.
-   Safety Specialist to independently own the final classification.
-   CAPA Specialist to independently close critical incidents.
-   M365 Guidance Specialist to influence Sleepsia quality severity.

This separation is required by the PRD. 


## 18. Interactive Mode Limitation

Interactive employee questions should not automatically start the
autonomous assessment workflow unless appropriate.

Interactive mode is intended to retrieve:

-   Open incidents.
-   CAPA status.
-   Internal quality policy.
-   Product care/use information.
-   Approved public product facts.
-   Microsoft operational guidance.

The same published agent supports both autonomous and interactive modes,
but the modes have different entry behavior.


## 19. Automation Boundary

The system is designed to demonstrate an enterprise multi-agent quality
workflow, but human review remains necessary for:

-   Manual Review cases.
-   Unresolved evidence gaps.
-   Repeated specialist failures.
-   Exhausted reassessment cycles.
-   Certain tenant/publishing limitations.
-   Cases where required operational data is unavailable.

The PRD includes `Manual Review` as an incident state for
automation-exhausted or unresolved failures.


## 20. Summary

The main known limitations are:

-   **Tenant dependency:** Teams/Microsoft 365 Copilot publishing may
    depend on organizational permissions and policies.
-   **Connector dependency:** Excel, Word, and Outlook actions depend on
    connector availability and permissions.
-   **MCP dependency:** Microsoft guidance depends on Microsoft Learn
    MCP availability, but MCP failure is non-blocking.
-   **Synthetic data:** The supplied dataset is small and synthetic.
-   **Bounded automation:** Reassessment is limited to two automated
    cycles.
-   **Specialist retry limit:** Failed specialists receive only one
    retry.
-   **Evidence dependency:** Missing or failed data must result in
    evidence gaps rather than invented conclusions.
-   **Report/notification independence:** Word or Outlook failure does
    not invalidate the quality decision.
-   **Safety boundary:** The system does not provide medical advice or
    public safety decisions.
-   **Policy boundary:** Public product information cannot override
    internal quality policy.
-   **Manual-review boundary:** unresolved automation or evidence
    problems require manual handling.

These limitations are intentional design boundaries rather than defects.
They ensure that the system does not claim success without evidence,
does not fabricate missing information, and does not allow external
guidance or specialist findings to override the Quality Supervisor's
decision authority.
