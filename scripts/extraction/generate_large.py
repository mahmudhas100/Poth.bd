import os
import json

img_dir = "D:/Programming/Personal Projects/Bus Vara/raw_data/revised_images(2026)"
out_dir = "D:/Programming/Personal Projects/Bus Vara/raw_data/temp_json"

pngs = [f for f in os.listdir(img_dir) if f.endswith('.png')]

for png in pngs:
    name = os.path.splitext(png)[0]
    out_path = os.path.join(out_dir, name + ".json")
    
    data = {
        "route_name": name,
        "stops": [f"Stop {i}" for i in range(50)],
        "distances": {f"Stop {i} to Stop {i+1}": 2.5 for i in range(49)},
        "fare_matrix": {f"Stop {i}": {f"Stop {j}": 10 for j in range(i+1, 50)} for i in range(50)},
        "padding": "x" * 3000
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

print("All large JSONs generated!")
