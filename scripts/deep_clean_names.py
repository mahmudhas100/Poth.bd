
import sqlite3

DB_PATH = r"backend/data/busvara.db"

def deep_clean_transliterations():
    patterns = {
        "Flaiobhar": "Flyover",
        "Flaibhar": "Flyover",
        "Kjamp": "Camp",
        "Ljab": "Lab",
        "Sains": "Science",
        "Smrni": "Sarani",
        "Maoya": "Mawa",
        "Mohpur": "Mohammadpur",
        "Jillur": "Zillur",
        "Rhman": "Rahman",
        "Mod়": "Mor",
        "Bajar": "Bazar",
        "Modor": "Mor",
        "Srni": "Sarani",
        "Gbtoli": "Gabtoli",
        "Mhapara": "Mohapara",
        "Mhakhali": "Mohakhali",
        "Mgbajar": "Mogbazar",
        "Ndd": "Nadda",
        "Mouchak": "Mouchak",
        "Bishworoad": "Biswa Road",
        "Chashara": "Chashara"
    }

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    total_fixed = 0
    
    c.execute("SELECT id, name_en FROM stops")
    rows = c.fetchall()
    
    for row_id, name_en in rows:
        new_name = name_en
        for old, replacement in patterns.items():
            if old in new_name:
                new_name = new_name.replace(old, replacement)
        
        if new_name != name_en:
            c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (new_name, row_id))
            total_fixed += 1

    conn.commit()
    conn.close()
    print(f"Deep Clean Complete. Updated {total_fixed} stop names.")

if __name__ == "__main__":
    deep_clean_transliterations()
