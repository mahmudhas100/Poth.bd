
import sqlite3
from collections import defaultdict

DB_PATH = 'backend/data/busvara.db'

def merge_identical_stops():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # 1. Find all stops grouped by name
    c.execute("SELECT id, name_en FROM stops")
    name_to_ids = defaultdict(list)
    for r in c.fetchall():
        name_to_ids[r['name_en']].append(r['id'])
        
    # 2. Process groups with more than one ID
    for name, ids in name_to_ids.items():
        if len(ids) > 1:
            stay_id = ids[0]
            delete_ids = ids[1:]
            
            print(f"Merging {name}: keeping {stay_id}, deleting {delete_ids}")
            
            for del_id in delete_ids:
                # Update route_stops
                c.execute("UPDATE route_stops SET stop_id = ? WHERE stop_id = ?", (stay_id, del_id))
                
                # Update fares (handle duplicates)
                c.execute("SELECT id, route_id, from_stop_id, to_stop_id FROM fares WHERE from_stop_id = ? OR to_stop_id = ?", (del_id, del_id))
                affected_fares = [dict(r) for r in c.fetchall()]
                
                for f in affected_fares:
                    new_f_sid = stay_id if f['from_stop_id'] == del_id else f['from_stop_id']
                    new_t_sid = stay_id if f['to_stop_id'] == del_id else f['to_stop_id']
                    
                    # Check for existing
                    c.execute("SELECT id FROM fares WHERE route_id = ? AND from_stop_id = ? AND to_stop_id = ? AND id != ?", 
                              (f['route_id'], new_f_sid, new_t_sid, f['id']))
                    exists = c.fetchone()
                    
                    if exists:
                        c.execute("DELETE FROM fares WHERE id = ?", (f['id'],))
                    else:
                        c.execute("UPDATE fares SET from_stop_id = ?, to_stop_id = ? WHERE id = ?", (new_f_sid, new_t_sid, f['id']))
                
                # Add to aliases if not already there
                c.execute("INSERT OR IGNORE INTO stop_aliases (stop_id, alias_name) VALUES (?, ?)", (stay_id, name))
                
                # Delete stop
                c.execute("DELETE FROM stops WHERE id = ?", (del_id,))
                
    conn.commit()
    conn.close()
    print("Cleanup complete.")

if __name__ == "__main__":
    merge_identical_stops()
