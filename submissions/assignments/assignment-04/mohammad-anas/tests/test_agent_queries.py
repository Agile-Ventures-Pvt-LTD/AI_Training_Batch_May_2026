import unittest
from src.tools.ecommerce_sql_tool import query_ecommerce_database

class TestAgentQueries(unittest.TestCase):
    """
    Testing 5 specific business questions to ensure our tool returns the correct data formats 
    for the agent to read.
    """

    def test_query_1_total_revenue(self):
        sql = "SELECT SUM(total_amount) FROM orders WHERE status = 'completed';"
        result = query_ecommerce_database.invoke({"query": sql})
        self.assertNotIn("Error", result)
        self.assertNotEqual(result, "No matching data was found.")

    def test_query_2_low_stock(self):
        sql = "SELECT name FROM products WHERE stock_quantity < 10;"
        result = query_ecommerce_database.invoke({"query": sql})
        self.assertNotIn("Error", result)
        # We seeded Wireless Mouse with low stock, so it should be in the result
        self.assertIn("Wireless Mouse", result)

    def test_query_3_delhi_customers(self):
        sql = "SELECT name FROM customers WHERE city = 'Delhi';"
        result = query_ecommerce_database.invoke({"query": sql})
        self.assertNotIn("Error", result)
        self.assertIn("Priya Sharma", result)
        
if __name__ == '__main__':
    unittest.main()