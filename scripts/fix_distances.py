import sqlite3

def fix_distances():
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    c.execute("SELECT id FROM routes")
    r_ids = [r[0] for r in c.fetchall()]
    
    fixes = 0
    for r_id in r_ids:
        c.execute("SELECT id, stop_order, distance_km FROM route_stops WHERE route_id=? ORDER BY stop_order", (r_id,))
        stops = c.fetchall()
        
        prev_dist = -1.0
        for rs_id, order, dist in stops:
            if dist < prev_dist:
                # Fix distance to be strictly increasing
                # We'll just add 0.5km to the previous distance as a safe patch
                new_dist = prev_dist + 0.5
                c.execute("UPDATE route_stops SET distance_km=? WHERE id=?", (new_dist, rs_id))
                fixes += 1
                prev_dist = new_dist
            else:
                prev_dist = dist
                
    conn.commit()
    conn.close()
    print(f"Fixed {fixes} non-increasing distance anomalies in the database.")

if __name__ == "__main__":
    fix_distances()
