
import json
import re

def final_cleanup():
    with open('data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # Comprehensive character mapping to catch what the simple rules missed
    mapping = {
        'অ': 'O', 'আ': 'A', 'ই': 'I', 'ঈ': 'I', 'উ': 'U', 'ঊ': 'U', 'ঋ': 'Ri', 'এ': 'E', 'ঐ': 'Oi', 'ও': 'O', 'ঔ': 'Ou',
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'n',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'f', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
        'য': 'j', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
        'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't',
        'া': 'a', 'ি': 'i', 'ী': 'ee', 'ু': 'u', 'ূ': 'oo', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
        '্': '', 'ং': 'ng', 'ঃ': '', 'ঁ': 'n', 'ৃ': 'ri'
    }

    def clean_mixed(text):
        res = ""
        for char in text:
            if ord(char) > 127:
                res += mapping.get(char, '') # Replace if in map, else delete
            else:
                res += char
        return res

    count = 0
    for stop in master_stops:
        old_en = stop["name_en"]
        new_en = clean_mixed(old_en)
        
        # Post-processing
        new_en = new_en.replace("  ", " ").strip().title()
        
        # Apply specific rules one last time
        if "Tv" in new_en: new_en = new_en.replace("Tv", "TV")
        if "Bandar" in new_en: new_en = new_en.replace("Bandar", "bandar") # User said 'bandar' lowercase? Or just spelled that way. I'll use Title case since it's a name. 
        # User instruction: "for বন্দর, we use bandar". I'll use "Bandar" for consistent title casing unless it looks weird.
        
        if new_en != old_en:
            stop["name_en"] = new_en
            count += 1

    with open('data/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

    print(f"Final cleanup finished. Fixed {count} more strings.")

if __name__ == "__main__":
    final_cleanup()
