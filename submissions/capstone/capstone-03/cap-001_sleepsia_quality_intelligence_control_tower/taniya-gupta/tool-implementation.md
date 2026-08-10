# Tool Implementation Details & Configuration Matrix

## 1. Complete Tool Inventory (14 Tools)

| Connector | Tool Name | Operation Type | Target Table / Purpose |
|---|---|---|---|
| **Excel Online** | `Get Unprocessed Complaints` | List rows present in a table | `Customer_Complaints` |
| **Excel Online** | `Get Product Master Data` | List rows present in a table | `Product_Master` |
| **Excel Online** | `Get Batch Register Data` | List rows present in a table | `Batch_Register` |
| **Excel Online** | `Get CAPA Register Data` | List rows present in a table | `CAPA_Register` |
| **Excel Online** | `Get Returns` | List rows present in a table | `Returns` |
| **Excel Online** | `Get Sales Summary` | List rows present in a table | `Sales_Summary` |
| **Excel Online** | `Get Owners Data` | List rows present in a table | `Owners` |
| **Excel Online** | `Get Quality Incidents Data` | List rows present in a table | `Quality_Incidents` |
| **Excel Online** | `Create Quality Incident Record` | Add a row into a table | `Quality_Incidents` |
| **Excel Online** | `Create CAPA Entry` | Add a row into a table | `CAPA_Register` |
| **Excel Online** | `Mark Complaint Processed` | Update a row | `Customer_Complaints` |
| **Word Online** | `Quality Report Generator` | Create a word document | Generates Word Investigation Report |
| **Office 365 Outlook** | `Quality Notification Sender` | Send an email (V2) | Sends HTML internal alert notifications |
| **MCP** | `Microsoft Learn MCP Server` | Model Context Protocol | Attached to `M365 Guidance Specialist` |