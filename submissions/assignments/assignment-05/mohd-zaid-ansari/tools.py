from langchain.tools import StructuredTool
from db_utils import execute_query, get_connection

def inspect_database_schema():
    """Help the participant and agent understand table names and available columns."""

    table_results=execute_query("select name from sqlite_master where type='table';")
    tables = [row["name"] for row in table_results]

    schema={}

    for table in tables:
        column_result=execute_query(f"PRAGMA table_info('{table}')")
        column=[row["name"] for row in column_result]
        schema[table]=column

    return{"tables":tables,
                "schema":schema}

inspect_schema = StructuredTool.from_function(inspect_database_schema)


def get_customer_profile(cust_id:str):
    """Find customer information by customer ID, email, phone, name or by card number"""
    
    query="""Select c.cust_id, c.first_name,c.last_name, c.email,ca.card_number from customer c
    join card ca on c.cust_id = ca.cust_id where c.cust_id = ? OR (c.first_name || ' ' || c.last_name) LIKE ?
    OR ca.card_number = ?"""

    params = (cust_id,f"%{cust_id}%",cust_id)

    return execute_query(query,params)

customer_profile = StructuredTool.from_function(get_customer_profile)


def get_card_details(cust_id):
    """Get card details linked with a customer and ensure card number masked with * and only last 4 digits are visible."""
    
    query="""SELECT c.card_number,c.expiry,ct.card_type, ct.card_network,
        ct.privilege FROM card c JOIN card_type ct ON c.card_type_id = ct.card_type_id
        WHERE c.cust_id=?"""

    return execute_query(query, (cust_id,))
    
card_details = StructuredTool.from_function(get_card_details)


def search_transactions(cust_id):
    """
    Search transaction using customer id and get its transaction id, transaction date, amount, merchant and transaction type.
    """

    query=""" SELECT t.TXN_ID,t.TX_DATETIME, t.TX_AMOUNT, m.merchant, tt.debit_credit
    from "transaction" t JOIN merchant m ON t.M_ID = m.id JOIN transaction_type tt
    ON t.TXN_TYPE_ID = tt.txn_type_id WHERE(? IS NULL OR t.TX_AMOUNT >= ?) ORDER BY t.TX_DATETIME DESC"""

  

    return execute_query(query, (cust_id,))

transactions_search = StructuredTool.from_function(search_transactions)


def get_customer_transactions(cust_id):
    """
     You are required to return the recent transaction of any customer.
    """
    query=""" SELECT t.TXN_ID,t.TX_DATETIME,t.TX_AMOUNT,m.merchant,tt.debit_credit
    from card c JOIN "transaction" t ON c.card_number=t.CARD_ID JOIN merchant m
    ON t.M_ID = m.id JOIN transaction_type tt ON t.TXN_TYPE_ID=tt.txn_type_id
    WHERE c.cust_id=? order by t.TX_DATETIME DESC"""

    return execute_query(query,(cust_id,))

customer_transactions = StructuredTool.from_function(get_customer_transactions)


def detect_suspicious_transactions():
    """
    Find the suspicious transaction that are above certain amount.
    """

    query = """SELECT t.TXN_ID,t.TX_DATETIME, t.TX_AMOUNT,m.merchant from "transaction" t
    JOIN merchant m ON t.M_ID = m.id where t.TX_AMOUNT > 250 order by t.TX_AMOUNT DESC"""
    return execute_query(query)

suspicious_transactions= StructuredTool.from_function(detect_suspicious_transactions)


def get_rewards_summary(cust_id):
    """
    Get reward points for a customer.
    Reward points = Total Spend / 100
    """

    query = """SELECT c.cust_id, CAST(SUM(t.TX_AMOUNT) / 100 AS INTEGER) AS reward_points
    FROM customer c JOIN card ca ON c.cust_id = ca.cust_id JOIN "transaction" t ON ca.card_number = t.CARD_ID
    WHERE c.cust_id = ? GROUP BY c.cust_id
    """
    return execute_query(query,(cust_id,))

rewards_summary = StructuredTool.from_function(get_rewards_summary)


def get_merchant_spend_summary():
     """
    Get the summary of total amount spend by merchant
    """
     query= """SELECT m.merchant,count (*) as transaction_count, ROUND(SUM(t.TX_AMOUNT),2) as total_spend
    from "transaction" t JOIN merchant m ON t.M_ID = m.id group by m.merchant order by total_spend DESC"""
     
     return execute_query(query)

merchant_spend_summary = StructuredTool.from_function(get_merchant_spend_summary)
