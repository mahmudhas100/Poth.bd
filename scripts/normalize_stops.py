
import sqlite3

DB_PATH = r"backend/data/busvara.db"

def normalize_stops():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Find English names that appear more than once
    c.execute("SELECT name_en, COUNT(*) as count FROM stops GROUP BY name_en HAVING count > 1")
    duplicates = c.fetchall()

    total_merged = 0

    for name_en, count in duplicates:
        # Get all IDs for this English name
        c.execute("SELECT id, name_bn FROM stops WHERE name_en = ? ORDER BY id ASC", (name_en,))
        rows = c.fetchall()
        
        master_id = rows[0][0]
        master_bn = rows[0][1]
        duplicate_ids = [r[0] for r in rows[1:]]

        for dup_id in duplicate_ids:
            # Re-map route_stops
            c.execute("UPDATE OR IGNORE route_stops SET stop_id = ? WHERE stop_id = ?", (master_id, dup_id))
            c.execute("DELETE FROM route_stops WHERE stop_id = ?", (dup_id,)) # Delete rows that failed IGNORE (redundant connections)

            # Re-map fares (From side)
            c.execute("UPDATE OR IGNORE fares SET from_stop_id = ? WHERE from_stop_id = ?", (master_id, dup_id))
            # Re-map fares (To side)
            c.execute("UPDATE OR IGNORE fares SET to_stop_id = ? WHERE to_stop_id = ?", (master_id, dup_id))
            
            # Delete remaining fares for the duplicate stop (failed updates due to uniqueness)
            c.execute("DELETE FROM fares WHERE from_stop_id = ? OR to_stop_id = ?", (dup_id, dup_id))

            # Delete the duplicate stop itself
            c.execute("DELETE FROM stops WHERE id = ?", (dup_id,))
            total_merged += 1

    conn.commit()
    conn.close()
    print(f"Normalization Complete. Merged {total_merged} duplicate stops.")

if __name__ == "__main__":
    normalize_stops()
