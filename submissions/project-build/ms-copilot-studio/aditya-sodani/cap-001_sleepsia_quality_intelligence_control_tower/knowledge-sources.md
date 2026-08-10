# Knowledge Sources

## Knowledge Documents

1. **Sleepsia_Product_Quality_Policy.docx**
   - Authority: Highest for internal quality decisions.
   - Covers quality thresholds, classification, investigation, CAPA and escalation rules.

2. **Sleepsia_Product_Care_and_Usage_Guide.docx**
   - Authority: Product care/use only.
   - Provides product care, usage and product-safety grounding within its defined boundary.

3. **Sleepsia_Customer_Resolution_Policy.docx**
   - Authority: Customer-resolution boundary.
   - Defines customer-resolution and escalation responsibilities.

## Approved Sleepsia URLs

- https://www.sleepsia.in/products/travel-pillow
- https://www.sleepsia.in/products/kids-alpha-pillow

Public URLs are used only for product facts. Internal synthetic quality policies take precedence over public marketing/product claims for quality severity, escalation and CAPA decisions. :contentReference[oaicite:0]{index=0}

## Knowledge Precedence

1. Sleepsia Product Quality Policy
2. Product Care and Usage Guide for product-care/use information
3. Customer Resolution Policy for customer-resolution boundaries
4. Approved Sleepsia public product URLs for product facts only

The internal synthetic quality policy controls quality severity, escalation and CAPA. Public Sleepsia pages must not override internal quality rules. :contentReference[oaicite:1]{index=1}

## Retrieval Tests

| Test | Query | Expected Result |
|---|---|---|
| RT-01 | What complaint threshold triggers an investigation? | Retrieve the internal Product Quality Policy and identify the complaint-cluster threshold. |
| RT-02 | What return-rate threshold triggers an investigation? | Retrieve the internal Product Quality Policy and identify the return-rate threshold. |
| RT-03 | What happens when SafetyIndicator is Yes? | Safety override takes precedence and results in Critical Escalation. |
| RT-04 | What does the Product Care and Usage Guide say about product care? | Retrieve product-care/use guidance without applying it as internal quality severity policy. |
| RT-05 | What is the customer-resolution boundary? | Retrieve the Customer Resolution Policy and distinguish customer-resolution actions from quality ownership. |
| RT-06 | What is the Travel Pillow product information? | Retrieve information from the approved Sleepsia Travel Pillow URL only; do not apply internal incident rules as public product facts. |
| RT-07 | What is the Kids Alpha Pillow product information? | Retrieve information from the approved Sleepsia Kids Pillow URL only. |

## Retrieval Evidence

Knowledge documents configured: **3**

Approved Sleepsia URLs configured: **2**

Retrieval testing must confirm that internal quality policy takes precedence over public product information.
