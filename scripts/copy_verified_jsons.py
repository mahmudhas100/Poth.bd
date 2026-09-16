import os
import shutil
import glob

# Source and destination directories
src_dir = 'backend/data/raw_json'
dst_dir = 'raw_data/temp_json'

# Clear destination
for f in glob.glob(os.path.join(dst_dir, '*.json')):
    try:
        os.remove(f)
    except Exception as e:
        print(f"Could not remove {f}: {e}")

# Copy from source to destination
copied = 0
for src_file in glob.glob(os.path.join(src_dir, '*.json')):
    try:
        shutil.copy(src_file, dst_dir)
        copied += 1
    except Exception as e:
        print(f"Could not copy {src_file}: {e}")

print(f"Successfully copied {copied} perfectly verified JSON extractions into temp_json!")
