# Tool Design

## 1. List rows present in a table

### Description
List rows present in a table.

### Used For
- Check duplicate leads.
- Read qualification rules.
- Read territory data.
- Read product data.
- Read sales owner data.
- Read action rules.

### Inputs
- Excel file
- Table name

### Outputs
- Matching rows from the selected table.

### Action Boundary
- Read data only.
- Do not add or update records.

---

## 2. Add a row into a table

### Description
Add a new row into the Excel table.

### Used For
- Create a new lead record when no duplicate is found.

### Inputs
- Lead details
- Classification
- Owner
- Confidence
- Processing status

### Outputs
- A new row is added to the Lead Register.

### Action Boundary
- Use only for new leads.
- Do not use for duplicate leads.

---

## 3. Update a row

### Description
Update a row using a key column. The input value will overwrite the specified cells and columns left blank will not be updated. In order to append (instead of overwrite) a value, use the "Get a row" action to retrieve the content first.

### Used For
- Update duplicate leads.
- Update classification.
- Update owner.
- Update latest action.
- Update processing status.

### Inputs
- Lead ID or Message ID
- Updated lead information

### Outputs
- Existing row is updated.

### Action Boundary
- Update existing records only.
- Do not create new records.

---

## 4. Create a Microsoft Word document

### Description
Creates a Microsoft Word file with the given content in the root directory (use only from Copilot Studio)

### Used For
- Generate reports for Hot and Qualified leads.

### Inputs
- Lead details
- Qualification score
- Classification
- Assigned owner
- Recommended action

### Outputs
- Microsoft Word report.

### Action Boundary
- Use only for Hot and Qualified leads.
- Do not create reports for Duplicate, Human Review Required, Additional Information Required, or Not a Sales Lead.

---

## 5. Reply to email (V3)

### Description
This operation replies to an email.

### Used For
- Send acknowledgement emails.
- Request missing information.
- Send the correct response based on lead classification.

### Inputs
- Recipient email
- Subject
- Email message

### Outputs
- Reply email sent.

### Action Boundary
- Do not reply for Duplicate leads.
- Do not send qualification results for Human Review Required cases.
- Do not send sales replies for Not a Sales Lead.