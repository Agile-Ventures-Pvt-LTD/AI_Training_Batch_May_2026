from tools import (
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_reward_summary,
    get_merchant_spend_summary
)

print("Databse Schema")
print(inspect_database_schema())

print("\n")
print("="*20)
print("\n")

print("Customer Proile")
print(get_customer_profile(12))

print("\n")
print("="*20)
print("\n")

print("Customer Card Details")
print(get_card_details(21))

print("\n")
print("="*20)
print("\n")

print("Search Trasnsaction")
print(search_transactions(21)) # Ther are multiple fileds which can be get the eaxct output.

print("\n")
print("="*20)
print("\n")

print("Customer Transactions")
print(get_customer_transactions(32))

print("\n")
print("="*20)
print("\n")

print("Statement Summary")
print(get_statement_summary(222))

print("\n")
print("="*20)
print("\n")

print("Reward Summary")
print(get_reward_summary(12))

print("\n")
print("="*20)
print("\n")

print("Merchant Spend Summary")
print(get_merchant_spend_summary())
