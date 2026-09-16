import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app" in data

def test_get_stops():
    response = client.get("/stops")
    assert response.status_code == 200
    stops = response.json()
    assert isinstance(stops, list)
    assert len(stops) > 0
    assert "name_en" in stops[0]
    assert "name_bn" in stops[0]

def test_search_stops_filter():
    response = client.get("/stops?q=Mirpur")
    assert response.status_code == 200
    stops = response.json()
    assert len(stops) > 0
    assert any("mirpur" in s["name_en"].lower() for s in stops)

def test_direct_fare_search():
    response = client.get("/search?from_stop=Mirpur 10&to_stop=Farmgate")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    first = results[0]
    assert first["type"] == "direct"
    assert first["fare"] > 0
    assert first["distance_km"] > 0
    assert len(first["stops"]) >= 2

def test_transit_fare_search():
    response = client.get("/search?from_stop=Mohammadpur&to_stop=Sadarghat")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any(r["type"] == "transit" for r in results)

def test_suggestion_search():
    response = client.get("/search?from_stop=Uttara&to_stop=Asad Gate")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any(r["type"] == "suggestion" for r in results)

def test_fuzzy_bengali_search():
    response = client.get("/search?from_stop=ফার্মগেট&to_stop=মিরপুর-১০")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0

def test_invalid_stop_not_found():
    response = client.get("/search?from_stop=NowhereXYZ123&to_stop=Farmgate")
    assert response.status_code == 404

def test_stops_include_aliases():
    response = client.get("/stops")
    assert response.status_code == 200
    stops = response.json()
    mirpur10 = next((s for s in stops if s["name_en"] == "Mirpur-10"), None)
    assert mirpur10 is not None
    assert "aliases" in mirpur10
    assert any("mirpur 10" in a.lower() for a in mirpur10["aliases"])

def test_mirpur_hyphen_space_equivalence():
    response1 = client.get("/search?from_stop=Mirpur 10&to_stop=Gulshan 1")
    assert response1.status_code == 200
    response2 = client.get("/search?from_stop=Mirpur-10&to_stop=Gulshan-1")
    assert response2.status_code == 200
    assert len(response1.json()) == len(response2.json())

def test_bahadur_shah_park_alias_resolution():
    response = client.get("/search?from_stop=Bahadur Shah Park&to_stop=Airport")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any(r["type"] == "direct" for r in results)

def test_mirpur_12_to_sadarghat_direct():
    response = client.get("/search?from_stop=Mirpur-12&to_stop=Sadarghat")
    assert response.status_code == 200
    results = response.json()
    assert any(r["type"] == "direct" and r["route_id"] == 271 for r in results)

if __name__ == "__main__":
    tests = [
        test_health,
        test_root,
        test_get_stops,
        test_search_stops_filter,
        test_direct_fare_search,
        test_transit_fare_search,
        test_suggestion_search,
        test_fuzzy_bengali_search,
        test_invalid_stop_not_found,
        test_stops_include_aliases,
        test_mirpur_hyphen_space_equivalence,
        test_bahadur_shah_park_alias_resolution,
        test_mirpur_12_to_sadarghat_direct,
    ]

    passed = 0
    for t in tests:
        try:
            t()
            print(f"✓ {t.__name__} PASSED")
            passed += 1
        except Exception as e:
            print(f"✗ {t.__name__} FAILED: {e}")
            raise e
    print(f"\nAll {passed}/{len(tests)} tests passed successfully!")

