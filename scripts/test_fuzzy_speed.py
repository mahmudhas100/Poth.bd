
import difflib
import time

STOP_NAMES = ["Stop " + str(i) for i in range(1200)]
q = "Stop 1199"

start = time.time()
matches = difflib.get_close_matches(q, STOP_NAMES, n=1, cutoff=0.7)
end = time.time()
print(f"difflib took: {end - start:.4f}s")

try:
    from rapidfuzz import process, utils
    start = time.time()
    matches = process.extractOne(q, STOP_NAMES, score_cutoff=70)
    end = time.time()
    print(f"rapidfuzz took: {end - start:.4f}s")
except ImportError:
    print("rapidfuzz not installed")
