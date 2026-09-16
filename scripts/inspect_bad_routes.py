import sqlite3

conn = sqlite3.connect('backend/data/busvara.db')
c = conn.cursor()

c.execute("SELECT id, route_name FROM routes")
routes = {r[0]: r[1] for r in c.fetchall()}

bad_routes = []
for r_id, r_name in routes.items():
    c.execute("SELECT s.name_en, rs.distance_km FROM route_stops rs JOIN stops s ON rs.stop_id = s.id WHERE rs.route_id=? ORDER BY rs.stop_order", (r_id,))
    stops = c.fetchall()
    prev_dist = -1.0
    for stop_name, dist in stops:
        if dist < prev_dist:
            bad_routes.append((r_id, r_name, stop_name, dist, prev_dist))
            break
        prev_dist = dist

for br in bad_routes:
    print(f"Route {br[0]} ({br[1]}): Distance dropped at {br[2]} from {br[4]}km to {br[3]}km")

conn.close()
