"use client";

import React, { useState } from "react";
import { TrainIcon, BusIcon } from "@/components/ui/Icons";
import {
  DirectRouteCard,
  TransitRouteCard,
  GroupedRouteCard,
  GroupedTransitCard,
  SuggestionBanner,
} from "@/components/RouteCards";
import {
  SearchResult,
  DisplayResult,
  GroupedDirectResult,
  GroupedTransitResult,
} from "@/types/transit";

function getSearchResultMode(r: SearchResult): {
  hasMetro: boolean;
  hasBus: boolean;
  isPureBus: boolean;
  isPureMetro: boolean;
} {
  if (r.type === "suggestion") {
    const isMetro = r.route.mode === "metro";
    return { hasMetro: isMetro, hasBus: !isMetro, isPureBus: !isMetro, isPureMetro: isMetro };
  }
  if (r.type === "direct") {
    const isMetro = r.mode === "metro";
    return { hasMetro: isMetro, hasBus: !isMetro, isPureBus: !isMetro, isPureMetro: isMetro };
  }
  const leg1Metro = r.leg1.mode === "metro";
  const leg2Metro = r.leg2.mode === "metro";
  return {
    hasMetro: leg1Metro || leg2Metro,
    hasBus: !leg1Metro || !leg2Metro,
    isPureBus: !leg1Metro && !leg2Metro,
    isPureMetro: leg1Metro && leg2Metro,
  };
}

function getDisplayResultMode(r: DisplayResult): {
  hasMetro: boolean;
  hasBus: boolean;
  isPureBus: boolean;
  isPureMetro: boolean;
} {
  if (r.type === "grouped") {
    return { hasMetro: false, hasBus: true, isPureBus: true, isPureMetro: false };
  }
  if (r.type === "grouped_transit") {
    const leg1Metro = r.leg1.mode === "metro";
    const leg2Metro = r.leg2.mode === "metro";
    return {
      hasMetro: leg1Metro || leg2Metro,
      hasBus: !leg1Metro || !leg2Metro,
      isPureBus: !leg1Metro && !leg2Metro,
      isPureMetro: leg1Metro && leg2Metro,
    };
  }
  return getSearchResultMode(r);
}

function isExpresswayResult(item: DisplayResult): boolean {
  if (item.type === "direct") {
    return item.service_type === "Expressway" || item.route_name.toLowerCase().includes("expressway") || item.route_name.includes("এক্সপ্রেসওয়ে");
  }
  if (item.type === "grouped") {
    return item.service_type === "Expressway" || item.routes.some((r) => r.service_type === "Expressway" || r.route_name.toLowerCase().includes("expressway") || r.route_name.includes("এক্সপ্রেসওয়ে"));
  }
  if (item.type === "transit") {
    const l1Exp = item.leg1.service_type === "Expressway" || item.leg1.route_name.toLowerCase().includes("expressway") || item.leg1.route_name.includes("এক্সপ্রেসওয়ে");
    const l2Exp = item.leg2.service_type === "Expressway" || item.leg2.route_name.toLowerCase().includes("expressway") || item.leg2.route_name.includes("এক্সপ্রেসওয়ে");
    return l1Exp || l2Exp;
  }
  if (item.type === "grouped_transit") {
    const l1Exp = item.leg1.service_type === "Expressway" || item.leg1.routes.some((r) => r.service_type === "Expressway" || r.route_name.toLowerCase().includes("expressway") || r.route_name.includes("এক্সপ্রেসওয়ে"));
    const l2Exp = item.leg2.service_type === "Expressway" || item.leg2.routes.some((r) => r.service_type === "Expressway" || r.route_name.toLowerCase().includes("expressway") || r.route_name.includes("এক্সপ্রেসওয়ে"));
    return l1Exp || l2Exp;
  }
  if (item.type === "suggestion") {
    return item.route.service_type === "Expressway" || item.route.route_name.toLowerCase().includes("expressway") || item.route.route_name.includes("এক্সপ্রেসওয়ে");
  }
  return false;
}

