try:
    from rapidfuzz import process
    HAS_RAPIDFUZZ = True
except ImportError:
    import difflib
    HAS_RAPIDFUZZ = False

from app.db.session import get_db

STOP_CACHE = {}  # name -> id
STOP_NAMES = []  # list of names for matching

BN_TO_EN = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
EN_TO_BN = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')

def normalize_key(text: str) -> str:
    """Normalize text by replacing hyphens, stripping punctuation and collapsing spaces."""
    import re
    t = text.lower().translate(BN_TO_EN)
    t = re.sub(r'[-_./(),&+\\]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

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
            sid = r['id']
            name_en_low = r['name_en'].lower()
            name_bn = r['name_bn']
            
            STOP_CACHE[name_en_low] = sid
            STOP_CACHE[name_bn] = sid
            STOP_NAMES.append(name_en_low)
            STOP_NAMES.append(name_bn)
            
            norm_en = normalize_key(name_en_low)
            if norm_en and norm_en not in STOP_CACHE:
                STOP_CACHE[norm_en] = sid
                STOP_NAMES.append(norm_en)
                
            norm_bn = normalize_key(name_bn)
            if norm_bn and norm_bn not in STOP_CACHE:
                STOP_CACHE[norm_bn] = sid
                STOP_NAMES.append(norm_bn)
            
        # Cache aliases (only for valid existing stops)
        c.execute("""
            SELECT sa.stop_id, sa.alias_name 
            FROM stop_aliases sa 
            JOIN stops s ON sa.stop_id = s.id
        """)
        for r in c.fetchall():
            sid = r['stop_id']
            alias_low = r['alias_name'].lower()
            if alias_low not in STOP_CACHE:
                STOP_CACHE[alias_low] = sid
                STOP_NAMES.append(alias_low)
            norm_alias = normalize_key(alias_low)
            if norm_alias and norm_alias not in STOP_CACHE:
                STOP_CACHE[norm_alias] = sid
                STOP_NAMES.append(norm_alias)

    print(f"Stop Cache initialized. Cached {len(STOP_NAMES)} variations.")

def resolve_stop_fuzzy(query: str):
    if not STOP_CACHE:
        init_stop_cache()

    q = query.strip().lower()
    if not q:
        return None
    
    # 1. Direct Hit
    if q in STOP_CACHE:
        return STOP_CACHE[q]

    # 2. Normalized Hit
    norm_q = normalize_key(q)
    if norm_q in STOP_CACHE:
        return STOP_CACHE[norm_q]

    # 3. Fuzzy Match
    if HAS_RAPIDFUZZ:
        match = process.extractOne(norm_q, STOP_NAMES, score_cutoff=70)
        if match:
            return STOP_CACHE[match[0]]
        match_raw = process.extractOne(q, STOP_NAMES, score_cutoff=70)
        if match_raw:
            return STOP_CACHE[match_raw[0]]
    else:
        matches = difflib.get_close_matches(norm_q, STOP_NAMES, n=1, cutoff=0.7)
        if matches:
            return STOP_CACHE[matches[0]]
        matches_raw = difflib.get_close_matches(q, STOP_NAMES, n=1, cutoff=0.7)
        if matches_raw:
            return STOP_CACHE[matches_raw[0]]

    return None

def get_stop_names(c, stop_id: int):
    c.execute("SELECT name_en, name_bn FROM stops WHERE id = ?", (stop_id,))
    res = c.fetchone()
    return (res['name_en'], res['name_bn']) if res else ("Unknown", "অজানা")
