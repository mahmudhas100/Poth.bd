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
  "Sadarghat (Bahadur Shah Park)": "Bahadur Shah Park, Sadarghat",
  "Bahadur Shah Park": "Bahadur Shah Park, Sadarghat",
  "Victoria Park": "Bahadur Shah Park, Sadarghat",
  "Sadarghat (Victoria Park)": "Bahadur Shah Park, Sadarghat",
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
  if (
    lower === "বাহাদুর শাহ পার্ক" ||
    lower === "ভিক্টোরিয়া পার্ক" ||
    lower === "সদরঘাট (বাহাদুর শাহ পার্ক)" ||
    lower === "সদরঘাট (ভিক্টোরিয়া পার্ক)"
  ) {
    return "Bahadur Shah Park, Sadarghat";
  }
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
 * Exact mapping for Dhaka MRT Line-6 stations so Google Maps navigation pins
 * directly to the elevated station gates/concourse instead of generic highway coordinates.
 */
const METRO_STATION_MAP: Record<string, string> = {
  // English
  "uttara north": "Uttara North Metro Station",
  "uttara north (diabari)": "Uttara North Metro Station",
  "diabari": "Uttara North Metro Station",
  "uttara center": "Uttara Center Metro Station",
  "uttara south": "Uttara South Metro Station",
  "pallabi": "Pallabi Metro Station",
  "mirpur-12 (pallabi)": "Pallabi Metro Station",
  "mirpur-12": "Pallabi Metro Station",
  "mirpur 12": "Pallabi Metro Station",
  "mirpur-11": "Mirpur 11 Metro Station",
  "mirpur 11": "Mirpur 11 Metro Station",
  "mirpur-10": "Mirpur 10 Metro Station",
  "mirpur 10": "Mirpur 10 Metro Station",
  "kazipara": "Kazipara Metro Station",
  "shewrapara": "Shewrapara Metro Station",
  "agargaon": "Agargaon Metro Station",
  "bijoy sarani": "Bijoy Sarani Metro Station",
  "farmgate": "Farmgate Metro Station",
  "kawran bazar": "Karwan Bazar Metro Station",
  "karwan bazar": "Karwan Bazar Metro Station",
  "shahbag": "Shahbagh Metro Station",
  "shahbagh": "Shahbagh Metro Station",
  "dhaka university": "Dhaka University Metro Station",
  "secretariat (paltan)": "Bangladesh Secretariat Metro Station",
  "secretariat": "Bangladesh Secretariat Metro Station",
  "bangladesh secretariat": "Bangladesh Secretariat Metro Station",
  "paltan": "Bangladesh Secretariat Metro Station",
  "purana paltan": "Bangladesh Secretariat Metro Station",
  "paltan mor": "Bangladesh Secretariat Metro Station",
  "press club (secretariat)": "Bangladesh Secretariat Metro Station",
  "press club": "Bangladesh Secretariat Metro Station",
  "motijheel": "Motijheel Metro Station",
  "kamalapur": "Kamalapur Metro Station",

  // Bengali
  "উত্তরা উত্তর": "Uttara North Metro Station",
  "উত্তরা উত্তর (দিয়াবাড়ী)": "Uttara North Metro Station",
  "দিয়াবাড়ী": "Uttara North Metro Station",
  "উত্তরা সেন্টার": "Uttara Center Metro Station",
  "উত্তরা দক্ষিণ": "Uttara South Metro Station",
  "পল্লবী": "Pallabi Metro Station",
  "মিরপুর-১২ (পল্লবী)": "Pallabi Metro Station",
  "মিরপুর-১২": "Pallabi Metro Station",
  "মিরপুর ১২": "Pallabi Metro Station",
  "মিরপুর-১১": "Mirpur 11 Metro Station",
  "মিরপুর ১১": "Mirpur 11 Metro Station",
  "মিরপুর-১০": "Mirpur 10 Metro Station",
  "মিরপুর ১০": "Mirpur 10 Metro Station",
  "কাজীপাড়া": "Kazipara Metro Station",
  "শেওড়াপাড়া": "Shewrapara Metro Station",
  "আগারগাঁও": "Agargaon Metro Station",
  "বিজয় সরণী": "Bijoy Sarani Metro Station",
  "ফার্মগেট": "Farmgate Metro Station",
  "কাওরানবাজার": "Karwan Bazar Metro Station",
  "কারওয়ান বাজার": "Karwan Bazar Metro Station",
  "শাহবাগ": "Shahbagh Metro Station",
  "ঢাকা বিশ্ববিদ্যালয়": "Dhaka University Metro Station",
  "সচিবালয় (পল্টন)": "Bangladesh Secretariat Metro Station",
  "সচিবালয়": "Bangladesh Secretariat Metro Station",
  "বাংলাদেশ সচিবালয়": "Bangladesh Secretariat Metro Station",
  "পল্টন": "Bangladesh Secretariat Metro Station",
  "পুরানা পল্টন": "Bangladesh Secretariat Metro Station",
  "পল্টন মোড়": "Bangladesh Secretariat Metro Station",
  "পল্টন মোড়": "Bangladesh Secretariat Metro Station",
  "প্রেসক্লাব (সচিবালয়)": "Bangladesh Secretariat Metro Station",
  "প্রেসক্লাব": "Bangladesh Secretariat Metro Station",
  "মতিঝিল": "Motijheel Metro Station",
  "কমলাপুর": "Kamalapur Metro Station",
};

export function resolveMetroStationForMaps(stop: string): string {
  if (!stop) return "";
  const trimmed = stop.trim();
  const lower = trimmed.toLowerCase();

  if (METRO_STATION_MAP[lower]) {
    return METRO_STATION_MAP[lower];
  }

  // If already contains "metro", keep as is
  if (/\bmetro\b/i.test(trimmed)) {
    return trimmed;
  }

  const cleanStop = trimmed.replace(/-/g, " ");
  return `${cleanStop} Metro Station`;
}

export interface DirectionOptions {
  isMetro?: boolean;
  originIsMetro?: boolean;
  destIsMetro?: boolean;
}

/**
 * Generates a Google Maps directions URL for navigation between transit stops.
 * Automatically resolves ambiguous names and appends "Metro Station" for MRT Line-6 stops.
 * Works natively across mobile (Google Maps App) and desktop browsers.
 */
export function getGoogleMapsDirectionUrl(
  origin: string,
  destination: string,
  options?: DirectionOptions | boolean
): string {
  const isMetro = typeof options === "boolean" ? options : options?.isMetro;
  const originMetro = typeof options === "object" ? (options.originIsMetro ?? isMetro) : isMetro;
  const destMetro = typeof options === "object" ? (options.destIsMetro ?? isMetro) : isMetro;

  const resolvedOrigin = originMetro ? resolveMetroStationForMaps(origin) : resolveStopForMaps(origin);
  const resolvedDest = destMetro ? resolveMetroStationForMaps(destination) : resolveStopForMaps(destination);

  const originParam = encodeURIComponent(resolvedOrigin);
  const destParam = encodeURIComponent(resolvedDest);

  return `https://www.google.com/maps/dir/?api=1&origin=${originParam}&destination=${destParam}&travelmode=transit`;
}

