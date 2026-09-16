import json

def calculate_fare(dist, rate=2.53, min_fare=10):
    if dist == 0: return 0
    fare = int(dist * rate + 0.5)
    return max(fare, min_fare)

data = []

# Page 8
stops_8 = ["শিয়ালবাড়ী", "অরিজিনাল দশ", "পূরবী", "কালশী মোড়", "মোঃ জিল্লুর রহমান ফ্লাইওভার", "কাকলী", "মহাখালী", "সাতরাস্তা", "মগবাজার", "মালিবাগ", "কাকরাইল", "ফকিরাপুল", "কমলাপুর (পীরজঙ্গী মাজার)"]
dist_8 = [0.0, 2.0, 3.0, 6.3, 9.8, 11.8, 13.6, 15.8, 17.3, 18.3, 19.3, 20.3, 21.3]
fares_8 = []
for i in range(len(stops_8)):
    for j in range(i + 1, len(stops_8)):
        d = abs(dist_8[j] - dist_8[i])
        fares_8.append({"from": stops_8[i], "to": stops_8[j], "fare": calculate_fare(d)})
data.append({
    "source_file": "brta-part4.pdf",
    "source_page": 8,
    "route_name": "শিয়ালবাড়ী হতে কমলাপুর (পীরজঙ্গী মাজার) (এ-৩৮০নং)",
    "stops": stops_8,
    "distances_km": dist_8,
    "fares": fares_8
})

# Page 9
stops_9 = ["গুলিস্তান", "ডেমরা", "রূপসী", "বরপা", "ভুলতা (গাউছিয়া)"]
dist_9 = [0.0, 9.5, 13.7, 15.1, 20.6]
fares_9 = []
for i in range(len(stops_9)):
    for j in range(i + 1, len(stops_9)):
        d = abs(dist_9[j] - dist_9[i])
        fares_9.append({"from": stops_9[i], "to": stops_9[j], "fare": calculate_fare(d)})
data.append({
    "source_file": "brta-part4.pdf",
    "source_page": 9,
    "route_name": "গুলিস্তান হতে ভুলতা (গাউছিয়া) (এ-৩৮১নং)",
    "stops": stops_9,
    "distances_km": dist_9,
    "fares": fares_9
})

# Page 10
stops_10 = ["সাইনবোর্ড", "মেয়র মোহাম্মদ ফ্লাইওভার", "চানখারপুল", "আজিমপুর", "নিউমার্কেট", "গাবতলী", "সাভার", "নবীনগর", "ইপিজেড", "জিরানী", "নন্দনপার্ক"]
dist_10 = [0.0, 4.0, 9.3, 11.3, 12.1, 19.7, 34.1, 42.5, 47.0, 52.0, 56.5]
fares_10 = []
for i in range(len(stops_10)):
    for j in range(i + 1, len(stops_10)):
        d = abs(dist_10[j] - dist_10[i])
        fares_10.append({"from": stops_10[i], "to": stops_10[j], "fare": calculate_fare(d)})
data.append({
    "source_file": "brta-part4.pdf",
    "source_page": 10,
    "route_name": "সাইনবোর্ড হতে নন্দনপার্ক (এ-৩৮৪নং)",
    "stops": stops_10,
    "distances_km": dist_10,
    "fares": fares_10
})

# Page 11
stops_11 = ["মদনপুর", "কাঁচপুর", "ডেমরা", "মেরাদিয়া বাজার", "বনশ্রী", "রামপুরা ব্রীজ", "যমুনা ফিউচার পার্ক", "কুড়িল", "ইসিবি চত্বর", "কালশি", "মিরপুর-১০", "মিরপুর-১", "গাবতলী", "হেমায়েতপুর", "সাভার", "ইপিজেড", "নন্দন পার্ক"]
dist_11 = [0.0, 4.0, 9.0, 15.6, 17.6, 18.6, 23.8, 24.8, 28.4, 30.3, 35.2, 37.0, 40.1, 48.1, 54.8, 68.0, 78.6]
fares_11 = []
for i in range(len(stops_11)):
    for j in range(i + 1, len(stops_11)):
        d = abs(dist_11[j] - dist_11[i])
        fares_11.append({"from": stops_11[i], "to": stops_11[j], "fare": calculate_fare(d)})
