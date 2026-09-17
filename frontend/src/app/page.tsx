"use client";

import { useState, useEffect } from "react";
import { AlertCircleIcon, NavigationIcon, DownloadIcon, TrainIcon, BusIcon } from "@/components/ui/Icons";
import { SearchHeader } from "@/components/SearchHeader";
import { RouteSearchForm } from "@/components/RouteSearchForm";
import { RouteModal } from "@/components/RouteModal";
import { Toast } from "@/components/ui/Toast";
import {
  DirectRouteCard,
  TransitRouteCard,
  SuggestionBanner,
  SkeletonLoader,
} from "@/components/RouteCards";
import { fetchStops, searchFare } from "@/lib/api";
import { Stop, SearchResult } from "@/types/transit";

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

export default function BusVaraApp() {
  const [fromStop, setFromStop] = useState("");
  const [toStop, setToStop] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [modeFilter, setModeFilter] = useState<"all" | "bus" | "metro">("all");
  const [sortBy, setSortBy] = useState<"recommended" | "fare" | "distance">("recommended");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stops, setStops] = useState<Stop[]>([]);
  const [isSearchExpanded, setIsSearchExpanded] = useState(true);
  const [hasSearched, setHasSearched] = useState(false);
  const [recentSearches, setRecentSearches] = useState<{ from: string; to: string }[]>([]);
  const [isOffline, setIsOffline] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [modalStops, setModalStops] = useState<string[]>([]);
  const [modalTitle, setModalTitle] = useState("");

  useEffect(() => {
    loadStops();

    try {
      const saved = localStorage.getItem("busvara_recents");
      if (saved) setRecentSearches(JSON.parse(saved));
    } catch (e) {
      console.error("Could not load recent searches:", e);
    }

    const updateOnlineStatus = () => setIsOffline(!navigator.onLine);
    window.addEventListener("online", updateOnlineStatus);
    window.addEventListener("offline", updateOnlineStatus);
    setIsOffline(!navigator.onLine);

    if (typeof window !== "undefined") {
      if (
        window.matchMedia("(display-mode: standalone)").matches ||
        (window.navigator as any).standalone
      ) {
        setIsInstalled(true);
      }

      const handleBeforeInstall = (e: Event) => {
        e.preventDefault();
        setDeferredPrompt(e);
      };

      const handleAppInstalled = () => {
        setDeferredPrompt(null);
        setIsInstalled(true);
        setToastMessage("অ্যাপটি সফলভাবে ইনস্টল করা হয়েছে!");
      };

      window.addEventListener("beforeinstallprompt", handleBeforeInstall);
      window.addEventListener("appinstalled", handleAppInstalled);

      // Deep linking check
      const params = new URLSearchParams(window.location.search);
      const urlFrom = params.get("from");
      const urlTo = params.get("to");
      if (urlFrom && urlTo) {
        setFromStop(urlFrom);
        setToStop(urlTo);
        executeSearch(urlFrom, urlTo);
      }

      return () => {
        window.removeEventListener("online", updateOnlineStatus);
        window.removeEventListener("offline", updateOnlineStatus);
        window.removeEventListener("beforeinstallprompt", handleBeforeInstall);
        window.removeEventListener("appinstalled", handleAppInstalled);
      };
    }

    return () => {
      window.removeEventListener("online", updateOnlineStatus);
      window.removeEventListener("offline", updateOnlineStatus);
    };
  }, []);

  const loadStops = async () => {
    try {
      const data = await fetchStops();
      setStops(data);
    } catch (err) {
      console.error("Could not fetch stops:", err);
    }
  };

  const handleSwap = () => {
    const temp = fromStop;
    setFromStop(toStop);
    setToStop(temp);
  };

  const saveRecentSearch = (from: string, to: string) => {
    setRecentSearches((prev) => {
      const filtered = prev.filter((s) => !(s.from === from && s.to === to));
      const updated = [{ from, to }, ...filtered].slice(0, 4);
      try {
        localStorage.setItem("busvara_recents", JSON.stringify(updated));
      } catch (e) {
        console.error(e);
      }
      return updated;
    });
  };

  const executeSearch = async (from: string, to: string) => {
    if (!from || !to) {
      setError("দয়া করে প্রস্থান এবং গন্তব্য স্থান উভয়ই নির্বাচন করুন।");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await searchFare(from, to);
      setResults(data);
      setModeFilter("all");
      setSortBy("recommended");
      setHasSearched(true);
      saveRecentSearch(from, to);
      setIsSearchExpanded(false);

      // Update URL query params without reloading
      if (typeof window !== "undefined") {
        const url = new URL(window.location.href);
        url.searchParams.set("from", from);
        url.searchParams.set("to", to);
        window.history.pushState({}, "", url.toString());
      }
    } catch (err: any) {
      setError(
        err.message === "Stop not recognized. Please check spelling."
          ? "গন্তব্য খুঁজে পাওয়া যায়নি। দয়া করে সঠিক বানান লিখুন।"
          : err.message
      );
      setResults([]);
      setIsSearchExpanded(true);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    executeSearch(fromStop, toStop);
  };

  const handleShare = async (
    fromBn: string,
    toBn: string,
    fromEn: string,
    toEn: string,
    routeName: string,
    distance: number,
    fare: number
  ) => {
    const isMetro = routeName.includes("MRT") || routeName.includes("মেট্রোরেল");
    const shareUrl = `${window.location.origin}${window.location.pathname}?from=${encodeURIComponent(fromEn)}&to=${encodeURIComponent(toEn)}`;
    const shareText = `${isMetro ? "🚇" : "🚌"} ${fromBn} ⇄ ${toBn} (${routeName})\n💰 ভাড়া: ৳${fare} (${distance} কি.মি.)\n\nPoth.bd তে দেখুন: ${shareUrl}`;

    if (navigator.share) {
      try {
        await navigator.share({
          title: `Poth.bd - ${fromBn} to ${toBn}`,
          text: shareText,
          url: shareUrl,
        });
        setToastMessage("শেয়ার সম্পন্ন হয়েছে!");
      } catch (e) {
        // User cancelled or share failed, fallback to copy
        await copyToClipboard(shareUrl);
      }
    } else {
      await copyToClipboard(shareUrl);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setToastMessage("রুট লিংক কপি করা হয়েছে!");
    } catch (err) {
      setToastMessage("লিংক কপি করা সম্ভব হয়নি");
    }
  };

  const openStopsModal = (stopsList: string[], title: string) => {
    setModalStops(stopsList);
    setModalTitle(title);
    setModalOpen(true);
  };

  const handleInstallApp = async () => {
    if (!deferredPrompt) return;
    try {
      deferredPrompt.prompt();
      const choiceResult = await deferredPrompt.userChoice;
      if (choiceResult.outcome === "accepted") {
        setDeferredPrompt(null);
      }
    } catch (err) {
      console.error("Install prompt error:", err);
    }
  };

  return (
    <main className="h-[100dvh] max-w-2xl mx-auto px-4 sm:px-5 pt-4 sm:pt-6 pb-2 sm:pb-4 relative z-10 flex flex-col overflow-hidden">
      {/* Subtle Top-Right Install Icon */}
      {!isInstalled && deferredPrompt && (
        <button
          onClick={handleInstallApp}
          type="button"
          title="অ্যাপ ইনস্টল করুন (Install App)"
          className="absolute top-4 sm:top-6 right-4 sm:right-5 z-30 p-2.5 rounded-full bg-white/80 hover:bg-white text-slate-600 hover:text-accent border border-slate-200/80 shadow-sm backdrop-blur-md transition-all active:scale-95 animate-in fade-in group"
        >
          <DownloadIcon size={18} className="group-hover:translate-y-0.5 transition-transform text-slate-700 group-hover:text-accent" />
          <span className="sr-only">অ্যাপ ইনস্টল করুন</span>
        </button>
      )}

      <Toast message={toastMessage} onClose={() => setToastMessage(null)} />

      <RouteModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        stops={modalStops}
        title={modalTitle}
      />

      {/* Hero Header */}
      <SearchHeader
        isSearchExpanded={isSearchExpanded}
        isOffline={isOffline}
      />

      {/* Search Section */}
      <RouteSearchForm
        fromStop={fromStop}
        setFromStop={setFromStop}
        toStop={toStop}
        setToStop={setToStop}
        stops={stops}
        loading={loading}
        isSearchExpanded={isSearchExpanded}
        setIsSearchExpanded={setIsSearchExpanded}
        hasSearched={hasSearched}
        recentSearches={recentSearches}
        onSearch={handleSearch}
        onSwap={handleSwap}
      />

      {/* Error Message */}
      {error && (
        <div className="bg-red-50/80 backdrop-blur-md border border-red-200 p-6 mb-12 rounded-2xl text-left animate-in zoom-in-95 duration-300 flex gap-4 items-start shadow-xl shadow-red-500/5">
          <AlertCircleIcon className="text-red-500 shrink-0 mt-0.5" />
          <div>
            <p className="text-red-800 font-bold font-display text-lg tracking-tight mb-1">
              Attention
            </p>
            <p className="text-red-700 text-sm font-medium">{error}</p>
          </div>
        </div>
      )}

      {/* Results Section */}
      <div className="flex-1 overflow-y-auto min-h-0 space-y-6 pb-2 pr-1 -mr-1 relative z-10">
        {loading && <SkeletonLoader />}

        {!loading && results.length > 0 && (() => {
          const metroCount = results.filter((r) => getSearchResultMode(r).hasMetro).length;
          const pureBusCount = results.filter((r) => getSearchResultMode(r).isPureBus).length;
          const anyBusCount = results.filter((r) => getSearchResultMode(r).hasBus).length;
          const busCount = pureBusCount > 0 ? pureBusCount : anyBusCount;

          const filtered = results.filter((r) => {
            if (modeFilter === "all") return true;
            const modeInfo = getSearchResultMode(r);
            if (modeFilter === "metro") return modeInfo.hasMetro;
            if (modeFilter === "bus") return pureBusCount > 0 ? modeInfo.isPureBus : modeInfo.hasBus;
            return true;
          });

          const displayedResults = [...filtered].sort((a, b) => {
            if (sortBy === "fare") {
              const fareA = a.type === "direct" ? a.fare : a.type === "transit" ? a.total_fare : a.route.fare;
              const fareB = b.type === "direct" ? b.fare : b.type === "transit" ? b.total_fare : b.route.fare;
              return fareA - fareB;
            }
            if (sortBy === "distance") {
              const distA = a.type === "direct" ? a.distance_km : a.type === "transit" ? a.total_distance_km : a.route.distance_km;
              const distB = b.type === "direct" ? b.distance_km : b.type === "transit" ? b.total_distance_km : b.route.distance_km;
              return distA - distB;
            }
            return 0; // Default backend priority (Metro pinned, then fare, then distance)
          });

          return (
            <>
              <div className="space-y-3 mb-5">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <h2 className="text-[10px] uppercase tracking-[0.3em] font-extrabold text-slate-400 flex items-center gap-2 font-display animate-in fade-in duration-500">
                      Available Routes ({displayedResults.length})
                    </h2>
                    <div className="h-px w-8 bg-gradient-to-r from-slate-200 to-transparent" />
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    {/* Mode Filter Control */}
                    {metroCount > 0 && busCount > 0 && (
                      <div className="inline-flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/70 shadow-inner w-fit">
                        <button
                          onClick={() => setModeFilter("all")}
                          className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all font-display ${
                            modeFilter === "all"
                              ? "bg-white text-slate-900 shadow-sm"
                              : "text-slate-500 hover:text-slate-800"
                          }`}
                        >
                          All ({results.length})
                        </button>
                        <button
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
                          onClick={() => setSortBy("recommended")}
                          title="মেট্রো ও সেরা ভাড়ার অগ্রাধিকার"
                          className={`px-2.5 py-1.5 rounded-lg text-xs font-bold transition-all font-display ${
                            sortBy === "recommended"
                              ? "bg-white text-slate-900 shadow-sm"
                              : "text-slate-500 hover:text-slate-800"
                          }`}
                        >
                          সুপারিশকৃত
                        </button>
                        <button
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
                        onOpenStops={openStopsModal}
                        onShare={handleShare}
                        animationClass={animationClass}
                      />
                    </div>
                  );
                }

                if (res.type === "direct") {
                  return (
                    <DirectRouteCard
                      key={i}
                      route={res}
                      onOpenStops={openStopsModal}
                      onShare={handleShare}
                      animationClass={animationClass}
                    />
                  );
                }

                return (
                  <TransitRouteCard
                    key={i}
                    result={res}
                    onOpenStops={openStopsModal}
                    onShare={handleShare}
                    animationClass={animationClass}
                  />
                );
              })}

              {displayedResults.length === 0 && (
                <div className="text-center py-14 bg-white/50 backdrop-blur border border-slate-200 border-dashed rounded-3xl animate-in zoom-in-95 duration-500">
                  <p className="text-slate-500 font-display font-medium text-base mb-3">
                    এই ফিল্টারে কোনো রুট পাওয়া যায়নি।
                  </p>
                  <button
                    onClick={() => setModeFilter("all")}
                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 rounded-xl text-xs font-bold text-slate-700 transition-colors font-display"
                  >
                    সকল রুট দেখুন
                  </button>
                </div>
              )}
            </>
          );
        })()}

        {results.length === 0 && !loading && !error && fromStop && toStop && (
          <div className="text-center py-20 bg-white/50 backdrop-blur border border-slate-200 border-dashed rounded-3xl animate-in zoom-in-95 duration-500">
            <NavigationIcon size={48} className="mx-auto text-slate-300 mb-4" />
            <p className="text-slate-500 font-display font-medium text-lg px-6">
              No direct or transit bus routes found.
            </p>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="shrink-0 mt-4 pt-4 border-t border-slate-200/60 flex flex-col items-center gap-2 relative z-10">
        <p className="text-[10px] font-extrabold uppercase tracking-[0.2em] text-slate-400 text-center font-display">
          © 2026 Poth.bd • Nationwide Transit Navigator
        </p>
      </footer>
    </main>
  );
}

