from typing import List
from pydantic import BaseModel

class Stop(BaseModel):
    id: int
    name_bn: str
    name_en: str

class FareResult(BaseModel):
    type: str = "direct"
    route_id: int
    route_name: str
    from_stop: str
    from_stop_bn: str
    to_stop: str
    to_stop_bn: str
    distance_km: float
    fare: int
    stops: List[str] = []

class SuggestionResult(BaseModel):
    type: str = "suggestion"
    original_stop: str
    suggested_stop: str
    suggested_stop_bn: str
    message: str
    route: FareResult

class TransitLeg(BaseModel):
    route_id: int
    route_name: str
    from_stop: str
    from_stop_bn: str
    to_stop: str
    to_stop_bn: str
    distance_km: float
    fare: int
    stops: List[str] = []

class TransitResult(BaseModel):
    type: str = "transit"
    transfer_at: str
    transfer_at_bn: str
    total_distance_km: float
    total_fare: int
    leg1: TransitLeg
    leg2: TransitLeg