function consolidateSearchResults(results: SearchResult[]): DisplayResult[] {
  const output: DisplayResult[] = [];
  const directGroupIndices = new Map<string, number>();
  const transitGroupIndices = new Map<string, number>();

  for (const r of results) {
    if (r.type === "direct" && r.mode !== "metro") {
      const isExp = r.service_type === "Expressway" || r.route_name.toLowerCase().includes("expressway") || r.route_name.includes("এক্সপ্রেসওয়ে");
      const key = `${r.from_stop}::${r.to_stop}::${isExp ? "expressway" : "regular"}`;
      const existingIdx = directGroupIndices.get(key);
      if (existingIdx !== undefined) {
        const item = output[existingIdx];
        if (item.type === "grouped") {
          if (!item.routes.some((x) => x.route_name === r.route_name && x.fare === r.fare)) {
            item.routes.push(r);
            item.min_fare = Math.min(item.min_fare, r.fare);
            item.max_fare = Math.max(item.max_fare, r.fare);
            item.min_distance_km = Math.round(Math.min(item.min_distance_km, r.distance_km) * 10) / 10;
            item.max_distance_km = Math.round(Math.max(item.max_distance_km, r.distance_km) * 10) / 10;
          }
        } else if (item.type === "direct") {
          const firstRoute = item;
          if (firstRoute.route_name !== r.route_name || firstRoute.fare !== r.fare) {
            const routes = [firstRoute, r];
            const fares = [firstRoute.fare, r.fare];
            const dists = [firstRoute.distance_km, r.distance_km];
            output[existingIdx] = {
              type: "grouped",
              from_stop: firstRoute.from_stop,
              from_stop_bn: firstRoute.from_stop_bn,
              to_stop: firstRoute.to_stop,
              to_stop_bn: firstRoute.to_stop_bn,
              service_type: isExp ? "Expressway" : "Regular",
              min_fare: Math.min(...fares),
              max_fare: Math.max(...fares),
              min_distance_km: Math.round(Math.min(...dists) * 10) / 10,
              max_distance_km: Math.round(Math.max(...dists) * 10) / 10,
              routes,
            } satisfies GroupedDirectResult;
          }
        }
      } else {
        directGroupIndices.set(key, output.length);
        output.push(r);
      }
    } else if (r.type === "transit") {
      const leg1Exp = r.leg1.service_type === "Expressway" || r.leg1.route_name.toLowerCase().includes("expressway") || r.leg1.route_name.includes("এক্সপ্রেসওয়ে");
      const leg2Exp = r.leg2.service_type === "Expressway" || r.leg2.route_name.toLowerCase().includes("expressway") || r.leg2.route_name.includes("এক্সপ্রেসওয়ে");
      const key = `${r.leg1.from_stop}::${r.transfer_at}::${r.leg2.to_stop}::${r.leg1.mode}::${r.leg2.mode}::${leg1Exp}::${leg2Exp}`;
      const existingIdx = transitGroupIndices.get(key);
      if (existingIdx !== undefined) {
        const item = output[existingIdx];
        if (item.type === "grouped_transit") {
          item.min_fare = Math.min(item.min_fare, r.total_fare);
          item.max_fare = Math.max(item.max_fare, r.total_fare);
          item.total_fare = item.min_fare;
          item.min_distance_km = Math.round(Math.min(item.min_distance_km, r.total_distance_km) * 10) / 10;
          item.max_distance_km = Math.round(Math.max(item.max_distance_km, r.total_distance_km) * 10) / 10;
          item.total_distance_km = item.min_distance_km;

          if (!item.leg1.routes.some((x) => x.route_name === r.leg1.route_name && x.fare === r.leg1.fare)) {
            item.leg1.routes.push(r.leg1);
            item.leg1.min_fare = Math.min(item.leg1.min_fare, r.leg1.fare);
            item.leg1.max_fare = Math.max(item.leg1.max_fare, r.leg1.fare);
            item.leg1.min_distance_km = Math.round(Math.min(item.leg1.min_distance_km, r.leg1.distance_km) * 10) / 10;
            item.leg1.max_distance_km = Math.round(Math.max(item.leg1.max_distance_km, r.leg1.distance_km) * 10) / 10;
          }

          if (!item.leg2.routes.some((x) => x.route_name === r.leg2.route_name && x.fare === r.leg2.fare)) {
            item.leg2.routes.push(r.leg2);
            item.leg2.min_fare = Math.min(item.leg2.min_fare, r.leg2.fare);
            item.leg2.max_fare = Math.max(item.leg2.max_fare, r.leg2.fare);
            item.leg2.min_distance_km = Math.round(Math.min(item.leg2.min_distance_km, r.leg2.distance_km) * 10) / 10;
            item.leg2.max_distance_km = Math.round(Math.max(item.leg2.max_distance_km, r.leg2.distance_km) * 10) / 10;
          }
        } else if (item.type === "transit") {
          const firstTransit = item;
          const isDifferentRoute =
            firstTransit.leg1.route_name !== r.leg1.route_name ||
            firstTransit.leg2.route_name !== r.leg2.route_name ||
            firstTransit.total_fare !== r.total_fare;

          if (isDifferentRoute) {
            const leg1Routes = [firstTransit.leg1];
            if (firstTransit.leg1.route_name !== r.leg1.route_name || firstTransit.leg1.fare !== r.leg1.fare) {
              leg1Routes.push(r.leg1);
            }
            const leg2Routes = [firstTransit.leg2];
            if (firstTransit.leg2.route_name !== r.leg2.route_name || firstTransit.leg2.fare !== r.leg2.fare) {
              leg2Routes.push(r.leg2);
            }

            const totalFares = [firstTransit.total_fare, r.total_fare];
            const totalDists = [firstTransit.total_distance_km, r.total_distance_km];
            const leg1Fares = [firstTransit.leg1.fare, r.leg1.fare];
            const leg1Dists = [firstTransit.leg1.distance_km, r.leg1.distance_km];
            const leg2Fares = [firstTransit.leg2.fare, r.leg2.fare];
            const leg2Dists = [firstTransit.leg2.distance_km, r.leg2.distance_km];

            output[existingIdx] = {
              type: "grouped_transit",
              min_fare: Math.min(...totalFares),
              max_fare: Math.max(...totalFares),
              total_fare: Math.min(...totalFares),
              min_distance_km: Math.round(Math.min(...totalDists) * 10) / 10,
              max_distance_km: Math.round(Math.max(...totalDists) * 10) / 10,
              total_distance_km: Math.round(Math.min(...totalDists) * 10) / 10,
              transfer_at: firstTransit.transfer_at,
              transfer_at_bn: firstTransit.transfer_at_bn,
              leg1: {
                from_stop: firstTransit.leg1.from_stop,
                from_stop_bn: firstTransit.leg1.from_stop_bn,
                to_stop: firstTransit.leg1.to_stop,
                to_stop_bn: firstTransit.leg1.to_stop_bn,
                mode: firstTransit.leg1.mode,
                min_fare: Math.min(...leg1Fares),
                max_fare: Math.max(...leg1Fares),
                min_distance_km: Math.round(Math.min(...leg1Dists) * 10) / 10,
                max_distance_km: Math.round(Math.max(...leg1Dists) * 10) / 10,
                duration_mins: firstTransit.leg1.duration_mins,
                routes: leg1Routes,
              },
              leg2: {
                from_stop: firstTransit.leg2.from_stop,
                from_stop_bn: firstTransit.leg2.from_stop_bn,
                to_stop: firstTransit.leg2.to_stop,
                to_stop_bn: firstTransit.leg2.to_stop_bn,
                mode: firstTransit.leg2.mode,
                min_fare: Math.min(...leg2Fares),
                max_fare: Math.max(...leg2Fares),
                min_distance_km: Math.round(Math.min(...leg2Dists) * 10) / 10,
                max_distance_km: Math.round(Math.max(...leg2Dists) * 10) / 10,
                duration_mins: firstTransit.leg2.duration_mins,
                routes: leg2Routes,
              },
            } satisfies GroupedTransitResult;
          }
        }
      } else {
        transitGroupIndices.set(key, output.length);
        output.push(r);
      }
    } else {
      output.push(r);
    }
  }

  // Sort routes inside each grouped result (cheapest first, then shortest)
  for (const item of output) {
    if (item.type === "grouped") {
      item.routes.sort((a, b) => a.fare - b.fare || a.distance_km - b.distance_km);
    } else if (item.type === "grouped_transit") {
      item.leg1.routes.sort((a, b) => a.fare - b.fare || a.distance_km - b.distance_km);
      item.leg2.routes.sort((a, b) => a.fare - b.fare || a.distance_km - b.distance_km);
    }
  }

  return output;
}

