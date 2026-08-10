# Known Limitations

This document outlines the functional and technical limitations of the current implementation of the **NovaRetail Support and Warranty Assistant**.

---

## 1. Integration Limitations

- **No Live Warranty Database Lookup:** The chatbot cannot connect to active customer databases or live ERP systems to retrieve order history, verify purchase invoice details, or validate serial numbers. All inputs (purchase date, invoice availability, serial match) are gathered via structured conversation questions and must be validated manually by human support.
- **No Direct Case Creation:** The chatbot cannot automatically write support tickets or warranty claims to CRM or ticketing systems (such as Salesforce or ServiceNow). Instead, the chatbot compiles a **Support Case Summary** at the end of the topic, which must be shared or copy-pasted for human follow-up.
- **No Live Repair Status tracking:** The chatbot cannot check the status of active repair jobs, return authorizations (RMA), or shipment schedules. If asked, the assistant will inform the user that live repair tracking is currently unavailable and escalate the case to Level 2 technical support.
- **No Inventory Visibility:** The chatbot has no access to warehouses or store inventory databases. It cannot check if replacement parts (such as laptop batteries, printer rollers, or chargers) are in stock.

---

## 2. Scope and Knowledge Limitations

- **Broad Product Coverage Limits:** Technical assistance is strictly limited to the reference models: **Lenovo ThinkPad E14 Gen 5** (laptop) and **HP LaserJet Pro MFP M428-M429** (printer), including their bundled charging accessories. General knowledge or search is disabled for all other models to prevent cross-product retrieval errors and hallucinations.
- **Emergency and Dispatch Limitations:** The chatbot cannot dispatch field technicians or coordinate emergency dispatch services. In safety-critical scenarios (fire, electric shock, injuries), the bot will advise the user to contact local emergency services (e.g., 100/101/112) immediately and move away from the product.
- **No Final Warranty Decisions:** The chatbot cannot make binding decisions to approve or reject warranty claims, nor can it authorize refunds, replacements, or commercial settlements. All warranty eligibility classifications are **preliminary** and must be reviewed and signed off by an authorized NovaRetail human representative.

---

## 3. Platform Limitations (Microsoft Copilot Studio)

- **Session Timeouts:** Standard webchat sessions expire after 15 minutes of user inactivity. Any unsaved troubleshooting step count or warranty date calculation will be lost upon session reset.
- **File Upload Parsing:** Document search is dependent on the Copilot Studio indexing service. If a complex layout in a product manual PDF is indexed incorrectly, the generative answers node may struggle to extract specific steps, in which case the user is redirected to a human technician.
- **Date Arithmetic Restrictions:** Due to platform-specific expressions in Power Fx / Copilot Studio, date age calculations rely on basic integer approximations of months between the current date (July 24, 2026) and the customer-input purchase date.
