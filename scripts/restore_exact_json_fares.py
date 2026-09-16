import json
import sqlite3
import glob
import os
import difflib

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "backend", "data", "busvara.db")

def resolve_stop_id(name, route_stops, c):
    name_clean = name.strip()
    
    # 1. Exact match in route's stops
    for st_id, st_name_bn in route_stops:
        if st_name_bn == name_clean:
            return st_id
            
    # 2. Exact match in aliases
    alias_map = {}
    for st_id, _ in route_stops:
        c.execute("SELECT alias_name FROM stop_aliases WHERE stop_id = ?", (st_id,))
        for row in c.fetchall():
            alias_map[row['alias_name']] = st_id
            
    if name_clean in alias_map:
        return alias_map[name_clean]
        
    # 3. Fuzzy match among route stops
    stop_names = [s[1] for s in route_stops]
    matches = difflib.get_close_matches(name_clean, stop_names, n=1, cutoff=0.7)
    if matches:
        match_name = matches[0]
        for st_id, st_name_bn in route_stops:
            if st_name_bn == match_name:
                return st_id
                
    # 4. Fuzzy match among aliases
    matches = difflib.get_close_matches(name_clean, list(alias_map.keys()), n=1, cutoff=0.7)
    if matches:
        return alias_map[matches[0]]
        
    return None

def migrate_exact_fares():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    json_files = glob.glob(os.path.join(os.path.dirname(__file__), "..", "patch_*.json"))
    
    total_updated = 0
    missing_stops = 0

    c.execute("SELECT id, route_name FROM routes")
    route_map = {row['route_name'].strip().lower(): row['id'] for row in c.fetchall()}

    for fpath in json_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
                
        for route_data in data:
            r_name = route_data.get('route_name', '').strip()
            route_id = None
            if r_name.lower() in route_map:
                route_id = route_map[r_name.lower()]
            else:
                for db_name, db_id in route_map.items():
                    if db_name in r_name.lower() or r_name.lower() in db_name:
                        route_id = db_id
                        break
            
            if not route_id:
                continue
                
            c.execute("""
                SELECT s.id, s.name_bn 
                FROM route_stops rs 
                JOIN stops s ON rs.stop_id = s.id 
                WHERE rs.route_id = ?
            """, (route_id,))
            route_stops = [(row['id'], row['name_bn']) for row in c.fetchall()]
            
            fares = route_data.get('fares', [])
            if not fares and 'fare_matrix' in route_data:
                 fares = []
                 stops_list = route_data.get('stops', [])
                 matrix = route_data['fare_matrix']
                 for i in range(len(stops_list)):
                     for j in range(len(stops_list)):
                         if i != j and matrix[i][j] > 0:
                             fares.append({'from': stops_list[i], 'to': stops_list[j], 'fare': matrix[i][j]})

            for f_entry in fares:
                from_name = f_entry.get('from')
                to_name = f_entry.get('to')
                fare_val = f_entry.get('fare')
                
                if not from_name or not to_name or not fare_val:
                    continue
                    
                try:
                    fare_val = int(fare_val)
                except ValueError:
                    continue
                    
                from_id = resolve_stop_id(from_name, route_stops, c)
                to_id = resolve_stop_id(to_name, route_stops, c)
                
                if from_id and to_id:
                    c.execute("""
                        UPDATE fares 
                        SET fare_tk = ? 
                        WHERE route_id = ? AND from_stop_id = ? AND to_stop_id = ?
                    """, (fare_val, route_id, from_id, to_id))
                    
                    c.execute("""
                        UPDATE fares 
                        SET fare_tk = ? 
                        WHERE route_id = ? AND from_stop_id = ? AND to_stop_id = ?
                    """, (fare_val, route_id, to_id, from_id))
                    
                    total_updated += c.rowcount
                else:
                    missing_stops += 1

    conn.commit()
    conn.close()
    print(f"Update complete. Total fare rows updated: {total_updated}")
    if missing_stops > 0:
        print(f"Warning: Could not resolve {missing_stops} stop references in the JSON.")

if __name__ == '__main__':
    migrate_exact_fares()
