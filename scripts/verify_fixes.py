import sqlite3, json, sys, os, re

DB_PATH = r"backend/data/busvara.db"

def transliterate_bn_to_en(text):
    mapping = {
        'ক': 'K', 'খ': 'Kh', 'গ': 'G', 'ঘ': 'Gh', 'ঙ': 'Ng',
        'চ': 'Ch', 'ছ': 'Chh', 'জ': 'J', 'ঝ': 'Jh', 'ঞ': 'N',
        'ট': 'T', 'ঠ': 'Th', 'ড': 'D', 'ঢ': 'Dh', 'ণ': 'N',
        'ত': 'T', 'থ': 'Th', 'দ': 'D', 'ধ': 'Dh', 'ন': 'N',
        'প': 'P', 'ফ': 'F', 'ব': 'B', 'ভ': 'Bh', 'ম': 'M',
        'য': 'J', 'র': 'R', 'ল': 'L', 'শ': 'Sh', 'ষ': 'Sh', 'স': 'S', 'হ': 'H',
        'ড়': 'R', 'ঢ়': 'Rh', 'য়': 'Y', 'ৎ': 'T', 'ং': 'Ng', 'ঃ': 'H', 'ঁ': 'N',
        'অ': 'O', 'আ': 'A', 'ই': 'I', 'ঈ': 'I', 'উ': 'U', 'ঊ': 'U',
        'ঋ': 'Ri', 'এ': 'E', 'ঐ': 'Oi', 'ও': 'O', 'ঔ': 'Ou',
        'া': 'a', 'ি': 'i', 'ী': 'i', 'ু': 'u', 'ূ': 'u',
        'ৃ': 'ri', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
        '্': '', '্য': 'y', '্র': 'r', 'র্': 'r'
    }
    result = "".join([mapping.get(c, c) for c in text])
    return result.replace('aa', 'a').replace('ii', 'i').replace('uu', 'u').strip().title()

def get_or_create_stop(c, name_bn):
    c.execute("SELECT id FROM stops WHERE name_bn=?", (name_bn,))
    row = c.fetchone()
    if row: return row[0]
    name_en = transliterate_bn_to_en(name_bn)
    c.execute("INSERT INTO stops (name_bn, name_en) VALUES (?, ?)", (name_bn, name_en))
    return c.lastrowid

def extract_route_number(route_name):
    matches = re.findall(r'\((.*?)\)', route_name)
    for m in matches:
        if 'এ-' in m or 'নং' in m:
            return m.replace('নং', '').strip()
    return matches[-1] if matches else None

def verify_and_patch(json_file):
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    for route in data:
        src_file = route.get("source_file", "unknown")
        src_page = route.get("source_page", 0)
        route_name = route.get("route_name", "")
        route_num = extract_route_number(route_name)
        
        route_id = None
        # 1. Identify Route strictly by Route Number
        if route_num:
            c.execute("SELECT id, route_name, source_file, source_page FROM routes WHERE route_name LIKE ?", (f'%({route_num}%',))
            existing_route = c.fetchone()
            if existing_route:
                route_id = existing_route['id']
                if existing_route['route_name'] != route_name or existing_route['source_file'] != src_file or existing_route['source_page'] != src_page:
                    print(f"[REALIGN] Route {route_id}: Updating metadata to {src_file} Page {src_page}, Name: {route_name}")
                    c.execute("UPDATE routes SET route_name=?, source_file=?, source_page=? WHERE id=?", (route_name, src_file, src_page, route_id))

        if not route_id:
            # Try matching by exact name
            c.execute("SELECT id FROM routes WHERE route_name=?", (route_name,))
            existing_route = c.fetchone()
            if existing_route:
                route_id = existing_route['id']
                print(f"[REALIGN] Route {route_id}: Updating metadata to {src_file} Page {src_page}")
                c.execute("UPDATE routes SET source_file=?, source_page=? WHERE id=?", (src_file, src_page, route_id))
            else:
                print(f"[NEW ROUTE] {route_name}. Inserting...")
                c.execute("INSERT INTO routes (route_name, source_file, source_page) VALUES (?,?,?)",
                          (route_name, src_file, src_page))
                route_id = c.lastrowid

        # 2. Verify Stops & Distances
        stops = route.get("stops", [])
        distances = route.get("distances_km", [])
        for order, stop_name in enumerate(stops):
            stop_id = get_or_create_stop(c, stop_name)
            new_dist = distances[order] if order < len(distances) else None
            
            c.execute("SELECT id, stop_order, distance_km FROM route_stops WHERE route_id=? AND stop_id=?", (route_id, stop_id))
            rs_row = c.fetchone()
            
            if not rs_row:
                print(f"  [GAP STOP] Route {route_id}: Missing stop '{stop_name}'. Inserting at order {order}.")
                c.execute("INSERT INTO route_stops (route_id, stop_id, stop_order, distance_km) VALUES (?,?,?,?)",
                          (route_id, stop_id, order, new_dist))
            else:
                if rs_row['stop_order'] != order or rs_row['distance_km'] != new_dist:
                    print(f"  [FIX DIST] Route {route_id}, Stop '{stop_name}': Dist {rs_row['distance_km']}->{new_dist}, Order {rs_row['stop_order']}->{order}")
                    c.execute("UPDATE route_stops SET stop_order=?, distance_km=? WHERE id=?", (order, new_dist, rs_row['id']))

        # 3. Verify Fares
        for fare_entry in route.get("fares", []):
            f_sid = get_or_create_stop(c, fare_entry["from"])
            t_sid = get_or_create_stop(c, fare_entry["to"])
            new_fare = int(fare_entry["fare"])
            
            c.execute("SELECT id, fare_tk FROM fares WHERE route_id=? AND from_stop_id=? AND to_stop_id=?", (route_id, f_sid, t_sid))
            f_row = c.fetchone()
            
            if not f_row:
                print(f"  [GAP FARE] Route {route_id}: Missing fare pair ({fare_entry['from']} -> {fare_entry['to']}). Inserting {new_fare}tk.")
                c.execute("INSERT INTO fares (route_id, from_stop_id, to_stop_id, fare_tk) VALUES (?,?,?,?)",
                          (route_id, f_sid, t_sid, new_fare))
                c.execute("INSERT OR IGNORE INTO fares (route_id, from_stop_id, to_stop_id, fare_tk) VALUES (?,?,?,?)",
                          (route_id, t_sid, f_sid, new_fare))
            else:
                if f_row['fare_tk'] != new_fare:
                    print(f"  [FIX FARE] Route {route_id} ({fare_entry['from']}->{fare_entry['to']}): {f_row['fare_tk']}tk -> {new_fare}tk")
                    c.execute("UPDATE fares SET fare_tk=? WHERE id=?", (new_fare, f_row['id']))
                    c.execute("UPDATE fares SET fare_tk=? WHERE route_id=? AND from_stop_id=? AND to_stop_id=?", (new_fare, route_id, t_sid, f_sid))

    conn.commit()
    conn.close()
    print(f"Verification and patching complete for {json_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_fixes.py <json_file>")
        sys.exit(1)
    verify_and_patch(sys.argv[1])