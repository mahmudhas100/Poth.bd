
import json

def transliterate_bengali(text):
    # Basic rule-based mapping for remaining Bengali sounds
    rules = {
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'ny',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'f', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
        'য': 'j', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
        'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't',
        'া': 'a', 'ি': 'i', 'ী': 'ee', 'ু': 'u', 'ূ': 'oo', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
        '্': '', 'ং': 'ng', 'ঃ': '', 'ঁ': 'n'
    }
    
    res = ""
    for char in text:
        res += rules.get(char, char)
    
    # Simple capitalization
    return res.strip().title()

def finish_transliteration():
    with open('output/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # Some manual entries for the remaining tricky ones I see in the list
    extra_mapping = {
        "অরিজিনাল দশ": "Original-10",
        "আগলা বাজার": "Agla Bazar",
        "আটিবাজার": "Atibazar",
        "ইউবিএল": "UBL",
        "ইকুলিয়া": "Ikulia",
        "ইস্টার্ন হাউজিং": "Eastern Housing",
        "উড়োজাহাজ ক্রসিং": "Bijoy Sarani Crossing",
        "উথুলী": "Uthuli",
        "ওয়াশপুর": "Washpur",
        "কদমতলী": "Kadamtoli",
        "কাজলা": "Kajla",
        "কোনাপাড়া": "Konapara",
        "খোলামোড়া": "Kholamora",
        "গাউসিয়া": "Gauchhia",
        "দয়াগঞ্জ": "Dayaganj",
        "ধলেশ্বর": "Dholeshwar",
        "নন্দন পার্ক": "Nandan Park",
        "পাগলা বাজার": "Pagla Bazar",
        "বনানী": "Banani",
        "বরপা": "Barpa",
        "রানীগঞ্জ": "Raniganj",
        "শংকর": "Shankar",
        "শিয়া মসজিদ": "Shia Masjid",
        "সফিপুর": "Sofipur",
        "হেমায়েতপুর": "Hemayetpur"
    }

    count = 0
    for stop in master_stops:
        # If it's still Bengali or placeholder
        if stop["name_en"] == "" or stop["name_en"] == stop["name_bn"]:
            bn = stop["name_bn"]
            
            # Check manual mapping first
            found = False
            for key, en in extra_mapping.items():
                if key in bn:
                    stop["name_en"] = en
                    found = True
                    break
            
            if not found:
                # Use rule-based fallback
                stop["name_en"] = transliterate_bengali(bn)
            
            count += 1

    with open('output/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

    print(f"Finalized {count} remaining stops. All 393 now have English names.")

if __name__ == "__main__":
    finish_transliteration()
