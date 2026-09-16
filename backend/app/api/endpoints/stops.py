from typing import List, Optional
from fastapi import APIRouter
from app.db.session import get_db
from app.schemas.fare import Stop

router = APIRouter()

@router.get("/stops", response_model=List[Stop])
async def get_stops(q: Optional[str] = None):
    with get_db() as conn:
        c = conn.cursor()
        if q:
            c.execute("SELECT * FROM stops WHERE name_en LIKE ? OR name_bn LIKE ?", (f'%{q}%', f'%{q}%'))
        else:
            c.execute("SELECT * FROM stops ORDER BY name_en")
        rows = c.fetchall()
        return [dict(r) for r in rows]
