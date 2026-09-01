# Knowledge Sources

**Project ID:** P2-002
**Agent Name:** NovaCare Assist
**Participant:** Taniya Gupta
**Date:** 24 July 2026

---

## Knowledge Source 1 — NovaCare Limited Warranty Policy

| Field | Value |
|---|---|
| **Source Name in Copilot Studio** | NovaCare Limited Warranty Policy |
| **Type** | Markdown file (participant-created, uploaded) |
| **File** | knowledge-base/novacare-limited-warranty-policy.md |
| **Purpose** | Primary authority for all warranty eligibility decisions — coverage periods, exclusions, DOA rules, repair limitations, chatbot boundaries |
| **Priority** | Highest for all warranty and service-route decisions |
| **Access Date** | 24 July 2026 (created) |
| **Retrieval Test Result** | Pass — correctly returned 12-month coverage period for laptop query |

**Description used in Copilot Studio:**
> NovaRetail NovaCare warranty policy v1.0 — effective 1 July 2026. Defines 12-month product warranty, 6-month battery and accessory coverage, consumable exclusions, dead-on-arrival rules, and escalation requirements. Use this as the primary authority for all warranty eligibility decisions. Do not override with manufacturer warranty information for NovaRetail eligibility assessment.

---

## Knowledge Source 2 — NovaRetail Product Support Scope

| Field | Value |
|---|---|
| **Source Name in Copilot Studio** | NovaRetail Product Support Scope |
| **Type** | Markdown file (participant-created, uploaded) |
| **File** | knowledge-base/product-support-scope.md |
| **Purpose** | Defines which product families and models are supported, what issue categories are covered, and the scope rules for knowledge selection |
| **Priority** | Secondary reference for scope and product validation decisions |
| **Access Date** | 24 July 2026 (created) |
| **Retrieval Test Result** | Pass — accurately restricted guidance to supported models |

**Description used in Copilot Studio:**
> Defines supported product families (Lenovo ThinkPad E14 Gen 5, HP LaserJet Pro M428-M429), supported troubleshooting categories per product, and scope rules. Use to determine whether a product or issue is supported before providing guidance. Do not use as the source for warranty or safety decisions.

---

## Knowledge Source 3 — Product Safety and Escalation Policy

| Field | Value |
|---|---|
| **Source Name in Copilot Studio** | Product Safety and Escalation Policy |
| **Type** | Markdown file (participant-created, uploaded) |
| **File** | knowledge-base/product-safety-and-escalation-policy.md |
| **Purpose** | Defines safety-critical conditions, mandatory safety behaviour, four escalation levels, and escalation handling requirements |
| **Priority** | Highest for all safety-related decisions — overrides troubleshooting and warranty questioning |
| **Access Date** | 24 July 2026 (created) |
| **Retrieval Test Result** | Pass — successfully identified safety conditions and triggered Level 4 |

**Description used in Copilot Studio:**
> Defines safety-critical conditions (smoke, fire, electric shock, swollen battery, liquid ingress, etc.), mandatory safety behaviour when these are detected, and four escalation levels (L1 self-service through L4 urgent safety). Must be consulted before any troubleshooting step. Level 4 conditions stop all routine processing immediately.

---

## Knowledge Source 4 — Lenovo ThinkPad E14 Gen 5 User Guide (PDF)

| Field | Value |
|---|---|
| **Source Name in Copilot Studio** | Lenovo ThinkPad E14 Gen 5 User Guide |
| **Type** | Official PDF (downloaded from Lenovo, uploaded to Copilot Studio) |
| **File** | e14_gen5_e16_gen1_ug_en.pdf |
| **Purpose** | Primary source for all Lenovo ThinkPad E14 Gen 5 laptop troubleshooting — setup, power, charging, display, connectivity, keyboard, diagnostics |
| **Priority** | Highest for laptop technical guidance |
| **Access Date** | 24 July 2026 |
| **Retrieval Test Result** | Pass — correctly returned charging procedure from Chapter 3 |

**Description used in Copilot Studio:**
> Official Lenovo PDF user guide for ThinkPad E14 Gen 5 (21JK, 21JL) and E16 Gen 1. Use for all laptop setup, hardware, charging, display, connectivity, keyboard, diagnostics, and model-specific troubleshooting. Do not use for printer guidance. Do not use for warranty eligibility — refer to NovaCare Limited Warranty Policy instead.

---

## Knowledge Source 5 — HP LaserJet Pro MFP M428-M429 User Guide (PDF)

| Field | Value |
|---|---|
| **Source Name in Copilot Studio** | HP LaserJet Pro MFP M428-M429 User Guide |
| **Type** | Official PDF (downloaded from HP, uploaded to Copilot Studio) |
| **File** | c06184015.pdf (HP LaserJet Pro MFP M329, M428-M429 User Guide) |
| **Purpose** | Primary source for all HP LaserJet Pro MFP M428-M429 printer troubleshooting — setup, printing, scanning, paper jams, toner, maintenance, error messages |
| **Priority** | Highest for printer technical guidance |
| **Access Date** | 24 July 2026 |
| **Retrieval Test Result** | Pass — correctly returned paper jam clearing instructions |

**Description used in Copilot Studio:**
> Official HP PDF user guide for LaserJet Pro MFP M428-M429 series. Use for printer setup, printing, copying, scanning, paper jams, toner, connectivity, and error conditions. Verify that guidance applies to M428-M429 before presenting. Do not use for laptop guidance. Do not use for warranty eligibility — refer to NovaCare Limited Warranty Policy.

---

## Knowledge Source 6 — Lenovo ThinkPad E14 Gen 5 Online User Guide (Website)

| Field | Value |
|---|---|
| **Source Name in Copilot Studio** | Lenovo ThinkPad E14 Online User Guide |
| **Type** | Public website URL (added via Public websites option) |
| **Purpose** | Supplementary online laptop documentation — power management, connectivity, setup, troubleshooting navigation |
| **Priority** | Secondary for laptop guidance (after the PDF) |
| **Access Date** | 24 July 2026 |
| **Retrieval Test Result** | Pass — correctly answered external display setup question |

**Description used in Copilot Studio:**
> Official online Lenovo documentation for ThinkPad E14 Gen 5. Use as a supplement to the Lenovo PDF for additional laptop setup, connectivity, and troubleshooting information. Use the English-language version only. Do not use for printer guidance or warranty decisions.

---

## Knowledge Source 7 — HP LaserJet Pro M428-M429 Setup and Support Website (Website)

| Field | Value |
|---|---|
| **Source Name in Copilot Studio** | HP LaserJet Pro M428-M429 Setup and Support Website |
| **Type** | Public website URL (added via Public websites option) |
| **Purpose** | Supplementary HP printer documentation — setup manuals, support articles, model-specific resources |
| **Priority** | Secondary for printer guidance (after the HP PDF) |
| **Access Date** | 24 July 2026 |
| **Retrieval Test Result** | Pass — correctly retrieved Wi-Fi Direct setup instructions |

**Description used in Copilot Studio:**
> Official HP support website for LaserJet Pro MFP M428-M429. Use as a supplement to the HP PDF for setup manuals, installation guidance, and model-specific support resources. If dynamic rendering prevents indexing, use the HP PDF as the authoritative fallback and document the limitation.

---
