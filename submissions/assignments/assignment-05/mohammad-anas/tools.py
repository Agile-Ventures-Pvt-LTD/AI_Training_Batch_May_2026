import json
from db_utils import (
    get_connection,
    row_to_dict,
    execute,
    fetch_one,
    fetch_all,
    inspect_schema,
)

def get_inspect_schema() -> str:
    """show the schema of the database"""
    try:
        tables = inspect_schema()
        schema = {}
        
        for table in tables:
            q = f"PRAGMA table_info('{table}')"
            column_data = fetch_all(q)
            
            if column_data:
                column_name = [col["name"] for col in column_data]
                
                schema[table] = column_name
        final_output = {
            "tables" : tables,
            "schema": schema
        }
        return json.dumps(final_output)
    except Exception as e:
        print(f"DEBUG TOOL ERROR: {e}")
        return f"error {e}"
            

def get_customer_profile(customer_id=None,email=None,phone=None,first_name=None,last_name=None):
    """Fetch customer details."""

    q = "SELECT * FROM customer WHERE 1=1"

    try:

        if customer_id:
            q += " AND cust_id = ?"
            res = fetch_one(q, (customer_id,))

        elif email:
            q += " AND email = ?"
            res = fetch_one(q, (email,))

        elif phone:
            q += " AND phone = ?"
            res = fetch_one(q, (phone,))

        elif first_name:
            q += " AND first_name = ?"
            res = fetch_one(q, (first_name,))

        elif last_name:
            q += " AND last_name = ?"
            res = fetch_one(q, (last_name,))

        else:
            return "Please provide search input"

        if not res:
            return "Customer not found"

        if res.get("email"):
            email_parts = res["email"].split("@")
            if len(email_parts) == 2:
                res["email"] = email_parts[0][:2] + "***@" + email_parts[1]

        if res.get("phone"):
            res["phone"] = "******" + str(res["phone"])[-4:]

        return json.dumps(res)

    except Exception as e:
        return f"error {e}"
        
def get_card_details(card_number=None, customer_id=None):
    """Fetch card details."""

    q = """
        SELECT card_number, valid_from, expiry, cust_id, card_type_id FROM card WHERE 1=1
    """

    try:

        if card_number:
            q += " AND card_number = ?"
            res = fetch_one(q, (card_number,))

        elif customer_id:
            q += " AND cust_id = ?"
            res = fetch_one(q, (customer_id,))

        else:
            return "Please provide card number or customer id"

        if not res:
            return "No card found"

        raw_card = str(res["card_number"])

        res["card_number"] = (
            "**** **** **** " +
            raw_card[-4:]
        )

        return json.dumps(res)

    except Exception as e:
        return f"error {e}"    
    
def search_transactions(customer_id: str = None, card_last4: str = None, merchant_name: str = None, min_amount: str = None, max_amount: str = None, from_date: str = None, to_date: str = None, transaction_type: str = None, limit: str = None) -> str:
    """Search transactions by multiple optional filters."""
    q = """
        SELECT 
            t.TXN_ID, 
            t.TX_DATETIME, 
            t.TX_AMOUNT, 
            m.merchant as merchant_name, 
            tt.debit_credit as transaction_type, 
            c.card_number
        FROM "transaction" t
        JOIN merchant m ON t.M_ID = m.id
        JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE 1=1
    """
    params = []

    try:
        if customer_id:
            q += " AND c.cust_id = ?"
            params.append(customer_id)
            
        if merchant_name:
            q += " AND m.merchant = ?"
            params.append(merchant_name)
            
        if min_amount:
            q += " AND t.TX_AMOUNT >= ?"
            params.append(min_amount)
            
        if max_amount:
            q += " AND t.TX_AMOUNT <= ?"
            params.append(max_amount)
            
        if from_date:
            q += " AND t.TX_DATETIME >= ?"
            params.append(from_date)
            
        if to_date:
            q += " AND t.TX_DATETIME <= ?"
            params.append(to_date)
            
        if transaction_type:
            q += " AND tt.debit_credit = ?"
            params.append(transaction_type)

        if card_last4:
            q += " AND c.card_number LIKE ?"
            params.append(f"%{card_last4}")
            
        if limit:
            q += " LIMIT ?"
            params.append(limit)
        q += " LIMIT 20"

        res = fetch_all(q, tuple(params))
        
        if res:
            for row in res:
                if row.get('card_number'):
                    raw_num = str(row['card_number']).replace(" ", "")
                    row['card_number'] = f"**** **** **** {raw_num[-4:]}"
            return str(res)
        else:
            return "No transactions found matching those filters."

    except Exception as e:
        print(f"DEBUG ERROR in search_transactions: {e}")
        return f"error {e}"
    
def  get_customer_transactions(customer_id:str) -> str:
    """Fetch the recent transctions of the customer by customer id"""
    q = """
        SELECT t.* FROM "transaction" t
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE c.cust_id = ?
        ORDER BY t.TX_DATETIME DESC 
        LIMIT 10
    """
    try:
       transactions_data = fetch_all(q, (customer_id,))
       final_output = {
            "customer_id": customer_id,
            "transaction_count": len(transactions_data), # Count how many we found
            "transactions": transactions_data
        }
       return json.dumps(final_output)
    except Exception as e:
        print(f"errro {e}")
        return f"error {e}"
    
def get_merchant_spend_summary() -> str:
    """Aggregate transaction amount by merchant type to see where money is being spent."""
    q = """
        SELECT 
            mt.merchant_type, 
            SUM(t.TX_AMOUNT) as total_spend, 
            COUNT(t.TXN_ID) as transaction_count
        FROM "transaction" t
        JOIN merchant m ON t.M_ID = m.id
        JOIN merchant_type mt ON m.merchant_type = mt.id
        GROUP BY mt.merchant_type
        ORDER BY total_spend DESC
    """
    try:
        res = fetch_all(q)
        
        final_output = {
            "group_by": "merchant_type",
            "results": res
        }
        return json.dumps(final_output)
    except Exception as e:
        print(f" DEBUG ERROR in get_merchant_spend_summary: {e}")
        return f"error {e}"
    
def detect_suspicious_transactions():
    """Detect suspicious transactions."""

    q = """SELECT TXN_ID, TX_AMOUNT, CARD_ID FROM "transaction" WHERE TX_AMOUNT > 75000
    """

    try:

        res = fetch_all(q)

        output = []

        for row in res:

            output.append(
                {
                    "txn_id": row["TXN_ID"],
                    "amount": row["TX_AMOUNT"],
                    "reason": "High value transaction"
                }
            )

        final_output = {
            "rule_applied": "amount > 75000",
            "count": len(output),
            "flagged_transactions": output
        }

        return json.dumps(final_output)

    except Exception as e:
        return f"error {e}"