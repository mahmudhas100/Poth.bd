import sqlite3
import json

def update_translit():
    with open('backend/data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)
        
    bn_to_en = {}
    for item in master_stops:
        bn = item['name_bn'].strip()
        en = item['name_en'].strip()
        bn_to_en[bn] = en

    print(f"Loaded {len(bn_to_en)} mappings from master_stops.json")
    print("Example for Abdullahpur:", bn_to_en.get("আব্দুল্লাহপুর"))

    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    stops = c.execute("SELECT id, name_bn, name_en FROM stops").fetchall()
    
    updated = 0
    missing = []
    
    for row in stops:
        sid, bn, current_en = row
        clean_bn = bn.strip()
        
        new_en = bn_to_en.get(clean_bn)
        
        if new_en:
            c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (new_en, sid))
            updated += 1
        else:
            missing.append(clean_bn)
            
    conn.commit()
    conn.close()
    
    print(f"Successfully updated {updated} stops.")
    print(f"Missing transliterations for {len(missing)} stops.")
    if missing:
        print("First 10 missing:", missing[:10])

if __name__ == "__main__":
    update_translit()
