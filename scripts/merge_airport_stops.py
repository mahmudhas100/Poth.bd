
import sqlite3

DB_PATH = 'backend/data/busvara.db'
STAY_ID = 36 # Airport
DELETE_ID = 186 # New Airport

def merge_stops():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print(f"Merging Stop ID {DELETE_ID} into {STAY_ID}...")
    
    # 1. Update route_stops
    # Need to be careful about duplicate stops in the same route after merge, 
    # but logically a route wouldn't have both "Airport" and "New Airport" as distinct sequential stops in a way that breaks things.
    c.execute("UPDATE route_stops SET stop_id = ? WHERE stop_id = ?", (STAY_ID, DELETE_ID))
    print(f"Updated {c.rowcount} rows in route_stops.")
    
    # 2. Update fares
    # This is trickier because of the UNIQUE(route_id, from_stop_id, to_stop_id) constraint.
    
    # First, find all fares involving the DELETE_ID
    c.execute("SELECT id, route_id, from_stop_id, to_stop_id, fare_tk FROM fares WHERE from_stop_id = ? OR to_stop_id = ?", (DELETE_ID, DELETE_ID))
    affected_fares = c.fetchall()
    
    for f_id, rid, f_sid, t_sid, fare in affected_fares:
        new_f_sid = STAY_ID if f_sid == DELETE_ID else f_sid
        new_t_sid = STAY_ID if t_sid == DELETE_ID else t_sid
        
        # Check if a fare for this route/stop combo already exists
        c.execute("SELECT id FROM fares WHERE route_id = ? AND from_stop_id = ? AND to_stop_id = ? AND id != ?", (rid, new_f_sid, new_t_sid, f_id))
        exists = c.fetchone()
        
        if exists:
            # Duplicate found, just delete this one
            c.execute("DELETE FROM fares WHERE id = ?", (f_id,))
        else:
            # No duplicate, update it
            c.execute("UPDATE fares SET from_stop_id = ?, to_stop_id = ? WHERE id = ?", (new_f_sid, new_t_sid, f_id))
            
    print("Updated fares table and handled potential duplicates.")
    
    # 3. Add alias
    c.execute("INSERT INTO stop_aliases (stop_id, alias_name) VALUES (?, ?)", (STAY_ID, "New Airport"))
    print("Added 'New Airport' as alias for 'Airport'.")
    
    # 4. Delete the stop
    c.execute("DELETE FROM stops WHERE id = ?", (DELETE_ID,))
    print(f"Deleted stop ID {DELETE_ID}.")
    
    conn.commit()
    conn.close()
    print("Merge complete.")

if __name__ == "__main__":
    merge_stops()
