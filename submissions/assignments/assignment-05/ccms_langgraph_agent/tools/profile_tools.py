try:
    from db_utils.db_connection import get_conn
    from utils.tool_utils import create_tool
except ImportError as e:
    print(f"Error: {e}")

def get_customer_profile(customer_id: str):
    '''Get customer profile details by customer ID.'''
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(
        '''
        SELECT *
        FROM customer
        WHERE cust_id = ?
        ''',
        (customer_id,)
    )
    try:
        result = cursor.fetchone()
    except ValueError as e:
        print(f"No customer with customer id {customer_id} found. Error: {e}")
    conn.close()
    return {
        "found": True,
        "customer": {
            "cust_id": result[0],
            "name": result[1]+" "+result[2],
            "email": result[3],
            "city": result[6],
            "state": result[7],
            "zip": result[8]
        }
    }


get_customer_profile_description = '''Get customer profile details by customer ID. Use for customer information lookup such as name, email, city, state, and ZIP code.'''

get_customer_profile_tool = create_tool(function=get_customer_profile, tool_name="get_customer_profile", tool_description=get_customer_profile_description)