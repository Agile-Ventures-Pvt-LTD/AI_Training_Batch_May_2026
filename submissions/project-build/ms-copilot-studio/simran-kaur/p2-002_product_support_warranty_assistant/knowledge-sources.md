# Knowledge Sources Document

## 1. Overview

The NovaCare Product Support and Warranty Assistant uses Microsoft Copilot Studio knowledge sources to provide grounded product support, troubleshooting guidance, warranty information, and safety instructions.

The knowledge architecture follows strict source precedence rules:

- Official manufacturer documentation is used for product operation and troubleshooting.
- NovaRetail-created policy documents are used for warranty and safety decisions.
- General AI knowledge is not used as a replacement for missing approved information.

---

# 2. Knowledge Source Summary

| Source Name | Source Type | Owner | Priority |
|---|---|---|---|
| NovaCare Limited Warranty Policy | Markdown Document | NovaRetail Technologies Pvt. Ltd. | 1 - Warranty Decisions |
| NovaRetail Product Support Scope | Markdown Document | NovaRetail Technologies Pvt. Ltd. | 2 - Product Scope Validation |
| NovaRetail Product Safety and Escalation Policy | Markdown Document | NovaRetail Technologies Pvt. Ltd. | 1 - Safety Decisions |
| Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 User Guide | PDF Manual | Lenovo | 1 - Laptop Technical Support |
| Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 Online User Guide | Public Website | Lenovo | 2 - Laptop Technical Support |
| HP LaserJet Pro MFP M329, M428-M429 User Guide | PDF Manual | HP | 1 - Printer Technical Support |
| HP LaserJet Pro MFP M428-M429 Setup and User Guides | Public Website | HP | 2 - Printer Technical Support |

---

# 3. NovaCare Limited Warranty Policy

## Source Details

**Source Name:**  
NovaCare Limited Warranty Policy

**Source Type:**  
Markdown Knowledge Document

**Title:**  
NovaCare Limited Warranty Policy Version 1.0

**Owner:**  
NovaRetail Technologies Pvt. Ltd.

**Official Link:**  
Internal NovaRetail knowledge-base document:
`knowledge-base/novacare-limited-warranty-policy.md`

**Access Date:**  
24 July 2026

---

## Purpose

This document defines the official NovaRetail warranty rules used for preliminary warranty assessment.

The source provides:

- Standard warranty duration.
- Warranty eligibility conditions.
- Covered and excluded scenarios.
- Battery and accessory coverage periods.
- Dead-on-arrival assessment rules.
- Required documents.
- Warranty escalation conditions.

---

## Priority

**Priority Level: 1**

Used as the primary authority for:

- Warranty eligibility.
- Warranty exclusions.
- Coverage periods.
- Service-route classification.

This source overrides manufacturer warranty assumptions for NovaRetail warranty decisions.

---

## Retrieval Result

**Status:** Successfully configured and tested.

Expected retrieval examples:

- Warranty duration questions.
- Accidental damage exclusions.
- Battery coverage period.
- Missing invoice handling.
- Dead-on-arrival assessment.

---

## Limitations

- Does not provide live warranty status.
- Does not access customer purchase records.
- Does not approve or reject warranty claims.
- Provides preliminary guidance only.
- Final decisions require authorised human validation.

---

# 4. NovaRetail Product Support Scope

## Source Details

**Source Name:**  
NovaRetail Product Support Scope

**Source Type:**  
Markdown Knowledge Document

**Title:**  
Product Support Scope

**Owner:**  
NovaRetail Technologies Pvt. Ltd.

**Official Link:**  
Internal NovaRetail knowledge-base document:
`knowledge-base/product-support-scope.md`

**Access Date:**  
24 July 2026

---

## Purpose

Defines supported products and prevents unsupported product guidance.

The source provides:

- Supported product families.
- Supported models.
- Allowed troubleshooting categories.
- Product identification rules.
- Scope restrictions.

Supported products:

- Lenovo ThinkPad E14 Gen 5 laptop.
- HP LaserJet Pro MFP M428-M429 printer.
- Bundled charger.
- Bundled power cable.

---

## Priority

**Priority Level: 2**

Used for:

- Product validation.
- Model identification.
- Scope enforcement.

---

## Retrieval Result

**Status:** Successfully configured and tested.

Expected retrieval examples:

- Supported model verification.
- Unsupported product handling.
- Product category identification.

---

## Limitations

- Does not contain detailed technical procedures.
- Does not replace manufacturer manuals.
- Does not provide warranty rules.

---

# 5. NovaRetail Product Safety and Escalation Policy

## Source Details

**Source Name:**  
NovaRetail Product Safety and Escalation Policy

**Source Type:**  
Markdown Knowledge Document

**Title:**  
Product Safety and Escalation Policy

**Owner:**  
NovaRetail Technologies Pvt. Ltd.

**Official Link:**  
Internal NovaRetail knowledge-base document:
`knowledge-base/product-safety-and-escalation-policy.md`

**Access Date:**  
24 July 2026

---

## Purpose

Defines mandatory safety handling behaviour before troubleshooting or warranty assessment.

The source provides:

- Safety-critical conditions.
- Safety classification levels.
- Required customer instructions.
- Escalation rules.

Safety conditions include:

- Smoke.
- Fire.
- Sparks.
- Electric shock.
- Burning smell.
- Battery swelling.
- Liquid exposure.
- Exposed wiring.

---

## Priority

**Priority Level: 1**

Used as the highest authority for safety-related decisions.

---

## Retrieval Result

**Status:** Successfully configured and tested.

