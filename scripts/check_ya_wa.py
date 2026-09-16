
import json
with open('data/master_stops.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for s in data:
    if 'য়' in s['name_bn'] or 'ওয়া' in s['name_bn']:
        print(f"BN: {s['name_bn']} | EN: {s['name_en']}")
