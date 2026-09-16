import re
from typing import List
from app.schemas.fare import FareResult, SuggestionResult, TransitLeg, TransitResult
from app.services.stop_service import resolve_stop_fuzzy, get_stop_names

def get_distance(c, route_id: int, stop1_id: int, stop2_id: int) -> float:
    c.execute("SELECT distance_km FROM route_stops WHERE route_id = ? AND stop_id = ?", (route_id, stop1_id))
    r1 = c.fetchone()
    c.execute("SELECT distance_km FROM route_stops WHERE route_id = ? AND stop_id = ?", (route_id, stop2_id))
    r2 = c.fetchone()
    
    if r1 and r2:
        return abs(r2['distance_km'] - r1['distance_km'])
    return 0.0

def get_intermediate_stops(c, route_id: int, stop1_id: int, stop2_id: int) -> List[str]:
    c.execute("SELECT stop_order FROM route_stops WHERE route_id = ? AND stop_id = ?", (route_id, stop1_id))
    order1 = c.fetchone()
    c.execute("SELECT stop_order FROM route_stops WHERE route_id = ? AND stop_id = ?", (route_id, stop2_id))
    order2 = c.fetchone()
    
    if not order1 or not order2:
        return []
        
    o1, o2 = order1[0], order2[0]
    min_o, max_o = min(o1, o2), max(o1, o2)
    
    c.execute("""
        SELECT s.name_bn
        FROM route_stops rs
        JOIN stops s ON rs.stop_id = s.id
        WHERE rs.route_id = ? AND rs.stop_order >= ? AND rs.stop_order <= ?
        ORDER BY rs.stop_order ASC
    """, (route_id, min_o, max_o))
    
    stops = [r[0] for r in c.fetchall()]
    if o1 > o2:
        stops.reverse()
    
    return stops

def format_route_name(c, route_name_raw: str, route_id: int) -> str:
    c.execute("""
        SELECT s.name_en 
        FROM route_stops rs
        JOIN stops s ON rs.stop_id = s.id
        WHERE rs.route_id = ? 
        ORDER BY rs.stop_order ASC
    """, (route_id,))
    stops = [r[0] for r in c.fetchall()]
    
    if stops and len(stops) >= 2:
        origin = stops[0]
        destination = stops[-1]

        match = re.search(r'\((এ-[০-৯\w]+(?:নং)?)\)', route_name_raw)
        route_num = match.group(1) if match else ""

        bn_to_en = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        route_num_en = route_num.translate(bn_to_en).replace('এ-', 'A-').replace('নং', '')

        suffix = f" ({route_num_en})" if route_num_en else ""
        return f"{origin} ⇄ {destination}{suffix}"
    
    return route_name_raw

def get_fare_amount(c, route_id: int, from_id: int, to_id: int, distance: float) -> int:
    c.execute("""
        SELECT fare_tk FROM fares 
        WHERE route_id = ? AND ((from_stop_id = ? AND to_stop_id = ?) OR (from_stop_id = ? AND to_stop_id = ?))
    """, (route_id, from_id, to_id, to_id, from_id))
    res = c.fetchone()
    if res:
        return res['fare_tk']
    
    if distance <= 0:
        return 0
    calculated = round(distance * 2.53)
    return max(10, calculated)

