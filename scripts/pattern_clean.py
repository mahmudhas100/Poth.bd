import sqlite3

DB_PATH = r"backend/data/busvara.db"

def pattern_clean():
    patterns = {
        "j়": "y",
        "d়": "r",
        "Modor": "Mor",
        "Bajar": "Bazar",
        "Bnggbhbn": "Bangabhaban",
        "Chtbr": "Chattar",
        "Ebhiniu": "Avenue",
        "Kjamp": "Camp",
        "Basstjand": "Bus Stand",
        "Basshtjand": "Bus Stand",
        "Ljab": "Lab",
        "Mtsjbhbn": "Matsya Bhaban",
        "Flaiobhar": "Flyover",
        "Flaibhar": "Flyover",
        "Smrni": "Sarani",
        "Srni": "Sarani",
        "Mgbajar": "Moghbazar",
        "Mhapara": "Mohapara",
        "Mhakhali": "Mohakhali",
        "Gbtoli": "Gabtoli",
        "Ndd": "Nadda",
        "Nddaa": "Nadda",
        "Nrdda": "Nadda",
        "Ecb": "ECB",
        "Cantt": "Cantonment",
        "Kjantnment": "Cantonment",
        "Kmars": "Commerce",
        "Mtijhil": "Motijheel",
        "Jsimuddin": "Jashimuddin",
        "Maoya": "Mawa",
        "Saj়": "Science",
        "Sayens": "Science",
        "Scienc": "Science",
        "Bhiktor": "Victoria",
        "Biktor": "Victoria",
        "Joj়Ar": "Joar",
        "Oj়Apda": "WAPDA",
        "Haujing": "Housing",
        "Dkshin": "South",
        "Puratn": "Old",
        "Setu": "Bridge",
        "Brij": "Bridge"
    }

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    total_fixed = 0
    c.execute("SELECT id, name_en FROM stops")
    rows = c.fetchall()
    
    for rid, name in rows:
        new_name = name
        for old, replacement in patterns.items():
            if old in new_name:
                new_name = new_name.replace(old, replacement)
        
        if new_name != name:
            c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (new_name, rid))
            total_fixed += 1

    conn.commit()
    conn.close()
    print(f"Pattern Clean Complete. Fixed {total_fixed} stops.")

if __name__ == "__main__":
    pattern_clean()
