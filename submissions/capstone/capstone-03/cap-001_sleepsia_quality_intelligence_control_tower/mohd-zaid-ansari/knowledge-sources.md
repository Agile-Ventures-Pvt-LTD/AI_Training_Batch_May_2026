# Knowledge Sources

## Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower uses internal knowledge documents and approved public product URLs to provide grounded responses during quality investigations. Internal policies always take precedence over public information.

---

# Configured Knowledge Sources

| Knowledge Source | Purpose | Authority |
|------------------|---------|-----------|
| **Sleepsia_Product_Quality_Policy.docx** | Defines quality thresholds, investigation rules, complaint classification, CAPA procedures, and escalation criteria. | **Highest authority** for all internal quality investigation and decision-making. |
| **Sleepsia_Product_Care_and_Usage_Guide.docx** | Provides product care instructions, usage guidelines, and product safety information. | Authoritative only for product care, usage guidance, and safety recommendations. |
| **Sleepsia_Customer_Resolution_Policy.docx** | Defines customer resolution processes and distinguishes customer service responsibilities from product quality investigations. | Highest authority for customer-resolution policies and ownership boundaries. |
| **Sleepsia Travel Pillow** | Public product specifications and feature information. | Public information only. Lower priority than internal policies. |
| **Sleepsia Kids Pillow** | Public product specifications and feature information. | Public information only. Lower priority than internal policies. |

---

# Approved Public URLs

- https://www.sleepsia.in/products/travel-pillow
- https://www.sleepsia.in/products/kids-alpha-pillow

---

# Knowledge Retrieval Precedence

The solution retrieves information using the following priority:

1. **Sleepsia_Product_Quality_Policy.docx**
2. **Sleepsia_Customer_Resolution_Policy.docx**
3. **Sleepsia_Product_Care_and_Usage_Guide.docx**
4. **Approved Sleepsia Public Product URLs**

If information exists in multiple sources, the higher-priority source is always used.

---

# Usage by Agents

| Agent | Knowledge Usage |
|---------|-----------------|
| Quality Supervisor | Internal quality policies and customer resolution policies |
| Complaint Pattern Specialist | Quality Policy |
| Returns Specialist | Customer Resolution Policy |
| Product/Batch Specialist | Product Care & Usage Guide and public product information |
| Customer Impact Specialist | Customer Resolution Policy |
| Safety Specialist | Product Care & Usage Guide and Quality Policy |
| CAPA Specialist | Quality Policy |
| M365 Guidance Specialist | Microsoft Learn MCP (not Sleepsia knowledge) |

---

# Knowledge Governance

- Use internal Sleepsia documents as the primary source of truth.
- Public URLs are used only for product information and specifications.
- Never use public information to override internal policies.
- Always return grounded, source-based responses.
- If information is unavailable in the configured knowledge sources, indicate that additional review is required rather than generating unsupported information.

---

# Conclusion

The configured knowledge sources ensure that every investigation follows approved Sleepsia quality policies while allowing public product information to supplement customer-facing responses without overriding internal business rules.