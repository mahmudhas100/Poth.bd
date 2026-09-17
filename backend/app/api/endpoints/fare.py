from typing import List, Union
from fastapi import APIRouter, HTTPException, Query
from app.db.session import get_db
from app.schemas.fare import FareResult, TransitResult, SuggestionResult
from app.services.fare_service import calculate_fare_search

router = APIRouter()

@router.get("/search", response_model=List[Union[FareResult, TransitResult, SuggestionResult]])
async def search_fare(
    from_stop: str = Query(..., min_length=1, max_length=60, description="Origin stop name"),
    to_stop: str = Query(..., min_length=1, max_length=60, description="Destination stop name")
):
    with get_db() as conn:
        c = conn.cursor()
        results, err = calculate_fare_search(c, from_stop, to_stop)
        
        if err:
            raise HTTPException(status_code=404, detail=err)
            
        return results
