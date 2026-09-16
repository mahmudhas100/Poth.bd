
import sqlite3

DB_PATH = r"backend/data/busvara.db"

def fix_transliterations():
    fixes = {
        "Karoj়An Bajar": "Karwan Bazar",
        "Bhiktorij়Apark": "Victoria Park",
        "Jnpth Mod়": "Janapath Mor",
        "Tarangr": "Taranagar",
        "Bsila": "Bosila",
        "Bouddh Mndir": "Buddhist Temple",
        "Gausia": "Gaushia",
        "Bamonra": "Bamonra",
        "Bhiktorij়A": "Victoria",
        "Jsim Uddin": "Jashim Uddin",
        "Bijy Srni": "Bijoy Sarani",
        "Mod়": "Mor",
        "Bajar": "Bazar",
        "Srni": "Sarani",
        "Abbdullahpur": "Abdullahpur",
        "Dhour": "Dhour",
        "Ghatarchr": "Ghatarchar",
        "Gbtoli": "Gabtoli",
        "Kmarpara": "Kamarpara",
        "Mhapara": "Mohapara",
        "Mhakhali": "Mohakhali",
        "Mgbajar": "Mogbazar",
        "Mouchak": "Mouchak",
        "Malibag": "Malibagh",
        "Rampura": "Rampura",
        "Badda Link Rd": "Badda Link Road",
        "Notun Bazar": "Notun Bazar",
        "Kuril Bisshoroad": "Kuril Biswa Road",
        "Airport": "Airport",
        "Uttara": "Uttara",
        "Gazipur Chow": "Gazipur Chowrasta",
        "Chowrasta": "Chowrasta",
        "Shonir Akhra": "Shonir Akhra",
        "Signboard": "Signboard",
        "Kanchpur": "Kanchpur",
        "Madanpur": "Madanpur",
        "Meghna Ghat": "Meghna Ghat",
        "Sonargaon": "Sonargaon",
        "Daudkandi": "Daudkandi",
        "Comilla": "Comilla",
        "Sayedabad": "Sayedabad",
        "Jatrabari": "Jatrabari",
        "Gulistan": "Gulistan",
        "Phulbaria": "Fulbaria",
        "Motijheel": "Motijheel",
        "Kamalapur": "Kamalapur",
        "Mugda": "Mugda",
        "Khilgaon": "Khilgaon",
        "Bashabo": "Basabo",
        "Meradia": "Meradia",
        "Banasree": "Banasree",
        "Demra": "Demra",
        "Postogola": "Postogola",
        "Jurain": "Jurain",
        "Dolaipar": "Dholaipar",
        "Babubazar": "Babubazar",
        "Nayabazar": "Nayabazar",
        "Azimpur": "Azimpur",
        "New Market": "New Market",
        "Science Lab": "Science Lab",
        "Nilkhet": "Nilkhet",
        "Dhaka College": "Dhaka College",
        "Kalabagan": "Kalabagan",
        "Dhanmondi": "Dhanmondi",
        "Jigatola": "Jigatola",
        "Mohammadpur": "Mohammadpur",
        "Adabor": "Adabor",
        "Shyamoli": "Shyamoli",
        "Kallyanpur": "Kallyanpur",
        "Mirpur": "Mirpur",
        "Pallabi": "Pallabi",
        "Kalshi": "Kalshi",
        "Bhashantek": "Bhashantek",
        "Cantonment": "Cantt",
        "Farmgate": "Farmgate",
        "Shahbagh": "Shahbagh",
        "Press Club": "Press Club",
        "Paltan": "Paltan",
        "Kakrail": "Kakrail",
        "Shantinagar": "Shantinagar",
        "Rajarbagh": "Rajarbagh",
        "Bishworoad": "Biswa Road"
    }

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    total_fixed = 0
    
    # 1. Direct replacements
    for old, new in fixes.items():
        c.execute("UPDATE stops SET name_en = ? WHERE name_en = ?", (new, old))
        total_fixed += c.rowcount

    # 2. Pattern based cleaning
    # Replace Bajar -> Bazar, Mod -> Mor, Srni -> Sarani, Bhiktorija -> Victoria
    patterns = {
        '%Bajar%': ('Bajar', 'Bazar'),
        '%Mod়%': ('Mod়', 'Mor'),
        '%Srni%': ('Srni', 'Sarani'),
        '%Bhiktorij়A%': ('Bhiktorij়A', 'Victoria'),
        '%Jnpth%': ('Jnpth', 'Janapath'),
        '%Biktorij়A%': ('Biktorij়A', 'Victoria')
    }

    for pattern, (old_sub, new_sub) in patterns.items():
        c.execute("SELECT id, name_en FROM stops WHERE name_en LIKE ?", (pattern,))
        rows = c.fetchall()
        for row_id, name_en in rows:
            new_name = name_en.replace(old_sub, new_sub)
            c.execute("UPDATE stops SET name_en = ? WHERE id = ?", (new_name, row_id))
            total_fixed += 1

    conn.commit()
    conn.close()
    print(f"Transliteration Fix Complete. Updated {total_fixed} stop names.")

if __name__ == "__main__":
    fix_transliterations()
