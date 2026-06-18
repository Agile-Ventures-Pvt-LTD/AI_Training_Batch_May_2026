from db_utils import execute_select_query
from langchain.tools import StructuredTool

def inspect_database_schema():
    """
    Get the complete database schema one time.

    Use this tool only when the user asks about tables or columns.
    After receiving the schema, explain it to the user and do not call this tool again.
    """
    query = """
            select name from sqlite_master where type='table' order by name
            """

    tables = execute_select_query(query)
    return f"Database schema:\n{tables}"


schema_tool = StructuredTool.from_function(inspect_database_schema)

def get_customer_profile(cust_id):
    """
    Get basic customer details using customer ID.
    """
    query = """ 
            SELECT cust_id, first_name,last_name, email,phone, city, state
            FROM customer WHERE cust_id = ?
            """

    return execute_select_query(query,(cust_id,))

customer_tool = StructuredTool.from_function(get_customer_profile)

def get_card_details(cust_id):
    """
    Get card details linked with a customer and ensure card number should be masked with '*' and only last 4 digit visible.
    """
    query = """
            SELECT c.card_number, c.expiry,ct.card_type, ct.card_network,ct.privilege
            FROM card c JOIN card_type ct ON c.card_type_id = ct.card_type_id 
            WHERE c.cust_id = ?
            """

    return execute_select_query(query,(cust_id,))

card_tool = StructuredTool.from_function(get_card_details)

def search_transactions(min_amount):
    """
    Find transactions based on amount filter.
    """
    query = """
            SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant, tt.debit_credit
            FROM "transaction" t JOIN merchant m ON t.M_ID = m.id JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
            WHERE t.TX_AMOUNT >= ?
            ORDER BY t.TX_AMOUNT DESC
            LIMIT 10
            """
    
    return execute_select_query(query,(min_amount,))

search_tool = StructuredTool.from_function(search_transactions)

def get_customer_transactions(cust_id, limit=5):
    """
    Show recent transactions for a customer.
    """
    query = """
            SELECT t.TXN_ID, t.TX_DATETIME,t.TX_AMOUNT, m.merchant,tt.debit_credit
            FROM "transaction" t JOIN card c ON t.CARD_ID = c.card_number
            JOIN merchant m ON t.M_ID = m.id
            JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
            WHERE c.cust_id = ?
            ORDER BY t.TX_DATETIME DESC
            LIMIT ?
            """
    
    return execute_select_query(query, (cust_id, limit))

customer_trans_tool = StructuredTool.from_function(get_customer_transactions)

def get_statement_summary(cust_id):
    """
    Get statement summary.
    """
    query = """
            SELECT COUNT(t.TXN_ID) AS total_transactions, SUM(t.TX_AMOUNT) AS total_spend, AVG(t.TX_AMOUNT) AS average_spend
            FROM card c JOIN "transaction" t ON c.card_number = t.CARD_ID
            WHERE c.cust_id = ?
            """
    
    return execute_select_query(query,(cust_id,))

statement_tool = StructuredTool.from_function(get_statement_summary)

def get_reward_summary(cust_id):
    """
    Calculate reward points from customer spending.
    """
    query = """
            SELECT SUM(t.TX_AMOUNT) AS total_spend
            FROM "transaction" t JOIN card c ON c.card_number = t.CARD_ID
            WHERE c.cust_id = ?
            """
    
    return execute_select_query(query,(cust_id,))

reward_tool = StructuredTool.from_function(get_reward_summary)

def get_merchant_spend_summary():
    """
    Show top merchants based on total spending.
    """
    query = """ 
            SELECT m.merchant,COUNT(t.TXN_ID) AS transactions,SUM(t.TX_AMOUNT) AS total_spend
            FROM "transaction" t JOIN merchant m ON t.M_ID = m.id 
            GROUP BY m.merchant
            ORDER BY total_spend DESC
            LIMIT 10
            """
    
    return execute_select_query(query)

merchant_tool = StructuredTool.from_function(get_merchant_spend_summary)