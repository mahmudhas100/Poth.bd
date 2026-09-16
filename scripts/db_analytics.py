
import sqlite3

DB_PATH = r"backend/data/busvara.db"

def run_analytics():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print("\n" + "="*50)
    print("      BUS VARA: DATABASE ANALYTICS (2026)")
    print("="*50)

    # 1. Network Scale
    routes_count = c.execute("SELECT count(*) FROM routes").fetchone()[0]
    stops_count = c.execute("SELECT count(*) FROM stops").fetchone()[0]
    fares_count = c.execute("SELECT count(*) FROM fares").fetchone()[0]
    
    print(f"\n--- Network Scale ---")
    print(f"Total Verified Routes:  {routes_count}")
    print(f"Total Unique Bus Stops: {stops_count}")
    print(f"Total Fare Segments:    {fares_count}")

    # 2. Distance Analytics
    longest = c.execute("""
        SELECT r.route_name, MAX(rs.distance_km) as dist 
        FROM route_stops rs 
        JOIN routes r ON rs.route_id = r.id 
        GROUP BY rs.route_id 
        ORDER BY dist DESC LIMIT 1
    """).fetchone()
    
    avg_dist = c.execute("""
        SELECT AVG(max_dist) FROM (
            SELECT MAX(distance_km) as max_dist FROM route_stops GROUP BY route_id
        )
    """).fetchone()[0]

    print(f"\n--- Distance Analytics ---")
    print(f"Longest Verified Route: {longest['route_name']}")
    print(f"Distance:               {longest['dist']} KM")
    print(f"Average Route Length:   {round(avg_dist, 2)} KM")

    # 3. Fare Analytics
    max_fare = c.execute("SELECT MAX(fare_tk) FROM fares").fetchone()[0]
    avg_fare = c.execute("SELECT AVG(fare_tk) FROM fares WHERE fare_tk > 0").fetchone()[0]
    
    print(f"\n--- Fare Analytics ---")
    print(f"Maximum Single Fare:    {max_fare} TK")
    print(f"Average Segment Fare:   {round(avg_fare, 2)} TK")
    print(f"Minimum Fare (Floor):   10 TK")

    # 4. Connectivity Analytics (Top 5 Hubs)
    print(f"\n--- Top 5 Connectivity Hubs ---")
    top_hubs = c.execute("""
        SELECT s.name_en, count(rs.route_id) as route_count 
        FROM route_stops rs 
        JOIN stops s ON rs.stop_id = s.id 
        GROUP BY s.id 
        ORDER BY route_count DESC LIMIT 5
    """).fetchall()
    
    for i, hub in enumerate(top_hubs, 1):
        print(f"{i}. {hub['name_en']:<20} ({hub['route_count']} routes)")

    # 5. Data Density
    avg_stops = c.execute("""
        SELECT AVG(stop_count) FROM (
            SELECT count(stop_id) as stop_count FROM route_stops GROUP BY route_id
        )
    """).fetchone()[0]
    
    print(f"\n--- Data Density ---")
    print(f"Average Stops per Route: {round(avg_stops, 1)}")
    print(f"Total Data Points:       {routes_count * stops_count} (Upper bound)")
    print("="*50 + "\n")

    conn.close()

if __name__ == "__main__":
    run_analytics()
