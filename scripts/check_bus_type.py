
import sqlite3
conn = sqlite3.connect('data/busvara.db')
c = conn.cursor()
c.execute("SELECT route_name FROM routes WHERE route_name LIKE '%মিনিবাস%'")
minibuses = c.fetchall()
c.execute("SELECT route_name FROM routes WHERE route_name NOT LIKE '%মিনিবাস%'")
buses = c.fetchall()
print(f"Minibus routes: {len(minibuses)}")
print(f"Bus routes: {len(buses)}")
conn.close()
