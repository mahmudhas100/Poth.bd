
import json
import re

def super_fix():
    with open('data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # 1. Manual Corrections for specific major mistakes found in diagnostics
    hard_fixes = {
        "কমলাপুর স্টেশন": "Kamalapur Station",
        "মিরপুর-১": "Mirpur-1",
        "মিরপুর-১০": "Mirpur-10",
        "মিরপুর-১১": "Mirpur-11",
        "মিরপুর-১২": "Mirpur-12",
        "মিরপুর-১৪": "Mirpur-14",
        "মিরপুর (চিড়িয়াখানা)": "Mirpur Zoo",
        "চিড়িয়াখানা": "Zoo",
        "গুলশান-১": "Gulshan-1",
        "গুলশান-২": "Gulshan-2",
        "বাড্ডা লিংক রোড": "Badda Link Road",
        "মধ্য বাড্ডা": "Middle Badda",
        "উত্তর বাড্ডা": "North Badda",
        "রামপুরা ব্রিজ": "Rampura Bridge",
        "আমতলী": "Amtoli",
        "মোহাম্মদপুর": "Mohammadpur",
        "সৈনিক ক্লাব": "Soinik Club",
        "সনি সিনেমা হল": "Sony Cinema Hall",
        "মতিঝিল": "Motijheel",
        "নটরডেম কলেজ": "Notre Dame College",
        "শাপলা চত্বর": "Shapla Chattar"
    }

    # 2. Pattern Fixes
    word_replacements = {
        "Steshn": "Station",
        "Raod": "Road",
        "Breej": "Bridge",
        "Kolej": "College",
        "Kalaeja": "College",
        "Centar": "Center",
        "Bajer": "Bazar",
        "Bajar": "Bazar",
        "Bazaar": "Bazar",
        "Sinji": "CNG",
        "Sinaji": "CNG",
        "SaiএNajai": "CNG"
    }

    # 3. Handle the "Mirpur()" type failures
    def fix_string(s, bn):
        # Fix numbers
        s = s.replace("- ", "-")
        # Standardize words
        for k, v in word_replacements.items():
            s = s.replace(k, v)
        
        # If it looks like a failed translit with empty parens
        if "()" in s:
            # Fallback to manual if possible
            for k, v in hard_fixes.items():
                if k in bn: return v
            # Else clean it
            s = s.replace("()", "")
        
        # Fix trailing punctuation
        s = s.rstrip(":").rstrip(",")
        
        return s.strip()

    # Apply fixes
    for stop in master_stops:
        bn = stop["name_bn"]
        if bn in hard_fixes:
            stop["name_en"] = hard_fixes[bn]
        else:
            # Check substrings
            for k, v in hard_fixes.items():
                if k in bn:
                    stop["name_en"] = stop["name_en"].replace(stop["name_en"], v) # placeholder logic
            
            stop["name_en"] = fix_string(stop["name_en"], bn)

    # 4. MERGE DUPLICATES (e.g., Kalshi and Kalshi)
    merged = {}
    for stop in master_stops:
        # Create a unique key by name_en
        key = stop["name_en"].lower().replace(" ", "").replace("-", "")
        if key not in merged:
            merged[key] = stop
        else:
            # Merge aliases
            existing = merged[key]
            # Combine aliases and keep unique
            new_aliases = list(set(existing["aliases"] + stop["aliases"] + [stop["name_bn"]]))
            existing["aliases"] = new_aliases
            # Prefer the shorter name_bn if they differ slightly
            if len(stop["name_bn"]) < len(existing["name_bn"]):
                existing["name_bn"] = stop["name_bn"]

    final_list = list(merged.values())

    with open('data/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"Super Fix Complete. Reduced master list from {len(master_stops)} to {len(final_list)} unique locations.")

if __name__ == "__main__":
    super_fix()
