# Dataset Notes — P2-006 Synthetic Operational Dataset

## Dataset Overview
The synthetic dataset supplied in `P2-006_Supply_Chain_Continuity_Lab_Data.xlsx` models the supply chain operations of NovaSphere Technologies Pvt. Ltd.

## Excel Named Tables Structure
1. `DisruptionRequestsTable`: Contains 6 seeded disruption requests (`DSP-001` through `DSP-006`) with disruption types (supplier delay, shipment delay, quality hold, supplier cancellation, partial shipment, material shortage).
2. `SuppliersTable`: Master list of 5 primary and alternate suppliers with quality scores, on-time delivery ratings, and risk levels.
3. `SKUMasterTable`: Master list of 8 SKUs with descriptions, primary supplier IDs, standard unit costs, criticality levels, and daily consumption rates.
4. `InventoryTable`: Stock balances across 8 inventory records, detailing On Hand, Reserved, Safety Stock, Quality Hold flags, and inbound quantities.
5. `PurchaseOrdersTable`: 10 purchase order records with status tracking (`Confirmed`, `Delayed`, `In Transit`, `Cancelled`).
6. `CustomerOrdersTable`: 10 customer orders with customer tiering (`Strategic`, `Priority`, `Standard`), SLA protected flags (`Yes`/`No`), order quantities, dollar values, required serial dates, and partial fulfillment permissions (`Yes`/`No`).
7. `AlternateSuppliersTable`: 8 alternate supplier mappings with approval flags (`Yes`/`No`), available capacities, standard/expedite lead times, and unit costs.
8. `RecoveryRulesTable`: Policy rules and decision threshold limits (`R-01` through `R-12`).
9. `StakeholdersTable`: Contact information for organizational roles (`Supply Chain Director`, `Finance Business Partner`, `Customer Operations Lead`, etc.).
