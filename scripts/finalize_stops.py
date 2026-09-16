
import json

def get_transliteration(bn_name):
    # Mapping for common Dhaka stops to ensure accuracy
    common_mapping = {
        "আজিমপুর": "Azimpur",
        "আসাদ গেট": "Asad Gate",
        "মহাখালী": "Mohakhali",
        "ফার্মগেট": "Farmgate",
        "শাহবাগ": "Shahbag",
        "গুলিস্তান": "Gulistan",
        "মতিঝিল": "Motijheel",
        "উত্তরা": "Uttara",
        "এয়ারপোর্ট": "Airport",
        "গাবতলী": "Gabtoli",
        "সাভার": "Savar",
        "বনানী": "Banani",
        "মগবাজার": "Moghbazar",
        "কাকরাইল": "Kakrail",
        "পল্টন": "Paltan",
        "শ্যামলী": "Shyamoli",
        "কল্যাণপুর": "Kalyanpur",
        "টেকনিক্যাল": "Technical",
        "মিরপুর": "Mirpur",
        "টঙ্গী": "Tongi",
        "নতুন বাজার": "Notun Bazar",
        "বসুন্ধরা": "Bashundhara",
        "কুড়িল": "Kuril",
        "খিলক্ষেত": "Khilkhet",
        "মৌচাক": "Mouchak",
        "মালিবাগ": "Malibagh",
        "বনশ্রী": "Banashree",
        "মোহাম্মদপুর": "Mohammadpur",
        "ধানমন্ডি": "Dhanmondi",
        "সাইন্সল্যাব": "Science Lab",
        "বাড্ডা": "Badda",
        "রামপুরা": "Rampura",
        "যাত্রাবাড়ী": "Jatrabari",
        "সায়েদাবাদ": "Sayedabad",
        "কমলাপুর": "Kamalapur",
        "টিকাটুলি": "Tikatuli",
        "সাতরাস্তা": "Satrasta",
        "কাকলী": "Kakoli",
        "বসিলা": "Basila",
        "নবীনগর": "Nabinagar",
        "বাইপাইল": "Baipail",
        "চন্দ্রা": "Chandra",
        "ইপিজেড": "EPZ",
        "সাভার": "Savar",
        "গাজীপুর": "Gazipur",
        "কোনাবাড়ী": "Konabari",
        "শ্রীপুর": "Sreepur",
        "মাওয়া": "Mawa",
        "নারায়ণগঞ্জ": "Narayanganj",
        "চাষাড়া": "Chashara",
        "সাইনবোর্ড": "Signboard",
        "কাঁচপুর": "Kanchpur",
        "মদনপুর": "Modonpur",
    }
    
    # Check common mapping first
    for key, val in common_mapping.items():
        if key in bn_name:
            return val
            
    # Fallback logic would go here, but I will provide a best-effort transcription
    # during the loop for the rest.
    return None

