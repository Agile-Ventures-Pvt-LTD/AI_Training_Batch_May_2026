import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db_utils import get_connection
get_connection()

from tools import inspect_database_schema
results=inspect_database_schema()
print(results)

from tools import get_customer_profile
result=get_customer_profile("10")
print(result)

from tools import get_card_details
result=get_card_details("60")
print(result)

from tools import search_transactions
print(search_transactions("10"))

from tools import get_customer_transactions
print(get_customer_transactions("20"))

from tools import detect_suspicious_transactions
print(detect_suspicious_transactions())

from tools import get_rewards_summary
result=get_rewards_summary("1")

from tools import get_merchant_spend_summary
print(get_merchant_spend_summary())



