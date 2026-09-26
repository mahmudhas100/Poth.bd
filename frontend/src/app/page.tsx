"use client";

import { useState, useEffect, useCallback } from "react";
import dynamic from "next/dynamic";
import { AlertCircleIcon, NavigationIcon, DownloadIcon } from "@/components/ui/Icons";
import { SearchHeader } from "@/components/SearchHeader";
import { RouteSearchForm } from "@/components/RouteSearchForm";
import { Toast } from "@/components/ui/Toast";
import { SkeletonLoader } from "@/components/SkeletonLoader";
import { fetchStops, searchFare } from "@/lib/api";
import { DEFAULT_COMMON_ROUTES, RoutePillItem } from "@/components/RecentSearches";
import { Stop, SearchResult } from "@/types/transit";

const RouteModal = dynamic(
  () => import("@/components/RouteModal").then((mod) => mod.RouteModal),
  { ssr: false }
);

const SearchResultsView = dynamic(
  () => import("@/components/SearchResultsView").then((mod) => mod.SearchResultsView),
  {
    ssr: false,
    loading: () => <SkeletonLoader />,
  }
);

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

export default function BusVaraApp() {
  const [fromStop, setFromStop] = useState("");
  const [toStop, setToStop] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stops, setStops] = useState<Stop[]>([]);
  const [isSearchExpanded, setIsSearchExpanded] = useState(true);
  const [hasSearched, setHasSearched] = useState(false);
  const [pills, setPills] = useState<RoutePillItem[]>(DEFAULT_COMMON_ROUTES);
  const [isPillsHidden, setIsPillsHidden] = useState(false);
  const [isOffline, setIsOffline] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [modalStops, setModalStops] = useState<string[]>([]);
  const [modalTitle, setModalTitle] = useState("");

  const recordSearchedPill = (from: string, to: string) => {
    setPills((prev) => {
      const filtered = prev.filter(
        (p) => !(p.from === from && p.to === to) && !(p.from === to && p.to === from)
      );
      const updated: RoutePillItem[] = [
        { from, to, isRecent: true },
        ...filtered,
      ].slice(0, 8);
      try {
        localStorage.setItem("poth_route_pills", JSON.stringify(updated));
      } catch (e) {
        console.error(e);
      }
      return updated;
    });
  };

  const executeSearch = useCallback(async (from: string, to: string) => {
    if (!from || !to) {
      setError("দয়া করে প্রস্থান এবং গন্তব্য স্থান উভয়ই নির্বাচন করুন।");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await searchFare(from, to);
      setResults(data);
      setHasSearched(true);
      recordSearchedPill(from, to);
      setIsSearchExpanded(false);

      // Update URL query params without reloading
      if (typeof window !== "undefined") {
        const url = new URL(window.location.href);
        url.searchParams.set("from", from);
        url.searchParams.set("to", to);
        window.history.pushState({}, "", url.toString());
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "গন্তব্য খুঁজে পাওয়া যায়নি।";
      setError(
        msg === "Stop not recognized. Please check spelling."
          ? "গন্তব্য খুঁজে পাওয়া যায়নি। দয়া করে সঠিক বানান লিখুন।"
          : msg
      );
      setResults([]);
      setIsSearchExpanded(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStops()
      .then((data) => setStops(data))
      .catch((err) => console.error("Could not fetch stops:", err));

    // Load route pills and hidden preference from localStorage after hydration
    try {
      const savedPills = localStorage.getItem("poth_route_pills") || localStorage.getItem("busvara_recents");
      if (savedPills) {
        const parsed = JSON.parse(savedPills);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setPills(parsed);
        }
      }
      const savedHidden = localStorage.getItem("poth_pills_hidden");
      if (savedHidden !== null) {
        setIsPillsHidden(savedHidden === "true");
      }
    } catch (e) {
      console.error("Could not load route pills:", e);
    }

    // Check offline status
    setIsOffline(!navigator.onLine);
    const updateOnlineStatus = () => setIsOffline(!navigator.onLine);
    window.addEventListener("online", updateOnlineStatus);
    window.addEventListener("offline", updateOnlineStatus);

    // Check standalone PWA installation status
    const nav = window.navigator as unknown as { standalone?: boolean };
    if (window.matchMedia("(display-mode: standalone)").matches || Boolean(nav.standalone)) {
      setIsInstalled(true);
    }

    const handleBeforeInstall = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
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
    if (urlFrom) setFromStop(urlFrom);
    if (urlTo) setToStop(urlTo);
    if (urlFrom && urlTo) {
      executeSearch(urlFrom, urlTo);
    }

    return () => {
      window.removeEventListener("online", updateOnlineStatus);
      window.removeEventListener("offline", updateOnlineStatus);
      window.removeEventListener("beforeinstallprompt", handleBeforeInstall);
      window.removeEventListener("appinstalled", handleAppInstalled);
    };
  }, [executeSearch]);

  const handleSwap = () => {
    const temp = fromStop;
    setFromStop(toStop);
    setToStop(temp);
    if (hasSearched && temp && toStop) {
      executeSearch(toStop, temp);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    executeSearch(fromStop, toStop);
  };

  const handleSelectPill = (from: string, to: string) => {
    setFromStop(from);
    setToStop(to);
    executeSearch(from, to);
  };

  const handleResetPills = () => {
    setPills(DEFAULT_COMMON_ROUTES);
    try {
      localStorage.removeItem("poth_route_pills");
      localStorage.removeItem("busvara_recents");
    } catch (e) {
      console.error(e);
    }
    setToastMessage("ডিফল্ট রুটে রিসেট করা হয়েছে");
  };

  const handleToggleHidePills = () => {
    setIsPillsHidden((prev) => {
      const next = !prev;
      try {
        localStorage.setItem("poth_pills_hidden", String(next));
      } catch (e) {
        console.error(e);
      }
      return next;
    });
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
      } catch {
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
    } catch {
      setToastMessage("লিংক কপি করতে ব্যর্থ হয়েছে।");
    }
  };

  const openStopsModal = (stops: string[], title: string) => {
    setModalStops(stops);
    setModalTitle(title);
    setModalOpen(true);
  };

  const handleInstallApp = async () => {
    if (!deferredPrompt) return;
    try {
      await deferredPrompt.prompt();
      const choice = await deferredPrompt.userChoice;
      if (choice.outcome === "accepted") {
        setDeferredPrompt(null);
        setIsInstalled(true);
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

      {modalOpen && (
        <RouteModal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          stops={modalStops}
          title={modalTitle}
        />
      )}

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
        recentSearches={pills}
        onSearch={handleSearch}
        onSwap={handleSwap}
        onSelectPill={handleSelectPill}
        onResetPills={handleResetPills}
        onToggleHidePills={handleToggleHidePills}
        isPillsHidden={isPillsHidden}
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

        {!loading && results.length > 0 && (
          <SearchResultsView
            key={`${fromStop}::${toStop}`}
            results={results}
            onOpenStops={openStopsModal}
            onShare={handleShare}
          />
        )}

        {results.length === 0 && !loading && !error && fromStop && toStop && hasSearched && (
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
