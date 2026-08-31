from tools import (inspect_database_schema,get_customer_profile,get_card_details,search_transactions,get_customer_transactions,
    get_statement_summary,get_rewards_summary,get_merchant_spend_summary,detect_suspicious_transactions)

print("Database Schema")
print(inspect_database_schema())
print("\n")

print("Customer Profile")
print(get_customer_profile("1"))
print("\n")

print("Card Details")
print(get_card_details("1"))
print("\n")

print("Search Transactions")
print(search_transactions(cust_id=1,limit=5))
print("\n")

print("Customer Transaction")
print(get_customer_transactions(cust_id=1,limit=5))
print("\n")

print("Statement Summary")
print(get_statement_summary(cust_id=1))
print("\n")

print("Reward Pints")
print(get_rewards_summary(cust_id=1))
print("\n")

print("Merchant Spend Summary")
print(get_merchant_spend_summary(group_by="merchant_type"))
print("\n")

print("Suspicious Transactions")
print(detect_suspicious_transactions())
print("\n")

print("All Test Completed Successfully.")