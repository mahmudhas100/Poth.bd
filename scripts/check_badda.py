import sqlite3

conn = sqlite3.connect('backend/data/busvara.db')
c = conn.cursor()

c.execute("SELECT * FROM stops WHERE name_en LIKE '%Badda%'")
print(c.fetchall())
conn.close()
