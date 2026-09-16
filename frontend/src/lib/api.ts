import { Stop, SearchResult } from "@/types/transit";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

/**
 * Fetch all canonical bus stops with offline fallback caching.
 */
export async function fetchStops(): Promise<Stop[]> {
  try {
    const res = await fetch(`${API_BASE}/stops`);
    if (!res.ok) throw new Error("Failed to load bus stops");
    const data: Stop[] = await res.json();
    try {
      localStorage.setItem("busvara_cached_stops", JSON.stringify(data));
    } catch (e) {
      console.warn("Could not write stops to localStorage:", e);
    }
    return data;
  } catch (err) {
    console.warn("API offline, checking cached stops fallback:", err);
    try {
      const cached = localStorage.getItem("busvara_cached_stops");
      if (cached) return JSON.parse(cached);
    } catch (e) {
      console.error("Failed reading cached stops:", e);
    }
    throw err;
  }
}

/**
 * Perform direct & transit fare search between two stops.
 */
export async function searchFare(fromStop: string, toStop: string): Promise<SearchResult[]> {
  const url = `${API_BASE}/search?from_stop=${encodeURIComponent(fromStop)}&to_stop=${encodeURIComponent(toStop)}`;
  const res = await fetch(url);
  
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || "অনুসন্ধান ব্যর্থ হয়েছে");
  }
  
  return res.json();
}
