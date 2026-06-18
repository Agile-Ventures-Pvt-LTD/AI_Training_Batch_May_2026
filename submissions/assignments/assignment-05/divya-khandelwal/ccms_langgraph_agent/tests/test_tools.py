import sys
import os
from tools import inspect_database_schema

# Add project root path
sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

result = inspect_database_schema.invoke({})


print(result)

from tools import get_customer_profile



result = get_customer_profile.invoke(
    {
        "cust_id":"1"
    }
)


print(result)


from tools import get_card_details

result = get_card_details.invoke(
    {
        "cust_id":"1"
    }
)
print(result)


from tools import get_statement_summary



result = get_statement_summary.invoke(
    {
        "cust_id":5
    }
)


print(result)

from tools import search_transactions



result = search_transactions.invoke(
    {
        "limit":5
    }
)


print(result)


from tools import get_rewards_summary



result = get_rewards_summary.invoke(
    {
        "cust_id":1
    }
)


print(result)


from tools import get_merchant_spend_summary



result = get_merchant_spend_summary.invoke(
    {
        "cust_id":1
    }
)


print(result)