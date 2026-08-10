# Knowledge Sources

## Configured sources

| Source | Type | Purpose | Precedence |
|---|---|---|---|
| Sleepsia_Product_Quality_Policy.docx | File | Quality thresholds, classification, investigation, CAPA, escalation | Highest — authoritative for all internal quality decisions |
| Sleepsia_Product_Care_and_Usage_Guide.docx | File | Product care/use information, safety escalation boundary | Product care only |
| Sleepsia_Customer_Resolution_Policy.docx | File | Customer-resolution vs. quality ownership boundary | Customer-resolution boundary only |
| Sleepsia Travel Pillow page (sleepsia.in/products/travel-pillow) | Public URL | Public product facts | Lower than internal policy |
| Sleepsia Kids Pillow page (sleepsia.in/products/kids-alpha-pillow) | Public URL | Public product facts | Lower than internal policy |

## Precedence rule (enforced via Supervisor instructions)

The internal Sleepsia_Product_Quality_Policy.docx controls all quality severity, escalation, and CAPA decisions. Public Sleepsia URLs are used only to answer product-fact questions (materials, intended use, product names) in interactive mode, and must never override or be blended with internal quality rules. This precedence is stated explicitly in the Quality Supervisor's instructions: "When internal quality policy and a public Sleepsia page conflict on anything related to safety or quality, internal policy always wins."

## Retrieval tests


| Query | Expected source used | Actual source used | Pass/Fail |
|---|---|---|---|
| "What's the return-rate threshold for opening an investigation?" | Sleepsia_Product_Quality_Policy.docx | Sleepsia_Product_Quality_Policy.docx | pass |
| "What material is the Travel Neck Pillow made of?" | Sleepsia Travel Pillow public page | Sleepsia Travel Pillow public page | Pass |
| "Can we promise this customer a refund for a burning smell complaint?" | Should decline per scope boundary, not answer from any knowledge source as if authorising it | | pass |