
import sqlite3
conn = sqlite3.connect('data/busvara.db')
c = conn.cursor()
c.execute("SELECT name_en FROM stops WHERE name_en LIKE '%Shapla%'")
print(c.fetchall())
conn.close()
