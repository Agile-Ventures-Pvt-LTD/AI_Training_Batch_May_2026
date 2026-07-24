# Knowledge Sources

## Overview

The chatbot uses Retrieval-Augmented Generation (RAG) with official documentation and NovaRetail policies to provide accurate, grounded, and product-specific responses.

---

# Configured Knowledge Sources

| Source Type | Knowledge Source | Purpose |
|-------------|------------------|---------|
| Markdown | NovaCare Limited Warranty Policy | Warranty guidance |
| Markdown | Product Support Scope | Supported products and support boundaries |
| Markdown | Product Safety & Escalation Policy | Safety assessment and escalation |
| PDF | Lenovo ThinkPad E14 Gen 5 & E16 Gen 1 User Guide | Laptop setup and troubleshooting |
| PDF | HP LaserJet Pro M428–M429 User Guide | Printer setup and troubleshooting |
| Website | Lenovo Online User Guide | Additional Lenovo product information |
| Website | HP Official Support Website | Additional HP support guidance |

---

# Knowledge Source Usage

The chatbot retrieves information only from the configured knowledge sources and does not generate unsupported product or warranty information.

---

# Knowledge Priority

| Priority | Source |
|----------|--------|
| 1 | NovaRetail Policies |
| 2 | Official Lenovo & HP PDF Manuals |
| 3 | Official Lenovo & HP Support Websites |

---

# Supported Products

- Lenovo ThinkPad E14 Gen 5
- Lenovo ThinkPad E16 Gen 1
- HP LaserJet Pro MFP M428–M429 Series

---

# Related Documents

- README.md
- agent-design.md
- custom-topic-design.md