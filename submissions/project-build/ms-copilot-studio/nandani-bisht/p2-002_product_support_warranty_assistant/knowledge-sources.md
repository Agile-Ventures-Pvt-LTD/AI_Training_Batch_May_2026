# Configured Knowledge Base Sources

The **NovaRetail Support and Warranty Assistant** utilizes 7 knowledge sources (2 official manual PDFs, 2 public support websites, and 3 internal policy documents) to ensure all customer support and warranty guidance is grounded and accurate.

---

## Knowledge Source Directory

| Source Name | Owner | Type | Official Link / File Name | Purpose | Priority / Precedence | Access Date | Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lenovo Laptop User Guide** | Lenovo | Official PDF | `ThinkPad E14 Gen 5 & E16 Gen 1 User Guide` | Technical specs, charging, display, and keyboard troubleshooting for Lenovo laptops. | **Priority 1** for laptop troubleshooting. | 24 July 2026 | PDF upload limit; does not cover NovaCare warranty terms. |
| **HP Printer User Guide** | HP | Official PDF | `HP LaserJet Pro MFP M329, M428-M429 User Guide` | Setup, paper jam resolution, scanning, and error codes for HP printers. | **Priority 1** for printer troubleshooting. | 24 July 2026 | Defer to PDF; verify that retrieved steps apply to the M428-M429 series specifically. |
| **Lenovo Support Website** | Lenovo | Official Website | [Lenovo E14 Gen 5 Online User Guide](https://pcsupport.lenovo.com/in/en/products/laptops-and-netbooks/thinkpad-edge-laptops/thinkpad-e14-gen-5-type-21jk-21jl) | Real-time laptop documentation, setup, and navigation guides. | **Priority 2** for laptop troubleshooting. | 24 July 2026 | Requires internet connection; must use English-language ending in `index_en.html`. |
| **HP Support Website** | HP | Official Website | [HP M428-M429 Setup & User Guides](https://support.hp.com/in-en) | Printer setup and online support articles. | **Priority 2** for printer troubleshooting. | 24 July 2026 | If website rendering prevents indexing, fallback to HP PDF as authoritative source. |
| **NovaCare Warranty Policy** | NovaRetail | Internal MD | `knowledge-base/novacare-limited-warranty-policy.md` | Authoritative source for warranty duration, coverage, exclusions, and DOA rules. | **Priority 1** for warranty eligibility. | 24 July 2026 | Internal document; cannot be modified by customer inquiries. |
| **Product Support Scope** | NovaRetail | Internal MD | `knowledge-base/product-support-scope.md` | Lists supported product models, categories, and general scope boundaries. | **Priority 3** for general support questions. | 24 July 2026 | Defines what models are out-of-scope. |
| **Product Safety and Escalation Policy** | NovaRetail | Internal MD | `knowledge-base/product-safety-and-escalation-policy.md` | Critical indicators, safety advice, escalation levels (1-4), and conflict handling rules. | **Priority 1** for safety & escalation routing. | 24 July 2026 | Safety instructions take absolute priority over any troubleshooting steps. |

---

## Grounding Rules and Precedence Implementation

To prevent cross-product retrieval errors and hallucinations, the following grounding controls are enforced in Copilot Studio:

1. **High Precision Node-Level Grounding:**
   - Technical questions about laptops redirect queries specifically to the **Lenovo Laptop User Guide** and **Lenovo Support Website**.
   - Technical questions about printers redirect queries specifically to the **HP Printer User Guide** and **HP Support Website**.
   - General warranty queries query only the **NovaCare Warranty Policy** and **Product Support Scope**.
2. **Conflict Resolution Strategy:**
   - If a manufacturer manual and the NovaCare policy conflict (e.g., regarding repair limits or warranty periods), the chatbot strictly follows **NovaCare Warranty Policy** and provides a citation explaining company policy precedence.
   - If a safety conflict is detected, the **Product Safety and Escalation Policy** immediately overrides all other documentation, stopping any technical steps.
3. **Citation Style:**
   - All generated answers are accompanied by standard inline citations referencing the source file name or official URL (e.g., *[Source: Lenovo User Guide PDF]* or *[Source: novacare-limited-warranty-policy.md]*).