interface SearchResultsViewProps {
  results: SearchResult[];
  onOpenStops: (stops: string[], title: string) => void;
  onShare: (
    fromBn: string,
    toBn: string,
    fromEn: string,
    toEn: string,
    routeName: string,
    distance: number,
    fare: number
  ) => void;
}

export const SearchResultsView: React.FC<SearchResultsViewProps> = ({
  results,
  onOpenStops,
  onShare,
}) => {
  const [modeFilter, setModeFilter] = useState<"all" | "bus" | "metro">("all");
  const [sortBy, setSortBy] = useState<"recommended" | "fare" | "distance">("recommended");

  const grouped = consolidateSearchResults(results);

  const metroCount = grouped.filter((r) => getDisplayResultMode(r).hasMetro).length;
  const pureBusCount = grouped.filter((r) => getDisplayResultMode(r).isPureBus).length;
  const anyBusCount = grouped.filter((r) => getDisplayResultMode(r).hasBus).length;
  const busCount = pureBusCount > 0 ? pureBusCount : anyBusCount;

  const filtered = grouped.filter((r) => {
    if (modeFilter === "all") return true;
    const modeInfo = getDisplayResultMode(r);
    if (modeFilter === "metro") return modeInfo.hasMetro;
    if (modeFilter === "bus") return pureBusCount > 0 ? modeInfo.isPureBus : modeInfo.hasBus;
    return true;
  });

  const displayedResults = [...filtered].sort((a, b) => {
    if (sortBy === "fare") {
      const fareA =
        a.type === "direct"
          ? a.fare
          : a.type === "transit"
          ? a.total_fare
          : a.type === "grouped" || a.type === "grouped_transit"
          ? a.min_fare
          : a.route.fare;
      const fareB =
        b.type === "direct"
          ? b.fare
          : b.type === "transit"
          ? b.total_fare
          : b.type === "grouped" || b.type === "grouped_transit"
          ? b.min_fare
          : b.route.fare;
      return fareA - fareB;
    }
    if (sortBy === "distance") {
      const distA =
        a.type === "direct"
          ? a.distance_km
          : a.type === "transit"
          ? a.total_distance_km
          : a.type === "grouped" || a.type === "grouped_transit"
          ? a.min_distance_km
          : a.route.distance_km;
      const distB =
        b.type === "direct"
          ? b.distance_km
          : b.type === "transit"
          ? b.total_distance_km
          : b.type === "grouped" || b.type === "grouped_transit"
          ? b.min_distance_km
          : b.route.distance_km;
      return distA - distB;
    }

    // Recommended default rank:
    // Tier 1: Direct Metro
    // Tier 2: Direct Expressway
    // Tier 3: Direct Regular Bus / Grouped Direct Bus
    // Tier 4: Transit with Metro or Expressway
    // Tier 5: Transit Bus Regular
    // Tier 6: Suggestions
    const rankOrder = (item: DisplayResult) => {
      if (item.type === "direct" && item.mode === "metro") return 1;
      if (item.type === "direct" || item.type === "grouped") {
        return isExpresswayResult(item) ? 2 : 3;
      }
      if (item.type === "transit" || item.type === "grouped_transit") {
        const isMetro = getDisplayResultMode(item).hasMetro;
        if (isMetro || isExpresswayResult(item)) return 4;
        return 5;
      }
      return 6;
    };
    const rankDiff = rankOrder(a) - rankOrder(b);
    if (rankDiff !== 0) return rankDiff;

    const fareA =
      a.type === "direct"
        ? a.fare
        : a.type === "transit"
        ? a.total_fare
        : a.type === "grouped" || a.type === "grouped_transit"
        ? a.min_fare
        : a.route.fare;
    const fareB =
      b.type === "direct"
        ? b.fare
        : b.type === "transit"
        ? b.total_fare
        : b.type === "grouped" || b.type === "grouped_transit"
        ? b.min_fare
        : b.route.fare;
    if (fareA !== fareB) return fareA - fareB;

    const distA =
      a.type === "direct"
        ? a.distance_km
        : a.type === "transit"
        ? a.total_distance_km
        : a.type === "grouped" || a.type === "grouped_transit"
        ? a.min_distance_km
        : a.route.distance_km;
    const distB =
      b.type === "direct"
        ? b.distance_km
        : b.type === "transit"
        ? b.total_distance_km
        : b.type === "grouped" || b.type === "grouped_transit"
        ? b.min_distance_km
        : b.route.distance_km;
    return distA - distB;
  });

  return (
    <>
      <div className="space-y-3 mb-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <h2 className="text-[10px] uppercase tracking-[0.3em] font-extrabold text-slate-400 flex items-center gap-2 font-display">
              Available Routes ({displayedResults.length})
            </h2>
            <div className="h-px w-8 bg-gradient-to-r from-slate-200 to-transparent" />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Mode Filter Control */}
            {metroCount > 0 && busCount > 0 && (
              <div className="inline-flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/70 shadow-inner w-fit">
                <button
                  type="button"
                  onClick={() => setModeFilter("all")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all font-display ${
                    modeFilter === "all"
                      ? "bg-white text-slate-900 shadow-sm"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  All ({grouped.length})
                </button>
                <button
                  type="button"
                  onClick={() => setModeFilter("metro")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 font-display ${
                    modeFilter === "metro"
                      ? "bg-emerald-600 text-white shadow-sm shadow-emerald-600/20"
                      : "text-emerald-700 hover:bg-emerald-50/80"
                  }`}
                >
                  <TrainIcon size={13} />
                  <span>Metro ({metroCount})</span>
                </button>
                <button
                  type="button"
                  onClick={() => setModeFilter("bus")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 font-display ${
                    modeFilter === "bus"
                      ? "bg-white text-slate-900 shadow-sm"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  <BusIcon size={13} />
                  <span>Bus ({busCount})</span>
                </button>
              </div>
            )}

            {/* Sort Control */}
            {displayedResults.length > 1 && (
              <div className="inline-flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/70 shadow-inner w-fit">
                <button
                  type="button"
                  onClick={() => setSortBy("recommended")}
                  title="মেট্রো ও সেরা ভাড়ার অগ্রাধিকার"
                  className={`px-2.5 py-1.5 rounded-lg text-xs font-bold transition-all font-display ${
                    sortBy === "recommended"
                      ? "bg-white text-slate-900 shadow-sm"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  সুপারিশকৃত
                </button>
                <button
                  type="button"
                  onClick={() => setSortBy("fare")}
                  title="সবচেয়ে কম ভাড়া আগে"
                  className={`px-2.5 py-1.5 rounded-lg text-xs font-bold transition-all font-display ${
                    sortBy === "fare"
                      ? "bg-white text-slate-900 shadow-sm"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  কম ভাড়া
                </button>
                <button
                  type="button"
                  onClick={() => setSortBy("distance")}
                  title="সবচেয়ে কম দূরত্ব আগে"
                  className={`px-2.5 py-1.5 rounded-lg text-xs font-bold transition-all font-display ${
                    sortBy === "distance"
                      ? "bg-white text-slate-900 shadow-sm"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  কম দূরত্ব
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {displayedResults.map((res, i) => {
        const animationClass = `animate-stagger-${Math.min(i + 1, 5)}`;

        if (res.type === "suggestion") {
          return (
            <div key={i}>
              <SuggestionBanner suggestion={res} />
              <DirectRouteCard
                route={res.route}
                onOpenStops={onOpenStops}
                onShare={onShare}
                animationClass={animationClass}
              />
            </div>
          );
        }

        if (res.type === "grouped") {
          return (
            <GroupedRouteCard
              key={i}
              group={res}
              onOpenStops={onOpenStops}
              onShare={onShare}
              animationClass={animationClass}
            />
          );
        }

        if (res.type === "grouped_transit") {
          return (
            <GroupedTransitCard
              key={i}
              result={res}
              onOpenStops={onOpenStops}
              onShare={onShare}
              animationClass={animationClass}
            />
          );
        }

        if (res.type === "direct") {
          return (
            <DirectRouteCard
              key={i}
              route={res}
              onOpenStops={onOpenStops}
              onShare={onShare}
              animationClass={animationClass}
            />
          );
        }

        return (
          <TransitRouteCard
            key={i}
            result={res}
            onOpenStops={onOpenStops}
            onShare={onShare}
            animationClass={animationClass}
          />
        );
      })}

      {displayedResults.length === 0 && (
        <div className="text-center py-14 bg-white/50 backdrop-blur border border-slate-200 border-dashed rounded-3xl animate-in zoom-in-95 duration-300">
          <p className="text-slate-500 font-display font-medium text-base mb-3">
            এই ফিল্টারে কোনো রুট পাওয়া যায়নি।
          </p>
          <button
            type="button"
            onClick={() => setModeFilter("all")}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 rounded-xl text-xs font-bold text-slate-700 transition-colors font-display"
          >
            সকল রুট দেখুন
          </button>
        </div>
      )}
    </>
  );
};
