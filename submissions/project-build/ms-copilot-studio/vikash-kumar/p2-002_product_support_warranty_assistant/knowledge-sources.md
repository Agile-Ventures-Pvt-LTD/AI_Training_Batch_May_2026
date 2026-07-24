# Knowledge Sources

## Overview

The NovaRetail Product Support & Warranty Assistant uses Retrieval-Augmented Generation (RAG) with official company policies, product documentation, and manufacturer support websites. Responses are generated only from configured knowledge sources to ensure accuracy, consistency, and compliance with project requirements.

---

# Knowledge Source Summary

| Priority | Source Name | Type | Purpose |
|----------|-------------|------|---------|
| 1 | Product Safety and Escalation Policy | Markdown | Safety assessment and escalation |
| 2 | NovaCare Limited Warranty Policy | Markdown | Warranty eligibility guidance |
| 3 | Product Support Scope | Markdown | Supported products and service scope |
| 4 | Lenovo ThinkPad E14 Gen 5 User Guide | PDF | Laptop troubleshooting |
| 5 | HP LaserJet Pro MFP M428-M429 User Guide | PDF | Printer troubleshooting |
| 6 | Lenovo Support Website | Website | Official Lenovo support information |
| 7 | HP Support Website | Website | Official HP support information |

---

# Knowledge Source Details

## 1. Product Safety and Escalation Policy

| Property | Value |
|----------|-------|
| **Source Name** | Product Safety and Escalation Policy |
| **Type** | Markdown Document |
| **Title** | Product Safety and Escalation Policy |
| **Owner** | NovaRetail |
| **Official Link** | Internal Project Document |
| **Purpose** | Defines mandatory safety checks, escalation rules, and prohibited troubleshooting actions. |
| **Priority** | Highest |
| **Access Date** | 24/07/2026 |
| **Retrieval Result** | Successfully indexed in Copilot Studio |
| **Limitations** | Applies only to supported products and project scenarios. |

---

## 2. NovaCare Limited Warranty Policy

| Property | Value |
|----------|-------|
| **Source Name** | NovaCare Limited Warranty Policy |
| **Type** | Markdown Document |
| **Title** | NovaCare Limited Warranty Policy |
| **Owner** | NovaRetail |
| **Official Link** | Internal Project Document |
| **Purpose** | Provides warranty coverage rules, exclusions, and preliminary warranty guidance. |
| **Priority** | High |
| **Access Date** | 24/07/2026 |
| **Retrieval Result** | Successfully indexed in Copilot Studio |
| **Limitations** | Final warranty decisions remain with authorised NovaRetail representatives. |

---

## 3. Product Support Scope

| Property | Value |
|----------|-------|
| **Source Name** | Product Support Scope |
| **Type** | Markdown Document |
| **Title** | Product Support Scope |
| **Owner** | NovaRetail |
| **Official Link** | Internal Project Document |
| **Purpose** | Defines supported products and service boundaries. |
| **Priority** | High |
| **Access Date** | 24/07/2026 |
| **Retrieval Result** | Successfully indexed in Copilot Studio |
| **Limitations** | Covers only products included in the project scope. |

---

## 4. Lenovo ThinkPad E14 Gen 5 User Guide

| Property | Value |
|----------|-------|
| **Source Name** | Lenovo ThinkPad E14 Gen 5 User Guide |
| **Type** | PDF Document |
| **Title** | Lenovo ThinkPad E14 Gen 5 User Guide |
| **Owner** | Lenovo |
| **Official Link** | https://support.lenovo.com |
| **Purpose** | Official troubleshooting, setup, maintenance, and operating instructions for the supported Lenovo laptop. |
| **Priority** | Medium |
| **Access Date** | 24/07/2026 |
| **Retrieval Result** | Successfully indexed in Copilot Studio |
| **Limitations** | Applies only to the Lenovo ThinkPad E14 Gen 5 model. |

---

## 5. HP LaserJet Pro MFP M428-M429 User Guide

| Property | Value |
|----------|-------|
| **Source Name** | HP LaserJet Pro MFP M428-M429 User Guide |
| **Type** | PDF Document |
| **Title** | HP LaserJet Pro MFP M428-M429 User Guide |
| **Owner** | HP Inc. |
| **Official Link** | https://support.hp.com |
| **Purpose** | Official troubleshooting, maintenance, printing, and scanning guidance for the supported HP printer. |
| **Priority** | Medium |
| **Access Date** | 24/07/2026 |
| **Retrieval Result** | Successfully indexed in Copilot Studio |
| **Limitations** | Applies only to the HP LaserJet Pro MFP M428-M429 series. |

---

## 6. Lenovo Support Website

| Property | Value |
|----------|-------|
| **Source Name** | Lenovo Support Website |
| **Type** | Website |
| **Title** | Lenovo Support |
| **Owner** | Lenovo |
| **Official Link** | https://support.lenovo.com |
| **Purpose** | Provides official online troubleshooting articles, drivers, firmware, FAQs, and product documentation. |
| **Priority** | Medium |
| **Access Date** | 24/07/2026|
| **Retrieval Result** | Successfully connected as a knowledge source |
| **Limitations** | Responses are limited to content available through the configured knowledge source. |

---

## 7. HP Support Website

| Property | Value |
|----------|-------|
| **Source Name** | HP Support Website |
| **Type** | Website |
| **Title** | HP Customer Support |
| **Owner** | HP Inc. |
| **Official Link** | https://support.hp.com |
| **Purpose** | Provides official troubleshooting articles, printer documentation, firmware updates, and FAQs. |
| **Priority** | Medium |
| **Access Date** | 24/07/2026 |
| **Retrieval Result** | Successfully connected as a knowledge source |
| **Limitations** | Responses are limited to content available through the configured knowledge source. |

---

# Knowledge Source Precedence

When multiple knowledge sources contain relevant information, the assistant follows this order of precedence:

1. Product Safety and Escalation Policy
2. NovaCare Limited Warranty Policy
3. Product Support Scope
4. Lenovo ThinkPad E14 Gen 5 User Guide
5. HP LaserJet Pro MFP M428-M429 User Guide
6. Lenovo Support Website
7. HP Support Website

Higher-priority sources override lower-priority sources if conflicting information exists.

---

# Retrieval Strategy

The assistant follows these retrieval principles:

- Retrieve information only from configured knowledge sources.
- Use product-specific documentation whenever available.
- Prioritize official policy documents for warranty and safety guidance.
- Do not generate unsupported technical or warranty information.
- Clearly state when the required information is unavailable.

---

# Limitations

The configured knowledge sources:

- Cover only the supported products defined in the project scope.
- Do not provide access to customer account information.
- Do not provide repair status or inventory availability.
- Do not integrate with CRM, ERP, or ticketing systems.
- Do not authorize warranty claims or repair approvals.
- May not contain information for unsupported products or future product releases.