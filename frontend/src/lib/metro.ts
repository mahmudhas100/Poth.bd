/**
 * Precise Dhaka MRT Line-6 Timetable Engine based on official DMTCL schedule:
 * https://dmtcl.gov.bd/pages/static-pages/6922df5f933eb65569e218ed
 *
 * Operational matrix:
 * 1. Sunday – Thursday (রবিবার – বৃহস্পতিবার)
 * 2. Friday (শুক্রবার)
 * 3. Saturday (শনিবার)
 *
 * Direction:
 * - Southbound (উত্তরা উত্তর থেকে মতিঝিল): Ends at 09:50 PM
 * - Northbound (মতিঝিল থেকে উত্তরা উত্তর): Ends at 10:30 PM
 */

const MRT_STATIONS_ORDER: Record<string, number> = {
  // English aliases
  "uttara north": 1,
  "uttara north (diabari)": 1,
  "diabari": 1,
  "uttara center": 2,
  "uttara south": 3,
  "pallabi": 4,
  "mirpur-12 (pallabi)": 4,
  "mirpur-12": 4,
  "mirpur 12": 4,
  "mirpur-11": 5,
  "mirpur 11": 5,
  "mirpur-10": 6,
  "mirpur 10": 6,
  "kazipara": 7,
  "shewrapara": 8,
  "agargaon": 9,
  "bijoy sarani": 10,
  "farmgate": 11,
  "kawran bazar": 12,
  "karwan bazar": 12,
  "shahbag": 13,
  "shahbagh": 13,
  "dhaka university": 14,
  "tsc": 14,
  "secretariat (paltan)": 15,
  "secretariat": 15,
  "bangladesh secretariat": 15,
  "paltan": 15,
  "purana paltan": 15,
  "paltan mor": 15,
  "press club (secretariat)": 15,
  "press club": 15,
  "motijheel": 16,

  // Bengali aliases
  "উত্তরা উত্তর": 1,
  "উত্তরা উত্তর (দিয়াবাড়ী)": 1,
  "দিয়াবাড়ী": 1,
  "উত্তরা সেন্টার": 2,
  "উত্তরা দক্ষিণ": 3,
  "পল্লবী": 4,
  "মিরপুর-১২ (পল্লবী)": 4,
  "মিরপুর-১২": 4,
  "মিরপুর ১২": 4,
  "মিরপুর-১১": 5,
  "মিরপুর ১১": 5,
  "মিরপুর-১০": 6,
  "মিরপুর ১০": 6,
  "কাজীপাড়া": 7,
  "শেওড়াপাড়া": 8,
  "আগারগাঁও": 9,
  "বিজয় সরণী": 10,
  "ফার্মগেট": 11,
  "কাওরানবাজার": 12,
  "কারওয়ান বাজার": 12,
  "শাহবাগ": 13,
  "ঢাকা বিশ্ববিদ্যালয়": 14,
  "টিএসসি": 14,
  "সচিবালয় (পল্টন)": 15,
  "সচিবালয়": 15,
  "বাংলাদেশ সচিবালয়": 15,
  "পল্টন": 15,
  "পুরানা পল্টন": 15,
  "পল্টন মোড়": 15,
  "পল্টন মোড়": 15,
  "প্রেসক্লাব (সচিবালয়)": 15,
  "প্রেসক্লাব": 15,
  "মতিঝিল": 16,
};

export const MRT_STATION_IDS = new Set<number>([
  1013, 1159, 1160, 855, 863, 844, 856, 857, 788, 1006, 743, 878, 773, 1161, 760, 943,
]);

export function isMetroStation(
  stop: { id?: number; name_en?: string; name_bn?: string; aliases?: string[] } | string
): boolean {
  if (!stop) return false;
  if (typeof stop === "object") {
    if (stop.id && MRT_STATION_IDS.has(stop.id)) return true;
    if (stop.name_en && isMetroStation(stop.name_en)) return true;
    if (stop.name_bn && isMetroStation(stop.name_bn)) return true;
    if (stop.aliases && stop.aliases.some((a) => a.toLowerCase().includes("metro") || isMetroStation(a))) return true;
    return false;
  }
  const lower = stop.trim().toLowerCase();
  if (MRT_STATIONS_ORDER[lower] !== undefined) return true;
  for (const name of Object.keys(MRT_STATIONS_ORDER)) {
    if (lower === name || lower.includes(name) || name.includes(lower)) {
      return true;
    }
  }
  return false;
}

export function getStationOrder(stop: string): number {
  if (!stop) return 1;
  const lower = stop.trim().toLowerCase();
  if (MRT_STATIONS_ORDER[lower] !== undefined) {
    return MRT_STATIONS_ORDER[lower];
  }
  for (const [name, order] of Object.entries(MRT_STATIONS_ORDER)) {
    if (lower.includes(name) || name.includes(lower)) {
      return order;
    }
  }
  return 1;
}

export type MetroDirection = "southbound" | "northbound";

