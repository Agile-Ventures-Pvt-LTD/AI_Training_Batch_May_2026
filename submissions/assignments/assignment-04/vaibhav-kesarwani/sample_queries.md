# Sample Queries

Below are are the sample queries in which the agent is tested.

---

### Q1. What is the total revenue from completed orders?

**Ans:** The total revenue generated from orders with a **completed** status is **$232,870.00**.

---

### Q2. Which customer has spent the most money?

**Ans:** The top‑spending customer is **Rahul Sharma** (customer ID 1). He has spent a total of **₹77,500.00** across all of his orders.

---

### Q3. Show the top 5 products by quantity sold.

**Ans:** **Top 5 best‑selling products (by total quantity sold)**  

| Rank | Product ID | Product Name | Quantity Sold |
|------|------------|--------------|---------------|
| 1 | 3 | Headphones | 6 |
| 2 | 8 | Water Bottle | 5 |
| 3 | 10 | Backpack | 4 |
| 4 | 13 | Notebook | 4 |
| 5 | 2 | Smartphone | 3 |

These figures represent the total number of units of each product that have been ordered across all completed (and pending) orders in the database. The headphones lead the list with six units sold, followed by the water bottle with five units.

---

### Q4. Which product category generated the highest revenue?

**Ans:** The **Electronics** category generated the highest revenue, totaling **$265,900.00**.

---

### Q5. How many orders are pending?

**Ans:** There are **5 pending orders** in the system.

---

### Q6. Show all cancelled orders with customer names.

**Ans:** Here are the cancelled orders along with the customers who placed them:

| Order ID | Customer Name | Order Date | Total Amount |
|----------|---------------|------------|--------------|
| 6 | Amit Kumar | 2024‑06‑11 | $1,500.00 |
| 15 | Sneha Joshi | 2024‑06‑08 | $3,000.00 |

These are the only orders in the database that have a status of **cancelled**.

---

### Q7. Which customers are from Delhi?

**Ans:** Here are the customers whose city is listed as **Delhi**:

| Customer ID | Name          | Email               | Signup Date |
|-------------|---------------|---------------------|-------------|
| 1           | Rahul Sharma  | rahul@gmail.com     | 2024‑01‑10  |

No other customers in the database are from Delhi.

---

### Q8. Which products have stock below 10?

**Ans:** Here are the products whose current inventory is **under 10 units**:

| Product ID | Name          | Category    | Price (₹) | Stock Quantity |
|------------|---------------|------------|----------|----------------|
| 2          | Smartphone    | Electronics| 25,000   | 5 |
| 4          | Keyboard      | Electronics| 1,500    | 4 |
| 5          | Mouse         | Electronics| 800      | 2 |
| 6          | Office Chair  | Furniture  | 7,000    | 8 |
| 7          | Desk          | Furniture  | 12,000   | 6 |
| 9          | Coffee Maker  | Home       | 3,500    | 7 |
| 15         | Monitor       | Electronics| 12,000   | 3 |

These items are low in stock and may need to be reordered soon to avoid stock‑outs.

---

### Q9. What is the average order value?

**Ans:** The average order value across all orders in the database is **$11,114.80**.

---

### Q10. Show total revenue by month.

**Ans:** **Total Revenue by Month (Completed Orders)**  

| Month (YYYY‑MM) | Total Revenue (USD) |
|-----------------|---------------------|
| 2024‑06 | $232,870.00 |

*Only completed orders are included in the calculation.*

---