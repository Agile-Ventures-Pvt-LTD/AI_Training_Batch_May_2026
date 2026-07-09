import sqlite3
from typing import Optional
from langchain_core.tools import tool
from db_utils import execute_query, execute_fetchone

_MASKING_CHAR = '*'

def _mask_email(email: str) -> str:
    """mask email addresses for privacy"""
    if not email or '@' not in email:
        return email
    name, domain = email.split('@', 1)
    return f"{name[:2]}{_MASKING_CHAR * 3}@{domain}"

def _mask_phone(phone: str) -> str:
    """mask all but the last 4 digits of a phone number."""
    if not phone or len(phone) < 4:
        return phone
    return f"{_MASKING_CHAR * 6}{phone[-4:]}"

def _mask_card_number(card_number: str) -> str:
    """mask all but the last 4 digits of a credit card number."""
    if not card_number or len(card_number) < 4:
        return card_number
    return f"{_MASKING_CHAR * 4} {_MASKING_CHAR * 4} {_MASKING_CHAR * 4} {card_number[-4:]}"

@tool
def inspect_database_schema(dummy: str = "") -> dict:
    """retrieve the database schema, including tables and columns."""
    try:
        tables_data = execute_query("select name from sqlite_master where type='table' and name not like 'sqlite_%';")
        tables = [row['name'] for row in tables_data]
        
        schema = {}
        for table in tables:
            columns_data = execute_query(f"PRAGMA table_info('{table}');")
            schema[table] = [row['name'] for row in columns_data]
            
        return {"tables": tables, "schema": schema}
    except Exception:
        return {
            "success": False,
            "message": "The requested data could not be retrieved due to a database schema mismatch."
        }

@tool
def get_customer_profile(cust_id: str) -> dict:
    """retrieve a customer's profile by id. sensitive data is automatically masked."""
    try:
        customer = execute_fetchone("select * from customer where cust_id = ?", (cust_id,))
        
        if not customer:
            return {"found": False, "message": f"No records found for customer {cust_id}."}
            
        customer['email'] = _mask_email(customer.get('email', ''))
        customer['phone'] = _mask_phone(customer.get('phone', ''))
        
        return {"found": True, "customer": customer}
    except Exception:
        return {
            "success": False,
            "message": "The requested data could not be retrieved due to a database schema mismatch."
        }

@tool
def get_card_details(cust_id: str) -> dict:
    """retrieve credit card details for a customer with masked numbers and removed cvvs."""
    try:
        rows = execute_query(
            "select * from card where cust_id = ?",
            (cust_id,)
        )

        if not rows:
            return {
                "found": False,
                "message": f"No cards found for customer {cust_id}."
            }

        cards = []

        for row in rows:
            row["card_number"] = _mask_card_number(
                str(row["card_number"])
            )

            row["security_code"] = "***"

            cards.append(row)

        return {
            "found": True,
            "cards": cards
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
@tool
def search_transactions(
    cust_id: Optional[str] = None, 
    merchant_id: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,    
    limit: int = 10
) -> dict:
    """search and filter transactions by customer, merchant, or amount ranges."""
    try:
        query = """
            select t.*, m.merchant as merchant_name 
            from "transaction" t 
            left join merchant m on t.M_ID = m.id 
            left join card c on t.CARD_ID = c.card_number 
            where 1=1
        """
        params = [] 
        if cust_id:
            query += " and c.cust_id = ?"
            params.append(cust_id)
        if merchant_id:
            query += " and t.M_ID = ?"
            params.append(merchant_id)
        if min_amount is not None:
            query += " and t.TX_AMOUNT >= ?"
            params.append(min_amount)
        if max_amount is not None:
            query += " and t.TX_AMOUNT <= ?"
            params.append(max_amount)
        query += " order by t.TX_DATETIME desc limit ?"
        params.append(limit)
        rows = execute_query(query, tuple(params))
        return {"count": len(rows), "transactions": rows}
    except Exception:
        return {
            "success": False,
            "message": "The requested data could not be retrieved due to a database schema mismatch."
        }

@tool
def get_customer_transactions(cust_id: str, limit: int = 5) -> dict:
    """fetch the most recent transactions for a specific customer."""
    try:
        return search_transactions.func(cust_id=cust_id, limit=limit)
    except Exception:
        return {
            "success": False,
            "message": "The requested data could not be retrieved due to a database schema mismatch."
        }

@tool
def get_statement_summary(cust_id: str) -> dict:
    """retrieve the latest statement summary and due amounts for a customer."""
    try:
        row = execute_fetchone("select * from statement where cust_id = ?", (cust_id,))
        
        if not row:
            return {"found": False, "message": f"No statement records found for customer {cust_id}."}
        return {"found": True, "statement": row}
    except Exception:
        return {
    "available": False,
    "message": "Statement information is not available in the current database."
}

@tool
def get_rewards_summary(cust_id: str) -> dict:
    """retrieve the total reward points for a customer."""
    try:
        row = execute_fetchone("select * from reward where cust_id = ?", (cust_id,))
        
        if not row:
            return {"found": False, "message": f"No reward records found for customer {cust_id}."}
        return {"found": True, "rewards": row}
    except Exception:
        return {
    "available": False,
    "message": "Rewards information is not available in the current database."
}

@tool
def get_merchant_spend_summary(limit: int = 10) -> dict:
    """aggregate and rank total customer spending by merchant type."""
    try:
        query = """
            select m.merchant_type, sum(t.TX_AMOUNT) as total_spend, count(t.TXN_ID) as transaction_count
            from "transaction" t
            join merchant m on t.M_ID = m.id
            group by m.merchant_type
            order by total_spend desc
            limit ?
        """
        rows = execute_query(query, (limit,))
        return {"group_by": "merchant_type", "results": rows}
    except Exception:
        return {
            "success": False,
            "message": "The requested data could not be retrieved due to a database schema mismatch."
        }
tools = [
    inspect_database_schema, 
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions, 
    get_statement_summary,
    get_rewards_summary,
    get_merchant_spend_summary
]