def calculate_fare_search(c, from_stop: str, to_stop: str):
    from_id = resolve_stop_fuzzy(from_stop)
    to_id = resolve_stop_fuzzy(to_stop)
    
    if not from_id or not to_id:
        return None, "Stop not recognized. Please check spelling."

    from_en, from_bn = get_stop_names(c, from_id)
    to_en, to_bn = get_stop_names(c, to_id)

    sql_direct_routes = """
        SELECT rs1.route_id, r.route_name
        FROM route_stops rs1
        JOIN route_stops rs2 ON rs1.route_id = rs2.route_id
        JOIN routes r ON rs1.route_id = r.id
        WHERE rs1.stop_id = ? AND rs2.stop_id = ?
        GROUP BY rs1.route_id
    """
    c.execute(sql_direct_routes, (from_id, to_id))
    rows = c.fetchall()
    
    direct_results = []
    for r in rows:
        dist = get_distance(c, r['route_id'], from_id, to_id)
        fare = get_fare_amount(c, r['route_id'], from_id, to_id, dist)
        clean_name = format_route_name(c, r['route_name'], r['route_id'])
        route_stops = get_intermediate_stops(c, r['route_id'], from_id, to_id)
        
        direct_results.append(FareResult(
            route_id=r['route_id'],
            route_name=clean_name,
            from_stop=from_en,
            from_stop_bn=from_bn,
            to_stop=to_en,
            to_stop_bn=to_bn,
            distance_km=round(dist, 2),
            fare=fare,
            stops=route_stops
        ))

    if direct_results:
        return direct_results, None

    # Suggestions Logic
    base_name = to_en.split()[0]
    if len(base_name) > 2:
        c.execute("SELECT id, name_en, name_bn FROM stops WHERE name_en LIKE ? AND id != ?", (f"{base_name}%", to_id))
        similar_stops = c.fetchall()
        
        suggestions = []
        for sim in similar_stops:
            sim_id = sim['id']
            c.execute(sql_direct_routes, (from_id, sim_id))
            sim_rows = c.fetchall()
            
            if sim_rows:
                r = sim_rows[0]
                dist = get_distance(c, r['route_id'], from_id, sim_id)
                fare = get_fare_amount(c, r['route_id'], from_id, sim_id, dist)
                clean_name = format_route_name(c, r['route_name'], r['route_id'])
                route_stops = get_intermediate_stops(c, r['route_id'], from_id, sim_id)
                
                suggestions.append(SuggestionResult(
                    original_stop=to_en,
                    suggested_stop=sim['name_en'],
                    suggested_stop_bn=sim['name_bn'],
                    message=f"'{to_bn}' এর সরাসরি বাস নেই, তবে '{sim['name_bn']}' এর সরাসরি বাস আছে।",
                    route=FareResult(
                        route_id=r['route_id'],
                        route_name=clean_name,
                        from_stop=from_en,
                        from_stop_bn=from_bn,
                        to_stop=sim['name_en'],
                        to_stop_bn=sim['name_bn'],
                        distance_km=round(dist, 2),
                        fare=fare,
                        stops=route_stops
                    )
                ))
        
        if suggestions:
            return suggestions[:3], None

    # Transit Search
    c.execute("SELECT DISTINCT route_id FROM route_stops WHERE stop_id = ?", (from_id,))
    routes_from = [r[0] for r in c.fetchall()]
    c.execute("SELECT DISTINCT route_id FROM route_stops WHERE stop_id = ?", (to_id,))
    routes_to = [r[0] for r in c.fetchall()]

    if not routes_from or not routes_to:
        return [], None

    query_transit = """
        SELECT DISTINCT stop_id FROM route_stops WHERE route_id IN ({})
        INTERSECT
        SELECT DISTINCT stop_id FROM route_stops WHERE route_id IN ({})
    """.format(','.join(map(str, routes_from)), ','.join(map(str, routes_to)))

    c.execute(query_transit)
    transfer_ids = [r[0] for r in c.fetchall() if r[0] not in [from_id, to_id]]

    transit_results = []
    seen_transits = set()

    for tp_id in transfer_ids:
        c.execute(sql_direct_routes, (from_id, tp_id))
        l1_routes = c.fetchall()
        c.execute(sql_direct_routes, (tp_id, to_id))
        l2_routes = c.fetchall()
        
        if l1_routes and l2_routes:
            tp_en, tp_bn = get_stop_names(c, tp_id)
            for l1 in l1_routes:
                for l2 in l2_routes:
                    transit_key = (l1['route_id'], l2['route_id'], tp_id)
                    if transit_key in seen_transits:
                        continue
                    seen_transits.add(transit_key)

                    d1 = get_distance(c, l1['route_id'], from_id, tp_id)
                    d2 = get_distance(c, l2['route_id'], tp_id, to_id)
                    
                    f1 = get_fare_amount(c, l1['route_id'], from_id, tp_id, d1)
                    f2 = get_fare_amount(c, l2['route_id'], tp_id, to_id, d2)
                    
                    name1 = format_route_name(c, l1['route_name'], l1['route_id'])
                    name2 = format_route_name(c, l2['route_name'], l2['route_id'])
                    
                    stops1 = get_intermediate_stops(c, l1['route_id'], from_id, tp_id)
                    stops2 = get_intermediate_stops(c, l2['route_id'], tp_id, to_id)
                    
                    leg1 = TransitLeg(
                        route_id=l1['route_id'],
                        route_name=name1,
                        from_stop=from_en,
                        from_stop_bn=from_bn,
                        to_stop=tp_en,
                        to_stop_bn=tp_bn,
                        distance_km=round(d1, 2),
                        fare=f1,
                        stops=stops1
                    )

                    leg2 = TransitLeg(
                        route_id=l2['route_id'],
                        route_name=name2,
                        from_stop=tp_en,
                        from_stop_bn=tp_bn,
                        to_stop=to_en,
                        to_stop_bn=to_bn,
                        distance_km=round(d2, 2),
                        fare=f2,
                        stops=stops2
                    )

                    transit_results.append(TransitResult(
                        transfer_at=tp_en,
                        transfer_at_bn=tp_bn,
                        total_distance_km=round(d1 + d2, 2),
                        total_fare=f1 + f2,
                        leg1=leg1,
                        leg2=leg2
                    ))

    transit_results.sort(key=lambda x: (x.total_fare, x.total_distance_km))
    return transit_results[:10], None
