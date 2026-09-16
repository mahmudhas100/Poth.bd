
import json
import re

def gold_standard_transliteration():
    with open('data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # 1. High-Confidence Manual Map (The "Gold Standard")
    # This covers the examples user gave + common Dhaka areas
    gold_map = {
        "টঙ্গী": "Tongi",
        "বসিলা": "Basila",
        "বরপা": "Barpa",
        "উত্তরা": "Uttara",
        "বনানী": "Banani",
        "মিরপুর": "Mirpur",
        "মহাখালী": "Mohakhali",
        "ফার্মগেট": "Farmgate",
        "শাহবাগ": "Shahbag",
        "গুলিস্তান": "Gulistan",
        "মতিঝিল": "Motijheel",
        "আজিমপুর": "Azimpur",
        "মোহাম্মদপুর": "Mohammadpur",
        "শ্যামলী": "Shyamoli",
        "কল্যাণপুর": "Kalyanpur",
        "গাবতলী": "Gabtoli",
        "সাভার": "Savar",
        "বাড্ডা": "Badda",
        "রামপুরা": "Rampura",
        "বনশ্রী": "Banashree",
        "মালিবাগ": "Malibagh",
        "মৌচাক": "Mouchak",
        "কাকরাইল": "Kakrail",
        "মগবাজার": "Moghbazar",
        "পল্টন": "Paltan",
        "কমলাপুর": "Kamalapur",
        "সায়েদাবাদ": "Sayedabad",
        "যাত্রাবাড়ী": "Jatrabari",
        "কাজলা": "Kajla",
        "কোনাপাড়া": "Konapara",
        "দয়াগঞ্জ": "Dayaganj",
        "টিকাটুলি": "Tikatuli",
        "ধুপখোলা": "Dhupkhola",
        "কেরানীগঞ্জ": "Keraniganj",
        "পোস্তগোলা": "Postogola",
        "জুরাইন": "Jurain",
        "রায়েরবাগ": "Rayirbagh",
        "শনির আখড়া": "Shonir Akhra",
        "সাইনবোর্ড": "Signboard",
        "কাঁচপুর": "Kanchpur",
        "মদনপুর": "Modonpur",
        "মেঘনা": "Meghna",
        "সোনারগাঁও": "Sonargaon",
        "মাওয়া": "Mawa",
        "নারায়ণগঞ্জ": "Narayanganj",
        "চাষাড়া": "Chashara",
        "নবীনগর": "Nabinagar",
        "বাইপাইল": "Baipail",
        "চন্দ্রা": "Chandra",
        "গাজীপুর": "Gazipur",
        "কোনাবাড়ী": "Konabari",
        "শ্রীপুর": "Sreepur",
        "আব্দুল্লাহপুর": "Abdullahpur",
        "কামারপাড়া": "Kamarpara",
        "খিলক্ষেত": "Khilkhet",
        "কুড়িল": "Kuril",
        "নর্দা": "Norda",
        "বসুন্ধরা": "Bashundhara",
        "নতুন বাজার": "Notun Bazar",
        "গুডনিপ": "Gudnip",
        "বেরাইদ": "Beraid",
        "ভুলতা": "Bhulta",
        "গাউছিয়া": "Gauchhia",
        "রূপসী": "Ruposhi",
        "সফিপুর": "Sofipur",
        "হেমায়েতপুর": "Hemayetpur",
        "ধামরাই": "Dhamrai",
        "মানিকগঞ্জ": "Manikganj",
        "পাটুরিয়া": "Paturia",
        "ধউর": "Dhour",
        "আশুলিয়া": "Ashulia",
        "জসিমউদ্দীন": "Jasimuddin",
        "আজমপুর": "Azampur",
        "হাউজ বিল্ডিং": "House Building",
        "রাজলক্ষ্মী": "Rajlakshmi",
        "পল্লবী": "Pallabi",
        "দুয়ারীপাড়া": "Duwaripara",
        "কালশী": "Kalshi",
        "ইসিবি": "ECB",
        "আগারগাঁও": "Agargaon",
        "কাজীপাড়া": "Kazipara",
        "শেওড়াপাড়া": "Shewrapara",
        "বিজয় সরণী": "Bijoy Sarani",
        "খামারের মোড়": "Khamar Bari",
        "ধানমন্ডি": "Dhanmondi",
        "জিগাতলা": "Jigatola",
        "শংকর": "Shankar",
        "সোবহানবাগ": "Sobhanbagh",
        "কলাবাগান": "Kalabagan",
        "সায়েন্সল্যাব": "Science Lab",
        "নীলক্ষেত": "Nilkhet",
        "নিউ মার্কেট": "New Market",
        "ঢাকা কলেজ": "Dhaka College",
        "সিটি কলেজ": "City College",
        "শান্তিনগর": "Shantinagar",
        "মালিবাগ": "Malibagh",
        "খিলগাঁও": "Khilgaon",
        "বাসাবো": "Basabo",
        "মুগদা": "Mugda",
        "টিকাটুলি": "Tikatuli",
        "সাতরাস্তা": "Satrasta",
        "তিব্বত": "Tibet",
        "নাবিস্কো": "Nabisco",
        "কুর্মিটোলা": "Kurmitola",
        "জেনারেল হাসপাতাল": "General Hospital",
        "বিএমএ": "BMA",
        "উড়োজাহাজ ক্রসিং": "Bijoy Sarani Crossing",
        "বেড়িবাঁধ": "Beribandh",
        "ধলেশ্বরী": "Dhaleshwari",
        "আগলা": "Agla",
        "মাঝির কান্দা": "Majhir Kanda",
        "টিকরপুর": "Tikarpur",
        "রুহিতপুর": "Rohitpur",
        "কোণাখোলা": "Konakhola",
        "জিঞ্জিরা": "Zinjira",
        "নয়াবাজার": "Nayabazar",
        "বাবুবাজার": "Babu Bazar",
        "ভিক্টোরিয়া পার্ক": "Victoria Park",
        "সদরঘাট": "Sadarghat",
        "ফুলবাড়িয়া": "Fulbaria",
        "বঙ্গবন্ধু এভিনিউ": "Bangabandhu Avenue"
    }

    # 2. Word mapping for parts of names
    word_map = {
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
        "সিটি": "City",
        "মার্কেট": "Market",
        "সুপার": "Super",
        "বিশ্বরোড": "Biswa Road",
        "লিংক": "Link",
        "কোয়ার্টার": "Quarter",
        "পাড়া": "Para",
        "পাড়া": "Para",
        "বাস্তুহারা": "Bastuhara",
        "চৌরাস্তা": "Chowrasta",
        "ব্রীজ পাড়": "Bridge",
        "রেলগেট": "Railgate",
        "সরণী": "Sarani",
        "সরণি": "Sarani",
        "এয়ারপোর্ট": "Airport",
        "এয়ারপোর্ট": "Airport"
    }

    # 3. Phonetic mapping with inherent 'a'
    phonetic_map = {
        'ক': 'ka', 'খ': 'kha', 'গ': 'ga', 'ঘ': 'gha', 'ঙ': 'nga',
        'চ': 'cha', 'ছ': 'chha', 'জ': 'ja', 'ঝ': 'jha', 'ঞ': 'nya',
        'ট': 'ta', 'ঠ': 'tha', 'ড': 'da', 'ঢ': 'dha', 'ণ': 'na',
        'ত': 'ta', 'থ': 'tha', 'দ': 'da', 'ধ': 'dha', 'ন': 'na',
        'প': 'pa', 'ফ': 'pha', 'ব': 'ba', 'ভ': 'bha', 'ম': 'ma',
        'য': 'ja', 'র': 'ra', 'ল': 'la', 'শ': 'sha', 'ষ': 'sha', 'স': 'sa', 'হ': 'ha',
        'ড়': 'ra', 'ঢ়': 'rha', 'য়': 'ya', 'ৎ': 't',
        # Vowels
        'া': 'a', 'ি': 'i', 'ী': 'ee', 'ু': 'u', 'ূ': 'oo', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
        'ৃ': 'ri',
        # Modifiers
        '্': 'HASANT', # Mark for removing the inherent 'a'
        'ং': 'ng', 'ঃ': '', 'ঁ': 'n'
    }

    def phonetics_advanced(text):
        res = []
        for char in text:
            if char in phonetic_map:
                res.append(phonetic_map[char])
            else:
                res.append(char)
        
        s = "".join(res)
        # Apply hasant rule (remove previous 'a')
        s = s.replace("aHASANT", "")
        s = s.replace("HASANT", "") # Safe catch
        
        # Post-process common endings
        if s.endswith("aa"): s = s[:-1]
        
        return s.title()

    count = 0
    for stop in master_stops:
        bn = stop["name_bn"]
        
        # Try Gold Map first
        matched = False
        for k, v in gold_map.items():
            if k == bn: # Exact match
                stop["name_en"] = v
                matched = True
                break
        
        if not matched:
            # Try sub-string match from gold map (e.g., "উত্তরা ১২ নম্বর" -> "Uttara ...")
            for k, v in gold_map.items():
                if k in bn:
                    # Replace the known part
                    temp = bn.replace(k, v + " ")
                    # Process the rest
                    final_parts = []
                    for part in temp.split():
                        if part == v:
                            final_parts.append(part)
                        elif part in word_map:
                            final_parts.append(word_map[part])
                        elif re.search(r'[\u0980-\u09FF]', part):
                            final_parts.append(phonetics_advanced(part))
                        else:
                            final_parts.append(part)
                    stop["name_en"] = " ".join(final_parts).replace("  ", " ").strip()
                    matched = True
                    break
        
        if not matched:
            # Fallback to word_map + advanced phonetics
            temp = bn
            for k, v in word_map.items():
                temp = temp.replace(k, " " + v + " ")
            
            final_parts = []
            for part in temp.split():
                if part in word_map.values():
                    final_parts.append(part)
                elif re.search(r'[\u0980-\u09FF]', part):
                    final_parts.append(phonetics_advanced(part))
                else:
                    final_parts.append(part)
            
            stop["name_en"] = " ".join(final_parts).replace("  ", " ").strip()

        # Final cleanup
        stop["name_en"] = re.sub(r'([a-zA-Z])\1+', r'\1\1', stop["name_en"]) # Remove triple+ letters
        stop["name_en"] = stop["name_en"].title().replace("Tv", "TV").strip()
        count += 1

    with open('data/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

    print(f"Gold standard refinement complete. Fixed {count} stops.")

if __name__ == "__main__":
    gold_standard_transliteration()
