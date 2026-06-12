import sqlite3
from pathlib import Path


DB_PATH = Path("data/ecommerce.db")
OUTPUT_DIR = Path("test_results")
OUTPUT_FILE = OUTPUT_DIR / "database_output.txt"


def test_database():

    report = []

    if not DB_PATH.exists():
        report.append("FAIL: Database file not found.")
    else:
        report.append(f"PASS: Database found at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = [row[0] for row in cursor.fetchall()]

    report.append("\nTables Found:")
    for table in tables:
        report.append(f"- {table}")

    for table in tables:

        report.append("\n" + "=" * 60)
        report.append(f"TABLE: {table}")
        report.append("=" * 60)

        cursor.execute(f"PRAGMA table_info({table})")

        columns = cursor.fetchall()

        for column in columns:
            report.append(
                f"{column[1]} ({column[2]})"
            )

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        report.append(
            f"\nRecord Count: {count}"
        )

    conn.close()

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        f.write("\n".join(report))

    print("\n".join(report))

    print(
        f"\nReport saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    test_database()