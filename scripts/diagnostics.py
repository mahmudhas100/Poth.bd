
import sqlite3

DB_PATH = 'backend/data/busvara.db'

def audit_logical_gaps():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # 1. Check for missing fares in sequences
    # If route R has stops [A, B, C], there should be a fare for (A,B), (B,C), and (A,C)
    # Most BRTA charts only list "A to B", "A to C", etc.
    
    c.execute("SELECT DISTINCT route_id FROM route_stops")
    routes = [r[0] for r in c.fetchall()]
    
    total_missing = 0
    for rid in routes:
        c.execute("SELECT stop_id FROM route_stops WHERE route_id = ? ORDER BY stop_order", (rid,))
        stops = [r[0] for r in c.fetchall()]
        
        for i in range(len(stops)):
            for j in range(i + 1, len(stops)):
                sid1 = stops[i]
                sid2 = stops[j]
                
                c.execute("SELECT id FROM fares WHERE route_id = ? AND ((from_stop_id = ? AND to_stop_id = ?) OR (from_stop_id = ? AND to_stop_id = ?))", 
                          (rid, sid1, sid2, sid2, sid1))
                if not c.fetchone():
                    total_missing += 1
                    
    print(f"Total potential missing fare records for existing route paths: {total_missing}")
    
    conn.close()

if __name__ == "__main__":
    audit_logical_gaps()
