import unittest
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ecommerce.db")

class TestDatabase(unittest.TestCase):
    
    def test_db_file_exists(self):
        """Check if the ecommerce.db file is actually created in the data folder."""
        self.assertTrue(os.path.exists(DB_PATH), "Database file is missing! Did you run create_database.py?")

    def test_tables_exist(self):
        """Check if all 4 required tables are present."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.assertIn('customers', tables)
        self.assertIn('products', tables)
        self.assertIn('orders', tables)
        self.assertIn('order_items', tables)

    def test_data_is_seeded(self):
        """Check if minimum required records are inserted (e.g., at least 10 customers)."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertGreaterEqual(count, 10, "Customers table should have at least 10 records.")

if __name__ == '__main__':
    unittest.main()