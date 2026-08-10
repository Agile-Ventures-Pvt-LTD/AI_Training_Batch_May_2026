from db_utils import fetch_all

tables = [
"users",
"devices",
"tickets",
"known_incidents",
"diagnostic_snapshots"
]

for table in tables:
    print("\n")
    print("=" * 50)
    print(table)
    print("=" * 50)

columns = fetch_all(
    f"PRAGMA table_info({table})"
)

for column in columns:
    print(column["name"])

