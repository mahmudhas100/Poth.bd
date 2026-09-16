import sqlite3
import json

conn = sqlite3.connect('backend/data/busvara.db')
c = conn.cursor()

c.execute("SELECT id, name_en, name_bn FROM stops ORDER BY name_en")
stops = c.fetchall()
conn.close()

with open("backend/data/all_stops_review.json", "w", encoding="utf-8") as f:
    json.dump([{"id": s[0], "name_en": s[1], "name_bn": s[2]} for s in stops], f, indent=4, ensure_ascii=False)

print("Exported to all_stops_review.json")
