
import sqlite3
import sys

DB_PATH = "data/busvara.db"

def test_query(from_name, to_name):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    query_stop = """
        SELECT id, name_en FROM stops 
        WHERE LOWER(name_en) = LOWER(?) 
           OR name_bn = ? 
           OR id IN (SELECT stop_id FROM stop_aliases WHERE alias_name = ?)
    """
    
    print(f"Searching for: {from_name} and {to_name}")
    
    c.execute(query_stop, (from_name, from_name, from_name))
    from_row = c.fetchone()
    
    c.execute(query_stop, (to_name, to_name, to_name))
    to_row = c.fetchone()
    
    if not from_row:
        print(f"Error: {from_name} not found")
        return
    if not to_row:
        print(f"Error: {to_name} not found")
        return
        
    print(f"Resolved IDs: {from_row['id']} ({from_row['name_en']}), {to_row['id']} ({to_row['name_en']})")

    sql = """
        SELECT 
            f.route_id, 
            r.route_name, 
            s1.name_en as from_stop, 
            s2.name_en as to_stop, 
            f.fare_tk as fare 
        FROM fares f
        JOIN routes r ON f.route_id = r.id
        JOIN stops s1 ON f.from_stop_id = s1.id
        JOIN stops s2 ON f.to_stop_id = s2.id
        WHERE (f.from_stop_id = ? AND f.to_stop_id = ?)
           OR (f.from_stop_id = ? AND f.to_stop_id = ?)
    """
    c.execute(sql, (from_row['id'], to_row['id'], to_row['id'], from_row['id']))
    results = c.fetchall()
    
    print(f"Found {len(results)} results:")
    for r in results:
        print(f"Route: {r['route_name']} | Fare: ৳{r['fare']}")
        
    conn.close()

if __name__ == "__main__":
    f = sys.argv[1] if len(sys.argv) > 1 else "Amtoli"
    t = sys.argv[2] if len(sys.argv) > 2 else "Motijheel"
    test_query(f, t)
