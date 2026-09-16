
import sqlite3
import re

DB_PATH = r"backend/data/busvara.db"

def clean_bn(name):
    if not name: return ""
    # Standardize common Bengali character variations
    name = name.replace('য়', 'য').replace('ড়', 'র').replace('ঢ়', 'র').replace('ৎ', 'ত')
    name = re.sub(r'[\s\(\)]', '', name) # Remove spaces and brackets for comparison
    return name

def final_polish():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Get all stops
    c.execute("SELECT id, name_en, name_bn FROM stops")
    stops = c.fetchall()
    
    seen_bn = {} # { cleaned_bn: master_id }
    merged = 0
    
    for sid, name_en, name_bn in stops:
        c_bn = clean_bn(name_bn)
        
        if c_bn in seen_bn:
            master_id = seen_bn[c_bn]
            
            # Merge this duplicate (sid) into master_id
            c.execute("UPDATE OR IGNORE route_stops SET stop_id = ? WHERE stop_id = ?", (master_id, sid))
            c.execute("DELETE FROM route_stops WHERE stop_id = ?", (sid,))
            c.execute("UPDATE OR IGNORE fares SET from_stop_id = ? WHERE from_stop_id = ?", (master_id, sid))
            c.execute("UPDATE OR IGNORE fares SET to_stop_id = ? WHERE to_stop_id = ?", (master_id, sid))
            c.execute("DELETE FROM fares WHERE from_stop_id = ? OR to_stop_id = ?", (sid, sid))
            c.execute("DELETE FROM stops WHERE id = ?", (sid,))
            merged += 1
        else:
            seen_bn[c_bn] = sid
            # Title Case Polish for English
            new_en = name_en.strip().title()
            c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (new_en, sid))

    conn.commit()
    conn.close()
    print(f"Final Polish Complete. Merged {merged} fuzzy duplicates.")

if __name__ == "__main__":
    final_polish()