export function getMetroDirection(fromStop: string, toStop: string): MetroDirection {
  const fromOrder = getStationOrder(fromStop);
  const toOrder = getStationOrder(toStop);
  return fromOrder > toOrder ? "northbound" : "southbound";
}

interface HeadwaySlot {
  startMin: number; // minutes since midnight
  endMin: number;
  headway: number; // minutes
}

// Sunday - Thursday Southbound (Uttara North -> Motijheel)
const SUN_THU_SOUTH: HeadwaySlot[] = [
  { startMin: 6 * 60 + 30, endMin: 7 * 60 + 10, headway: 20 },
  { startMin: 7 * 60 + 11, endMin: 7 * 60 + 30, headway: 10 },
  { startMin: 7 * 60 + 31, endMin: 8 * 60 + 10, headway: 8 },
  { startMin: 8 * 60 + 11, endMin: 10 * 60 + 0, headway: 5 },
  { startMin: 10 * 60 + 1, endMin: 15 * 60 + 20, headway: 8 },
  { startMin: 15 * 60 + 21, endMin: 16 * 60 + 44, headway: 6 },
  { startMin: 16 * 60 + 45, endMin: 20 * 60 + 4, headway: 5 },
  { startMin: 20 * 60 + 5, endMin: 21 * 60 + 0, headway: 10 },
  { startMin: 21 * 60 + 1, endMin: 21 * 60 + 30, headway: 15 },
  { startMin: 21 * 60 + 31, endMin: 21 * 60 + 50, headway: 20 },
];

// Sunday - Thursday Northbound (Motijheel -> Uttara North)
const SUN_THU_NORTH: HeadwaySlot[] = [
  { startMin: 7 * 60 + 15, endMin: 7 * 60 + 55, headway: 10 },
  { startMin: 7 * 60 + 56, endMin: 8 * 60 + 45, headway: 8 },
  { startMin: 8 * 60 + 46, endMin: 10 * 60 + 35, headway: 5 },
  { startMin: 10 * 60 + 36, endMin: 15 * 60 + 55, headway: 8 },
  { startMin: 15 * 60 + 56, endMin: 17 * 60 + 19, headway: 6 },
  { startMin: 17 * 60 + 20, endMin: 20 * 60 + 39, headway: 8 },
  { startMin: 20 * 60 + 40, endMin: 21 * 60 + 40, headway: 10 },
  { startMin: 21 * 60 + 41, endMin: 22 * 60 + 10, headway: 15 },
  { startMin: 22 * 60 + 11, endMin: 22 * 60 + 30, headway: 20 },
];

// Friday Southbound (Uttara North -> Motijheel)
const FRI_SOUTH: HeadwaySlot[] = [
  { startMin: 15 * 60 + 0, endMin: 16 * 60 + 36, headway: 8 },
  { startMin: 16 * 60 + 37, endMin: 18 * 60 + 42, headway: 6 },
  { startMin: 18 * 60 + 43, endMin: 20 * 60 + 18, headway: 8 },
  { startMin: 20 * 60 + 19, endMin: 21 * 60 + 0, headway: 10 },
  { startMin: 21 * 60 + 1, endMin: 21 * 60 + 30, headway: 15 },
  { startMin: 21 * 60 + 31, endMin: 21 * 60 + 50, headway: 20 },
];

// Friday Northbound (Motijheel -> Uttara North)
const FRI_NORTH: HeadwaySlot[] = [
  { startMin: 15 * 60 + 20, endMin: 17 * 60 + 11, headway: 8 },
  { startMin: 17 * 60 + 12, endMin: 19 * 60 + 17, headway: 6 },
  { startMin: 19 * 60 + 18, endMin: 20 * 60 + 53, headway: 8 },
  { startMin: 20 * 60 + 54, endMin: 21 * 60 + 40, headway: 10 },
  { startMin: 21 * 60 + 41, endMin: 22 * 60 + 10, headway: 15 },
  { startMin: 22 * 60 + 11, endMin: 22 * 60 + 30, headway: 20 },
];

// Saturday Southbound (Uttara North -> Motijheel)
const SAT_SOUTH: HeadwaySlot[] = [
  { startMin: 6 * 60 + 30, endMin: 7 * 60 + 25, headway: 20 },
  { startMin: 7 * 60 + 26, endMin: 7 * 60 + 49, headway: 12 },
  { startMin: 7 * 60 + 50, endMin: 8 * 60 + 39, headway: 10 },
  { startMin: 8 * 60 + 40, endMin: 10 * 60 + 39, headway: 8 },
  { startMin: 10 * 60 + 40, endMin: 15 * 60 + 29, headway: 10 },
  { startMin: 15 * 60 + 30, endMin: 16 * 60 + 25, headway: 8 },
  { startMin: 16 * 60 + 26, endMin: 18 * 60 + 55, headway: 6 },
  { startMin: 18 * 60 + 56, endMin: 19 * 60 + 51, headway: 8 },
  { startMin: 19 * 60 + 52, endMin: 21 * 60 + 30, headway: 15 },
  { startMin: 21 * 60 + 31, endMin: 21 * 60 + 50, headway: 20 },
];

