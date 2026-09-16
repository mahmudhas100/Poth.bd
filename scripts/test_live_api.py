
import requests

def test_live_api():
    try:
        response = requests.get("http://localhost:8000/search?from_stop=Airport&to_stop=Shyamoli")
        if response.status_code == 200:
            data = response.json()
            for r in data:
                print(f"Type: {r['type']} | Route: {r.get('route_name', 'Transit')} | Fare: ৳{r.get('fare', r.get('total_fare'))}")
                if r['type'] == 'transit':
                    print(f"  Leg 1: {r['leg1']['route_name']}")
                    print(f"  Leg 2: {r['leg2']['route_name']}")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Could not connect to API: {e}")

if __name__ == "__main__":
    test_live_api()
