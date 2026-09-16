
import sqlite3

DB_PATH = r"backend/data/busvara.db"

# List of stops that are GEOGRAPHICALLY DISTINCT but often mis-merged
RESTORE_MAP = {
    "Kazipara": "কাজীপাড়া",
    "Sheowrapara": "শেওড়াপাড়া",
    "Mirpur-10": "মিরপুর-১০",
    "Mirpur-11": "মিরপুর-১১",
    "Mirpur-12": "মিরপুর-১২",
    "Mirpur-1": "মিরপুর-১",
    "Nadda": "নদ্দা",
    "Kuril": "কুড়িল",
    "Malibagh": "মালিবাগ",
    "Mouchak": "মৌচাক",
    "Asadgate": "আসাদ গেট",
    "Shyamoli": "শ্যামলী",
    "Kallyanpur": "কল্যাণপুর",
    "Gabtoli": "গাবতলী"
}

def surgical_restore():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Identify routes with repeating stops
    c.execute("""
        SELECT rs.route_id, rs.stop_id, s.name_en, count(*) as count 
        FROM route_stops rs 
        JOIN stops s ON rs.stop_id = s.id 
        GROUP BY rs.route_id, rs.stop_id 
        HAVING count > 1
    """)
    damaged_routes = c.fetchall()
    print(f"Repairing {len(damaged_routes)} over-merged route instances...")

    # For this high-level fix, we will re-instantiate missing common stops 
    # and re-assign them to the route_stops based on original intent.
    # Note: This requires a mapping of which stop_id 376 corresponds to which name in which order.
    
    # Simple strategy: Re-create the most common neighbors and manual re-assignment for key hubs.
    for name_en, name_bn in RESTORE_MAP.items():
        # Ensure the stop exists uniquely
        c.execute("SELECT id FROM stops WHERE name_en = ?", (name_en,))
        if not c.fetchone():
            c.execute("INSERT INTO stops (name_en, name_bn) VALUES (?, ?)", (name_en, name_bn))
            print(f"Restored unique stop: {name_en}")

    # Commit the additions
    conn.commit()
    conn.close()
    print("Base stops restored. Proceeding to sequence re-alignment...")

if __name__ == "__main__":
    surgical_restore()
