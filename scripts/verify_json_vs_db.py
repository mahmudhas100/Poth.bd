import json
import sqlite3
import glob
import os

DB_PATH = 'backend/data/busvara.db'

def check_mismatches():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    json_files = glob.glob('patch_*.json')
    
    total_checked = 0
    mismatches = 0
    
    # Pre-fetch routes to ID map
    c.execute("SELECT id, route_name FROM routes")
    route_map = {row['route_name'].strip(): row['id'] for row in c.fetchall()}

    for fpath in json_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for route_data in data:
            r_name = route_data['route_name'].strip()
            if r_name not in route_map:
                continue
                
            route_id = route_map[r_name]
            
            # Fetch route stops in order
            c.execute("SELECT stop_id FROM route_stops WHERE route_id = ? ORDER BY stop_order", (route_id,))
            db_stops = [row['stop_id'] for row in c.fetchall()]
            
            # Ensure number of stops matches
            if 'fares' in route_data:
                fare_matrix = route_data['fares']
            elif 'fare_matrix' in route_data:
                fare_matrix = route_data['fare_matrix']
            else:
                continue
                
            if len(db_stops) != len(fare_matrix):
                continue
                
            # Check matrix
            for i in range(len(db_stops)):
                for j in range(len(db_stops)):
                    if i == j: continue
                    
                    s1 = db_stops[i]
                    s2 = db_stops[j]
                    
                    try:
                        expected_fare = int(fare_matrix[i][j])
                    except (ValueError, TypeError):
                        continue # Skip non-integer values if any
                    
                    if expected_fare == 0:
                        continue
                        
                    # Get DB fare
                    c.execute("SELECT fare_tk FROM fares WHERE route_id = ? AND from_stop_id = ? AND to_stop_id = ?", (route_id, s1, s2))
                    db_res = c.fetchone()
                    if db_res:
                        db_fare = db_res['fare_tk']
                        total_checked += 1
                        if db_fare != expected_fare:
                            mismatches += 1

    conn.close()
    print(f"Total checked: {total_checked}")
    print(f"Mismatches: {mismatches}")

if __name__ == '__main__':
    check_mismatches()
