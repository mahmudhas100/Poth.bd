import sqlite3

conn = sqlite3.connect('backend/data/busvara.db')
c = conn.cursor()

c.execute("SELECT id, name_en, name_bn FROM stops WHERE name_en LIKE '%airport%' COLLATE NOCASE")
res = c.fetchall()
for r in res:
    print(r)

c.execute("SELECT * FROM stop_aliases WHERE alias_name LIKE '%airport%' COLLATE NOCASE")
aliases = c.fetchall()
print("\nAliases:")
for a in aliases:
    print(a)

conn.close()
