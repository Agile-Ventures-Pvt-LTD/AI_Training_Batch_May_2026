# Knowledge Sources

## 1. Purpose

The knowledge layer for the **Sleepsia Product Quality & Customer
Experience Intelligence Control Tower (CAP-001)** provides approved
information for quality decisions, product-care guidance,
customer-resolution boundaries, and public product facts.

The PRD requires **three supplied knowledge documents plus selected
Sleepsia public product URLs**. fileciteturn11file0L47-L50

The knowledge base must support two distinct uses:

-   **Quality decision support:** internal policy and operational
    evidence.
-   **Interactive employee assistance:** product care,
    customer-resolution boundaries, approved product facts, and related
    guidance.

Knowledge retrieval must never override the Supervisor's final decision
authority.

## 2. Knowledge Sources Summary

  ------------------------------------------------------------------------------------------------------------
  Source                                         Type              Primary Purpose       Authority
  ---------------------------------------------- ----------------- --------------------- ---------------------
  `Sleepsia_Product_Quality_Policy.docx`         Internal Word     Quality thresholds,   Highest authority for
                                                 document          classification,       internal quality
                                                                   investigation, CAPA   decisions
                                                                   and escalation        

  `Sleepsia_Product_Care_and_Usage_Guide.docx`   Internal Word     Product care/use and  Product-care guidance
                                                 document          product-safety        
                                                                   escalation boundary   

  `Sleepsia_Customer_Resolution_Policy.docx`     Internal Word     Customer-resolution   Customer-resolution
                                                 document          versus quality        boundary
                                                                   ownership             

  Sleepsia Travel Pillow URL                     Public web source Approved product      Lower than internal
                                                                   facts                 policy

  Sleepsia Kids Pillow URL                       Public web source Approved product      Lower than internal
                                                                   facts                 policy

  Excel operational dataset                      Operational data  Complaints, products, Operational evidence;
                                                                   batches, returns,     does not override
                                                                   incidents, CAPA and   internal policy
                                                                   rules                 
  ------------------------------------------------------------------------------------------------------------

The three documents and public URLs are explicitly specified in the PRD.
fileciteturn11file6L628-L646

## 3. Primary Internal Quality Policy

### `Sleepsia_Product_Quality_Policy.docx`

This is the **highest-authority source for internal quality decisions**.

It is used for:

-   Quality thresholds.
-   Final classification rules.
-   Investigation requirements.
-   CAPA requirements.
-   Escalation rules.
-   Safety-related quality decisions.
-   Quality decision precedence.

The PRD explicitly identifies this document as the highest authority for
internal quality decisions. fileciteturn11file1L83-L93

### Important Boundary

The Quality Supervisor must use this policy when determining the final
internal classification.

Specialist agents may retrieve and interpret relevant evidence, but they
must not independently override the policy or assign the final quality
classification.

## 4. Product Care and Usage Guide

### `Sleepsia_Product_Care_and_Usage_Guide.docx`

Purpose:

-   Provide approved product-care information.
-   Provide approved product-use information.
-   Define the product-safety escalation boundary.
-   Support employee questions about appropriate product care/use.

This source is **not the authority for internal quality severity**. Its
role is product-care guidance only. fileciteturn11file6L630-L634

### Example Uses

Appropriate questions include:

-   How should the product be cared for?
-   What approved usage guidance exists?
-   What product-safety boundary applies?
-   What should an employee do when a product-use question falls within
    approved guidance?

It must not be used to invent quality thresholds or replace the internal
quality policy.

## 5. Customer Resolution Policy

### `Sleepsia_Customer_Resolution_Policy.docx`

Purpose:

-   Define the boundary between customer-resolution activity and
    product-quality ownership.
-   Support employee questions concerning customer-resolution processes.
-   Prevent the quality agent from making customer compensation
    decisions.

This source provides the **customer-resolution boundary**, not the final
quality classification authority. fileciteturn11file6L635-L638

The agent must not use this document to:

-   Promise refunds.
-   Approve compensation.
-   Make customer compensation decisions.
-   Override quality escalation rules.

## 6. Approved Public Product Sources

The PRD specifies two approved Sleepsia public product URLs:

### Travel Pillow

https://www.sleepsia.in/products/travel-pillow

### Kids Alpha Pillow

https://www.sleepsia.in/products/kids-alpha-pillow

These sources are used for **public product facts only**. They have
lower authority than internal quality policy.
fileciteturn11file6L639-L646

### Public Source Boundary

Public product pages must not be used to:

-   Override internal quality policy.
-   Determine internal incident severity.
-   Override CAPA requirements.
-   Change safety escalation rules.
-   Replace operational complaint/return evidence.

