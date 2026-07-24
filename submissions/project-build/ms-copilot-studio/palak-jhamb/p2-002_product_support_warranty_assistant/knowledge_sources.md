# Knowledge Sources

The NovaCare Product Support Assistant uses NovaRetail policy documents and official manufacturer documentation to provide grounded product support, troubleshooting, safety, and preliminary warranty guidance.

| Exact Source Name | Type | Title / Owner | Official Link | Purpose | Priority | Access Date | Retrieval Result | Limitations |
|---|---|---|---|---|---|---|---|---|
| **Hp website** | Public website | HP Support / HP Inc. | https://support.hp.com/us-en/product/setup-user-guides/hp-laserjet-pro-mfp-m428-m429-series/19202485 | Secondary source for HP LaserJet Pro MFP M428-M429 setup, operation, and troubleshooting guidance. | Secondary – Printer Technical | 24 Jul 2026 | Ready | Dynamic pages may not always index or retrieve consistently. |
| **Lenovo website** | Public website | Lenovo Support / Lenovo | https://download.lenovo.com/pccbbs/pubs/e14_gen5_e16_gen1/index_en.html | Secondary source for Lenovo ThinkPad E14 Gen 5 product operation and troubleshooting. | Secondary – Laptop Technical | 24 Jul 2026 | Ready | Website content may change and retrieval depends on successful indexing. |
| **Lenovo PDF user guide** | File / PDF | ThinkPad E14 Gen 5 / E16 Gen 1 User Guide – Lenovo | Uploaded knowledge file | Primary source for Lenovo laptop setup, operation, safety, and troubleshooting. | **Primary – Laptop Technical** | 24 Jul 2026 | Ready | Limited to information contained in the uploaded guide/version. |
| **HP PDF user guide** | File / PDF | HP LaserJet Pro MFP M329, M428-M429 User Guide – HP Inc. | Uploaded knowledge file | Primary source for supported HP printer setup, printing, scanning, maintenance, and troubleshooting. | **Primary – Printer Technical** | 24 Jul 2026 | Ready | Limited to information contained in the uploaded guide/version. |
| **NovaRetail Product Safety and Escalation Policy** | File | NovaRetail Technologies Pvt. Ltd. | Internal knowledge file | Defines safety indicators, mandatory safety responses, and escalation levels. | **Primary – Safety** | 24 Jul 2026 | Ready | Applies only to the defined NovaRetail support and escalation scope. |
| **NovaCare Limited Warranty Policy** | File | NovaRetail Technologies Pvt. Ltd. | Internal knowledge file | Defines warranty periods, eligibility, exclusions, DOA rules, and warranty boundaries. | **Primary – Warranty** | 24 Jul 2026 | Ready | Assessments are preliminary; final decisions require authorised human validation. |
| **NovaRetail Product Support Scope** | File | NovaRetail Technologies Pvt. Ltd. | Internal knowledge file | Defines supported products, models, issue categories, and unsupported-product handling. | **Primary – Product Scope** | 24 Jul 2026 | Ready | Model-specific support is limited to products explicitly included in the scope. |

## Source Priority

### Product Troubleshooting
1. Official product-manual PDF
2. Official manufacturer website
3. NovaRetail Product Support Scope

### Warranty
1. NovaCare Limited Warranty Policy
2. NovaRetail Product Safety and Escalation Policy
3. Relevant official manufacturer information

### Safety
1. NovaRetail Product Safety and Escalation Policy
2. Official manufacturer safety documentation
3. Human escalation when information is unavailable or uncertain

## Retrieval and Grounding Rules

All seven configured knowledge sources currently show a **Ready** status in Microsoft Copilot Studio.

The agent selects the source according to the product and question type. Lenovo sources are used for Lenovo laptop technical guidance, HP sources for HP printer technical guidance, and NovaRetail policies for warranty, safety, escalation, and supported-product decisions.

The agent must not invent missing product specifications, error-code meanings, warranty rules, or troubleshooting procedures. When reliable information cannot be retrieved, it should clearly state the limitation and recommend the appropriate human-support route.
