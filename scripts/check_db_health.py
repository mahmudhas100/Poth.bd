import sqlite3

def check_inconsistencies():
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    issues = []

    # 1. Orphaned stops
    c.execute("""
        SELECT id, name_en FROM stops 
        WHERE id NOT IN (SELECT stop_id FROM route_stops)
        AND id NOT IN (SELECT from_stop_id FROM fares)
        AND id NOT IN (SELECT to_stop_id FROM fares)
    """)
    orphans = c.fetchall()
    if orphans:
        issues.append(f"Found {len(orphans)} orphaned stops (not in any route or fare).")

    # 2. Invalid routes (less than 2 stops)
    c.execute("""
        SELECT route_id, COUNT(stop_id) as stop_count 
        FROM route_stops 
        GROUP BY route_id 
        HAVING stop_count < 2
    """)
    invalid_routes = c.fetchall()
    if invalid_routes:
        issues.append(f"Found {len(invalid_routes)} routes with fewer than 2 stops.")

    # 3. Missing fares constraints
    c.execute("""
        SELECT count(*) FROM fares 
        WHERE from_stop_id NOT IN (SELECT id FROM stops) 
           OR to_stop_id NOT IN (SELECT id FROM stops)
    """)
    bad_fares = c.fetchone()[0]
    if bad_fares > 0:
        issues.append(f"Found {bad_fares} fares pointing to non-existent stops.")

    # 4. Out of order distances
    c.execute("""
        SELECT route_id 
        FROM route_stops 
        GROUP BY route_id
    """)
    all_routes = [r[0] for r in c.fetchall()]
    
    bad_distances = 0
    for r_id in all_routes:
        c.execute("SELECT stop_order, distance_km FROM route_stops WHERE route_id=? ORDER BY stop_order", (r_id,))
        stops = c.fetchall()
        prev_dist = -1.0
        for order, dist in stops:
            if dist < prev_dist:
                bad_distances += 1
                break # Only count route once
            prev_dist = dist
            
    if bad_distances > 0:
        issues.append(f"Found {bad_distances} routes with non-increasing distances.")

    # 5. Missing route definitions
    c.execute("""
        SELECT count(DISTINCT route_id) FROM route_stops 
        WHERE route_id NOT IN (SELECT id FROM routes)
    """)
    bad_route_defs = c.fetchone()[0]
    if bad_route_defs > 0:
        issues.append(f"Found {bad_route_defs} route_stops pointing to non-existent route IDs.")

    if not issues:
        print("No major inconsistencies found! The database looks healthy.")
    else:
        print("Found the following inconsistencies:")
        for issue in issues:
            print("- " + issue)

    conn.close()

if __name__ == "__main__":
    check_inconsistencies()
