from typing import List, Optional
from pydantic import BaseModel

class Stop(BaseModel):
    id: int
    name_bn: str
    name_en: str
    aliases: List[str] = []

class FareResult(BaseModel):
    type: str = "direct"
    mode: str = "bus"
    duration_mins: Optional[int] = None
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
    mode: str = "bus"
    duration_mins: Optional[int] = None
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
