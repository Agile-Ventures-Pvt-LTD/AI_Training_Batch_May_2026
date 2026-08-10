from db.connection import get_database
def test_database_connection():
    db = get_database()
    tables = db.get_usable_table_names()
    assert len(tables) > 0

def test_orders_table_exists():
    db = get_database()
    tables = db.get_usable_table_names()
    assert "orders" in tables