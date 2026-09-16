
import json

def final_patch():
    with open('data/master_stops.json', 'r', encoding='utf-8') as f:
        master_stops = json.load(f)

    patches = {
        "নবীনগর": "Nabinagar",
        "সাভার": "Savar",
        "বাস্তুহারা": "Bastuhara",
        "গাউসিয়া": "Gausia",
        "চন্দ্রা": "Chandra",
        "ধামরাই": "Dhamrai",
        "সফিপুর": "Sofipur",
        "আশুলিয়া": "Ashulia",
        "বাইপাইল": "Baipail",
        "জিরাবো": "Jirabo",
        "ধউর": "Dhour",
        "আব্দুল্লাহপুর": "Abdullahpur",
        "কামারপাড়া": "Kamarpara",
        "মগবাজার": "Moghbazar",
        "মৌচাক": "Mouchak",
        "শান্তিনগর": "Shantinagar",
        "মালিবাগ": "Malibagh",
        "খিলগাঁও": "Khilgaon",
        "বাসাবো": "Basabo",
        "মুগদা": "Mugda",
        "সায়েদাবাদ": "Sayedabad",
        "যাত্রাবাড়ী": "Jatrabari",
        "টিকাটুলি": "Tikatuli",
        "দয়াগঞ্জ": "Dayaganj",
        "পোস্তগোলা": "Postogola",
        "কেরানীগঞ্জ": "Keraniganj",
        "জুরাইন": "Jurain",
        "রায়েরবাগ": "Rayirbagh",
        "নারায়নগঞ্জ": "Narayanganj",
        "চাষাড়া": "Chashara"
    }

    count = 0
    for stop in master_stops:
        bn = stop["name_bn"]
        for k, v in patches.items():
            if k in bn:
                # If it's a messy phonetic string, replace the whole thing or just the part
                if len(stop["name_en"]) > 2: # heuristic to avoid replacing empty
                    # Check if the current name_en looks like a mess
                    if any(x in stop["name_en"].lower() for x in ['nbin', 'sabhar', 'tnggi']):
                         stop["name_en"] = stop["name_en"].replace("Sabhar", "Savar").replace("Nbingr", "Nabinagar").replace("Tnggi", "Tongi")
        
        # Specific fixes from visual scan of verify_fixes.py
        if stop["name_bn"] == "নবীনগর (সাভার)": stop["name_en"] = "Nabinagar (Savar)"
        if stop["name_bn"] == "টঙ্গী(বাস্তুহারা)": stop["name_en"] = "Tongi (Bastuhara)"

    with open('data/master_stops.json', 'w', encoding='utf-8') as f:
        json.dump(master_stops, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    final_patch()
