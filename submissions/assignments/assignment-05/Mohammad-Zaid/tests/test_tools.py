# Testing 

from db_tools import (
    
    inspect_database_schema,
    
    get_card_details,
    
    get_customer_profile,
    
    search_transactions,
    
    get_customer_transactions,
    
    get_rewards_summary,
    
    get_merchant_spend_summary,
    
    get_statement_summary,
    
    )


print("\n---Testing Database Schema---")
res = inspect_database_schema()
print(res)


print("\n---Testing Customer Profile---")
res = get_customer_profile(5)
print(res)


print("\n---Testing Transaction Search---")
result = search_transactions(limit=5)
print(result)


print("\n---Testing Card Details---")
res = get_card_details(786)
print(res)


print("\n---Testing Statement Summary---")
res = get_statement_summary(92)
print(res)


print("\n---Testing Customer Transactions---")
res = get_customer_transactions(72)
print(res)


print("\n---Testing Reward Summary---")
res = get_rewards_summary(101)
print(res)


print("\n---Testing Merchant's Spend Summary---")
res = get_merchant_spend_summary()
print(res)