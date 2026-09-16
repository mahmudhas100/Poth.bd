import sqlite3

DB_PATH = r"backend/data/busvara.db"

def definitive_fix():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 1. Comprehensive Mapping of "Robotic" and variant strings to "Gold Standard" names
    mapping = {
        # Science Lab Cluster
        "Saj়Ens Lab": "Science Lab", "Saj়Ensljab": "Science Lab", "Sayens Lab": "Science Lab",
        "Sayensljab": "Science Lab", "Sayensljabh": "Science Lab", "Scienceljabh": "Science Lab",
        "Scienceljab:": "Science Lab", "Saj়Ensljabh": "Science Lab", "Sayensljabh:": "Science Lab",
        "Sayensljab:": "Science Lab", "Science Lab": "Science Lab", "Science Lab ": "Science Lab",
        
        # Victoria Park Cluster
        "Bhiktoriyapark": "Victoria Park", "Bhiktorij়Apark": "Victoria Park", "Bhiktoriya Park": "Victoria Park",
        "Bhiktorij়A Park": "Victoria Park", "Biktorij়A Park": "Victoria Park", "Victoria Park": "Victoria Park",
        
        # Mirpur Cluster
        "Mirpur ১": "Mirpur-1", "Mirpur ১০": "Mirpur-10", "Mirpur ১১": "Mirpur-11", "Mirpur ১২": "Mirpur-12",
        "Mirpur ২": "Mirpur-2", "Mirpur-6": "Mirpur-6", "Mirpur ১১ ৩/২": "Mirpur-11 3/2",
        
        # Major Hubs & Robotic Fixes
        "Bijj়Ngr": "Bijoy Nagar", "Bijy Ngr": "Bijoy Nagar", "Kajipad়A": "Kajipara",
        "Sheod়Apad়A": "Sheowrapara", "Sheorapara": "Sheowrapara", "Matuj়Ail": "Matuail",
        "Sanarpad়": "Sanarpar", "Konapad়A": "Konapara", "Dolaipad়": "Dholaipar",
        "Dholaipad়": "Dholaipar", "Mugdapad়A": "Mugdapara", "Teghrij়A": "Teghoria",
        "Gauchhij়A": "Gaushia", "Gauchhiya": "Gaushia", "Gendarij়A": "Gandaria",
        "Jj়Kali Mndir": "Joykali Mandir", "Jiro Pj়Ent": "Zero Point", "Jiro Pyent": "Zero Point",
        "Chej়Armjan Bad়I": "Chairman Bari", "Birulij়A": "Birulia", "Nndipad়A": "Nandipara",
        "Nndipara Brij": "Nandipara Bridge", "Jabi (Sabhar)": "JU (Savar)", "Bhaoj়Ar Bhiti": "Bhawar Viti",
        "Jj়Debpur": "Joydebpur", "Jj়Debpur Chouh": "Joydebpur Chowrasta", "Joj়Ar Sahara": "Joar Sahara",
        "Oj়Apda": "WAPDA", "Bnggbhbn": "Bangabhaban", "Mshakhali": "Mohakhali",
        "Mhakhali": "Mohakhali", "Mgbajar": "Mogbazar", "Moghbazar": "Mogbazar",
        "Khilgano": "Khilgaon", "Khilgano Taltla": "Khilgaon Taltola", "Mohammdpur": "Mohammadpur",
        "Mohammdpur (Asad Ebhiniu)": "Mohammadpur (Asad Avenue)", "Jsimuddin": "Jashimuddin",
        "Jatrabari": "Jatrabari", "Jatrabad়I": "Jatrabari", "Saj়Edabad": "Sayedabad",
        "Paturiya": "Paturia", "Flaiobhar": "Flyover", "Flaibhar": "Flyover", "Mod়": "Mor",
        "Srni": "Sarani", "Smrni": "Sarani", "Jnpth": "Janapath", "Bajar": "Bazar",
        "Bnggbndhu": "Bangabandhu", "Ebhiniu": "Avenue", "Kmarpara": "Kamarpara",
        "Kamar Para": "Kamarpara", "Kamarpad়A": "Kamarpara", "Gbtoli": "Gabtoli",
        "Gabtli": "Gabtoli", "Asadgeit": "Asadgate", "Asadget": "Asadgate", "Asad Gate": "Asadgate",
        "Bshundhara": "Bashundhara", "Biman Bandar": "Airport", "Biman Bndr": "Airport",
        "Mscot Plaza": "Mascot Plaza", "Haujing": "Housing", "Abbdullahpur": "Abdullahpur",
        "Washpur": "Washpur", "Oj়Ashpur": "Washpur", "Ansarkjamp": "Ansar Camp"
    }

    total_renamed = 0
    
    print("--- Phase 1: Cleaning Names ---")
    for old, new in mapping.items():
        c.execute("UPDATE stops SET name_en = ? WHERE name_en = ?", (new, old))
        total_renamed += c.rowcount
    
    # Generic Pattern Clean for 'j়' and 'd়' artifacts
    c.execute("SELECT id, name_en FROM stops WHERE name_en LIKE '%j়%' OR name_en LIKE '%d়%'")
    rows = c.fetchall()
    for row in rows:
        clean_name = row['name_en'].replace('j়', 'y').replace('d়', 'r')
        c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (clean_name, row['id']))
        total_renamed += 1

    print(f"Cleaned/Renamed {total_renamed} stops.")

    print("\n--- Phase 2: Deduplicating Hubs ---")
    c.execute("SELECT name_en, COUNT(*) as c FROM stops GROUP BY name_en HAVING c > 1")
    dups = c.fetchall()
    
    total_merged = 0
    for d in dups:
        name = d['name_en']
        c.execute("SELECT id FROM stops WHERE name_en = ? ORDER BY id ASC", (name,))
        ids = [r['id'] for r in c.fetchall()]
        master_id = ids[0]
        duplicate_ids = ids[1:]
        
        for dup_id in duplicate_ids:
            # Update all references
            c.execute("UPDATE OR IGNORE route_stops SET stop_id = ? WHERE stop_id = ?", (master_id, dup_id))
            c.execute("DELETE FROM route_stops WHERE stop_id = ?", (dup_id,))
            c.execute("UPDATE OR IGNORE fares SET from_stop_id = ? WHERE from_stop_id = ?", (master_id, dup_id))
            c.execute("UPDATE OR IGNORE fares SET to_stop_id = ? WHERE to_stop_id = ?", (master_id, dup_id))
            c.execute("DELETE FROM fares WHERE from_stop_id = ? OR to_stop_id = ?", (dup_id, dup_id))
            c.execute("DELETE FROM stops WHERE id = ?", (dup_id,))
            total_merged += 1
            
    print(f"Merged {total_merged} duplicate stop IDs.")

    conn.commit()
    conn.close()
    print("\nDefinitive Fix Complete.")

if __name__ == "__main__":
    definitive_fix()
