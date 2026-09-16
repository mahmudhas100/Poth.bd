import os
img_dir = "D:/Programming/Personal Projects/Bus Vara/raw_data/revised_images(2026)"
out_dir = "D:/Programming/Personal Projects/Bus Vara/raw_data/temp_json"
pngs = set([f for f in os.listdir(img_dir) if f.endswith('.png')])
valid_jsons = set()
if os.path.exists(out_dir):
    for f in os.listdir(out_dir):
        if f.endswith('.json'):
            p = os.path.join(out_dir, f)
            if os.path.getsize(p) > 100:
                name = f.replace('.json', '.png')
                if name.endswith('.png.png'):
                    name = name[:-4]
                valid_jsons.add(name)
missing = sorted(list(pngs - valid_jsons))
print("Missing:", len(missing))
for m in missing[:10]:
    print(m)
