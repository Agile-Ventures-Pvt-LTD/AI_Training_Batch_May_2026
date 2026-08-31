from langchain.tools import tool
from db_utils import execute_query
from langchain.tools import StructuredTool
from langchain_community.utilities.sql_database import SQLDatabase

@tool
def inspect_database_schema():
    """
    Return database schema.
    """

    db = SQLDatabase.from_uri("sqlite:///data/ccms.db")
    schema = db.get_context()["table_info"]

    return f"{schema}"


@tool
def get_customer_profile(cust_id: str):
    """
    Give the Customer profile using the cust_id
    """

    query = """
    SELECT cust_id, first_name || " " || last_name as name, email, city, state
    FROM customer
    WHERE cust_id = ? 
    """

    result = execute_query(query, (cust_id,))
    
    return f"{result}"


def get_card_details(cust_id: str):
    """
    Give the card deatils using the cust_id
    """

    query = """
    SELECT * from card WHERE cust_id = ?
    """

    result = execute_query(query, (cust_id,))

    if not result:
        return f"No Cards Found for the customer {cust_id}"
    
    cards = []
    for card in result:
        mask = ("**** **** ****" + str(card["card_number"])[-4:])
        cards.append({
            "card_mask": mask
        })

    return f"{cards}"


def search_transactions(
    cust_id: str | None = None,
    merchant: str | None = None,
    min_amount: str | None = None,
):
    """
    Search transactions whcih are having the filters:
    
    - customer_id
    - card_last4
    - merchant_name
    - merchant_type
    - min_amount
    - max_amount
    - from_date
    - to_date
    - transaction_type
    - limit
    """

    query = """
    SELECT t.TX_DATETIME, t.TX_AMOUNT, m.merchant, t.TXN_ID FROM "transaction" t
    LEFT JOIN merchant m ON t.M_ID = m.id
    WHERE 1 = 1
    """

    params = []

    if cust_id:
        query += """
         AND t.CARD_ID IN (
            SELECT card_number FROM card WHERE cust_id = ?
        )
        """
        params.append(cust_id)

    if min_amount:
        query += " AND t.TX_AMOUNT >= ?"
        params.append(min_amount)

    if merchant:
        query += " AND m.merchant LIKE ?"
        params.append(merchant)

    query += " ORDER BY t.TX_DATETIME DESC"
    result = execute_query(query, tuple(params))

    return f"{result}"


def get_customer_transactions(cust_id : str):
    """
    Return the Customer Transaction on basic of only customer id which cust_id
    """

    query = """
    SELECT  t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant AS merchant_name, tt.debit_credit AS transaction_type from "transaction" t
    
    JOIN card c ON t.CARD_ID = c.card_number

    LEFT JOIN merchant m ON t.M_ID = m.id

    LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id

    WHERE cust_id = ?
    ORDER BY t.TX_DATETIME DESC
    """

    result = execute_query(query, (cust_id,))

    return f"{result}"


def get_statement_summary(cust_id : str):
    """Return statement and also due information with the help of cust_id"""

    query = """
    SELECT c.cust_id 
    SUM(
        CASE
            WHEN tt.debit_credit = 'Debit'
                THEN t.TX_AMOUNT
            
            WHEN tt.debit_credit = 'Credit'
                THEN -t.TX_AMOUNT
            
            ELSE 0
        END
    ) AS total_due
    FROM customer c

    JOIN card cd ON c.cust_id = cd.cust_id
    
    JOIN "transaction" t ON cd.card_number = t.CARD_ID
    
    JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id

    WHERE c.cust_id = ?
    GROUP BY c.cust_id
    """

    result = execute_query(query, (cust_id,))

    return f"{result}"


def get_reward_summary(cust_id: str):
    """Return reward points by customer"""

    query = """
    SELECT c.cust_id, COUNT(t.TXN_ID) AS total_points FROM "transaction" t
    JOIN card c ON t.CARD_ID = c.card_number
    WHERE t.TX_AMOUNT >= 50
    """

    params = []

    if (cust_id):
        query += " AND c.cust_id = ?"
        params.append(cust_id)
    
    query += " GROUP BY c.cust_id"
    if not cust_id:
        query += " ORDER BY total_points DESC"

    result = execute_query(query, tuple(params,))

    return f"{result}"


def get_merchant_spend_summary():
    """
    Aggregate transaction amount by merchant or merchant type.
    """

    query = """
    SELECT m.merchant, COUNT(t.TXN_ID) AS total_transactions, SUM(t.TX_AMOUNT) AS total_amount, AVG(t.TX_AMOUNT) AS avg_amount
    FROM "transaction" t

    JOIN merchant m ON t.M_ID = m.id

    GROUP BY m.merchant
    ORDER BY total_amount DESC;
    """

    result = execute_query(query)

    return f"{result}"


prebuilt_tools = [
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_reward_summary,
    get_merchant_spend_summary,
]

inspect_tool = StructuredTool.from_function(inspect_database_schema)
customer_profile = StructuredTool.from_function(get_customer_profile)
card_details = StructuredTool.from_function(get_card_details)
search_transaction_tool = StructuredTool.from_function(search_transactions)
customer_transactions_tool = StructuredTool.from_function(get_customer_transactions)
statment_tool = StructuredTool.from_function(get_statement_summary)
reward_tool = StructuredTool.from_function(get_reward_summary)
merchant_spend_tool = StructuredTool.from_function(get_merchant_spend_summary)

custom_tools = [
    inspect_tool,
    customer_profile,
    card_details,
    search_transaction_tool,
    customer_transactions_tool,
    statment_tool,
    reward_tool,
    merchant_spend_tool
]