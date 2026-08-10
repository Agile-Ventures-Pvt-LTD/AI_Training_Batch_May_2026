# Custom Topic Design

## Custom Topic 1 – Guided Product Troubleshooting and Safety Triage

**Purpose**
Guide users through troubleshooting while checking for safety issues.

**Triggers**
Laptop issue, printer issue, device not working, troubleshooting help.

**Inputs**
Product family, model, issue description, issue category, safety symptoms.

**Variables**
ProductFamily, ProductModel, IssueCategory, ProductStillWorks, TroubleshootingCompleted, Safety flags.

**Entities**
Product Family, Product Model, Issue Category.

**Validation**
Supported product, required inputs, valid responses.

**Conditions**
Safety detection, troubleshooting progress, issue resolved.

**Loop**
Continue troubleshooting until resolved, cancelled, or safety issue detected.

**Redirects**
- Product Safety Assessment
- Warranty Eligibility and Service Route Assessment

**Knowledge Sources**
- HP printer manual PDF
- Lenovo laptop manual PDF
- Lenovo Support
- HP Support
- novacare-limited-warranty-policy
- product-safety-and-escalation-policy
- product-support-scope

**Outcome**
Issue resolved, safety escalation, or warranty assessment.

**Escalation**
Smoke, fire, sparks, burning smell, electric shock, excessive heat, damaged/swollen battery.

**Cancellation**
User cancels or unsupported product.

**Limitations**
Supports only laptops and printers.

---

## Custom Topic 2 – Warranty Eligibility and Service Route Assessment

**Purpose**
Provide preliminary warranty guidance and recommend the appropriate service route.

**Triggers**
Warranty, repair, replacement, coverage, warranty status.

**Inputs**
Product details, purchase information, damage indicators, troubleshooting status.

**Variables**
PurchaseDate, ProductAge, InvoiceAvailable, AccidentalDamage, LiquidDamage, ConsumableItem, PreliminaryClassification, RecommendedServiceRoute.

**Entities**
Product Family, Product Model, Purchase Date.

**Validation**
Valid purchase date, supported product, required responses.

**Conditions**
Coverage check, exclusions, DOA assessment, repeat repair, service route.

**Loop**
Update responses and recalculate assessment if needed.

**Redirects**
- Guided Product Troubleshooting
- Support Case Summary

**Knowledge Sources**
- HP printer manual PDF
- Lenovo laptop manual PDF
- Lenovo Support
- HP Support
- novacare-limited-warranty-policy
- product-safety-and-escalation-policy
- product-support-scope

**Outcome**
Potentially Covered, Potentially Excluded, Outside Coverage, DOA, Specialist Review.

**Escalation**
Safety issue, repeat repairs, disputed assessment.

**Cancellation**
User cancels or insufficient information.

**Limitations**
Preliminary assessment only; no warranty approval or live system access.

