
import sqlite3

DB_PATH = 'backend/data/busvara.db'

def apply_optimizations():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("Applying database indexing...")
    
    # route_stops indexes
    c.execute("CREATE INDEX IF NOT EXISTS idx_rs_route_id ON route_stops(route_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_rs_stop_id ON route_stops(stop_id)")
    
    # fares indexes
    c.execute("CREATE INDEX IF NOT EXISTS idx_f_route_id ON fares(route_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_f_from_stop_id ON fares(from_stop_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_f_to_stop_id ON fares(to_stop_id)")
    
    # stops indexes
    c.execute("CREATE INDEX IF NOT EXISTS idx_s_name_en ON stops(name_en)")
    
    conn.commit()
    conn.close()
    print("Optimization complete.")

if __name__ == "__main__":
    apply_optimizations()
