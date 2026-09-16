
import sqlite3
conn = sqlite3.connect('backend/data/busvara.db')
print("Airport ID:", conn.execute("SELECT id FROM stops WHERE name_en='Airport'").fetchone()[0])
print("Rampura Bridge ID:", conn.execute("SELECT id FROM stops WHERE name_en='Rampura Bridge'").fetchone()[0])
print("Rampura TV Center ID:", conn.execute("SELECT id FROM stops WHERE name_en='Rampura TV Center'").fetchone()[0])
conn.close()
