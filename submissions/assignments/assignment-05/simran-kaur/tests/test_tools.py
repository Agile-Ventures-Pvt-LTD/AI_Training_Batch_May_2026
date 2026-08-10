from db_utils import get_connection
from tools import get_customer_profile,search_transactions

def test_database_connection():

    conn = get_connection()

    assert conn is not None

    conn.close()


def test_get_customer_profile():

    result = get_customer_profile(

            {"cust_id": 91}
    )
    assert result is not None



    #run using `python -m pytest tests/test_tools.py`