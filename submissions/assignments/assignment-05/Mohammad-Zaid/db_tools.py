# db_tools.py

from db_utils import run_query

def inspect_database_schema():
    """
    Returns available database tables and their columns.
    Use when the user asks about schema, tables, or database structure.
    """
    # to get tables
    tables_query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """
    tables = run_query(tables_query)
    print("---calling inspect_database_schema tool---")
        
    return tables
        

def get_customer_profile(cust_id):
    """
    Returns customer profile information for a given customer ID.
    Use when the user asks about customer details or profile.
    """

    query = """
    SELECT cust_id, first_name, last_name, email, phone, city, state
    FROM customer
    WHERE cust_id = ?
    LIMIT 1
    """
    print("---calling get_customer_profile tool---")
    
    return run_query(query, (cust_id,))

def get_card_details(cust_id=None):
    """
    Returns card information linked to a customer.
    Use when the user asks about card details or card status.
    """

    query = """
    SELECT c.card_number, c.valid_from, c.expiry,
           ct.card_type, ct.card_network
    FROM card c
    LEFT JOIN card_type ct
    ON c.card_type_id = ct.card_type_id
    WHERE c.cust_id = ?
    """
    print("----calling get_card_details tool---")
    
    return run_query(query, (cust_id,))

def search_transactions(limit=5):
    """
    Returns recent transaction records from the database.
    Use when the user asks about transactions or spending activity.
    """

    query = """
    SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT,
           m.merchant, tt.debit_credit
    FROM "transaction" t
    JOIN merchant m
    ON t.M_ID = m.id
    JOIN transaction_type tt
    ON t.TXN_TYPE_ID = tt.txn_type_id
    ORDER BY t.TX_DATETIME DESC
    LIMIT ?
    """
    print("---calling search_transactions tool---")

    return run_query(query, (limit,))

def get_customer_transactions(cust_id):
    """
    Returns transactions associated with a customer.
    Use when the user asks for a customer's transaction history.
    """

    query = """
    SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant
    FROM "transaction" t
    JOIN card c
    ON t.CARD_ID = c.card_number
    JOIN merchant m
    ON t.M_ID = m.id
    WHERE c.cust_id = ?
    ORDER BY t.TX_DATETIME DESC
    LIMIT 10
    """
    print("---calling get_customer_transactions tool---")
    return run_query(query, (cust_id,))

def get_statement_summary(cust_id):
    """
    Returns statement and payment summary for a customer.
    Use when the user asks about dues, statements, or payment information.
    """

    query = """
    SELECT COUNT(*), SUM(t.TX_AMOUNT)
    FROM "transaction" t
    JOIN card c
    ON t.CARD_ID = c.card_number
    WHERE c.cust_id = ?
    """
    print("---calling get_statement_summary tool---")
    
    return run_query(query, (cust_id,))

def get_rewards_summary(cust_id):
    """
    Returns reward points information for a customer.
    Use when the user asks about rewards or loyalty points.
    """

    query = """
    SELECT t.TXN_ID, t.TX_AMOUNT
    FROM "transaction" t
    JOIN card c
    ON t.CARD_ID = c.card_number
    WHERE c.cust_id = ?
    AND TX_AMOUNT > 50
    """
    print("---calling get_rewrds_summary tool---")

    return run_query(query, (cust_id,))

def get_merchant_spend_summary():
    """
    Returns spending aggregated by merchant or merchant category.
    Use when the user asks for spending analysis or merchant summaries.
    """

    query = """
    SELECT mt.merchant_type,
           SUM(t.TX_AMOUNT),
           COUNT(*)
    FROM "transaction" t
    JOIN merchant m
    ON t.M_ID = m.id
    JOIN merchant_type mt
    ON m.merchant_type = mt.id
    GROUP BY mt.merchant_type
    ORDER BY SUM(t.TX_AMOUNT) DESC
    LIMIT 5
    """
    print("---calling get_merchant_spend_summary tool---")

    return run_query(query)

# Your masking function
def mask_email(email: str):
    username, domain = email.split("@")
    masked_uname = username[0] + "*" * (len(username)-2) + username[len(username)-1]
    masked_email = masked_uname + '@' + domain
    return masked_email

