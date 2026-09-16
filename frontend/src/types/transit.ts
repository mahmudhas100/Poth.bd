export interface Stop {
  id: number;
  name_bn: string;
  name_en: string;
  aliases?: string[];
}

export interface TransitLeg {
  route_id: number;
  route_name: string;
  from_stop: string;
  from_stop_bn: string;
  to_stop: string;
  to_stop_bn: string;
  distance_km: number;
  fare: number;
  stops: string[];
}

export interface DirectFareResult {
  type: "direct";
  route_id: number;
  route_name: string;
  from_stop: string;
  from_stop_bn: string;
  to_stop: string;
  to_stop_bn: string;
  distance_km: number;
  fare: number;
  stops: string[];
}

export interface TransitResult {
  type: "transit";
  transfer_at: string;
  transfer_at_bn: string;
  total_distance_km: number;
  total_fare: number;
  leg1: TransitLeg;
  leg2: TransitLeg;
}

export interface SuggestionResult {
  type: "suggestion";
  original_stop: string;
  suggested_stop: string;
  suggested_stop_bn: string;
  message: string;
  route: DirectFareResult;
}

export type SearchResult = DirectFareResult | TransitResult | SuggestionResult;
