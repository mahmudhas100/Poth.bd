import sqlite3
import json

conn = sqlite3.connect('backend/data/busvara.db')
c = conn.cursor()

# Search routes
query = """
SELECT id, route_name 
FROM routes 
WHERE route_name LIKE '%elevated%' 
   OR route_name LIKE '%expressway%'
   OR route_name LIKE '%এলিভেটেড%' 
   OR route_name LIKE '%এক্সপ্রেসওয়ে%'
   OR route_name LIKE '%এক্সপ্রেসওয়ে%'
"""
c.execute(query)
routes = c.fetchall()

print("Routes:")
for r in routes:
    print(r)

# Search stops
query_stops = """
SELECT id, name_en, name_bn
FROM stops 
WHERE name_en LIKE '%elevated%' 
   OR name_en LIKE '%expressway%'
   OR name_bn LIKE '%এলিভেটেড%' 
   OR name_bn LIKE '%এক্সপ্রেসওয়ে%'
   OR name_bn LIKE '%এক্সপ্রেসওয়ে%'
"""
c.execute(query_stops)
stops = c.fetchall()

print("\nStops:")
for s in stops:
    print(s)

conn.close()
