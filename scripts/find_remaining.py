
import sqlite3
from rapidfuzz import process, fuzz

DB_PATH = 'backend/data/busvara.db'

def find_potential_duplicates():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT id, name_en FROM stops")
    stops = [dict(r) for r in c.fetchall()]
    
    found = []
    checked_ids = set()
    
    for s1 in stops:
        checked_ids.add(s1['id'])
        for s2 in stops:
            if s2['id'] in checked_ids:
                continue
            
            score = fuzz.ratio(s1['name_en'], s2['name_en'])
            if score > 85: # High similarity threshold
                found.append((s1['name_en'], s2['name_en'], score))
                
    conn.close()
    return found

if __name__ == "__main__":
    dupes = find_potential_duplicates()
    for d in dupes:
        print(f"Similarity {d[2]}%: {d[0]} <-> {d[1]}")
