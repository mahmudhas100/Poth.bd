
import sqlite3

DB_PATH = "data/busvara.db"

def find_transit(from_id, to_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 1. Find all routes passing through the origin
    c.execute("SELECT DISTINCT route_id FROM route_stops WHERE stop_id = ?", (from_id,))
    routes_from = [r['route_id'] for r in c.fetchall()]

    # 2. Find all routes passing through the destination
    c.execute("SELECT DISTINCT route_id FROM route_stops WHERE stop_id = ?", (to_id,))
    routes_to = [r['route_id'] for r in c.fetchall()]

    print(f"Routes from origin: {len(routes_from)}")
    print(f"Routes to destination: {len(routes_to)}")

    # 3. Find intermediate stops where you can transfer
    # A stop S is a transfer point if:
    #   - Stop S is in a route from Routes_From
    #   - AND Stop S is in a route from Routes_To
    
    query = """
        SELECT DISTINCT s.id, s.name_en
        FROM route_stops rs1
        JOIN route_stops rs2 ON rs1.stop_id = rs2.stop_id
        JOIN stops s ON rs1.stop_id = s.id
        WHERE rs1.route_id IN ({}) 
        AND rs2.route_id IN ({})
        AND s.id != ? AND s.id != ?
    """
    query = query.format(','.join(map(str, routes_from)), ','.join(map(str, routes_to)))

    c.execute(query, (from_id, to_id))
    transfer_points = c.fetchall()

    print(f"\nFound {len(transfer_points)} potential transfer points:")
    for tp in transfer_points[:10]: # Show first 10
        print(f"- {tp['name_en']}")

    # 4. Pick the best transfer (simple heuristic: first one for now)
    if transfer_points:
        best_tp = transfer_points[0]
        tp_id = best_tp['id']
        
        # Get fares for the two legs
        # Leg 1: From -> TP
        c.execute("SELECT r.route_name, f.fare_tk FROM fares f JOIN routes r ON f.route_id = r.id WHERE (f.from_stop_id = ? AND f.to_stop_id = ?) OR (f.from_stop_id = ? AND f.to_stop_id = ?) LIMIT 1", (from_id, tp_id, tp_id, from_id))
        leg1 = c.fetchone()
        
        # Leg 2: TP -> To
        c.execute("SELECT r.route_name, f.fare_tk FROM fares f JOIN routes r ON f.route_id = r.id WHERE (f.from_stop_id = ? AND f.to_stop_id = ?) OR (f.from_stop_id = ? AND f.to_stop_id = ?) LIMIT 1", (tp_id, to_id, to_id, tp_id))
        leg2 = c.fetchone()
        
        if leg1 and leg2:
            print(f"\nRecommended Route:")
            print(f"1. Take '{leg1['route_name']}' to {best_tp['name_en']} (Fare: ৳{leg1['fare_tk']})")
            print(f"2. Transfer at {best_tp['name_en']}")
            print(f"3. Take '{leg2['route_name']}' to Destination (Fare: ৳{leg2['fare_tk']})")
            print(f"Total Estimated Fare: ৳{leg1['fare_tk'] + leg2['fare_tk']}")

    conn.close()

if __name__ == "__main__":
    # Amtoli (263) to Shapla Chattar (259)
    find_transit(263, 259)

