# Sample Queries — Tested Against ecommerce.db

---

### 1. What is the total revenue from completed orders?

**SQL used:**
```sql
SELECT SUM(total_amount) AS total_revenue FROM orders WHERE status = 'completed';
```

**Agent Response:**
The total revenue from completed orders is Rs. 68,800.

---

### 2. Which customer has spent the most money?

**SQL used:**
```sql
SELECT c.name, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 1;
```

**Agent Response:**
The highest spending customer is Priya Sharma with a total completed purchase value of Rs. 11,500.

---

### 3. Show the top 5 products by quantity sold.

**SQL used:**
```sql
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name
ORDER BY total_sold DESC
LIMIT 5;
```

**Agent Response:**
The top 5 products by quantity sold are:
1. Desk Lamp — 18 units
2. Keyboard — 12 units
3. AI Handbook — 12 units
4. Protein Shaker — 11 units
5. Coffee Mug — 11 units

---

### 4. Which product category generated the highest revenue?

**SQL used:**
```sql
SELECT p.category, SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC
LIMIT 1;
```

**Agent Response:**
Electronics is the highest revenue-generating category with total sales of Rs. 37,878.

---

### 5. How many orders are pending?

**SQL used:**
```sql
SELECT COUNT(*) AS pending_orders FROM orders WHERE status = 'pending';
```

**Agent Response:**
There are currently 4 pending orders.

---

### 6. Show all cancelled orders with customer names.

**SQL used:**
```sql
SELECT c.name, o.order_id, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'cancelled';
```

**Agent Response:**
There are 3 cancelled orders:
1. Ananya Verma — Order #5 on 2025-01-15 — Rs. 1,800
2. Vikram Malhotra — Order #12 on 2025-01-30 — Rs. 1,900
3. Arjun Singh — Order #24 on 2025-02-25 — Rs. 2,100

---

### 7. Which customers are from Delhi?

**SQL used:**
```sql
SELECT name, email FROM customers WHERE city = 'Delhi';
```

**Agent Response:**
There are 3 customers from Delhi:
1. Rohan Mehta — rohan@gmail.com
2. Neha Gupta — neha@gmail.com
3. Karan Kapoor — karan@gmail.com

---

### 8. Which products have stock below 10?

**SQL used:**
```sql
SELECT name, category, stock_quantity
FROM products
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;
```

**Agent Response:**
The following products are running low on stock (below 10 units):
1. Wireless Mouse — Electronics — 5 units
2. Yoga Mat — Fitness — 6 units
3. Mixer Grinder — Kitchen — 7 units
4. Laptop Stand — Electronics — 8 units
5. Coffee Mug — Kitchen — 8 units
6. Data Science Guide — Books — 9 units

---

### 9. What is the average order value?

**SQL used:**
```sql
SELECT ROUND(AVG(total_amount), 2) AS avg_order_value FROM orders;
```

**Agent Response:**
The average order value across all orders is Rs. 3,300.

---

### 10. Show total revenue by month.

**SQL used:**
```sql
SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
FROM orders
GROUP BY month
ORDER BY month;
```

**Agent Response:**
Monthly revenue breakdown:
- January 2025 — Rs. 36,200
- February 2025 — Rs. 46,300

---

### 11. Which city has the highest number of customers?

**SQL used:**
```sql
SELECT city, COUNT(*) AS customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC
LIMIT 1;
```

**Agent Response:**
Delhi has the highest number of customers with 3 registered customers.

---

### 12. Which customers have placed more than 2 orders?

**SQL used:**
```sql
SELECT c.name, COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING order_count > 2;
```

**Agent Response:**
The following customers have placed more than 2 orders:
1. Rohan Mehta — 3 orders
2. Priya Sharma — 3 orders
3. Neha Gupta — 3 orders
4. Arjun Singh — 3 orders
5. Ananya Verma — 3 orders

---

### 13. What are the top 3 most expensive products?

**SQL used:**
```sql
SELECT name, category, price
FROM products
ORDER BY price DESC
LIMIT 3;
```

**Agent Response:**
The top 3 most expensive products are:
1. Smart Watch — Electronics — Rs. 5,999
2. Mixer Grinder — Kitchen — Rs. 3,499
3. Dumbbells — Fitness — Rs. 2,499

---

### 14. Which product has never been ordered?

**SQL used:**
```sql
SELECT p.name, p.category
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;
```

**Agent Response:**
The following product has never been ordered:
- Smart Watch — Electronics

---

### 15. Show total sales by product category.

**SQL used:**
```sql
SELECT p.category, SUM(oi.quantity * oi.unit_price) AS total_sales
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY total_sales DESC;
```

**Agent Response:**
Total sales by product category:
1. Electronics — Rs. 37,878
2. Kitchen — Rs. 32,279
3. Books — Rs. 17,881
4. Fitness — Rs. 16,782
5. Home — Rs. 14,382
