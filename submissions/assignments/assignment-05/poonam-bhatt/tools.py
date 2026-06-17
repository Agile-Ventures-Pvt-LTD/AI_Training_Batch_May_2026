from db_utils import execute_query

def inspect_database_schema():
    """
    Show available tables in the database.
    """
    print("TOOL CALLED: inspect_database_schema")

    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """

    return execute_query(query)


def get_customer_profile(customer_id: int):
    """
    Retrieve customer profile information
    including name, email, phone and address.
    Use ONLY when user asks for customer profile.
    """

    query = """
    SELECT *
    FROM customer
    WHERE cust_id = ?
    """

    return str(
        execute_query(
            query,
            (customer_id,)
        )
    )
    
        



def find_customer_by_name(name: str):
    """
    Find customer by first or last name.
    """

    query = """
    SELECT *
    FROM customer
    WHERE first_name LIKE ?
       OR last_name LIKE ?
    """

    return str(
        execute_query(
            query,
            (f"%{name}%", f"%{name}%")
        )
    )
    
from db_utils import mask_card

def get_card_details(customer_id: int):
    """
    Use this tool when the user asks:
    - card details
    - card information
    - cards owned by a customer
    - customer cards
    - credit card details

    Input:
    customer_id

    Returns:
    card number (masked), expiry date, valid from date,
    card type information.
    
    Retrieve card details for a customer.
    Use ONLY when user asks about cards.
    
    """

    query = """
    SELECT *
    FROM card
    WHERE cust_id = ?
    """

    print("TOOL CALLED: get card details")

    rows = execute_query(query, (customer_id,))

    result = []

    for row in rows:
        result.append({
                "card_number": mask_card(row["card_number"]),
                "valid_from": row["valid_from"],
                "expiry": row["expiry"],
                "card_type_id": row["card_type_id"]
            })

    return str(result)
def find_customer_by_card(card_number: int):
    """
    Find customer using card number.
    """

    query = """
    SELECT
        c.*
    FROM customer c
    JOIN card cd
    ON c.cust_id = cd.cust_id
    WHERE cd.card_number = ?
    """

    return str(
        execute_query(
            query,
            (card_number,)
        )
    )

def get_customer_transactions(
    customer_id: int,
    limit: int = 5
):
    """
    Get transactions for a customer.
    """

    query = """
    SELECT
        t.*
    FROM "transaction" t
    JOIN card c
        ON t.CARD_ID = c.card_number
    WHERE c.cust_id = ?
    ORDER BY t.TX_DATETIME DESC
    LIMIT ?
    """

    return str(
        execute_query(
            query,
            (customer_id, limit)
        )
    )


def search_transactions(
    min_amount: float = 0,
    limit: int = 5
):
    """
    Search transactions above an amount.
    """

    query = """
    SELECT TX_DATETIME,TX_AMOUNT,TX_TYPE
    FROM transaction
    WHERE TX_AMOUNT >= ?
    LIMIT : int = 5
    """

    return str(
        execute_query(
            query,
            (min_amount, limit)
        )
    )


def get_merchant_spend_summary():
    """
    Aggregate spend by merchant.
    """

    query = """
    SELECT
    m.merchant,
    SUM(t.TX_AMOUNT) AS total_spend
    FROM "transaction" t
    JOIN merchant m
    ON t.M_ID = m.id
    GROUP BY m.merchant
    ORDER BY total_spend DESC
    LIMIT 10
    """

    return str(
        execute_query(query)
    )
    

def detect_suspicious_transactions():
    """
    Detect suspicious transactions above 50000 dollars.
    Use this tool whenever the user asks:
    - suspicious transactions
    - fraud detection
    - unusual activity
    """

    print("TOOL CALLED: detect_suspicious_transactions")


    query = """
    SELECT *
    FROM "transaction"
    WHERE TX_AMOUNT > 50000
    LIMIT 10
    """

    results = str(
        execute_query(query)
    )
    return results[:10]


def get_expiring_cards():
    """
    Find cards expiring in the next 90 days.
    """

    query = """
    SELECT
        card_number,
        expiry,
        cust_id
    FROM card
    WHERE date(expiry) <= date('now', '+90 day')
    ORDER BY expiry ASC
    LIMIT 20
    """

    results= str(execute_query(query))
    return results[:10]


def get_customer_activity_summary(customer_id: int):
    """
    Customer transaction summary.
    """

    query = """
    SELECT
        COUNT(*) as total_transactions,
        SUM(t.TX_AMOUNT) as total_spend,
        AVG(t.TX_AMOUNT) as avg_spend,
        MAX(t.TX_AMOUNT) as highest_transaction
    FROM "transaction" t
    JOIN card c
        ON t.CARD_ID = c.card_number
    WHERE c.cust_id = ?
    """

    return str(
        execute_query(
            query,
            (customer_id,)
        )
    )


def get_high_value_transactions(
    amount: float = 50000
):
    """
    Transactions above threshold.
    """

    query = """
    SELECT
        TXN_ID,
        CARD_ID,
        TX_AMOUNT,
        TX_DATETIME
    FROM "transaction"
    WHERE TX_AMOUNT >= ?
    LIMIT 20
    """

    return str(
        execute_query(
            query,
            (amount,)
        )
    )


def get_customer_spend_summary(
    customer_id: int
):
    """
    Spending summary by customer.
    """

    query = """
    SELECT
        SUM(t.TX_AMOUNT),
        AVG(t.TX_AMOUNT),
        COUNT(*)
    FROM "transaction" t
    JOIN card c
        ON t.CARD_ID = c.card_number
    WHERE c.cust_id = ?
    """

    return str(
        execute_query(
            query,
            (customer_id,)
        )
    )


from langchain_core.tools import StructuredTool

tools = [
    StructuredTool.from_function(inspect_database_schema),
    StructuredTool.from_function(get_customer_profile),

    StructuredTool.from_function(
        func=find_customer_by_name,
        name="find_customer",
        description="Find customer by first or last name"
    ),

    StructuredTool.from_function(get_card_details),
    StructuredTool.from_function(find_customer_by_card),
    StructuredTool.from_function(get_customer_transactions),
    StructuredTool.from_function(search_transactions),
    StructuredTool.from_function(get_merchant_spend_summary),
    StructuredTool.from_function(detect_suspicious_transactions),
    StructuredTool.from_function(get_expiring_cards),
    StructuredTool.from_function(get_customer_activity_summary),
    StructuredTool.from_function(get_high_value_transactions),
    StructuredTool.from_function(get_customer_spend_summary),
]

