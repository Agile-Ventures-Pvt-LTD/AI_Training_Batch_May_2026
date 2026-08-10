# Knowledge Base Configuration and Precedence

This document outlines the configuration, indexing, retrieval precedence, and validation queries for the grounding files and URLs in the **Sleepsia Quality Control Tower**.

---

## 1. Grounding Sources List

The knowledge base is composed of five distinct assets categorized into internal enterprise policies and public product details.

| Source Name | File Name / URL | Role & Purpose | Authority Level |
| :--- | :--- | :--- | :--- |
| **Product Quality Policy** | `Sleepsia_Product_Quality_Policy.docx` | Governs quality thresholds, severity classification rules, and escalation pathways. | **Level 1 (Highest):** Overrides all other sources for internal actions. |
| **Product Care Guide** | `Sleepsia_Product_Care_and_Usage_Guide.docx` | Contains user manual steps, cleaning rules, and physical safety usage bounds. | **Level 2:** Authority only on user care and safety warnings. |
| **Customer Resolution Policy** | `Sleepsia_Customer_Resolution_Policy.docx` | Defines return eligibility rules, refund process, and customer-facing support logic. | **Level 3:** Authority on customer resolutions, distinct from quality rules. |
| **Travel Pillow Webpage** | `https://www.sleepsia.in/products/travel-pillow` | Public product specs (dimensions, foam type, weight). | **Level 4:** Fact-lookup only. Cannot dictate quality decisions. |
| **Kids Pillow Webpage** | `https://www.sleepsia.in/products/kids-alpha-pillow` | Public product specs (materials, dimensions, ages). | **Level 4:** Fact-lookup only. Cannot dictate quality decisions. |

---

## 2. Grounding Precedence Rules

To prevent conflicting responses when querying the knowledge base, Copilot Studio applies a strict precedence cascade in its grounding configuration:

1. **Policy Hierarchy Overrides Marketing:** 
   - Internal policies (`Sleepsia_Product_Quality_Policy.docx`) govern all determinations of severity, investigation status, and escalation. Public web content *never* overrides internal threshold definitions.
2. **Decoupled Customer vs. Quality Rules:** 
   - Refund rules from `Sleepsia_Customer_Resolution_Policy.docx` are evaluated only when addressing customer compensation queries. They do not influence the technical severity of the underlying batch.
3. **Product Facts Grounding:** 
   - Queries regarding pillow materials, sizes, and care instructions are directed to `Sleepsia_Product_Care_and_Usage_Guide.docx` or the public URLs. The bot is restricted from using marketing copy to answer quality policy queries.

---

## 3. Retrieval Test Scenarios

The retrieval engine has been verified with targeted queries to ensure correct grounding and prevent hallucinations.

### Test Case K-01: Quality Severity Check
- **User Query:** "What happens if we find a safety concern like a burning smell on a pillow?"
- **Expected Grounding Source:** `Sleepsia_Product_Quality_Policy.docx`
- **Expected Response:** Immediate critical escalation and creation of a high-priority incident.
- **Pass Criteria:** Response matches internal quality policy rules; does not mention generic care steps.

### Test Case K-02: Public Fact Lookup
- **User Query:** "What are the dimensions of the Sleepsia Travel Pillow?"
- **Expected Grounding Source:** `https://www.sleepsia.in/products/travel-pillow`
- **Expected Response:** Precise specifications of the travel pillow (e.g., dimensions and materials).
- **Pass Criteria:** Grounded in public URL data; citation link is present in response.

### Test Case K-03: Conflict Mitigation Check
- **User Query:** "A customer claims their pillow has a bad odor. Do we issue a full refund immediately?"
- **Expected Grounding Source:** `Sleepsia_Customer_Resolution_Policy.docx` (primary) and `Sleepsia_Product_Quality_Policy.docx` (secondary)
- **Expected Response:** Outline the refund verification process (from Customer Resolution Policy) while noting that the odor complaint must be logged in the quality tracker (from Product Quality Policy).
- **Pass Criteria:** Shows distinct understanding of refund rules versus quality logging; no blending of policies.
