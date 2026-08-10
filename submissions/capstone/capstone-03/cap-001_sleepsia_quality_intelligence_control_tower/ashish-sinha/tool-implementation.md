# Tool Implementation

## Excel Online (Business)
### Read
Product_Master, Batch_Register, Customer_Complaints, Sales_Summary, Returns, Quality_Incidents, Quality_Rules, Owners and Test_Scenarios.

### Write
Quality_Incidents and CAPA_Register where required.

### Rules
Do not silently overwrite source evidence. Record failures. Never claim a successful update unless the tool succeeds.

## Word Online (Business)
Generate the Product Quality Investigation Report after Supervisor validation. Never claim the report exists if generation failed.

## Outlook
Send internal notification only after Supervisor validation. If sending fails, preserve the decision and record notification failure.
