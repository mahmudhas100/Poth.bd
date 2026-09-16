
import sqlite3
conn = sqlite3.connect('backend/data/busvara.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM stops WHERE name_en LIKE '%Airport%'")
for r in c.fetchall():
    print(dict(r))
conn.close()
