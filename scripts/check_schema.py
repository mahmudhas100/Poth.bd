
import sqlite3
conn = sqlite3.connect('backend/data/busvara.db')
for r in conn.execute("SELECT sql FROM sqlite_master WHERE type='table'"):
    print(r[0])
conn.close()