// Saturday Northbound (Motijheel -> Uttara North)
const SAT_NORTH: HeadwaySlot[] = [
  { startMin: 7 * 60 + 15, endMin: 8 * 60 + 24, headway: 12 },
  { startMin: 8 * 60 + 25, endMin: 9 * 60 + 14, headway: 10 },
  { startMin: 9 * 60 + 15, endMin: 11 * 60 + 14, headway: 8 },
  { startMin: 11 * 60 + 15, endMin: 16 * 60 + 4, headway: 10 },
  { startMin: 16 * 60 + 5, endMin: 17 * 60 + 0, headway: 8 },
  { startMin: 17 * 60 + 1, endMin: 19 * 60 + 30, headway: 6 },
  { startMin: 19 * 60 + 31, endMin: 20 * 60 + 26, headway: 8 },
  { startMin: 20 * 60 + 27, endMin: 21 * 60 + 40, headway: 10 },
  { startMin: 21 * 60 + 41, endMin: 22 * 60 + 10, headway: 15 },
  { startMin: 22 * 60 + 11, endMin: 22 * 60 + 30, headway: 20 },
];

export interface MetroLiveStatus {
  isOpen: boolean;
  statusText: string;
  headwayMinutes: number | null;
  firstTrain: string;
  lastTrain: string;
  direction: MetroDirection;
  directionLabel: string;
  dayLabel: string;
  tooltipText: string;
}

export function getMetroLiveStatus(fromStop?: string, toStop?: string): MetroLiveStatus {
  const now = new Date();
  // Adjust to Bangladesh Standard Time (UTC+6)
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  const bst = new Date(utc + 6 * 3600000);

  const day = bst.getDay(); // 0 = Sunday, 1 = Monday, ..., 5 = Friday, 6 = Saturday
  const currentMinutes = bst.getHours() * 60 + bst.getMinutes();

  const direction: MetroDirection = fromStop && toStop ? getMetroDirection(fromStop, toStop) : "southbound";
  const isSouth = direction === "southbound";
  const directionLabel = isSouth ? "উত্তরা উত্তর → মতিঝিল" : "মতিঝিল → উত্তরা উত্তর";

  let slots: HeadwaySlot[];
  let dayLabel: string;

  if (day === 5) {
    dayLabel = "শুক্রবার";
    slots = isSouth ? FRI_SOUTH : FRI_NORTH;
  } else if (day === 6) {
    dayLabel = "শনিবার";
    slots = isSouth ? SAT_SOUTH : SAT_NORTH;
  } else {
    dayLabel = "রবিবার – বৃহস্পতিবার";
    slots = isSouth ? SUN_THU_SOUTH : SUN_THU_NORTH;
  }

  const firstSlot = slots[0];
  const lastSlot = slots[slots.length - 1];

  const firstTrainMin = firstSlot.startMin;
  const lastTrainMin = lastSlot.endMin;

  const isOpen = currentMinutes >= firstTrainMin && currentMinutes <= lastTrainMin;

  let currentHeadway: number | null = null;
  if (isOpen) {
    for (const slot of slots) {
      if (currentMinutes >= slot.startMin && currentMinutes <= slot.endMin) {
        currentHeadway = slot.headway;
        break;
      }
    }
  }

  const formatTime = (mins: number) => {
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    const period = h >= 12 ? "PM" : "AM";
    const displayH = h > 12 ? h - 12 : h === 0 ? 12 : h;
    const displayM = m < 10 ? `0${m}` : `${m}`;
    return `${displayH}:${displayM} ${period}`;
  };

  const firstTrain = formatTime(firstTrainMin);
  const lastTrain = formatTime(lastTrainMin);

  let tooltipText = "";
  if (isOpen) {
    tooltipText = `${dayLabel} (${directionLabel}): প্রথম ট্রেন ${firstTrain}, শেষ ট্রেন ${lastTrain}। এখন বিরতি: ${currentHeadway} মিনিট।`;
  } else {
    if (currentMinutes < firstTrainMin) {
      tooltipText = `মেট্রো বর্তমানে বন্ধ। আজ ${dayLabel} ${directionLabel} রুটে প্রথম ট্রেন ছাড়বে ${firstTrain}।`;
    } else {
      tooltipText = `আজকের মতো মেট্রো চলাচল বন্ধ হয়েছে (${directionLabel} রুটে শেষ ট্রেন ছিল ${lastTrain})। আগামীকাল সকালে পুনরায় চালু হবে।`;
    }
  }

  return {
    isOpen,
    statusText: isOpen ? "চলমান" : "বন্ধ",
    headwayMinutes: currentHeadway,
    firstTrain,
    lastTrain,
    direction,
    directionLabel,
    dayLabel,
    tooltipText,
  };
}
