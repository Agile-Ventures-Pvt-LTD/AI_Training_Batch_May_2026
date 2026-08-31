from tools import (get_card_details,get_customer_profile,get_customer_transactions,get_merchant_spend_summary,
                   get_reward_summary,get_statement_summary,inspect_database_schema,search_transactions)


print("\nTesting Database Schema")
result = inspect_database_schema()
print(result)


print("\nTesting Customer Profile")
result = get_customer_profile(1)
print(result)


print("\nTesting Card Details")
result = get_card_details(1)
print(result)


print("\nTesting Transaction Search")
result = search_transactions(5000)
print(result)


print("\nTesting Customer Transactions")
result = get_customer_transactions(1, 5)
print(result)


print("\nTesting Statement Summary")
result = get_statement_summary(1)
print(result)


print("\nTesting Reward Summary")
result = get_reward_summary(1)
print(result)


print("\nTesting Merchant Spend Summary")
result = get_merchant_spend_summary()
print(result)