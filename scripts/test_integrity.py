
import sqlite3

DB_PATH = r"backend/data/busvara.db"

def run_consistency_test():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get a random sample of 50 fares
    c.execute("""
        SELECT f.fare_tk, rs1.distance_km as d1, rs2.distance_km as d2, 
               s1.name_bn as from_stop, s2.name_bn as to_stop, r.route_name
        FROM fares f
        JOIN route_stops rs1 ON f.route_id = rs1.route_id AND f.from_stop_id = rs1.stop_id
        JOIN route_stops rs2 ON f.route_id = rs2.route_id AND f.to_stop_id = rs2.stop_id
        JOIN stops s1 ON f.from_stop_id = s1.id
        JOIN stops s2 ON f.to_stop_id = s2.id
        JOIN routes r ON f.route_id = r.id
        ORDER BY RANDOM() LIMIT 50
    """)
    samples = c.fetchall()

    pass_count = 0
    fail_count = 0

    print(f"{'Route':<30} | {'From' :<15} | {'To':<15} | {'DB Fare':<5} | {'Calc Fare':<5} | {'Status'}")
    print("-" * 100)

    for s in samples:
        dist = abs(s['d2'] - s['d1'])
        calc_fare = max(10, round(dist * 2.53))
        
        status = "✅ PASS" if abs(s['fare_tk'] - calc_fare) <= 1 else "❌ FAIL"
        
        if status == "✅ PASS": pass_count += 1
        else: fail_count += 1
        
        print(f"{s['route_name'][:30]:<30} | {s['from_stop'][:15]:<15} | {s['to_stop'][:15]:<15} | {s['fare_tk']:<7} | {calc_fare:<9} | {status}")

    conn.close()
    print("-" * 100)
    print(f"Total Samples: 50 | Passed: {pass_count} | Failed: {fail_count}")

if __name__ == "__main__":
    run_consistency_test()