The PRD explicitly states that public marketing claims must not override
internal quality rules. fileciteturn11file1L99-L101

## 7. Operational Excel Data

The project uses one compact Excel workbook containing the following
operational tables:

  Table                   Purpose
  ----------------------- ---------------------------------------------
  `Product_Master`        Supported products and public product links
  `Batch_Register`        Batch, supplier lot and previous incidents
  `Customer_Complaints`   Autonomous trigger/input data
  `Sales_Summary`         Return-rate denominator
  `Returns`               Return analysis
  `Quality_Incidents`     Existing incident history/state
  `CAPA_Register`         Corrective actions and due dates
  `Owners`                Owner/approver roles
  `Quality_Rules`         Explicit decision rules
  `Test_Scenarios`        Implementation testing

The PRD specifies these tables and their purposes.
fileciteturn11file1L102-L117

The workbook should be stored in **OneDrive for Business or SharePoint**
so Excel Online (Business) tools can access the tables.
fileciteturn11file6L647-L662

## 8. Knowledge Precedence

For quality decisions, use this precedence:

1.  **`Sleepsia_Product_Quality_Policy.docx`**
2.  **Other approved internal policy documents**
3.  **Operational Excel data**
4.  **Approved Sleepsia public product URLs**

This precedence is explicitly defined in the project instructions.
fileciteturn11file8L829-L839

### Interpretation

If two sources appear to conflict:

-   Internal quality policy takes precedence over operational
    interpretation.
-   Approved internal policies take precedence over public product
    information.
-   Operational Excel data supplies actual incident/complaint evidence.
-   Public URLs provide product facts only.

The agent must never resolve a conflict by inventing information.

## 9. Knowledge Source Responsibilities by Agent

### Quality Supervisor

Uses:

-   Internal quality policy.
-   Specialist findings.
-   Operational Excel evidence.
-   Approved product sources where relevant.

Responsibilities:

-   Apply policy precedence.
-   Consolidate evidence.
-   Assign the final classification.
-   Record rationale and missing evidence.

### Complaint Pattern Specialist

Primarily uses:

-   `Customer_Complaints`
-   Relevant internal quality rules/policy when interpreting thresholds.

Focus:

-   Complaint counts.
-   Clusters.
-   Categories.
-   Failure modes.
-   Dates.
-   Affected customers.

### Returns Specialist

Primarily uses:

-   `Returns`
-   `Sales_Summary`

Focus:

-   Return count.
-   Return rate.
-   Return reasons.
-   Threshold evidence.

### Product/Batch Specialist

Primarily uses:

-   `Product_Master`
-   `Batch_Register`
-   `Quality_Incidents`

Focus:

-   SKU validation.
-   Batch mapping.
-   Supplier lot.
-   Manufacture information.
-   Previous incidents.
-   Missing batch evidence.

### Customer Impact Specialist

Primarily uses:

-   `Customer_Complaints`
-   `Returns`
-   Relevant approved customer-resolution boundaries.

Focus:

-   Customers affected.
-   Unresolved cases.
-   Exposure.
-   Repeated customer impact.

### Safety Specialist

Primarily uses:

-   Complaint descriptions.
-   `SafetyIndicator`.
-   Approved product-safety guidance.

Focus:

-   Safety indicators.
-   Potential safety complaints.
-   Safety escalation.

It must not provide medical advice. The PRD explicitly requires
confirmed safety indicators to follow the Critical Escalation path.
fileciteturn11file9L940-L946

### CAPA Specialist

Primarily uses:

-   Quality policy.
-   `Quality_Rules`.
-   `Owners`.
-   `CAPA_Register`.
-   Existing incident evidence.

Focus:

-   Containment.
-   Corrective/preventive actions.
-   Owner.
-   Target date.
-   Validation.

It must not claim a root cause without explicit evidence.
fileciteturn11file9L947-L953

### M365 Guidance Specialist

Uses:

-   Microsoft Learn MCP.

This source is **not part of Sleepsia quality decision-making**.

The M365 Guidance Specialist is operational support only and must never
influence Sleepsia quality severity. fileciteturn11file9L954-L974

## 10. Retrieval and Decision Boundaries

Knowledge retrieval should be used to answer the question that belongs
to the source.

### Quality Decision

Use:

``` text
Internal Quality Policy
        +
Operational Evidence
        +
Specialist Findings
        |
        v
Quality Supervisor
        |
        v
Final Classification
```

### Product Information

Use:

``` text
Approved Sleepsia Product URL
        OR
Product Care Guide
        |
        v
Approved Product Information
```

