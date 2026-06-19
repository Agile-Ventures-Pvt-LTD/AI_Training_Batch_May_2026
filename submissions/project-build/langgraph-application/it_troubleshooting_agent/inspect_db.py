import sqlite3
from pathlib import Path
p=Path('data/database/it_support.db')
print('DB exists:', p.exists())
if not p.exists():
    raise SystemExit(1)
conn=sqlite3.connect(str(p))
cur=conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables=[r[0] for r in cur.fetchall()]
print('Tables:', tables)
for t in tables:
    try:
        cur.execute(f'SELECT COUNT(*) FROM {t}')
        cnt=cur.fetchone()[0]
    except Exception as e:
        cnt=str(e)
    print(f'Table {t}: rows={cnt}')
    try:
        cur.execute(f'SELECT * FROM {t} LIMIT 3')
        rows=cur.fetchall()
        print('Sample rows:', rows)
    except Exception as e:
        print('Sample rows: error', e)
conn.close()
