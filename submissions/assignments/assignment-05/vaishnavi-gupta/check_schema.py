from db_utils import get_table_schema

tables = [
    "customer",
    "card",
    "card_type",
    "transaction",
    "transaction_type",
    "merchant",
    "merchant_type",
    "transaction_terminal",
    "netbanking"
]

for table in tables:
    print("\n" + "=" * 80)
    print(table.upper())
    print("=" * 80)

    schema = get_table_schema(table)

    for column in schema:
        print(column["name"])