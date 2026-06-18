import json
import os

from langchain_core.tools import tool

from db_utils import get_connection



OUTPUT_DIR = "outputs/tool_outputs"


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)



def save_tool_output(filename, data):
    """
    Save tool response separately
    for evaluation
    """

    filepath = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(
        filepath,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            default=str
        )



def execute_query(query, params=()):
    """
    Execute safe parameterized SELECT query
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            query,
            params
        )

        rows = cursor.fetchall()


        return [
            dict(row)
            for row in rows
        ]


    except Exception as e:

        return {
            "error":str(e)
        }


    finally:

        conn.close()



def execute_single(query, params=()):
    """
    Return single database record
    """

    result = execute_query(
        query,
        params
    )


    if isinstance(result,list):

        if len(result)>0:
            return result[0]

        return None


    return result



def get_schema():

    """
    Read database schema
    """

    conn = get_connection()

    cursor = conn.cursor()


    tables = cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    ).fetchall()


    schema={}


    for table in tables:

        table_name = table["name"]


        columns = cursor.execute(
            f"""
            PRAGMA table_info("{table_name}")
            """
        ).fetchall()


        schema[table_name]=[
            column["name"]
            for column in columns
        ]


    conn.close()


    return {

        "tables":
        list(schema.keys()),


        "schema":
        schema

    }

@tool
def inspect_database_schema():
    """
    Inspect database tables and columns.
    """

    result = get_schema()


    save_tool_output(
        "schema_output.json",
        result
    )


    return result



@tool
def get_customer_profile(
    cust_id: str
):
    """
    Get customer profile using customer ID.
    Sensitive fields are masked.
    """

    query = """

    SELECT

    cust_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    state

    FROM customer

    WHERE cust_id = ?

    """


    customer = execute_single(
        query,
        (cust_id,)
    )


    if customer is None:

        result = {

            "found": False,

            "message":
            "Customer not found"

        }


    else:

        # Combine first and last name

        name = (
            customer.get("first_name","")
            +
            " "
            +
            customer.get("last_name","")
        )


        # Mask email

        email = customer.get(
            "email"
        )


        if email:

            parts = email.split("@")

            masked_email = (
                parts[0][0]
                +
                "****@"
                +
                parts[1]
            )

        else:

            masked_email = None



        # Mask phone

        phone = customer.get(
            "phone"
        )


        if phone:

            masked_phone = (
                "******"
                +
                str(phone)[-4:]
            )

        else:

            masked_phone = None



        result = {

            "found": True,

            "customer": {

                "cust_id":
                customer.get("cust_id"),


                "name":
                name,


                "email":
                masked_email,


                "phone":
                masked_phone,


                "city":
                customer.get("city"),


                "state":
                customer.get("state")

            }

        }



    # Save separate evaluation output

    save_tool_output(
        "customer_profile_output.json",
        result
    )


    return result


@tool
def get_card_details(
    cust_id: int
):
    """
    Get card details for customer.
    Sensitive fields are masked.
    """

    query = """

    SELECT

    card_number,
    valid_from,
    expiry,
    cust_id,
    card_type_id

    FROM card

    WHERE cust_id = ?

    """


    cards = execute_query(
        query,
        (cust_id,)
    )


    if not cards:

        result = {

            "found": False,

            "message":
            "No cards found for customer"

        }


    else:

        masked_cards = []


        for card in cards:

            card_number = str(
                card["card_number"]
            )


            masked_number = (
                "**** **** **** "
                +
                card_number[-4:]
            )


            masked_cards.append(

                {

                    "card_number":
                    masked_number,


                    "valid_from":
                    card["valid_from"],


                    "expiry":
                    card["expiry"],


                    "card_type_id":
                    card["card_type_id"]

                }

            )



        result = {

            "found": True,

            "customer_id":
            cust_id,

            "card_count":
            len(masked_cards),

            "cards":
            masked_cards

        }



    save_tool_output(
        "card_details_output.json",
        result
    )


    return result


@tool
def search_transactions(
    card_id: int = None,
    min_amount: float = None,
    limit: int = 10
):
    """
    Search transactions using filters.
    """

    query = """

    SELECT

    TXN_ID,
    TX_DATETIME,
    CARD_ID,
    TERMINAL_ID,
    TX_AMOUNT,
    TXN_TYPE_ID,
    M_ID

    FROM "transaction"

    WHERE 1=1

    """

    params = []


    # Filter by card

    if card_id is not None:

        query += """

        AND CARD_ID = ?

        """

        params.append(
            card_id
        )


    # Filter by amount

    if min_amount is not None:

        query += """

        AND TX_AMOUNT >= ?

        """

        params.append(
            min_amount
        )


    query += """

    ORDER BY TX_DATETIME DESC

    LIMIT ?

    """

    params.append(
        limit
    )


    transactions = execute_query(
        query,
        tuple(params)
    )


    result = {

        "count":
        len(transactions),


        "transactions":
        transactions

    }


    save_tool_output(
        "transaction_output.json",
        result
    )


    return result



@tool
def get_customer_transactions(
    cust_id: int,
    limit: int = 5
):
    """
    Get recent transactions of a customer.
    """

    query = """

    SELECT

    t.TXN_ID,
    t.TX_DATETIME,
    t.CARD_ID,
    t.TX_AMOUNT,
    t.TERMINAL_ID,
    t.TXN_TYPE_ID,
    t.M_ID


    FROM "transaction" t


    JOIN card c

    ON t.CARD_ID = c.card_type_id


    WHERE c.cust_id = ?


    ORDER BY 
    t.TX_DATETIME DESC


    LIMIT ?

    """


    transactions = execute_query(
        query,
        (
            cust_id,
            limit
        )
    )


    result = {

        "customer_id":
        cust_id,


        "transaction_count":
        len(transactions),


        "transactions":
        transactions

    }


    save_tool_output(
        "customer_transactions_output.json",
        result
    )


    return result

@tool
def get_statement_summary(
    cust_id: int
):
    """
    Generate customer statement summary
    using transaction history.
    """

    query = """

    SELECT

    COUNT(t.TXN_ID) AS total_transactions,

    SUM(t.TX_AMOUNT) AS total_spend,

    AVG(t.TX_AMOUNT) AS average_transaction,

    MAX(t.TX_AMOUNT) AS highest_transaction,

    MIN(t.TX_DATETIME) AS statement_start_date,

    MAX(t.TX_DATETIME) AS statement_end_date


    FROM transaction t


    JOIN card c

    ON t.CARD_ID = c.card_number


    WHERE c.cust_id = ?

    """


    summary = execute_single(
        query,
        (cust_id,)
    )


    if summary:

        # Risk calculation

        total_spend = summary.get(
            "total_spend",
            0
        )


        if total_spend > 100000:

            risk_level = "HIGH"


        elif total_spend > 50000:

            risk_level = "MEDIUM"


        else:

            risk_level = "LOW"



        result = {

            "customer_id":
            cust_id,


            "statement":

            {

                "total_transactions":
                summary.get(
                    "total_transactions"
                ),


                "total_spend":
                summary.get(
                    "total_spend"
                ),


                "average_transaction":
                summary.get(
                    "average_transaction"
                ),


                "highest_transaction":
                summary.get(
                    "highest_transaction"
                ),


                "statement_start_date":
                summary.get(
                    "statement_start_date"
                ),


                "statement_end_date":
                summary.get(
                    "statement_end_date"
                ),


                "risk_level":
                risk_level

            }

        }


    else:

        result = {

            "customer_id":
            cust_id,

            "message":
            "No transaction history found"

        }



    save_tool_output(
        "statement_summary_output.json",
        result
    )


    return result


@tool
def get_rewards_summary(
    cust_id: int
):
    """
    Calculate customer reward summary
    from transaction spending.
    """


    query = """

    SELECT

    SUM(t.TX_AMOUNT) AS total_spend


    FROM "transaction" t


    JOIN card c

    ON t.CARD_ID = c.card_number


    WHERE c.cust_id = ?

    """


    spend = execute_single(
        query,
        (cust_id,)
    )

    print("REWARD QUERY RESULT:")
    print(spend)

    if (
    spend
    and isinstance(spend, dict)
    and spend.get("total_spend") is not None
):


        total_spend = spend["total_spend"]


        # Reward calculation
        reward_points = int(
            total_spend / 100
        )


        if reward_points >= 10000:

            tier = "PLATINUM"


        elif reward_points >= 5000:

            tier = "GOLD"


        else:

            tier = "SILVER"



        result = {


            "customer_id":
            cust_id,


            "rewards":

            {

                "total_spend":
                total_spend,


                "reward_points":
                reward_points,


                "reward_tier":
                tier

            }

        }


    else:


        result = {

            "customer_id":
            cust_id,


            "rewards":

            {

                "total_spend":0,

                "reward_points":0,

                "reward_tier":"NONE"

            }

        }



    save_tool_output(
        "rewards_summary_output.json",
        result
    )


    return result


@tool
def get_merchant_spend_summary(
    cust_id: int
):
    """
    Get spending summary grouped by merchant.
    """


    query = """

    SELECT


    m.id AS merchant_id,

    m.merchant,

    mt.merchant_type,


    COUNT(t.TXN_ID)
    AS transaction_count,


    SUM(t.TX_AMOUNT)
    AS total_spend,


    AVG(t.TX_AMOUNT)
    AS average_spend



    FROM "transaction" t



    JOIN card c

    ON t.CARD_ID = c.card_number



    JOIN merchant m

    ON t.M_ID = m.id



    JOIN merchant_type mt

    ON m.merchant_type = mt.id



    WHERE c.cust_id = ?



    GROUP BY

    m.id,

    m.merchant,

    mt.merchant_type



    ORDER BY

    total_spend DESC


    """



    merchant_data = execute_query(
        query,
        (cust_id,)
    )



    result = {


        "customer_id":
        cust_id,


        "merchant_count":
        len(merchant_data),


        "merchant_spending":
        merchant_data


    }



    save_tool_output(
        "merchant_spend_summary_output.json",
        result
    )


    return result