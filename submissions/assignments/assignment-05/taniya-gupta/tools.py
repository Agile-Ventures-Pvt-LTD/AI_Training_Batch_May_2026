import pandas as pd
from langchain_core.tools import tool
from db_utils import run
from output_formatter import format_as_table
from datetime import datetime, timedelta

def mask_card_number(card_number):
    """Masks card number showing only last 4 digits."""
    card_str = str(card_number)
    return "**** **** **** " + card_str[-4:]

def parse_id(value):
    """extract numeric ids"""
    text = str(value).strip().lower()
    if text in ("all", "none", ""):
        return None
    digits = "".join(c for c in text if c.isdigit())
    return int(digits) if digits else None

def parse_num(value):
    """extract numeric values from inputs."""
    text = str(value).strip().lower()
    if text in ("all", "none", ""):
        return None
    text = text.replace("$", "").replace(",", "")
    return float(text)

    
@tool
def get_database_schema():
    """return all tables and their columns."""
    tables = run("SELECT name FROM sqlite_master WHERE type='table';", ())
    schema = []
    for table in tables["name"]:
        columns = run(f'PRAGMA table_info("{table}");', ())
        schema.append(f"{table}: {', '.join(columns['name'])}")
    return "\n".join(schema)

@tool
def get_customer_profile(search_query):
    """find customer by ID, email, phone, name, or card number."""

    if isinstance(search_query, dict):
        search_query = next(iter(search_query.values()), "")
    
    search_query = str(search_query)
    
    # by card number
    if search_query.isdigit() and len(search_query) >= 12:
        query = """
        SELECT *
        FROM customer
        WHERE cust_id IN (
            SELECT cust_id
            FROM card
            WHERE card_number = ?
        )"""
        result = run(query, (search_query,))
    # Searching by customer details
    else:
        customer_id = parse_id(search_query)
        query = """
        SELECT *
        FROM customer
        WHERE cust_id = ?
           OR email = ?
           OR phone = ?
           OR first_name LIKE ?
           OR last_name LIKE ?
        """
        result = run(query,(customer_id,search_query,search_query,f"%{search_query}%",f"%{search_query}%"))
    return format_as_table(result)

@tool
def get_card_details(cust_id = None, last_4 = None, expiring_days = None):
    """show card details by customer ID, last 4 digits, or expiry date."""
    customer_id = parse_id(cust_id)
    days = parse_num(expiring_days)
    query = "SELECT * FROM card WHERE 1=1"
    params = []
    if customer_id:
        query += " AND cust_id=?"
        params.append(customer_id)
    if last_4:
        query += " AND CAST(card_number AS TEXT) LIKE ?"
        params.append(f"%{last_4}")

    df = run(query, tuple(params))
    if days and not df.empty:
            df["expiry"] = pd.to_datetime(df["expiry"])
            end_date = datetime.now() + timedelta(days=int(days))
            df = df[(df["expiry"] >= datetime.now()) &
                (df["expiry"] <= end_date) ]

    if "card_number" in df.columns:
        df["card_number"] = df["card_number"].apply(mask_card_number)

    sensitive_cols = ["pin", "security_code"]
    df = df.drop(columns=[col for col in sensitive_cols if col in df.columns])
    return format_as_table(df)

@tool
def search_transactions(cust_id = None, min_amt = None, merchant = None):
    """get transactions by ID, min amount, or merchant."""
    customer_id = parse_id(cust_id)
    amount = parse_num(min_amt)
    query = """
    SELECT
        t.TX_DATETIME,
        t.TX_AMOUNT,
        m.merchant,
        t.TXN_ID
    FROM "transaction" t
    LEFT JOIN merchant m ON t.M_ID = m.id
    WHERE 1=1
    """
    params = []
    if customer_id:
        query += """
        AND t.CARD_ID IN (
            SELECT card_number
            FROM card
            WHERE cust_id = ?
        )"""
        params.append(customer_id)

    if amount:
        query += " AND t.TX_AMOUNT >= ?"
        params.append(amount)
    if merchant:
        query += " AND m.merchant LIKE ?"
        params.append(f"%{merchant}%")
    query += " ORDER BY t.TX_DATETIME DESC"
    df = run(query, tuple(params))
    return format_as_table(df)

