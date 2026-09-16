import json

def calculate_fare(dist):
    fare = round(dist * 2.53)
    return max(10, fare)

pages = [
    {
        "source_file": "brta-part1.pdf", "source_page": 1,
        "route_name": "কালশী হতে কাঁচপুর ব্রীজ (এ-১০১নং)",
        "stops": ["কালশী", "মিরপুর-১২", "মিরপুর-১০", "কাজীপাড়া", "শেওড়াপাড়া", "ফার্মগেট", "শাহবাগ", "পল্টন", "গুলিস্তান", "টিকাটুলী", "সায়েদাবাদ", "যাত্রাবাড়ী", "সাইনবোর্ড", "কাঁচপুর ব্রীজ"],
        "distances_km": [0.0, 2.2, 4.9, 6.1, 6.8, 11.8, 13.9, 15.6, 16.6, 17.8, 18.9, 19.9, 24.8, 28.8]
    },
    {
        "source_file": "brta-part1.pdf", "source_page": 2,
        "route_name": "পল্লবী হতে সদরঘাট (এ-১০২নং)",
        "stops": ["পল্লবী (মিরপুর-১২)", "মিরপুর-১১ ৩/২", "বেকালী হোটেল", "মিরপুর-১১", "মিরপুর-১০", "কাজীপাড়া", "ফার্মগেট", "প্রেসক্লাব", "টিএন্ডটি", "রায়সাহেব বাজার", "ভিক্টোরিয়া পার্ক"],
        "distances_km": [0.0, 0.8, 0.9, 1.8, 2.3, 3.9, 8.0, 13.2, 14.9, 15.9, 16.9]
    },
    {
        "source_file": "brta-part1.pdf", "source_page": 3,
        "route_name": "পল্লবী (দুয়ারীপাড়া) হতে ঢাকেশ্বরী (এ-১০৫নং)",
        "stops": ["দুয়ারীপাড়া", "মিরপুর-১২", "মিরপুর সাড়ে ১১", "বেকালী হোটেল", "মিরপুর-১১", "মিরপুর-১০", "কাজীপাড়া", "শেওড়াপাড়া", "আগারগাঁও", "ধানমন্ডি", "শুক্রাবাদ", "ঢাকেশ্বরী মন্দির"],
        "distances_km": [0.0, 0.9, 1.3, 1.8, 2.3, 3.2, 4.6, 6.3, 9.0, 10.6, 11.1, 15.1]
    },
    {
        "source_file": "brta-part1.pdf", "source_page": 4,
        "route_name": "দুয়ারীপাড়া হতে ঢাকেশ্বরী (এ-১১০নং)",
        "stops": ["দুয়ারীপাড়া", "প্রশিকা", "মিরপুর থানা", "মিরপুর-১", "আনসারক্যাম্প", "টেকনিক্যাল", "আসাদগেট", "সায়েন্সল্যাব", "রুয়েট", "গুলিস্তান"],
        "distances_km": [0.0, 2.0, 2.8, 3.9, 4.6, 6.6, 9.1, 11.8, 14.9, 16.9]
    },
    {
        "source_file": "brta-part1.pdf", "source_page": 5,
        "route_name": "পল্লবী (সিরামিক) হতে দিলকুশা সোনালী ব্যাংক (এ-১১১নং)",
        "stops": ["পল্লবী (সিরামিক)", "মিরপুর-১১ ৩/২", "বেকালী হোটেল", "মিরপুর-১১", "মিরপুর-১০", "কাজীপাড়া", "ফার্মগেট", "পল্টন", "স্টেডিয়াম", "নটরডাম কলেজ"],
        "distances_km": [0.0, 0.9, 1.1, 1.6, 2.6, 3.9, 8.0, 13.6, 13.8, 17.0]
    }
]

output = []
for p in pages:
    route_data = {
        "source_file": p["source_file"],
        "source_page": p["source_page"],
        "route_name": p["route_name"],
        "stops": p["stops"],
        "distances_km": p["distances_km"],
        "fares": []
    }
    num_stops = len(p["stops"])
    for i in range(num_stops):
        for j in range(i + 1, num_stops):
            dist = abs(p["distances_km"][j] - p["distances_km"][i])
            fare = calculate_fare(dist)
            route_data["fares"].append({
                "from": p["stops"][i],
                "to": p["stops"][j],
                "fare": fare
            })
    output.append(route_data)

with open('patch_pages_1_5.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
