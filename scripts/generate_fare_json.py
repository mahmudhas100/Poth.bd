import json, math, sys

def generate_json(route_name, stops, distances, src_file, src_page, rate=2.53, min_fare=10):
    fares = []
    for i in range(len(stops)):
        for j in range(i + 1, len(stops)):
            dist = abs(distances[j] - distances[i])
            fare = math.floor(dist * rate + 0.5)
            if fare < min_fare:
                fare = min_fare
            fares.append({"from": stops[i], "to": stops[j], "fare": int(fare)})
    
    return {
        "source_file": src_file,
        "source_page": src_page,
        "route_name": route_name,
        "stops": stops,
        "distances_km": distances,
        "fares": fares
    }

if __name__ == "__main__":
    # Example usage via command line or just import it
    pass
