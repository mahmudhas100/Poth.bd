import sqlite3
import os

def final_checks():
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    issues = []

    # Check for empty stop names
    c.execute("SELECT id FROM stops WHERE name_en IS NULL OR name_en = '' OR name_bn IS NULL OR name_bn = ''")
    empty_stops = c.fetchall()
    if empty_stops:
        issues.append(f"Found {len(empty_stops)} stops with empty names.")

    # Check for zero or negative fares
    c.execute("SELECT count(*) FROM fares WHERE fare_tk <= 0")
    bad_fares = c.fetchone()[0]
    if bad_fares > 0:
        issues.append(f"Found {bad_fares} fares with 0 or negative amounts.")

    # Check for weirdly large fares (e.g. OCR error reading 10 as 100)
    c.execute("SELECT id, route_id, from_stop_id, to_stop_id, fare_tk FROM fares WHERE fare_tk > 150")
    large_fares = c.fetchall()
    if large_fares:
        issues.append(f"Found {len(large_fares)} fares > 150 TK (might be OCR errors).")

    # Check for duplicate route names
    c.execute("SELECT route_name, count(*) FROM routes GROUP BY route_name HAVING count(*) > 1")
    dup_routes = c.fetchall()
    if dup_routes:
        issues.append(f"Found {len(dup_routes)} duplicate route names.")

    conn.close()

    if not issues:
        print("Database looks completely clean in these final checks.")
    else:
        for i in issues:
            print("- " + i)

if __name__ == "__main__":
    final_checks()
