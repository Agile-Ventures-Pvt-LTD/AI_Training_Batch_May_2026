# Knowledge Sources Registry

| Source Name | Type | Owner | Official Link / File Name | Purpose & Priority | Retrieval Result & Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `NovaCare_Warranty_Policy` | Markdown File | NovaRetail | `novacare-limited-warranty-policy.md` | **Priority 1 (Warranty):** 12-month standard terms, 6-month battery rule, exclusions, and DOA criteria. | **Active.** Overrides manufacturer warranty terms. |
| `NovaRetail_Support_Scope` | Markdown File | NovaRetail | `product-support-scope.md` | **Priority 1 (Scope):** Defines supported models and troubleshooting boundaries. | **Active.** Filters out unsupported brands. |
| `NovaRetail_Safety_Policy` | Markdown File | NovaRetail | `product-safety-and-escalation-policy.md` | **Priority 1 (Safety):** Defines hazards and Level 1-4 escalation rules. | **Active.** Triggers emergency instructions. |
| `Lenovo_Laptop_Manual_PDF` | Official PDF | Lenovo | `Lenovo_ThinkPad_E14_E16_UserGuide.pdf` | **Priority 1 (Technical):** Setup, battery, display, and reset instructions. | **Active.** Primary source for laptop RAG answers. |
| `HP_Printer_Manual_PDF` | Official PDF | HP | `HP_LaserJet_MFP_M428_M429_Manual.pdf` | **Priority 1 (Technical):** Paper jams, offline errors, and control panel codes. | **Active.** Primary source for printer RAG answers. |
| `Lenovo_Online_Support_Web` | Public Website | Lenovo | `https://pcsupport.lenovo.com/...` | **Priority 2 (Supplementary):** Online reference for drivers and general diagnostics. | **Active.** Fallback if PDF lacks specific syntax. |
| `HP_Online_Support_Web` | Public Website | HP | `https://support.hp.com/in-en` | **Priority 2 (Supplementary):** General HP support navigation. | **Limited Indexing.** Uses uploaded PDF as primary fallback. |