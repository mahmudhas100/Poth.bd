try:
    from rapidfuzz import process
    HAS_RAPIDFUZZ = True
except ImportError:
    import difflib
    HAS_RAPIDFUZZ = False

from app.db.session import get_db

STOP_CACHE = {}  # name -> id
STOP_NAMES = []  # list of names for matching

def init_stop_cache():
    """Build the fuzzy search cache on application startup."""
    global STOP_CACHE, STOP_NAMES
    STOP_CACHE.clear()
    STOP_NAMES.clear()

    with get_db() as conn:
        c = conn.cursor()
        
        # Cache stops
        c.execute("SELECT id, name_en, name_bn FROM stops")
        for r in c.fetchall():
            name_en_low = r['name_en'].lower()
            STOP_CACHE[name_en_low] = r['id']
            STOP_CACHE[r['name_bn']] = r['id']
            STOP_NAMES.append(name_en_low)
            STOP_NAMES.append(r['name_bn'])
            
        # Cache aliases (only for valid existing stops)
        c.execute("""
            SELECT sa.stop_id, sa.alias_name 
            FROM stop_aliases sa 
            JOIN stops s ON sa.stop_id = s.id
        """)
        for r in c.fetchall():
            alias_low = r['alias_name'].lower()
            if alias_low not in STOP_CACHE:
                STOP_CACHE[alias_low] = r['stop_id']
                STOP_NAMES.append(alias_low)

    print(f"Stop Cache initialized. Cached {len(STOP_NAMES)} variations.")

def resolve_stop_fuzzy(query: str):
    if not STOP_CACHE:
        init_stop_cache()

    q = query.strip().lower()
    
    # 1. Direct Cache Hit
    if q in STOP_CACHE:
        return STOP_CACHE[q]

    # 2. Fuzzy Match
    if HAS_RAPIDFUZZ:
        match = process.extractOne(q, STOP_NAMES, score_cutoff=70)
        if match:
            return STOP_CACHE[match[0]]
    else:
        matches = difflib.get_close_matches(q, STOP_NAMES, n=1, cutoff=0.7)
        if matches:
            return STOP_CACHE[matches[0]]

    return None

def get_stop_names(c, stop_id: int):
    c.execute("SELECT name_en, name_bn FROM stops WHERE id = ?", (stop_id,))
    res = c.fetchone()
    return (res['name_en'], res['name_bn']) if res else ("Unknown", "অজানা")
