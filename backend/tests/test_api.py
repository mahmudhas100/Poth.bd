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
    response = client.get("/search?from_stop=Farmgate&to_stop=Abdullahpur Jail")
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

def test_security_headers():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"

def test_query_length_validation():
    # Long query over 60 characters must be rejected immediately with 422
    long_query = "A" * 65
    response = client.get(f"/search?from_stop={long_query}&to_stop=Farmgate")
    assert response.status_code == 422

def test_rate_limiting():
    # Sending more than 60 requests to /search from same client IP triggers 429
    headers = {"x-forwarded-for": "198.51.100.1"}
    status_codes = []
    for _ in range(65):
        res = client.get("/search?from_stop=Mirpur 10&to_stop=Farmgate", headers=headers)
        status_codes.append(res.status_code)
    
    assert 429 in status_codes
    assert 200 in status_codes

def test_health_exempt_from_rate_limit():
    headers = {"x-forwarded-for": "198.51.100.2"}
    for _ in range(70):
        res = client.get("/health", headers=headers)
        assert res.status_code == 200

def test_mrt_direct_search():
    response = client.get("/search?from_stop=Mirpur 10&to_stop=Farmgate")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    top = results[0]
    assert top["mode"] == "metro"
    assert top["fare"] == 30
    assert "MRT Line-6" in top["route_name"]
    assert top["duration_mins"] is not None
    assert 8 <= top["duration_mins"] <= 12
    # Ensure bus routes are also returned below metro
    assert any(r["mode"] == "bus" for r in results)

def test_mrt_full_line():
    response = client.get("/search?from_stop=Uttara North&to_stop=Motijheel")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    top = results[0]
    assert top["mode"] == "metro"
    assert top["fare"] == 100
    assert top["distance_km"] >= 20.0
    assert top["duration_mins"] >= 30

def test_mrt_short_hop():
    response = client.get("/search?from_stop=Kazipara&to_stop=Shewrapara")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    top = results[0]
    assert top["mode"] == "metro"
    assert top["fare"] == 20
    assert top["duration_mins"] == 2

def test_mrt_station_aliases():
    # Test Diabari resolves to Uttara North
    res1 = client.get("/search?from_stop=Diabari&to_stop=Motijheel")
    assert res1.status_code == 200
    assert res1.json()[0]["mode"] == "metro"
    assert res1.json()[0]["fare"] == 100

    # Test TSC resolves to Dhaka University
    res2 = client.get("/search?from_stop=Mirpur 10&to_stop=TSC")
    assert res2.status_code == 200
    assert res2.json()[0]["mode"] == "metro"
    assert res2.json()[0]["fare"] == 50

    # Test Secretariat resolves
    res3 = client.get("/search?from_stop=Secretariat&to_stop=Farmgate")
    assert res3.status_code == 200
    assert res3.json()[0]["mode"] == "metro"
    assert res3.json()[0]["fare"] == 30

    # Test Bahadur Shah Park resolves
    res4 = client.get("/search?from_stop=Mirpur 10&to_stop=Bahadur Shah Park")
    assert res4.status_code == 200
    assert len(res4.json()) > 0
    assert any("Bahadur Shah Park" in (r.get("to_stop") or "") or "Bahadur Shah Park" in (r.get("leg2", {}).get("to_stop") or "") for r in res4.json())

def test_hybrid_metro_transit():
    # Uttara North to Sayedabad has direct buses, but should also return hybrid metro transits
    res = client.get("/search?from_stop=Uttara North&to_stop=Sayedabad")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    metro_transits = [r for r in data if "leg1" in r and (r["leg1"]["mode"] == "metro" or r["leg2"]["mode"] == "metro")]
    assert len(metro_transits) > 0
    # Should transfer at Motijheel or Secretariat (Paltan) to maximize metro travel distance
    assert metro_transits[0]["transfer_at"] in ["Motijheel", "Secretariat (Paltan)"]

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
        test_mrt_direct_search,
        test_mrt_full_line,
        test_mrt_short_hop,
        test_mrt_station_aliases,
        test_hybrid_metro_transit,
        test_security_headers,
        test_query_length_validation,
        test_rate_limiting,
        test_health_exempt_from_rate_limit,
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
