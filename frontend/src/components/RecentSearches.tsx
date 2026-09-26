"use client";

import React from "react";

export interface RoutePillItem {
  from: string;
  to: string;
  isRecent?: boolean;
}

export const DEFAULT_COMMON_ROUTES: RoutePillItem[] = [
  { from: "মিরপুর-১০", to: "মতিঝিল", isRecent: false },
  { from: "উত্তরা", to: "ফার্মগেট", isRecent: false },
  { from: "ফার্মগেট", to: "সদরঘাট", isRecent: false },
  { from: "মিরপুর-১২", to: "আজিমপুর", isRecent: false },
  { from: "গাবতলি", to: "সায়েদাবাদ", isRecent: false },
  { from: "ধানমন্ডি ২৭", to: "গুলশান-১", isRecent: false },
  { from: "কুড়িল বিশ্বরোড", to: "নিউ মার্কেট", isRecent: false },
  { from: "এয়ারপোর্ট", to: "কমলাপুর", isRecent: false },
];

interface RecentSearchesProps {
  searches: RoutePillItem[];
  onSelect: (from: string, to: string) => void;
  onReset?: () => void;
  onToggleHide?: () => void;
  isHidden?: boolean;
}

export const RecentSearches: React.FC<RecentSearchesProps> = ({
  searches,
  onSelect,
  onReset,
  onToggleHide,
  isHidden = false,
}) => {
  if (isHidden) {
    return (
      <div className="mb-3 pt-1 flex justify-end animate-in fade-in duration-200">
        <button
          type="button"
          onClick={onToggleHide}
          className="text-xs font-medium font-bengali text-slate-500 hover:text-accent bg-slate-100/90 hover:bg-blue-50 px-3 py-1 rounded-full border border-slate-200/70 transition-all duration-200 flex items-center gap-1.5 active:scale-95 shadow-2xs hover:shadow-xs"
        >
          <span>কমন রুটগুলি</span>
          <span className="text-[10px] text-slate-400">▾</span>
        </button>
      </div>
    );
  }

  const items = searches.length > 0 ? searches : DEFAULT_COMMON_ROUTES;

  return (
    <div className="mb-4 pt-1 space-y-2 animate-in fade-in slide-in-from-top-1 duration-200">
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500 font-display">
          কমন ও সাম্প্রতিক রুট
        </span>
        <div className="flex items-center gap-2">
          {onReset && (
            <button
              type="button"
              onClick={onReset}
              title="ডিফল্ট রুটে রিসেট করুন"
              className="text-[10px] text-slate-500 hover:text-rose-600 font-medium font-bengali transition-colors"
            >
              রিসেট
            </button>
          )}
          {onToggleHide && (
            <>
              <span className="text-slate-300 text-[10px]">•</span>
              <button
                type="button"
                onClick={onToggleHide}
                title="লুকান"
                className="text-[10px] text-slate-500 hover:text-slate-800 font-medium font-bengali transition-colors"
              >
                লুকান
              </button>
            </>
          )}
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
        {items.map((item, idx) => (
          <button
            key={`${item.from}-${item.to}-${idx}`}
            type="button"
            onClick={() => onSelect(item.from, item.to)}
            className={`px-2.5 py-1 rounded-full text-xs font-bengali font-medium transition-all duration-200 ease-out flex items-center gap-1.5 shadow-2xs hover:scale-[1.03] active:scale-95 group ${
              item.isRecent
                ? "bg-blue-50/90 text-accent border border-blue-200/80 hover:bg-blue-100/90 hover:shadow-xs"
                : "bg-slate-100/90 hover:bg-blue-50 hover:text-accent border border-slate-200/60 text-slate-600 hover:shadow-xs"
            }`}
          >
            {item.isRecent && (
              <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse shrink-0" />
            )}
            <span>{item.from}</span>
            <span className="text-slate-400 group-hover:text-accent transition-colors">⇄</span>
            <span>{item.to}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
