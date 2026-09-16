/**
 * Maps ambiguous, generic stop names into exact, unambiguous real-world POIs
 * on Google Maps to prevent "Did you mean?" disambiguation prompts (e.g. helipads, etc.).
 */
const AMBIGUOUS_STOP_RESOLVER: Record<string, string> = {
  // Generic single nouns that trigger "Did you mean?" or helipad prompts
  Airport: "Hazrat Shahjalal International Airport",
  Zoo: "Bangladesh National Zoo, Mirpur",
  Stadium: "Bangabandhu National Stadium",

  // Transit hubs and landmarks commonly confused by geocoders
  Technical: "Technical Mor, Mirpur",
  Amtoli: "Amtoli, Mohakhali",
  Chowrasta: "Gazipur Chowrasta",
  Signboard: "Signboard Bus Stand",
  GPO: "Dhaka GPO",
  "High Court": "High Court Mazar",
  "College Gate": "College Gate, Mirpur Road",
  "Shishu Mela": "Shishu Mela, Shyamoli",
  Rainbow: "Rainbow Crossing, Moghbazar",
  Workshop: "Mirpur 14 Workshop",
  Purabi: "Purabi Cinema Hall, Mirpur",
  Proshika: "Proshika Mor, Mirpur",
  Ittefaq: "Ittefaq Mor, Motijheel",
  Nabisco: "Nabisco Mor, Tejgaon",
  Kakoli: "Kakoli Bus Stand, Banani",
  "Bishwa Road": "Kuril Bishwa Road",
  "Biswa Road": "Kuril Bishwa Road",
};

export function resolveStopForMaps(stop: string): string {
  if (!stop) return "";
  const trimmed = stop.trim();
  const lower = trimmed.toLowerCase();

  // Match English case-insensitively
  for (const [key, resolved] of Object.entries(AMBIGUOUS_STOP_RESOLVER)) {
    if (key.toLowerCase() === lower) {
      return resolved;
    }
  }

  // Match Bengali stop names
  if (lower === "এয়ারপোর্ট" || lower === "বিমানবন্দর") {
    return "Hazrat Shahjalal International Airport";
  }
  if (lower === "চিড়িয়াখানা") {
    return "Bangladesh National Zoo, Mirpur";
  }
  if (lower === "স্টেডিয়াম") {
    return "Bangabandhu National Stadium";
  }
  if (lower === "টেকনিক্যাল") {
    return "Technical Mor, Mirpur";
  }
  if (lower === "আমতলী") {
    return "Amtoli, Mohakhali";
  }
  if (lower === "চৌরাস্তা") {
    return "Gazipur Chowrasta";
  }
  if (lower === "সাইনবোর্ড") {
    return "Signboard Bus Stand";
  }

  return trimmed;
}

/**
 * Generates a Google Maps directions URL for navigation between transit stops.
 * Automatically resolves ambiguous names to their prominent landmark.
 * Works natively across mobile (Google Maps App) and desktop browsers.
 */
export function getGoogleMapsDirectionUrl(
  origin: string,
  destination: string
): string {
  const resolvedOrigin = resolveStopForMaps(origin);
  const resolvedDest = resolveStopForMaps(destination);

  const originParam = encodeURIComponent(resolvedOrigin);
  const destParam = encodeURIComponent(resolvedDest);

  return `https://www.google.com/maps/dir/?api=1&origin=${originParam}&destination=${destParam}&travelmode=transit`;
}

