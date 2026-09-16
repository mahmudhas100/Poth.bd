import sqlite3

def find_routes():
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    print("Abdullahpur variants in stops:")
    for row in c.execute("SELECT id, name_bn, name_en FROM stops WHERE name_bn LIKE '%আব্দুল্লাহ%' OR name_bn LIKE '%আব্দুলা%' OR name_en LIKE '%abdull%'"):
        print(row)
        
    print("\nFarmgate variants in stops:")
    for row in c.execute("SELECT id, name_bn, name_en FROM stops WHERE name_bn LIKE '%ফার্মগেট%' OR name_en LIKE '%farmgate%'"):
        print(row)

    print("\nFinding routes that contain BOTH Abdullahpur (by any ID) and Farmgate (by any ID)...")
    c.execute("""
        SELECT r.id, r.route_name 
        FROM routes r
        JOIN route_stops rs1 ON r.id = rs1.route_id
        JOIN stops s1 ON rs1.stop_id = s1.id
        JOIN route_stops rs2 ON r.id = rs2.route_id
        JOIN stops s2 ON rs2.stop_id = s2.id
        WHERE (s1.name_bn LIKE '%আব্দুল্লাহ%' OR s1.name_bn LIKE '%আব্দুলা%' OR s1.name_en LIKE '%abdull%')
          AND (s2.name_bn LIKE '%ফার্মগেট%' OR s2.name_en LIKE '%farmgate%')
    """)
    routes = c.fetchall()
    if routes:
        for r in routes:
            print(f"Found route: {r}")
    else:
        print("No routes found connecting them directly in the DB!")
        
    conn.close()

if __name__ == "__main__":
    find_routes()
