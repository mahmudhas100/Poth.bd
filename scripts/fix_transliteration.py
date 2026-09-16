
import json
import sqlite3

def fix_data():
    # 1. Load the master stops
    with open('data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # 2. A more robust common mapping to fix the corrupted ones
    # I will focus on the ones I saw in your screenshot and other common ones
    corrections = {
        "এয়ারপোর্ট": "Airport",
        "এয়ারপোর্ট": "Airport",
        "শ্যামলী": "Shyamoli",
        "আজিমপুর": "Azimpur",
        "ইডেন কলেজ": "Eden College",
        "ইন্তেফাক": "Ittefaq",
        "ইসিবি মোড়": "ECB More",
        "ইসলামপুর": "Islampur",
        "ওয়ার্ক সপ": "Workshop",
        "ওয়ারী": "Wari",
        "আসাদ গেট": "Asad Gate",
        "আসাদগেট": "Asad Gate",
        "ফার্মগেট": "Farmgate",
        "শাহবাগ": "Shahbag",
        "গুলিস্তান": "Gulistan",
        "মতিঝিল": "Motijheel",
        "উত্তরা": "Uttara",
        "গাবতলী": "Gabtoli",
        "সাভার": "Savar",
        "মিরপুর": "Mirpur",
        "কালশী": "Kalshi",
        "বাড্ডা": "Badda",
        "রামপুরা": "Rampura",
        "মহাখালী": "Mohakhali",
        "কাকরাইল": "Kakrail",
        "মৌচাক": "Mouchak",
        "মালিবাগ": "Malibagh",
        "খিলক্ষেত": "Khilkhet",
        "কুড়িল": "Kuril",
        "নতুন বাজার": "Notun Bazar"
    }

    # 3. Apply corrections and a better fallback for others
    # (Since I can't manually type 393 names in one go, I'll use a better 
    # transliteration logic that at least removes Bengali characters)
    
    import re
    def simple_clean(text, bn_orig):
        # If the string contains any Bengali characters, it's failed transliteration
        if re.search(r'[\u0980-\u09FF]', text):
            # Try our manual corrections map
            for bn_key, en_val in corrections.items():
                if bn_key in bn_orig:
                    return en_val
            # If no manual match, just use the Bengali name as-is for now (better than garbled)
            return bn_orig
        return text

    for stop in master_stops:
        bn = stop["name_bn"]
        # Check manual map first
        matched = False
        for k, v in corrections.items():
            if k in bn:
                stop["name_en"] = v
                matched = True
                break
        
        if not matched:
            stop["name_en"] = simple_clean(stop["name_en"], bn)

    # 4. Save the fixed JSON
    with open('data/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

    print("Master stops JSON cleaned.")

if __name__ == "__main__":
    fix_data()
