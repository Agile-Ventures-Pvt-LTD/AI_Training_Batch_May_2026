# Known Limitations

---

# Purpose

This document describes the known functional, technical, and operational limitations of the Product Support and Warranty Assistant.

These limitations are intentional and align with the project scope defined for the chatbot. They ensure that the assistant provides safe, reliable, and policy-compliant guidance without making decisions that require human authorization.

---

# Functional Limitations

## Supported Products Only

The chatbot only supports the following products:

### Laptop

- Lenovo ThinkPad E14 Gen 5

### Printer

- HP LaserJet Pro MFP M428-M429

Requests related to unsupported products receive general guidance or are redirected to human support.

---

## Limited Product Categories

The chatbot currently supports only:

- Laptop
- Printer

Other product categories such as desktops, monitors, tablets, servers, networking devices, accessories not covered by the policy, or third-party hardware are outside the scope of this implementation.

---

## Model-Specific Guidance

Model-specific troubleshooting is only available for supported products.

If the customer provides an unknown or unsupported model, the chatbot does not generate technical instructions and recommends contacting technical support.

---

# Warranty Assessment Limitations

The chatbot performs only a **preliminary warranty assessment**.

It does **not**:

- Approve warranty claims.
- Reject warranty claims.
- Guarantee repair eligibility.
- Guarantee replacement eligibility.
- Create warranty claims.
- Submit service requests.
- Verify warranty status from a live database.
- Override company warranty policies.

Final decisions must always be made by an authorized NovaRetail representative.

---

# No Live System Integration

The chatbot is not connected to live enterprise systems.

It cannot access:

- Customer accounts
- Warranty databases
- CRM systems
- Service management systems
- Repair history databases
- Inventory systems
- Order management systems
- Delivery tracking systems

All responses are based only on configured knowledge sources and information provided by the customer.

---

# Limited Troubleshooting Scope

The chatbot provides only first-line troubleshooting.

It does not:

- Perform remote diagnostics
- Control customer devices
- Access system logs
- Execute software updates
- Install drivers
- Modify operating system settings automatically
- Repair hardware
- Confirm that a repair has been completed

---

# Safety Restrictions

For customer safety, the chatbot intentionally avoids:

- Instructing customers to open electronic devices
- Asking customers to dismantle hardware
- Suggesting electrical repairs
- Recommending battery disassembly
- Continuing troubleshooting after a safety-critical condition has been identified

Safety-critical cases are immediately escalated to human support.

---

# Product Documentation Dependency

The chatbot answers technical questions using configured knowledge sources.

If required information is not available in:

- Lenovo documentation
- HP documentation
- NovaCare Warranty Policy
- Product Support Scope
- Product Safety Policy

the chatbot informs the customer that the information is unavailable instead of generating unsupported answers.

---

# Knowledge Source Coverage

The chatbot only retrieves information from approved knowledge sources.

It does not use:

- Community forums
- Blogs
- Social media
- Third-party repair websites
- User-generated content
- Unverified technical articles

This restriction improves reliability but may reduce the amount of available information.

---

# Warranty Policy Scope

The implemented warranty logic follows the provided NovaCare policy.

The chatbot does not evaluate:

- Country-specific consumer protection laws
- Extended warranties
- Third-party warranty providers
- Insurance claims
- Retailer-specific replacement policies

---

# Product Age Calculation

Warranty periods are calculated using the purchase date provided by the customer.

Incorrect or missing purchase information may affect the preliminary assessment.

The chatbot requests corrections when invalid dates are detected.

---

# No Image Analysis

The chatbot cannot currently analyze:

- Product photographs
- Physical damage images
- Error screen screenshots
- Printed output quality
- Serial number labels

All assessments rely on customer descriptions.

---

# No Document Verification

The chatbot cannot verify uploaded documents such as:

- Purchase invoices
- Warranty cards
- Delivery receipts
- Service reports

Customers may be asked to provide these documents during human review.

---

# Limited Personalization

The chatbot does not maintain customer profiles or long-term conversation history.

Each conversation is treated independently unless the platform provides session context.

---

# Language Support

The chatbot is currently designed for English-language conversations only.

Support for additional languages is outside the scope of this implementation.

---

# Performance Limitations

Response quality depends on:

- Availability of relevant knowledge sources
- Accuracy of customer-provided information
- Supported product models
- Clarity of customer questions

Ambiguous or incomplete requests may require additional clarification.

---

# AI Limitations

Although the chatbot uses Retrieval-Augmented Generation (RAG), AI-generated responses may still be limited by:

- Missing documentation
- Ambiguous customer input
- Conflicting information
- Unsupported scenarios

When information cannot be verified, the chatbot explicitly states that the information is unavailable rather than guessing.

---

# Privacy Limitations

To protect customer privacy, the chatbot intentionally avoids requesting:

- Passwords
- PINs
- Banking information
- Credit or debit card details
- Confidential documents
- Personal files

This may prevent the chatbot from resolving issues that require account verification.

---

# Escalation Limitations

The chatbot recommends escalation but cannot:

- Assign technicians
- Schedule repairs
- Create support tickets
- Book appointments
- Contact emergency services on behalf of the customer

Customers must follow the provided guidance to reach the appropriate support channel.

---

# Current Technical Constraints

The current implementation does not include:

- Dynamics 365 integration
- Microsoft Dataverse integration
- Live Power Automate workflows
- CRM connectivity
- Inventory lookup
- Shipment tracking
- Repair tracking
- Automated email notifications
- SMS notifications
- Push notifications
- Voice interaction
- OCR-based invoice verification
- Image recognition
- Barcode or QR code scanning

These capabilities can be added in future versions through additional integrations.

---

# Future Enhancement Opportunities

Potential future improvements include:

- Live warranty verification
- CRM integration
- Automatic support ticket creation
- Repair appointment scheduling
- Real-time inventory availability
- Multilingual support
- Voice-enabled conversations
- Image-based diagnostics
- OCR invoice processing
- Product serial number recognition
- Customer authentication
- Personalized customer profiles
- Microsoft Teams integration
- Power BI reporting dashboard

---

# Conclusion

The Product Support and Warranty Assistant is intentionally designed as a **first-line support solution**. It focuses on delivering safe, consistent, and policy-compliant guidance while avoiding actions that require human judgment, access to enterprise systems, or legal authority.

These limitations ensure that the chatbot remains reliable, transparent, and aligned with NovaRetail's operational policies while providing an effective customer support experience.