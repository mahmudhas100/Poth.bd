import sqlite3
con = sqlite3.connect('backend/data/busvara.db')
cursor = con.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
for row in cursor.fetchall():
    if row[0]:
        print(row[0])
con.close()
