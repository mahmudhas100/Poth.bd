
import sqlite3
import math

DB_PATH = 'data/busvara.db'

def migrate_fares():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Rates effective April 23, 2026
    RATE_BUS = 2.53
    RATE_MINIBUS = 2.43
    MIN_FARE_BUS = 10
    MIN_FARE_MINIBUS = 8

    print("Starting migration to 2026 BRTA rates...")

    # 1. Get all routes
    c.execute("SELECT id, route_name FROM routes")
    routes = c.fetchall()

    total_updated = 0

    for route in routes:
        route_id = route['id']
        name = route['route_name']
        
        # Determine rate
        is_minibus = "মিনিবাস" in name
        rate = RATE_MINIBUS if is_minibus else RATE_BUS
        min_f = MIN_FARE_MINIBUS if is_minibus else MIN_FARE_BUS
        
        # 2. Get all stops and distances for this route
        c.execute("SELECT stop_id, distance_km FROM route_stops WHERE route_id = ? ORDER BY stop_order", (route_id,))
        stops = c.fetchall()
        
        # 3. Update every fare pair for this route
        # We match based on from_stop_id, to_stop_id, and route_id
        for i in range(len(stops)):
            for j in range(len(stops)):
                if i == j: continue
                
                s1 = stops[i]
                s2 = stops[j]
                
                distance = abs(s2['distance_km'] - s1['distance_km'])
                
                # Formula: round up if >= 0.5
                new_fare = math.floor(distance * rate + 0.5)
                if new_fare < min_f:
                    new_fare = min_f
                
                # Update DB
                c.execute("""
                    UPDATE fares 
                    SET fare_tk = ? 
                    WHERE route_id = ? AND from_stop_id = ? AND to_stop_id = ?
                """, (new_fare, route_id, s1['stop_id'], s2['stop_id']))
                total_updated += c.rowcount

    conn.commit()
    conn.close()
    print(f"Migration complete! Recalculated {total_updated} fare entries across {len(routes)} routes.")

if __name__ == "__main__":
    migrate_fares()
