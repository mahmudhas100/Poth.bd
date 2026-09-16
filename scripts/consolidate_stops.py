
import sqlite3
import re

DB_PATH = r"backend/data/busvara.db"

# Master Mapping: { "canonical": ["variation1", "variation2", ...] }
# This targets the messy output I just saw.
CONSOLIDATION_MAP = {
    "Abdullahpur": ["Abdullahpur (Jelkhana)", "Abdullahpur Jail", "Abbdullahpur"],
    "Airport": ["Eyarport", "Biman Bandar", "Biman Bndr", "Airport"],
    "Azampur": ["Ajmpur"],
    "Azimpur": ["Azimpur (Dhakeshwari)"],
    "Badda": ["Badda (Ashraf Get)", "Badda (Nurer Chala)", "Badda Link Road", "North Badda", "Middle Badda", "Merul Badda"],
    "Banashree": ["Banashree (Meradia)", "Bnshri(Meradiya)"],
    "Banglamotor": ["Banglamotr", "Banglamtr", "Banglamotor"],
    "Basabo": ["Bashabo"],
    "Basila": ["Bosila", "Basila Bridge", "Basila Cng Stand"],
    "Bijoy Sarani": ["Bijy Sarani", "Bijoy Sarani Crossing", "Urojahaj Krsing"],
    "Biswa Road": ["Bishb Rod", "Bishbrod (Sayedabad)"],
    "Chashara": ["Naraj়Ngnj (Chashara)", "Narayangannj Chashara", "Chashara Basstjand", "Chashara Bus Stand", "Narayngnj Chashara"],
    "Dhour": ["Dhour Bridge", "Dhour More", "Dhur Mor"],
    "Diyabari": ["Diabari", "Diabari (Beribandh)", "Diabari Chowrasta", "Diabari More", "Diyabari (Beribandh)", "Diyabari Chourasta", "Diyabari Mor", "Uttara Diabari", "Uttra Diyabari", "Uttrar Diyabari"],
    "ECB More": ["Ecb Chattar", "Ecb More", "Manikdi (Ecb More)", "Manikdi (Isibi Mor)"],
    "Fantasy Kingdom": ["Fjantasi", "Fjantasi Kingdm", "Fantasy Kingdom"],
    "Gabtoli": ["Gabtli", "Gbtoli", "Gabtoli Bridge"],
    "Gazipur Chowrasta": ["Gajipur Chouh", "Gajipur Chourasta", "Gazipur Chowrasta", "Joydebpur Chowrasta", "Jj়Debpur Chouh"],
    "Gulistan": ["Gulistan (Bnggbndhu Ebhiniu)", "Gulistan (Fulbaria)", "Gulistan (Hanif Flyover)", "Gulistan More", "Fullbaria", "Fulbariya", "Ftulla"],
    "Hanif Flyover": ["Meyr Mohammd Flyover"],
    "Ittefaq": ["Ittefak", "Ittefak Mor"],
    "Jashimuddin": ["Jashim Uddin", "Jsimuddin"],
    "Kamalapur": ["Kamalapur (Pirjangi Mazar)", "Kamalapur Station", "Kamalpur", "Pirjangi Mazar"],
    "Kamarpara": ["Kmarpara", "Kamar Para", "Kamarpad়A"],
    "Khamarbari": ["Khamarbari Mor"],
    "Khilgaon": ["Khilgano", "Khilgano (Taltla)", "Khilgaon Taltola", "Khilgano Taltla"],
    "Moghbazar": ["Mgbajar", "Mogbazar"],
    "Mohammadpur": ["Mohpur", "Mo:Pur", "Mohammadpur (Asad Avenue)", "Mohammadpur (Japan Garden Siti)", "Mohammadpur Basstjand", "Mohammadpur Taun Hl", "Mohammdpur Basshtjand", "Mohammdpur Shiya Msjid", "Mohbasstjand", "Town Hall"],
    "Motijheel": ["Mtijhil (Shapla Chtbr)", "Shapla Chattar"],
    "Nandipara": ["Nndipad়A", "Nandipara Bridge", "Nndipara Brij"],
    "Narayanganj": ["Nahgnj Lingk Rod", "Narayngnj", "Narayanganj Link Road"],
    "Paturia": ["Paturiya", "Paturiya (Beribandh)"],
    "Rajlakshmi": ["Rajlkshi"],
    "Rampura": ["Rampura (Banashree)", "Rampura Bazar", "Rampura Bridge", "Rampura Tv Center", "Tv Center"],
    "Science Lab": ["Saj়Ensljab", "Sayens Lab", "Sayensljab", "Sayensljabh", "Scienceljabh", "Sayensljabh:", "Sains Ljab", "Science Lab "],
    "Sheowrapara": ["Sheod়Apad়A", "Sheora", "Sheora Para", "Shewra", "Shewrapara", "Kazipara", "Kajipara", "Kajipad়A"],
    "Uttara": ["Uttra-১০", "Uttra-১২", "Uttra Haujing", "House Building", "Haus Bilding"]
}

def consolidate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    total_merged = 0
    
    # 1. First Pass: Hard Mapping
    for canonical, variations in CONSOLIDATION_MAP.items():
        # Get/Create master ID
        c.execute("SELECT id FROM stops WHERE name_en = ?", (canonical,))
        row = c.fetchone()
        if not row:
            # If canonical name doesn't exist, use first variation as base
            c.execute("SELECT id FROM stops WHERE name_en IN (%s)" % ','.join(['?']*len(variations)), variations)
            base_row = c.fetchone()
            if base_row:
                master_id = base_row[0]
                c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (canonical, master_id))
            else:
                continue
        else:
            master_id = row[0]

        # Merge every variation into master_id
        for var in variations:
            c.execute("SELECT id FROM stops WHERE name_en = ?", (var,))
            dups = c.fetchall()
            for (dup_id,) in dups:
                if dup_id == master_id: continue
                
                # Re-map relations
                c.execute("UPDATE OR IGNORE route_stops SET stop_id = ? WHERE stop_id = ?", (master_id, dup_id))
                c.execute("DELETE FROM route_stops WHERE stop_id = ?", (dup_id,))
                c.execute("UPDATE OR IGNORE fares SET from_stop_id = ? WHERE from_stop_id = ?", (master_id, dup_id))
                c.execute("UPDATE OR IGNORE fares SET to_stop_id = ? WHERE to_stop_id = ?", (master_id, dup_id))
                c.execute("DELETE FROM fares WHERE from_stop_id = ? OR to_stop_id = ?", (dup_id, dup_id))
                c.execute("DELETE FROM stops WHERE id = ?", (dup_id,))
                total_merged += 1

    # 2. Second Pass: Phonetic cleaning of artifacts like 'j়', 'd়', etc.
    c.execute("SELECT id, name_en FROM stops")
    stops = c.fetchall()
    for sid, name_en in stops:
        clean = name_en.replace('j়', 'y').replace('d়', 'r').replace('Modor', 'Mor').replace('Bajar', 'Bazar')
        if clean != name_en:
            c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (clean, sid))

    conn.commit()
    conn.close()
    print(f"Consolidation Complete. Merged {total_merged} stops.")

if __name__ == "__main__":
    consolidate()
