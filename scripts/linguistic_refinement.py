
import json
import re

def refine_transliteration():
    with open('data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # 1. Linguistic Overrides
    word_mapping = {
        "বন্দর": "bandar",
        "টিভি": "TV",
        "হাসপাতাল": "Hospital",
        "কলেজ": "College",
        "সিনেমা হল": "Cinema Hall",
        "হল": "Hall",
        "বাজার": "Bazar",
        "রোড": "Road",
        "গেট": "Gate",
        "গেইট": "Gate",
        "ব্রীজ": "Bridge",
        "ব্রিজ": "Bridge",
        "ব্যাংক": "Bank",
        "সেন্টার": "Center",
        "পার্ক": "Park",
        "ফ্লাইওভার": "Flyover",
        "মোড়": "More",
        "মোড়": "More",
        "চত্বর": "Chattar",
        "চতুর": "Chattar",
        "স্ট্যান্ড": "Stand",
        "স্ট্যাণ্ড": "Stand",
        "হাউজিং": "Housing",
        "এভিনিউ": "Avenue",
        "ক্রসিং": "Crossing",
        "জেনারেল": "General",
        "গার্ডেন": "Garden",
        "সিটি": "City",
        "স্কুল": "School",
        "মাজার": "Mazar",
        "পাবলিক": "Public",
        "ইউনিভার্সিটি": "University",
        "মেডিক্যাল": "Medical",
        "ক্লিনিক": "Clinic",
        "মার্কেট": "Market",
        "সুপার": "Super",
        "বিশ্বরোড": "Biswa Road",
        "লিংক": "Link",
        "কোয়ার্টার": "Quarter",
        "পাড়া": "Para",
        "পাড়া": "Para"
    }

    # 2. Phonetic Rules
    phonetic_rules = {
        'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y',
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'f', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
        'য': 'j', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
        'া': 'a', 'ি': 'i', 'ী': 'ee', 'ু': 'u', 'ূ': 'oo', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
        '্': '', 'ং': 'ng', 'ঃ': '', 'ঁ': 'n'
    }

    def phonetics(text):
        res = ""
        for char in text:
            res += phonetic_rules.get(char, char)
        return res.title()

    count = 0
    for stop in master_stops:
        bn = stop["name_bn"]
        en = bn
        
        # Priority 1: Check if the whole string is in a manual correction map (high confidence)
        manual_map = {
            "এয়ারপোর্ট": "Airport", "এয়ারপোর্ট": "Airport", "শ্যামলী": "Shyamoli", "আজিমপুর": "Azimpur",
            "মোহাম্মদপুর": "Mohammadpur", "মিরপুর": "Mirpur", "উত্তরা": "Uttara", "গাবতলী": "Gabtoli",
            "সাভার": "Savar", "মহাখালী": "Mohakhali", "বনানী": "Banani", "ফার্মগেট": "Farmgate",
            "শাহবাগ": "Shahbag", "গুলিস্তান": "Gulistan", "মতিঝিল": "Motijheel", "কাকরাইল": "Kakrail",
            "মৌচাক": "Mouchak", "মালিবাগ": "Malibagh", "রামপুরা": "Rampura", "বাড্ডা": "Badda"
        }
        
        if bn in manual_map:
            en = manual_map[bn]
        else:
            # Priority 2: Replace English words inside Bengali text
            temp_en = bn
            for bn_word, en_word in word_mapping.items():
                temp_en = temp_en.replace(bn_word, " " + en_word + " ")
            
            # Priority 3: Transliterate remaining parts
            final_parts = []
            for part in temp_en.split():
                if part in word_mapping.values():
                    final_parts.append(part)
                else:
                    # If it still contains Bengali, use phonetic rules
                    if re.search(r'[\u0980-\u09FF]', part):
                        final_parts.append(phonetics(part))
                    else:
                        final_parts.append(part)
            
            en = " ".join(final_parts).strip()
            # Clean up double spaces
            en = re.sub(r'\s+', ' ', en)

        # Apply specific rule for "ড়" -> "r" (redundant but safe)
        en = en.replace('ড়', 'r') 

        stop["name_en"] = en
        count += 1

    with open('data/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

    print(f"Refined {count} stops with linguistic rules.")

if __name__ == "__main__":
    refine_transliteration()
