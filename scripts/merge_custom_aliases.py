import sqlite3

def merge_custom(merges):
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    merged = 0
    for target_en, dup_en in merges.items():
        # Find canonical ID
        c.execute("SELECT id FROM stops WHERE name_en = ?", (target_en,))
        target_res = c.fetchone()
        
        # Find dup ID
        c.execute("SELECT id FROM stops WHERE name_en = ?", (dup_en,))
        dup_res = c.fetchone()
        
        if target_res and dup_res:
            target_id = target_res[0]
            dup_id = dup_res[0]
            
            # Update route_stops
            c.execute("SELECT id FROM route_stops WHERE stop_id = ?", (dup_id,))
            for (rs_id,) in c.fetchall():
                try:
                    c.execute("UPDATE route_stops SET stop_id = ? WHERE id = ?", (target_id, rs_id))
                except sqlite3.IntegrityError:
                    c.execute("DELETE FROM route_stops WHERE id = ?", (rs_id,))
            
            # Update fares
            c.execute("SELECT id FROM fares WHERE from_stop_id = ?", (dup_id,))
            for (f_id,) in c.fetchall():
                try:
                    c.execute("UPDATE fares SET from_stop_id = ? WHERE id = ?", (target_id, f_id))
                except sqlite3.IntegrityError:
                    c.execute("DELETE FROM fares WHERE id = ?", (f_id,))
                    
            c.execute("SELECT id FROM fares WHERE to_stop_id = ?", (dup_id,))
            for (f_id,) in c.fetchall():
                try:
                    c.execute("UPDATE fares SET to_stop_id = ? WHERE id = ?", (target_id, f_id))
                except sqlite3.IntegrityError:
                    c.execute("DELETE FROM fares WHERE id = ?", (f_id,))
            
            # Optional: Keep the duplicate name as a formal alias in stop_aliases
            # so the fuzzy search still catches it easily without needing to keep the physical stop
            c.execute("INSERT OR IGNORE INTO stop_aliases (stop_id, alias_name) VALUES (?, ?)", (target_id, dup_en))
            
            # Delete duplicate
            c.execute("DELETE FROM stops WHERE id = ?", (dup_id,))
            merged += 1
            print(f"Merged '{dup_en}' into '{target_en}'")
            
    conn.commit()
    conn.close()
    print(f"Merged {merged} custom aliases.")

if __name__ == "__main__":
    merges = {
        "Airport": "New Airport",
        "Mirpur-1": "Mirpur (1)",
        "Mirpur-10": "Mirpur (10)",
        "Mirpur-14": "Mirpur (14)",
        "Gulistan": "Gulistan More",
        "Badda Link Road": "Badda Link Road/Moddho Badda"
    }
    merge_custom(merges)
