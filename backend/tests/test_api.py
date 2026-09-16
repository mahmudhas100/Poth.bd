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

