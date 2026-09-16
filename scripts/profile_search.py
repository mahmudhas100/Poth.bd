
import time
import requests

def profile_search(from_stop, to_stop):
    start = time.time()
    try:
        response = requests.get(f"http://127.0.0.1:8000/search?from_stop={from_stop}&to_stop={to_stop}")
        end = time.time()
        print(f"Search '{from_stop}' -> '{to_stop}': {response.status_code} in {end - start:.4f}s")
        if response.status_code == 200:
            print(f"  Results: {len(response.json())}")
    except Exception as e:
        print(f"Search '{from_stop}' -> '{to_stop}' failed: {e}")

if __name__ == "__main__":
    # Test some likely transit routes
    profile_search("Airport", "Motijheel") # Direct
    profile_search("Abdullahpur", "Gabtoli") # Might be transit
    profile_search("Mirpur 10", "Jatrabari") # Likely transit
