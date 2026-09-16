
import sqlite3

DB_PATH = r"backend/data/busvara.db"

# Cluster Map: { "Canonical Name": ["Variation 1", "Variation 2", ...] }
CLUSTERS = {
    "Abdullahpur": ["Abdullahpur (Jelkhana)", "Abdullahpur Jail"],
    "Asadgate": ["Asad Avenue", "Asad Geit", "Asadgate", "Asadget"],
    "Amin Bazar": ["Aminbajar"],
    "Ashulia": ["Ashuliya"],
    "Azampur": ["Ajmpur", "Azampur"],
    "Babu Bazar": ["Babu Bazar Bridge", "Babubajar", "Babubajar Brij", "Babubajar Setu"],
    "Badda": ["Badda (Ashraf Get)", "Badda (Nurer Chala)"],
    "Banglamotor": ["Banglamotr", "Banglamtr", "Banglamotor"],
    "Science Lab": ["Saj়Ens Lab", "Saj়Ensljab", "Sayens Lab", "Sayensljab", "Sayensljabh", "Scienceljabh", "Scienceljab:", "Saj়Ensljabh", "Sayensljabh:", "Sains Ljab", "Science Lab (সাইন্স ল্যাব)"],
    "Victoria Park": ["Bhiktoriyapark", "Bhiktorij়Apark", "Bhiktoriya Park", "Bhiktorij়A Park", "Biktorij়A Park", "Victoria Park (ভিক্টোরিয়াপার্ক)"],
    "Bijoy Sarani": ["Bijoy Sarani Crossing", "Bijy Smrni", "Bijoy Sarani (বিজয় সরণী)", "Bijoy Sarani (বিজয় সরণী)"],
    "Mirpur-1": ["Mirpur ১", "Mirpur-1"],
    "Mirpur-10": ["Mirpur ১০", "Mirpur-10"],
    "Mirpur-11": ["Mirpur ১১", "Mirpur-11"],
    "Mirpur-12": ["Mirpur ১২", "Mirpur-12"],
    "Kamarpara": ["Kmarpara", "Kamar Para", "Kamarpad়A"],
    "Gabtoli": ["Gabtli", "Gbtoli", "Gabtoli Bridge"],
    "Mohammadpur": ["Mohpur", "Mohammdpur", "Mohammdpur (Asad Ebhiniu)", "Mohammdpur Shij়A Msjid", "Mohammadpur Shia Masjid"],
    "Karwan Bazar": ["Karoj়An Bajar", "Kaoranbajar", "Karwan Bazar (কারওয়ান বাজার)"],
    "Mogbazar": ["Mgbajar", "Moghbazar", "Mogbazar Mor"],
    "Staff Quarter": ["Staf Koyatar", "Demra Staf Koyatar", "Amuliya Staf Koyartar", "Staff Road"],
    "Flyover": ["Flaiobhar", "Flaibhar"],
    "Biswa Road": ["Bishb Rod", "Kuril Bisshoroad", "Bishworoad", "Kuril Bishbrod"],
    "Dholaipar": ["Dholaipad়", "Dolaipar"]
}

def standardize():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    total_merged = 0
    
    for canonical, variations in CLUSTERS.items():
        # 1. Get/Create the Canonical ID
        c.execute("SELECT id FROM stops WHERE name_en = ?", (canonical,))
        row = c.fetchone()
        if not row:
            # If canonical doesn't exist, try to find one of the variations to use as base
            c.execute("SELECT id FROM stops WHERE name_en IN (%s)" % ','.join(['?']*len(variations)), variations)
            base_row = c.fetchone()
            if base_row:
                master_id = base_row[0]
                c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (canonical, master_id))
            else:
                continue # Skip if no variations found either
        else:
            master_id = row[0]

        # 2. Merge variations
        for var in variations:
            if var == canonical: continue
            
            c.execute("SELECT id FROM stops WHERE name_en = ?", (var,))
            dup_rows = c.fetchall()
            for (dup_id,) in dup_rows:
                if dup_id == master_id: continue
                
                # Re-map route_stops
                c.execute("UPDATE OR IGNORE route_stops SET stop_id = ? WHERE stop_id = ?", (master_id, dup_id))
                c.execute("DELETE FROM route_stops WHERE stop_id = ?", (dup_id,))
                
                # Re-map fares
                c.execute("UPDATE OR IGNORE fares SET from_stop_id = ? WHERE from_stop_id = ?", (master_id, dup_id))
                c.execute("UPDATE OR IGNORE fares SET to_stop_id = ? WHERE to_stop_id = ?", (master_id, dup_id))
                c.execute("DELETE FROM fares WHERE from_stop_id = ? OR to_stop_id = ?", (dup_id, dup_id))
                
                # Delete duplicate stop
                c.execute("DELETE FROM stops WHERE id = ?", (dup_id,))
                total_merged += 1

    conn.commit()
    conn.close()
    print(f"Standardization complete. Merged {total_merged} duplicate entries.")

if __name__ == "__main__":
    standardize()
