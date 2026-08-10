from db_utils import get_connection
import sqlite3
from pprint import pprint

#==============TOOL 1=========================
def inspect_database_schema():

    """
    It will inspect the schema of ccms.db database
    """
    conn=get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table';
    """)

    tables = cursor.fetchall()

    schema_info = {
        "tables": [],
        "schema": {}
    }

    for table in tables:
        table_name = table[0]

        # Add table name to tables list
        schema_info["tables"].append(table_name)

        # Get column information
        cursor.execute(f'PRAGMA table_info("{table_name}")')

        columns = cursor.fetchall()

        schema_info["schema"][table_name] = [
            column[1] for column in columns
        ]

    conn.close()
    return schema_info

# schema=inspect_database_schema()
# print(schema)


#==============TOOL2=======================
def get_customer_profile(
    
    cust_id=None,
    first_name=None,
    last_name=None,
    card_number=None
):
    """
    this tool is used to find customer information by customer ID, email, phone, or name.
    It take input as 

    {
    "cust_id": 91
    }
    If user query mentions CUST-1001 it means 1001
    
    Output should strictly be in this form where found=true if value exist and found=false is value not exist

    }
    "found": true,
    "customer": {
    "cust_id": 91,
    "name": "Anika Sharma",
    "email": "masked@example.com",
    "city": "Pune",
    "state": "Maharashtra"
    }
    Sensitive data rule:
    Mask phone and email if necessary.
    """

    filters = {}

    if cust_id:
        filters["cust_id"] = cust_id

    if first_name:
        filters["first_name"] = first_name

    if last_name:
        filters["last_name"] = last_name

    if card_number:
        filters["card_number"] = card_number

    conn=get_connection()

    conn.row_factory=sqlite3.Row

    cursor=conn.cursor()

    column_name, column_value = next(iter(filters.items()))


    #-------check whether column value exist------
    cursor.execute(f"""SELECT EXISTS(SELECT 1
                    FROM customer ct
                    WHERE {column_name}=?)""",(column_value,))

    found = bool(cursor.fetchone()[0])
    if not found:
        conn.close()

        return {
            "found": False,
            "customer": None
        }

    cursor.execute(f"""
                    SELECT ct.* 
                    from customer ct
                    where {column_name}=?
                        """,(column_value,))
        
    customer_info=dict(cursor.fetchone())

    conn.close()
    return {"found":True,
            "customer":customer_info}

#===============TO0L 3======================


def get_card_details(
    cust_id=None,
    card_last4=None,
    card_number=None
):
    """
    Get card information for a customer or card identifier.

    It takes input as a dictionary. 

    Output should not expose:
    full card number
    security_code
    password
    security answers
    
    Expected masking:
    **** **** **** 1234
    """

    filters = {}

    if cust_id:
        filters["cust_id"] = cust_id

    if card_last4:
        filters["card_last4"] = card_last4

    if card_number:
        filters["card_number"] = card_number


    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    column_name,column_value=next(iter(filters.items()))
    cursor.execute(f"""SELECT * 
                   FROM card 
                   WHERE {column_name}=?""",(column_value,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return {"found": False,
                "card": None
                }

    card_info = dict(row)
    conn.close()

    card_number = str(card_info['card_number'])
    masked_card = '**** **** **** ' + card_number[-4:]
    card_info['card_number'] = masked_card

    card_info.pop('security_code', None)

    return {"found": True,
            "card": card_info}


#=====================TOOL 4==============================

def search_transactions(
    cust_id=None,
    merchant=None,
    merchant_type=None,
    min_amount=None,
    max_amount=None,
    transaction_type=None,
    card_last4=None,
    from_date=None,
    to_date=None,
    limit=10
):
    """
    Search transactions by filters.

    Supported filters:

    -customer_id
    -card_last4
    -merchant_name
    -merchant_type
    -min_amount
    -max_amount
    -from_date
    -to_date
    -transaction_type
    -limit

    It takes input as a dictionary
    Output:
    {
    
        "count": 5,
        "transactions": [
        {
        "txn_id": "TXN-1001",
        "txn_datetime": "2026-01-15 11:30:00",
        "amount": 4500,
        "merchant": "Amazon",
        "transaction_type": "Debit",
        "remarks": "Online purchase"
        }
    }
    """

    filters = {}

    if cust_id is not None:
        filters["cust_id"] = cust_id

    if merchant:
        filters["merchant"] = merchant

    if merchant_type:
        filters["merchant_type"] = merchant_type

    if min_amount is not None:
        filters["min_amount"] = min_amount

    if max_amount is not None:
        filters["max_amount"] = max_amount

    if transaction_type:
        filters["transaction_type"] = transaction_type

    if card_last4:
        filters["card_last4"] = card_last4

    if from_date:
        filters["from_date"] = from_date

    if to_date:
        filters["to_date"] = to_date

    filters["limit"] = limit

    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    values=[]

    query="""
        SELECT 
            t.*,
            m.merchant,
            mt.merchant_type,
            tt.debit_credit
        FROM "transaction" t 

        LEFT JOIN merchant m
        ON t.M_ID=m.id

        LEFT JOIN card c
        ON t.CARD_ID=c.card_number

        LEFT JOIN merchant_type mt
        ON m.merchant_type = mt.id

        LEFT JOIN transaction_type tt
        ON t.TXN_TYPE_ID = tt.txn_type_id

        where 1=1 """

    
    if "cust_id" in filters:
        query += " AND c.cust_id = ?"
        values.append(filters["cust_id"])

    if "merchant" in filters:
        query += " AND m.merchant = ?"
        values.append(filters["merchant"])

    if "min_amount" in filters:
        query += " AND t.TX_AMOUNT >= ?"
        values.append(filters["min_amount"])

    if "max_amount" in filters:
        query += " AND t.TX_AMOUNT <= ?"
        values.append(filters["max_amount"])
    
    if "M_ID" in filters:
        query += " AND t.M_ID = ?"
        values.append(filters["M_ID"])

    if "merchant_type" in filters:
        query += " AND mt.merchant_type = ?"
        values.append(filters["merchant_type"])

    if "transaction_type" in filters:
        query += " AND tt.debit_credit = ?"
        values.append(filters["transaction_type"])
    
    if "from_date" in filters:
        query += " AND t.TX_DATETIME >= ?"
        values.append(filters["from_date"])

    if "to_date" in filters:
        query += " AND t.TX_DATETIME <= ?"
        values.append(filters["to_date"])

    if "card_last4" in filters:
        query += " AND substr(c.card_number,-4)=?"
        values.append(filters["card_last4"])

    query += " ORDER BY t.TX_DATETIME DESC"

    limit = filters.get("limit",10)
    query += f" LIMIT {limit}"

    

    # for column, value in filters.items():
    #     query=query + f" AND {column}= ?"
    #     values=values+(value,)
    cursor.execute(query,tuple(values))
        
    rows=cursor.fetchall()


    conn.close()
    count_trans=len(rows)

    trans_info=[dict(row) for row in rows]



    return {"count":count_trans,
            "transactions":trans_info}


#===================TOOL 5============================

def get_customer_transactions(
    cust_id,
    limit=10
):

   
    """
    Purpose:
    It takes customer id as input.
    Return recent transactions for a customer.
    Required output:
        {
            "customer_id": "",
            "transaction_count": 0,
            "transactions": []
        }

"""

    filters = {
        "cust_id": cust_id,
        "limit": limit
    }

    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    column_name,column_value=next(iter(filters.items()))
    cursor.execute("""
                    SELECT
                        c.cust_id customer_id,
                        t.TXN_ID,
                        TX_DATETIME,
                        TX_AMOUNT
                    FROM card c
                    JOIN "transaction" t
                    ON c.card_number=t.CARD_ID
                   WHERE c.cust_id=? 
                   ORDER BY t.TX_DATETIME DESC
                   LIMIT 5
                    """,(column_value,))
    
    rows=cursor.fetchall()
    conn.close()

    if not rows:
            return {
                "customer_id": column_value,
                "transaction_count": 0,
                "transactions": []
            }


    count=len(rows)
    trans_info=[dict(row) for row in rows]

    return {
        "customer_id": rows[0]["customer_id"],
        "transaction_count": count,
        "transactions": trans_info
    }


#==================TOOL 6===================

def get_statement_summary(
    cust_id=None,
    card_number=None
):


    """
    Purpose:  Return statement and due information.
    Expected output:
        {
        "customer_id": "",
        "total_amount_due": 0,
        "min_amount_due": 0,
        "statement_date": "",
        "due_date": "",
        "risk_level": "LOW | MEDIUM | HIGH
        }
    """
    filters = {}

    if cust_id:
        filters["cust_id"] = cust_id

    if card_number:
        filters["card_number"] = card_number


    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    column_name, column_value=next(iter(filters.items()))
    # print(f"Column Name:{column_name}")
    # print(f"Column Value:{column_value}")
    cursor.execute(f"""
                    SELECT
                        c.cust_id customer_id,
                        SUM(t.TX_AMOUNT) total_amount_due,
                        DATE(MAX(t.TX_DATETIME)) statement_date,
                        DATE(MAX(t.TX_DATETIME),'15 days') due_date
                   FROM card c
                   JOIN "transaction" t
                   ON c.card_number=t.CARD_ID
                   WHERE {column_name}=?
                   GROUP BY c.cust_id
                    """,(column_value,))
  
    statement_summary=dict(cursor.fetchone())

    conn.close()

    total_amount_due=statement_summary['total_amount_due']
    statement_summary['min_amount_due']=round(total_amount_due*0.05,2)

    if statement_summary['total_amount_due']<10000:
        statement_summary['risk_level']="LOW"

    elif statement_summary['total_amount_due']<50000:
        statement_summary['risk_level']="MEDIUM"

    else:
        statement_summary['risk_level']="HIGH"


    return statement_summary

#=======================TOOL 7====================
def get_reward_summary(
    cust_id=None,
    card_number=None
):



    """
    Purpose:
    Return reward points by customer or card.
    Expected output:
    {
        "customer_id": "",
        "reward_points": 0,
        "related_transactions": []
    }
    """

    filters = {}

    if cust_id:
        filters["cust_id"] = cust_id

    if card_number:
        filters["card_number"] = card_number

    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    column_name,column_value=next(iter(filters.items()))
    cursor.execute(f"""
                    SELECT 
                        c.cust_id customer_id,
                        round(SUM(t.TX_AMOUNT)/100,2) rewards_points
                   FROM card c
                   JOIN "transaction" t
                   ON c.card_number=t.CARD_ID
                   WHERE c.cust_id=?
                   GROUP BY c.cust_id
                   """,(column_value,))
    
    result=dict(cursor.fetchone())
   
    cursor.execute(f"""
                    SELECT 
                        t.TXN_ID,
                        t.TX_AMOUNT,
                        t.TX_DATETIME
                   FROM card c
                   JOIN "transaction" t
                   ON c.card_number=t.CARD_ID
                   WHERE c.cust_id=?
                   GROUP BY c.cust_id
                   LIMIT 5
                   """,(column_value,))
    
    rows=cursor.fetchall()
    transaction=[dict(row) for row in rows]
    conn.close()
    return {"customer_id":result["customer_id"],
            "rewards_points": result["rewards_points"],
            "related_transactions":transaction}


#=================TOOL 8=======================

def get_merchant_spend_summary(
    merchant_type=None
):

    """
    Purpose:
    It takes merchant type as input.
    Aggregate transaction amount by merchant or merchant type.

    Expected output:

    {
    
        "group_by": "merchant_type",
        "results": [
            {
            "merchant_type": "Electronics",
            "total_spend": 120000,
            "transaction_count": 18
            }
        ]
    }

    """
    
    filters = {}

    if merchant_type:
        filters["merchant_type"] = merchant_type


    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    column_name,column_value=next(iter(filters.items()))
    cursor.execute("""
                    SELECT 
                        mt.merchant_type merchant_type,
                        SUM(t.TX_AMOUNT) total_spent,
                        COUNT(t.TXN_ID) transaction_count
                   FROM merchant_type mt

                   JOIN merchant m
                   ON mt.id=m.merchant_type

                   JOIN "transaction" t
                   ON t.M_ID=M.id

                   WHERE mt.merchant_type=?
                   GROUP BY mt.merchant_type

                   """,(column_value,))
    
    result=dict(cursor.fetchone())
    # count=len(result)

    return {"group_by":"merchant_type",
            "results":[
                {"merchant_type":result["merchant_type"],
                 "total_spent":result["total_spent"],
                 "transaction_count":result["transaction_count"]}
            ]}
    