data.append({
    "source_file": "brta-part4.pdf",
    "source_page": 11,
    "route_name": "মদনপুর হতে নন্দনপার্ক (এ-৩৮৬নং)",
    "stops": stops_11,
    "distances_km": dist_11,
    "fares": fares_11
})

# Page 12
stops_12 = ["কালামপুর", "ধামরাই", "নবীনগর", "সাভার", "হেমায়েতপুর", "গাবতলী", "আসাদগেট", "ফার্মগেট", "শাহবাগ", " প্রেসক্লাব", "গুলিস্তান", "ভিক্টোরিয়া পার্ক"]
dist_12 = [0.0, 3.3, 11.5, 19.5, 27.5, 33.0, 38.0, 40.0, 43.0, 47.0, 47.5, 49.5]
fares_12 = []
for i in range(len(stops_12)):
    for j in range(i + 1, len(stops_12)):
        d = abs(dist_12[j] - dist_12[i])
        fares_12.append({"from": stops_12[i], "to": stops_12[j], "fare": calculate_fare(d)})
data.append({
    "source_file": "brta-part4.pdf",
    "source_page": 12,
    "route_name": "কালামপুর হতে ভিক্টোরিয়াপার্ক (এ-৩৮৭নং)",
    "stops": stops_12,
    "distances_km": dist_12,
    "fares": fares_12
})

# Page 13
stops_13 = ["সাভার", "হেমায়েতপুর", "গাবতলী", "টেকনিক্যাল", "মিরপুর-২", "মিরপুর-১১", "কালশি", "মোঃ জিল্লুর রাহমান ফ্লাইওভার", "শেওড়া", "কুড়িল ফ্লাইওভার", "নর্দা", "বেরাইদ"]
dist_13 = [0.0, 6.6, 14.2, 15.0, 18.2, 19.8, 23.6, 25.8, 27.8, 28.8, 30.1, 37.4]
fares_13 = []
for i in range(len(stops_13)):
    for j in range(i + 1, len(stops_13)):
        d = abs(dist_13[j] - dist_13[i])
        fares_13.append({"from": stops_13[i], "to": stops_13[j], "fare": calculate_fare(d)})
data.append({
    "source_file": "brta-part4.pdf",
    "source_page": 13,
    "route_name": "সাভার হতে বেরাইদ (এ-৩৯৩নং)",
    "stops": stops_13,
    "distances_km": dist_13,
    "fares": fares_13
})

# Page 14
stops_14 = ["ঘাটার চর", "বসিলা", "মোহাম্মদপুর", "শংকর", "শ্যামলী", "ধানমন্ডি", "জিগাতলা", "সাইন্সল্যাবঃ", "শাহবাগ", "প্রেসক্লাব", "গুলিস্তান", "হানিফ ফ্লাইওভার", "শনির আখড়া", "রায়েরবাগ", "কাঁচপুর", "মদনপুর", "সোনারগাঁও"]
dist_14 = [0.0, 2.8, 4.3, 6.3, 6.8, 7.3, 8.3, 10.3, 11.3, 12.3, 14.3, 14.8, 19.3, 20.3, 27.3, 30.3, 39.4]
fares_14 = []
for i in range(len(stops_14)):
    for j in range(i + 1, len(stops_14)):
        d = abs(dist_14[j] - dist_14[i])
        fares_14.append({"from": stops_14[i], "to": stops_14[j], "fare": calculate_fare(d)})
data.append({
    "source_file": "brta-part4.pdf",
    "source_page": 14,
    "route_name": "ঘাটার চর হতে সোনারগাঁও (এ-৪০৬নং)",
    "stops": stops_14,
    "distances_km": dist_14,
    "fares": fares_14
})

with open('patch_part4_8_14.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