@tool
def get_merchant_spend_summary(cust_id = None, by_type = False):
    """total amount spent by merchant or merchant type."""
    customer_id = parse_id(cust_id)
    params = []
    if by_type:
        select_col = "mt.merchant_type"
        query = """
        SELECT mt.merchant_type, SUM(t.TX_AMOUNT) AS total
        FROM "transaction" t
        JOIN merchant m ON t.M_ID = m.id
        JOIN merchant_type mt ON m.merchant_type = mt.id
        """
    else:
        select_col = "m.merchant"
        query = """
        SELECT m.merchant, SUM(t.TX_AMOUNT) AS total
        FROM "transaction" t
        JOIN merchant m ON t.M_ID = m.id
        """
    if customer_id:
        query += """
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE c.cust_id = ?
        """
        params.append(customer_id)
    query += f"""
    GROUP BY {select_col}
    ORDER BY total DESC
    """
    df = run(query, tuple(params))
    return format_as_table(df)

@tool
def get_statement_summary(cust_id = None, min_due = None):
    """total due and minimum due (i.e 5% of total spending) including customer names."""
    customer_id = parse_id(cust_id)
    minimum_due = parse_num(min_due)
    query = """
    SELECT
        cu.first_name,
        cu.last_name,
        c.card_number,
        SUM(t.TX_AMOUNT) AS total_amount_due,
        SUM(t.TX_AMOUNT) * 0.05 AS minimum_amount_due
    FROM "transaction" t
    JOIN card c ON t.CARD_ID = c.card_number
    JOIN customer cu ON c.cust_id = cu.cust_id
    """
    params = []
    if customer_id:
        query += " WHERE c.cust_id = ?"
        params.append(customer_id)
    query += " GROUP BY c.card_number"
    if minimum_due:
        query += " HAVING minimum_amount_due >= ?"
        params.append(minimum_due)
    query += " ORDER BY total_amount_due DESC"
    df = run(query, tuple(params))
    if not df.empty and "card_number" in df.columns:
        df["card_number"] = df["card_number"].apply(mask_card_number)
    return format_as_table(df)

@tool
def get_rewards_summary(cust_id = None):
    """reward points ( where we get 1 point for every transaction of $50 or more)."""
    customer_id = parse_id(cust_id)
    query = """
    SELECT
        c.cust_id,
        COUNT(t.TXN_ID) AS total_points
    FROM "transaction" t
    JOIN card c ON t.CARD_ID = c.card_number
    WHERE t.TX_AMOUNT >= 50
    """
    params = []
    if customer_id:
        query += " AND c.cust_id = ?"
        params.append(customer_id)
    query += " GROUP BY c.cust_id"
    if not customer_id:
        query += " ORDER BY total_points DESC"
    df = run(query, tuple(params))
    return format_as_table(df)

@tool
def get_notifications(cust_id = None):
    """transaction alerts for high value transactions"""
    customer_id = parse_id(cust_id)
    query = """
    SELECT
        t.TX_DATETIME,
        t.TX_AMOUNT,
        m.merchant,
        'High Value Alert' AS alert_type
    FROM "transaction" t
    JOIN merchant m ON t.M_ID = m.id
    JOIN card c ON t.CARD_ID = c.card_number
    WHERE t.TX_AMOUNT > 50000
    """
    params = []
    if customer_id:
        query += " AND c.cust_id = ?"
        params.append(customer_id)
    query += " ORDER BY t.TX_DATETIME DESC"
    df = run(query, tuple(params))
    return format_as_table(df)

@tool
def detect_suspicious_transactions(cust_id = None):
    """transactions which are over $75,000."""
    customer_id = parse_id(cust_id)
    query = """
    SELECT *
    FROM "transaction"
    WHERE TX_AMOUNT > 75000
    """
    params = []
    if customer_id:
        query += """
        AND CARD_ID IN (
            SELECT card_number
            FROM card
            WHERE cust_id = ?
        )
        """
        params.append(customer_id)
    query += " ORDER BY TX_DATETIME DESC"
    df = run(query, tuple(params))
    return format_as_table(df)

TOOLS = [get_database_schema, get_customer_profile, get_card_details, search_transactions, get_merchant_spend_summary, get_statement_summary, get_rewards_summary, get_notifications, detect_suspicious_transactions]
