from langchain.tools import StructuredTool
from db_utils import query_execution
from datetime import datetime, timedelta

def inspect_database_schema():
    """Return database tables and columns."""
    tables = query_execution("""
        select name
        from sqlite_master
        where type = 'table'
        order by name """)
    schema = {}
    for table in tables:
        table_name = table["name"]
        columns = query_execution(f"PRAGMA table_info('{table_name}')")
        schema[table_name] = [col["name"] for col in columns]
    return {
        "tables": [table["name"] for table in tables],
        "schema": schema
    }

inspect_datbase_tool = StructuredTool.from_function(inspect_database_schema)

def get_customer_profile(cust_id: str):
    """Get customer details."""
    query = """
    select cust_id, first_name, last_name, email, phone, city, state
    from customer
    where cust_id = ?
    """
    result = query_execution(query, (cust_id,))
    if not result:
        return {"found": False}
    customer = result[0]
    return {
        "found": True,
        "customer": {
            "cust_id": customer["cust_id"],
            "name": f"{customer['first_name']} {customer['last_name']}",
            "email": customer["email"],
            "phone": customer["phone"],
            "city": customer["city"],
            "state": customer["state"]
        }
    }

customer_profile_tool = StructuredTool.from_function(get_customer_profile)

def get_card_details(cust_id: str):
    """Get customer cards."""
    query = "select * from card where cust_id = ?"
    results = query_execution(query, (cust_id,))
    cards = []
    for card in results:
        cards.append({
            "card_number": f"****{str(card['card_number'])[-4:]}"
        })
    return {"cards": cards}

card_details_tool = StructuredTool.from_function(get_card_details)

def search_transactions(cust_id=None,card_last4=None,merchant_name=None,merchant_type=None,min_amount=None,max_amount=None,from_date=None,to_date=None,transaction_type=None,limit=5):
    """Search transactions using filters."""
    query = """
    select t.txn_id,t.tx_datetime,t.tx_amount,c.cust_id,c.first_name,c.last_name,card.card_number,m.merchant,mt.merchant_type,tt.debit_credit,tt.lcl_intnl
    from "transaction" t JOIN card
    on t.card_id = card.card_number
    join customer c
    on card.cust_id = c.cust_id
    join merchant m
    on t.m_id = m.id
    join merchant_type mt
    on m.merchant_type = mt.id
    join transaction_type tt
    on t.txn_type_id = tt.txn_type_id
    """
    conditions = []
    params = []
    if cust_id:
        conditions.append("c.cust_id = ?")
        params.append(cust_id)
    if card_last4:
        conditions.append("substr(card.card_number, -4) = ?")
        params.append(card_last4)
    if merchant_name:
        conditions.append("m.merchant = ?")
        params.append(merchant_name)
    if merchant_type:
        conditions.append("mt.merchant_type = ?")
        params.append(merchant_type)
    if min_amount:
        conditions.append("t.tx_amount >= ?")
        params.append(min_amount)
    if max_amount:
        conditions.append("t.tx_amount <= ?")
        params.append(max_amount)
    if from_date:
        conditions.append("date(t.tx_datetime) >= ?")
        params.append(from_date)
    if to_date:
        conditions.append("date(t.tx_datetime) <= ?")
        params.append(to_date)
    if transaction_type:
        conditions.append("tt.debit_credit = ?")
        params.append(transaction_type)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY t.tx_datetime DESC LIMIT ?"
    params.append(limit)
    results = query_execution(query, tuple(params))
    for txn in results:
        txn["card_number"] = f"****{str(txn['card_number'])[-4:]}"
    return {
        "count": len(results),
        "transactions": results
    }

search_transactions_tool = StructuredTool.from_function(search_transactions)

def get_customer_transactions(cust_id,from_date=None,to_date=None,limit=10):
    """Get customer transactions."""
    return search_transactions(
        cust_id=cust_id,
        from_date=from_date,
        to_date=to_date,
        limit=limit
    )

customer_transcations_tool = StructuredTool.from_function(get_customer_transactions)

def get_statement_summary(cust_id):
    """Get statement summary."""
    query = """
    select round(SUM(t.tx_amount), 2) as total_amount_due
    from "transaction" t join card c
    on t.card_id = c.card_number
    where c.cust_id = ?
    """
    result = query_execution(query, (cust_id,))
    total_amount_due = result[0]["total_amount_due"] or 0
    min_amount_due = round(total_amount_due * 0.05, 2)
    statement_date = datetime.today().date()
    due_date = statement_date + timedelta(days=15)

    if total_amount_due >= 5000:
        risk_level = "High"
    elif total_amount_due >= 2000:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    return {
        "cust_id": cust_id,
        "total_amount_due": total_amount_due,
        "min_amount_due": min_amount_due,
        "statement_date": str(statement_date),
        "due_date": str(due_date),
        "risk_level": risk_level
    }

statement_summary_tool = StructuredTool.from_function(get_statement_summary)

def get_rewards_summary(cust_id):
    """Get reward points."""
    query = """
    select t.txn_id, t.tx_datetime, t.TX_AMOUNT
    from "transaction" t join card c
    on t.card_id = c.card_number
    where c.cust_id = ?
    order by t.TX_AMOUNT desc
    limit 10
    """
    results = query_execution(query, (cust_id,))
    reward_points = 0
    for txn in results:
        reward_points += int(txn["TX_AMOUNT"] // 10)
    return {
        "cust_id": cust_id,
        "reward_points": reward_points,
        "related_transactions": results
    }

rewards_summary_tool = StructuredTool.from_function(get_rewards_summary)

def get_merchant_spend_summary(grouped_by="merchant_type"):
    """Get merchant spending summary."""
    if grouped_by == "merchant":
        query = """
        select m.merchant, round(sum(t.tx_amount), 2) as total_spend,count(*) as transaction_count
        from "transaction" t join merchant m
        on t.m_id = m.id
        group by m.merchant
        order by total_spend desc
        """
    else:
        query = """
        select mt.merchant_type, round(sum(t.tx_amount), 2) as total_spend, count(*) as transaction_count
        from "transaction" t join merchant m
        on t.m_id = m.id
        join merchant_type mt
        on m.merchant_type = mt.id
        group by mt.merchant_type
        order by total_spend desc
        """
    results = query_execution(query)
    return {
        "group_by": grouped_by,
        "results": results
    }

merchant_spend_summary_tool = StructuredTool.from_function(get_merchant_spend_summary)

def detect_suspicious_transactions():
    """Find high-value transactions."""
    query = """
    select txn_id, tx_amount, tx_datetime
    from "transaction"
    where tx_amount > 75000
    """
    results = query_execution(query)
    flagged_transactions = []
    for txn in results:
        flagged_transactions.append({
            "txn_id": txn["txn_id"],
            "amount": txn["tx_amount"],
            "reason": "High-value transaction"
        })
    return {
        "count": len(flagged_transactions),
        "flagged_transactions": flagged_transactions
    }

suspicious_transactions_tool = StructuredTool.from_function(detect_suspicious_transactions)

tools = [inspect_datbase_tool,customer_profile_tool,card_details_tool,search_transactions_tool,customer_transcations_tool,statement_summary_tool,rewards_summary_tool,merchant_spend_summary_tool,suspicious_transactions_tool,]