from typing import List, Optional
from fastapi import APIRouter, Query
from app.db.session import get_db
from app.schemas.fare import Stop

router = APIRouter()

@router.get("/stops", response_model=List[Stop])
async def get_stops(q: Optional[str] = Query(None, max_length=60)):
    with get_db() as conn:
        c = conn.cursor()
        
        # Load aliases grouped by stop_id
        c.execute("SELECT stop_id, alias_name FROM stop_aliases")
        alias_map = {}
        for row in c.fetchall():
            alias_map.setdefault(row['stop_id'], []).append(row['alias_name'])

        if q:
            c.execute("SELECT id, name_en, name_bn FROM stops WHERE name_en LIKE ? OR name_bn LIKE ?", (f'%{q}%', f'%{q}%'))
        else:
            c.execute("SELECT id, name_en, name_bn FROM stops ORDER BY name_en")
        
        stops_list = []
        for r in c.fetchall():
            stop_data = dict(r)
            stop_data['aliases'] = alias_map.get(r['id'], [])
            stops_list.append(stop_data)
            
        return stops_list