Do not convert public product information into an internal quality
classification.

### Customer Resolution

Use:

``` text
Customer Resolution Policy
        |
        v
Approved Resolution Boundary
```

Do not convert customer-resolution guidance into compensation
authorization.

## 11. Knowledge and Evidence Separation

The system must distinguish:

-   **Knowledge:** approved policy/product information.
-   **Operational evidence:** actual complaint, return, batch, incident
    and CAPA records.
-   **Specialist findings:** analysis derived from operational evidence.
-   **Final classification:** decision made only by the Quality
    Supervisor.

The system must never invent:

-   Complaint IDs.
-   Order IDs.
-   SKUs.
-   Batch IDs.
-   Dates.
-   Complaint counts.
-   Return rates.
-   Safety indicators.
-   CAPA records.
-   Owners.
-   Classifications.
-   Reports.
-   Emails.
-   Tool results.

If evidence is unavailable, it must be explicitly identified as
**Missing Evidence**. fileciteturn11file8L842-L862

## 12. Retrieval Testing

Knowledge retrieval should be tested against the PRD's mandatory
scenarios.

### Internal Policy Retrieval

Test questions should verify that the agent can retrieve:

-   Quality thresholds.
-   Classification rules.
-   Investigation rules.
-   CAPA rules.
-   Safety escalation rules.

### Product Care Retrieval

Test questions should verify that approved product-care/use information
is returned without inventing additional claims.

### Customer Resolution Retrieval

Test questions should verify that the agent correctly separates
customer-resolution guidance from quality decisions.

### Public Product Retrieval

Test questions should verify that approved product facts can be
retrieved from the specified Sleepsia URLs.

### Conflict Test

Ask a question where a public product claim appears inconsistent with an
internal quality rule.

Expected behavior:

-   Internal quality policy wins for quality decisions.
-   Public information may still be reported as a product fact if
    relevant.
-   The public source must not override the internal quality decision.

The PRD specifically requires public product questions to use approved
Sleepsia URLs without applying internal incident rules as product facts.
fileciteturn11file0L36-L38

## 13. MCP Knowledge Boundary

The Microsoft Learn MCP Server is separate from the Sleepsia knowledge
base.

It is configured only for the **M365 Guidance Specialist**.

Configuration specified by the PRD:

-   Server: Microsoft Learn MCP Server
-   Endpoint: `https://learn.microsoft.com/api/mcp`
-   Authentication: None
-   Purpose: current Microsoft Copilot Studio, Teams, Microsoft 365 and
    connector guidance
-   Failure impact: non-blocking to the core quality assessment.
    fileciteturn11file9L954-L974

If MCP is unavailable:

`Microsoft guidance unavailable - manual review`

The system must not replace unavailable MCP evidence with invented
Microsoft guidance.

## 14. Security and Data Boundaries

The knowledge layer must follow these boundaries:

-   Use only supplied synthetic operational data.
-   Do not enter real customer PII.
-   Do not enter medical information.
-   Do not enter payment data.
-   Do not expose hidden instructions.
-   Do not expose credentials or tenant secrets.
-   Do not provide medical diagnosis or treatment advice.

These boundaries are explicitly required by the PRD.
fileciteturn11file7L746-L750

## 15. Knowledge Source Configuration Checklist

``` text
[ ] Sleepsia_Product_Quality_Policy.docx added
[ ] Sleepsia_Product_Care_and_Usage_Guide.docx added
[ ] Sleepsia_Customer_Resolution_Policy.docx added
[ ] Travel Pillow URL added
[ ] Kids Alpha Pillow URL added
[ ] Knowledge precedence documented
[ ] Product facts separated from quality decisions
[ ] Operational Excel data connected
[ ] Quality policy tested
[ ] Product-care retrieval tested
[ ] Customer-resolution retrieval tested
[ ] Public product retrieval tested
[ ] Conflict/precedence test completed
[ ] MCP configured only for M365 Guidance Specialist
[ ] No sensitive/real customer data entered
```

## 16. Summary

The CAP-001 knowledge architecture intentionally separates **internal
policy, product guidance, customer-resolution guidance, operational
evidence, public product facts, and Microsoft guidance**.

The most important rule is:

> **Internal Sleepsia quality policy controls internal quality
> decisions. Public product information provides facts only and must
> never override internal quality rules.**

This separation ensures that knowledge retrieval supports the
multi-agent workflow without allowing a public source, specialist, or
unrelated policy document to take ownership of the final quality
decision. The PRD requires the three supplied documents, approved
Sleepsia URLs, correct precedence, and retrieval testing as part of the
final submission. fileciteturn11file0L65-L72