Expected retrieval examples:

- Smoke from device.
- Swollen battery.
- Electrical shock.
- Liquid damage.

---

## Limitations

- Does not diagnose hardware failures.
- Does not provide repair instructions.
- Cannot contact emergency services automatically.

---

# 6. Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 User Guide

## Source Details

**Source Name:**  
Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 User Guide

**Source Type:**  
Official PDF Manual

**Title:**  
ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 User Guide

**Owner:**  
Lenovo

**Official Link:**  
Lenovo Official Support Documentation

`https://download.lenovo.com/pccbbs/mobiles_pdf/tp_e14_e16_gen5_ug_en.pdf`

**Access Date:**  
24 July 2026

---

## Purpose

Provides official technical information for Lenovo laptop support.

Used for:

- Laptop setup.
- Hardware features.
- Charging guidance.
- Battery information.
- Display troubleshooting.
- Network connectivity.
- Keyboard and touchpad guidance.
- Diagnostics.

---

## Priority

**Priority Level: 1**

Primary source for Lenovo ThinkPad troubleshooting.

---

## Retrieval Result

**Status:** Successfully uploaded and configured in Copilot Studio.

Tested retrieval scenarios:

- Laptop charging issues.
- Display problems.
- Wi-Fi connectivity.
- Power-related issues.

---

## Limitations

- Used only for technical guidance.
- Not used for NovaRetail warranty decisions.
- Applies only to supported Lenovo ThinkPad models.
- Does not provide live repair information.

---

# 7. Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 Online User Guide

## Source Details

**Source Name:**  
Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 Online User Guide

**Source Type:**  
Official Public Website Knowledge Source

**Title:**  
ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 Online User Guide

**Owner:**  
Lenovo

**Official Link:**  
Lenovo Support Website

`https://download.lenovo.com/pccbbs/pubs/tp_e14_e16_gen5/index_en.html`

**Access Date:**  
24 July 2026

---

## Purpose

Provides online Lenovo documentation for:

- Product navigation.
- Setup information.
- Power management.
- Connectivity.
- Troubleshooting references.

---

## Priority

**Priority Level: 2**

Secondary Lenovo technical source after the official PDF manual.

---

## Retrieval Result

**Status:** Added as public website knowledge source.

Retrieval tested for:

- Setup guidance.
- Product navigation.
- Connectivity information.

---

## Limitations

- Website indexing may vary.
- PDF manual remains the authoritative Lenovo source.
- Does not determine warranty eligibility.

---

# 8. HP LaserJet Pro MFP M329, M428-M429 User Guide

## Source Details

**Source Name:**  
HP LaserJet Pro MFP M329, M428-M429 User Guide

**Source Type:**  
Official PDF Manual

**Title:**  
HP LaserJet Pro MFP M329, M428-M429 User Guide

**Owner:**  
HP

**Official Link:**  
HP Official Support Documentation

`https://h10032.www1.hp.com/ctg/Manual/c06296566.pdf`

**Access Date:**  
24 July 2026

---

## Purpose

Provides official printer troubleshooting information.

Used for:

- Printer setup.
- Printing issues.
- Scanning.
- Paper jams.
- Connectivity.
- Print quality.
- Toner guidance.
- Error conditions.

---

## Priority

**Priority Level: 1**

Primary source for HP printer troubleshooting.

---

## Retrieval Result

**Status:** Successfully uploaded and configured in Copilot Studio.

Tested retrieval scenarios:

- Printer offline.
- Paper jam.
- Print quality issues.
- Scan failures.

---

## Limitations

- Applies only to HP LaserJet Pro MFP M428-M429 series.
- Does not provide NovaRetail warranty decisions.
- Does not provide live support status.

---

# 9. HP LaserJet Pro MFP M428-M429 Setup and User Guides

## Source Details

**Source Name:**  
HP LaserJet Pro MFP M428-M429 Setup and User Guides

**Source Type:**  
Official Public Website Knowledge Source

**Title:**  
HP LaserJet Pro MFP M428-M429 Setup and User Guides

**Owner:**  
HP

**Official Link:**  
HP Support Website

`https://support.hp.com`

**Access Date:**  
24 July 2026

---

## Purpose

Provides official online HP support resources.

Used for:

- Setup information.
- Installation guidance.
- Support documentation.
- Printer navigation.

---

## Priority

**Priority Level: 2**

Secondary source after HP PDF manual.

---

## Retrieval Result

**Status:** Configured and tested where indexing was available.

---

## Limitations

- HP website content may depend on dynamic rendering.
- PDF manual remains the authoritative printer troubleshooting source.
- Website availability does not guarantee all pages are indexed.

---

# 10. Knowledge Conflict Resolution

When multiple sources provide different information, the agent follows:

## Product Troubleshooting

1. Official product manual PDF.
2. Official manufacturer website.
3. NovaRetail Product Support Scope.

## Warranty Decisions

1. NovaCare Limited Warranty Policy.
2. NovaRetail Safety Policy.
3. Manufacturer warranty references.

## Safety Decisions

1. NovaRetail Safety and Escalation Policy.
2. Manufacturer safety instructions.
3. Human escalation.

The agent must not silently combine conflicting information.

---

# 11. Overall Knowledge Configuration Status

| Area | Status |
|---|---|
| NovaRetail Warranty Policy | Configured |
| Product Support Scope | Configured |
| Safety Policy | Configured |
| Lenovo PDF Manual | Configured |
| Lenovo Website | Configured |
| HP PDF Manual | Configured |
| HP Website | Configured |
| Retrieval Testing | Completed |
