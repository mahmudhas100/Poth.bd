
import json
import re

def apply_user_rules():
    with open('data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # Specific manual overrides for words containing these patterns
    # to ensure they look like proper English
    overrides = {
        "ওয়া": "wa",
        "য়": "y",
        "ড়": "r"
    }

    # High-priority manual list for common Dhaka stops
    manual_gold = {
        "ওয়ারী": "Wari",
        "ওয়াশপুর": "Washpur",
        "দয়াগঞ্জ": "Dayaganj",
        "সায়দাবাদ": "Sayedabad",
        "সায়েদাবাদ": "Sayedabad",
        "দিয়াবাড়ী": "Diabari",
        "দিয়াবাড়ি": "Diabari",
        "চৌরাস্তা": "Chowrasta",
        "গাউসিয়া": "Gausiya",
        "ফুলবাড়িয়া": "Fulbaria",
        "বনানী": "Banani",
        "মহাখালী": "Mohakhali",
        "খিলক্ষেত": "Khilkhet"
    }

    def clean_en(en, bn):
        # 1. Check gold map first
        for k, v in manual_gold.items():
            if k in bn:
                # If the entire word is the key, replace entire EN
                if k == bn: return v
                # Else try to replace the part (heuristic)
                # But safer to just return a polished version of current EN if it's close
        
        # 2. Fix 'wa' and 'y' issues in existing EN
        # If BN has 'ওয়া', make sure EN has 'wa' instead of 'ya' or 'oya'
        if "ওয়া" in bn and "Wa" not in en:
            # Heuristic: replace the starting 'Y' or 'Oya'
            en = re.sub(r'^(Y|Oya)', 'Wa', en)
            en = en.replace("oyas", "was")
        
        # 3. If BN has 'য়', make sure EN uses 'y'
        if "য়" in bn and "y" not in en.lower():
            # If it used 'ia' or 'ja', change to 'ya'
            en = en.replace("ia", "ya").replace("ja", "ya")

        return en

    for stop in master_stops:
        bn = stop["name_bn"]
        en = stop["name_en"]
        
        # Apply the logic
        stop["name_en"] = clean_en(en, bn)
        
        # Final polish
        # Fix the "Jgnnath Bishbbidjaly" type ones
        if "Bishbbidjaly" in stop["name_en"]:
             stop["name_en"] = "Jagannath University"
        
        # Ensure title case
        stop["name_en"] = stop["name_en"].title().replace("Tv", "TV").replace("Cng", "CNG")

    with open('data/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

    print("User-defined transliteration rules applied.")

if __name__ == "__main__":
    apply_user_rules()
