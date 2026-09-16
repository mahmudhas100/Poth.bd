import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "backend", "data", "busvara.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Get all fares and join with route_stops to get distances
query = """
SELECT 
    f.route_id, r.route_name,
    f.from_stop_id, rs1.distance_km as from_dist, s1.name_en as from_name,
    f.to_stop_id, rs2.distance_km as to_dist, s2.name_en as to_name,
    f.fare_tk
FROM fares f
JOIN routes r ON f.route_id = r.id
JOIN route_stops rs1 ON f.route_id = rs1.route_id AND f.from_stop_id = rs1.stop_id
JOIN route_stops rs2 ON f.route_id = rs2.route_id AND f.to_stop_id = rs2.stop_id
JOIN stops s1 ON f.from_stop_id = s1.id
JOIN stops s2 ON f.to_stop_id = s2.id
"""

c.execute(query)
rows = c.fetchall()

RATE_PER_KM = 2.53
MIN_FARE = 10

total_segments = len(rows)
perfect_matches = 0
within_1_tk = 0
within_2_tk = 0
major_deviations = 0

deviation_examples = []

for row in rows:
    distance = abs(row['to_dist'] - row['from_dist'])
    # Standard formula
    expected_fare_raw = distance * RATE_PER_KM
    expected_fare = max(MIN_FARE, round(expected_fare_raw))
    
    actual_fare = row['fare_tk']
    
    diff = abs(expected_fare - actual_fare)
    
    if diff == 0:
        perfect_matches += 1
        within_1_tk += 1
        within_2_tk += 1
    elif diff == 1:
        within_1_tk += 1
        within_2_tk += 1
    elif diff == 2:
        within_2_tk += 1
    else:
        major_deviations += 1
        if len(deviation_examples) < 10:
            deviation_examples.append(f"Route: {row['route_name']} | {row['from_name']} -> {row['to_name']} | Dist: {distance:.2f}km | Expected: {expected_fare} TK | Actual: {actual_fare} TK")

print(f"Total fare segments analyzed: {total_segments}")
print(f"Perfect matches (Exact to {RATE_PER_KM} TK/km + rounding): {perfect_matches} ({perfect_matches/total_segments*100:.2f}%)")
print(f"Within 1 TK variance: {within_1_tk} ({within_1_tk/total_segments*100:.2f}%)")
print(f"Within 2 TK variance: {within_2_tk} ({within_2_tk/total_segments*100:.2f}%)")
print(f"Major deviations (>2 TK): {major_deviations} ({major_deviations/total_segments*100:.2f}%)")

if deviation_examples:
    print("\nExamples of major deviations (possibly tolls, flyovers, or entry errors):")
    for ex in deviation_examples:
        print(ex)
