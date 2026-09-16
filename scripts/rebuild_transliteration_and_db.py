import os
import json
import sqlite3
import re

TEMP_DIR = "backend/data/raw_json"
DB_PATH = "backend/data/busvara.db"

# Minimal manual transliteration for any Bengali characters
MANUAL_MAP = {
    "এয়ারপোর্ট": "Airport",
    "শ্যামলী": "Shyamoli",
    "আজিমপুর": "Azimpur",
    "ইডেন কলেজ": "Eden College",
    "ইসিবি মোড়": "ECB More",
    "গুলিস্তান": "Gulistan",
    "মতিঝিল": "Motijheel",
    "উত্তরা": "Uttara",
    "গাবতলী": "Gabtoli",
    "সাভার": "Savar",
    "মিরপুর": "Mirpur"
}

def basic_translit(bn_text):
    if bn_text in MANUAL_MAP:
        return MANUAL_MAP[bn_text]
    # Very basic fallback for testing
    return bn_text.replace(" ", "_").upper()

def rebuild():
    print("Connecting to DB...")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    print("Clearing tables...")
    cur.execute("DELETE FROM fares")
    cur.execute("DELETE FROM route_stops")
    cur.execute("DELETE FROM routes")
    # For a full rebuild we'd also clear stops, but let's keep it safe and just append new ones if needed, or clear.
    cur.execute("DELETE FROM stops")
    
    print("Processing extracted JSON files...")
    files = [f for f in os.listdir(TEMP_DIR) if f.endswith(".json")]
    
    # Process files in order. If 'fixed' is in the filename, process it last to overwrite or we can just track inserted routes.
    # To handle duplicates, we track which route names we have already inserted.
    files.sort(key=lambda x: ("fixed" in x, x)) # prioritize fixed files by processing them last if we did UPSERT, but we do INSERT so let's just track names.
    
    stop_id_map = {}
    inserted_routes = set()
    
    for f in files:
        with open(os.path.join(TEMP_DIR, f), 'r', encoding='utf-8') as file:
            try:
                data_list = json.load(file)
            except:
                continue
            
            for data in data_list:
                if 'route_name' not in data:
                    continue
                route_name = data['route_name']
                if route_name in inserted_routes:
                    continue
                inserted_routes.add(route_name)
                source = data.get('source_file', f)
                source_page = data.get('source_page', 1)
                
                cur.execute("INSERT INTO routes (route_name, source_file, source_page) VALUES (?, ?, ?)",
                            (route_name, source, source_page))
                route_id = cur.lastrowid
                
                # Insert stops
                stops = data.get('stops', [])
                distances = data.get('distances_km', [])
                for i, stop_item in enumerate(stops):
                    if isinstance(stop_item, dict):
                        stop_bn = stop_item.get('name', 'Unknown')
                        dist = stop_item.get('distance', 0.0)
                    else:
                        stop_bn = stop_item
                        dist = distances[i] if i < len(distances) else 0.0
                        
                    if stop_bn not in stop_id_map:
                        stop_en = basic_translit(stop_bn)
                        cur.execute("INSERT INTO stops (name_bn, name_en) VALUES (?, ?)", (stop_bn, stop_en))
                        stop_id_map[stop_bn] = cur.lastrowid
                    
                    s_id = stop_id_map[stop_bn]
                    cur.execute("INSERT INTO route_stops (route_id, stop_id, stop_order, distance_km) VALUES (?, ?, ?, ?)",
                                (route_id, s_id, i+1, dist))
                
                # Insert fares
                fares = data.get('fares', [])
                for fare_info in fares:
                    f_from = fare_info.get('from')
                    f_to = fare_info.get('to')
                    f_amt = fare_info.get('fare', 0)
                    
                    if f_from in stop_id_map and f_to in stop_id_map:
                        cur.execute("""INSERT OR IGNORE INTO fares (route_id, from_stop_id, to_stop_id, fare_tk) 
                                       VALUES (?, ?, ?, ?)""", 
                                    (route_id, stop_id_map[f_from], stop_id_map[f_to], f_amt))
                        
    con.commit()
    con.close()
    print("Database successfully rebuilt from fresh JSON data!")

if __name__ == "__main__":
    rebuild()
