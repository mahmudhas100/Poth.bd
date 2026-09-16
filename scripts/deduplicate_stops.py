import sqlite3

def deduplicate():
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    # 1. Group stops by name_en
    groups = {}
    stops = c.execute("SELECT id, name_en FROM stops").fetchall()
    for sid, name_en in stops:
        groups.setdefault(name_en, []).append(sid)
        
    merged_groups = 0
    deleted_stops = 0
    deleted_fares = 0
    deleted_rs = 0
    
    for name_en, sids in groups.items():
        if len(sids) > 1:
            sids.sort()
            canonical_id = sids[0]
            duplicate_ids = sids[1:]
            
            for dup_id in duplicate_ids:
                # Update route_stops
                c.execute("SELECT id, route_id FROM route_stops WHERE stop_id = ?", (dup_id,))
                for rs_id, route_id in c.fetchall():
                    try:
                        c.execute("UPDATE route_stops SET stop_id = ? WHERE id = ?", (canonical_id, rs_id))
                    except sqlite3.IntegrityError:
                        c.execute("DELETE FROM route_stops WHERE id = ?", (rs_id,))
                        deleted_rs += 1
                
                # Update fares
                # We have to do this carefully. Updating from_stop_id
                c.execute("SELECT id FROM fares WHERE from_stop_id = ?", (dup_id,))
                for (f_id,) in c.fetchall():
                    try:
                        c.execute("UPDATE fares SET from_stop_id = ? WHERE id = ?", (canonical_id, f_id))
                    except sqlite3.IntegrityError:
                        c.execute("DELETE FROM fares WHERE id = ?", (f_id,))
                        deleted_fares += 1
                        
                # Updating to_stop_id
                c.execute("SELECT id FROM fares WHERE to_stop_id = ?", (dup_id,))
                for (f_id,) in c.fetchall():
                    try:
                        c.execute("UPDATE fares SET to_stop_id = ? WHERE id = ?", (canonical_id, f_id))
                    except sqlite3.IntegrityError:
                        c.execute("DELETE FROM fares WHERE id = ?", (f_id,))
                        deleted_fares += 1
                
                # Delete duplicate stop
                c.execute("DELETE FROM stops WHERE id = ?", (dup_id,))
                deleted_stops += 1
            merged_groups += 1
            
    conn.commit()
    conn.close()
    
    print(f"Deduplication complete. Merged {merged_groups} groups (based on name_en).")
    print(f"Deleted {deleted_stops} duplicate stops.")
    print(f"Deleted {deleted_rs} duplicate route_stops entries.")
    print(f"Deleted {deleted_fares} duplicate fare entries.")

if __name__ == "__main__":
    deduplicate()