def finalize_master_stops():
    with open('output/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    # Note: I am manually providing translations here for the most common ones 
    # to ensure high quality results for the demo.
    
    mapping_data = {
        "আজিমপুর": "Azimpur", "আসাদ গেট": "Asad Gate", "মহাখালী": "Mohakhali", "ফার্মগেট": "Farmgate",
        "শাহবাগ": "Shahbag", "গুলিস্তান": "Gulistan", "মতিঝিল": "Motijheel", "উত্তরা": "Uttara",
        "এয়ারপোর্ট": "Airport", "গাবতলী": "Gabtoli", "সাভার": "Savar", "বনানী": "Banani",
        "মগবাজার": "Moghbazar", "কাকরাইল": "Kakrail", "পল্টন": "Paltan", "শ্যামলী": "Shyamoli",
        "কল্যাণপুর": "Kalyanpur", "টেকনিক্যাল": "Technical", "মিরপুর-১০": "Mirpur-10",
        "মিরপুর-১": "Mirpur-1", "টঙ্গী": "Tongi", "নতুন বাজার": "Notun Bazar", "বসুন্ধরা": "Bashundhara",
        "কুড়িল": "Kuril", "খিলক্ষেত": "Khilkhet", "মৌচাক": "Mouchak", "মালিবাগ": "Malibagh",
        "বনশ্রী": "Banashree", "মোহাম্মদপুর": "Mohammadpur", "ধানমন্ডি": "Dhanmondi",
        "সাইন্সল্যাব": "Science Lab", "বাড্ডা": "Badda", "রামপুরা": "Rampura", "যাত্রাবাড়ী": "Jatrabari",
        "সায়েদাবাদ": "Sayedabad", "কমলাপুর": "Kamalapur", "টিকাটুলি": "Tikatuli", "সাতরাস্তা": "Satrasta",
        "কাকলী": "Kakoli", "বসিলা": "Basila", "নবীনগর": "Nabinagar", "বাইপাইল": "Baipail",
        "চন্দ্রা": "Chandra", "ইপিজেড": "EPZ", "গাজীপুর": "Gazipur", "কোনাবাড়ী": "Konabari",
        "মাওয়া": "Mawa", "নারায়ণগঞ্জ": "Narayanganj", "চাষাড়া": "Chashara", "সাইনবোর্ড": "Signboard",
        "কাঁচপুর": "Kanchpur", "মদনপুর": "Modonpur", "সনি সিনেমা হল": "Sony Cinema Hall",
        "কালশী": "Kalshi", "ইসিবি চত্বর": "ECB Chattar", "শেওড়াপাড়া": "Shewrapara",
        "কাজীপাড়া": "Kazipara", "আগারগাঁও": "Agargaon", "বিজয় সরণী": "Bijoy Sarani",
        "ঢাকা কলেজ": "Dhaka College", "সিটি কলেজ": "City College", "নিউ মার্কেট": "New Market",
        "নীলক্ষেত": "Nilkhet", "সোহরাওয়ার্দী হাসপাতাল": "Suhrawardy Hospital", "শিশুমেলা": "Shishumela",
        "কলেজ গেট": "College Gate", "শ্যামলী রিং রোড": "Shyamoli Ring Road",
        "জিগাতলা": "Jigatola", "শংকর": "Shankar", "টাউন হল": "Town Hall", "আসাদ এভিনিউ": "Asad Avenue",
        "মোহাম্মদপুর বাস স্ট্যান্ড": "Mohammadpur Bus Stand", "বেরাইদ": "Beraid", "গুডনিপ": "Gudnip",
        "ধউর": "Dhour", "আব্দুল্লাহপুর": "Abdullahpur", "কামারপাড়া": "Kamarpara",
        "জসিমউদ্দীন": "Jasimuddin", "আজমপুর": "Azampur", "হাউজ বিল্ডিং": "House Building",
        "রাজলক্ষ্মী": "Rajlakshmi", "নর্দা": "Norda", "পুরবী": "Purabi", "অরিজিনাল-১০": "Original-10",
        "মিরপুর-২": "Mirpur-2", "মিরপুর-১১": "Mirpur-11", "মিরপুর-১২": "Mirpur-12",
        "মিরপুর-১৪": "Mirpur-14", "পল্লবী": "Pallabi", "দুয়ারীপাড়া": "Duwaripara",
        "কালশী মোড়": "Kalshi More", "জিল্লুর রহমান ফ্লাইওভার": "Zillur Rahman Flyover",
        "যমুনা ফিউচার পার্ক": "Jamuna Future Park", "প্রগতি সরণী": "Progoti Sarani",
        "নতুন বাজার": "Notun Bazar", "বাড্ডা": "Badda", "রামপুরা টিভি সেন্টার": "Rampura TV Center",
        "আবুল হোটেল": "Abul Hotel", "রাজমনি": "Rajmoni", "স্টেডিয়াম": "Stadium", "ফুলবাড়িয়া": "Fulbaria",
        "বাবু বাজার": "Babu Bazar", "কেরানীগঞ্জ": "Keraniganj", "পোস্তগোলা": "Postogola",
        "জুরাইন": "Jurain", "দয়াগঞ্জ": "Dayaganj", "ধুপখোলা": "Dhupkhola", "টিকাটুলি": "Tikatuli",
        "সায়দাবাদ": "Sayedabad", "জনপথ": "Jonopath", "রায়েরবাগ": "Rayirbagh", "শনির আখড়া": "Shonir Akhra",
        "মেঘনা ঘাট": "Meghna Ghat", "সোনারগাঁও": "Sonargaon", "মদনপুর": "Modonpur",
        "কাঁচপুর ব্রীজ": "Kanchpur Bridge", "তারাবো": "Tarabo", "সুলতানা কামাল ব্রীজ": "Sultana Kamal Bridge",
        "ডেমরা": "Demra", "স্টাফ কোয়ার্টার": "Staff Quarter", "মেরাদিয়া": "Meradia",
        "বনশ্রী": "Banashree", "মৌচাক": "Mouchak", "শান্তিনগর": "Shantinagar", "মগবাজার": "Moghbazar",
        "বাংলামটর": "Banglamotor", "কাওরান বাজার": "Kawran Bazar", "ফার্মগেট": "Farmgate",
        "মানিক মিয়া এভিনিউ": "Manik Mia Avenue", "সায়েন্সল্যাব": "Science Lab",
        "আজিমপুর": "Azimpur", "বকশিবাজার": "Bakshibazar", "চানখারপুল": "Chankharpul",
        "গুলিস্তান": "Gulistan", "ফুলবাড়ীয়া": "Fulbaria", "নয়াবাজার": "Nayabazar",
        "জিঞ্জিরা": "Zinjira", "কোণাখোলা": "Konakhola", "রুহিতপুর": "Rohitpur", "টিকরপুর": "Tikarpur",
        "কোমরগঞ্জ": "Komorganj", "বান্দুরা": "Bandura", "বারুয়াখালী": "Baruakhali",
        "খাসিয়াখালী": "Khasiakhali", "বেড়িবাঁধ": "Beribandh", "নবাবগঞ্জ": "Nawabganj",
        "মাঝির কান্দা": "Majhir Kanda", "আগলা বাজার": "Agla Bazar", "বক্সনগর": "Boxnagar",
        "শুরগঞ্জ": "Shurganj", "বামনরা": "Bamonra", "খারশুর": "Kharshur", "সৈয়দপুর": "Syedpur",
        "রামের কান্দা": "Ramer Kanda", "ভুলতা": "Bhulta", "গাউছিয়া": "Gauchhia",
        "রূপসী": "Ruposhi", "বরপা": "Barpa", "কালামপুর": "Kalampur", "ধামরাই": "Dhamrai",
        "মানিকগঞ্জ": "Manikganj", "পাটুরিয়া": "Paturia", "সফিপুর": "Sofipur", "মাওয়াঘাট": "Mawaghat"
    }

    count = 0
    for stop in master_stops:
        bn = stop["name_bn"]
        # Try to find a match in the manual mapping
        for key, en in mapping_data.items():
            if key in bn:
                stop["name_en"] = en
                count += 1
                break
        
        # If still empty, use a placeholder or basic translit rule
        if not stop["name_en"]:
            stop["name_en"] = bn # Fallback to Bengali if no translation found

    with open('output/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

    print(f"Transliterated {count} out of {len(master_stops)} stops.")

if __name__ == "__main__":
    finalize_master_stops()
