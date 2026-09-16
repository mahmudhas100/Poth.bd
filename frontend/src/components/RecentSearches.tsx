"use client";

import React from "react";

interface RecentSearchItem {
  from: string;
  to: string;
}

interface RecentSearchesProps {
  searches: RecentSearchItem[];
  onSelect: (from: string, to: string) => void;
}

export const RecentSearches: React.FC<RecentSearchesProps> = ({
  searches,
  onSelect,
}) => {
  if (searches.length === 0) return null;

  return (
    <div className="mb-4 flex flex-wrap items-center gap-2 pt-2">
      <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 font-display">
        Recent:
      </span>
      {searches.map((item, idx) => (
        <button
          key={idx}
          type="button"
          onClick={() => onSelect(item.from, item.to)}
          className="px-2.5 py-1 bg-slate-100/90 hover:bg-blue-50 hover:text-accent border border-slate-200/60 rounded-full text-xs font-bengali font-medium text-slate-600 transition-colors flex items-center gap-1 shadow-2xs"
        >
          <span>{item.from}</span>
          <span className="text-slate-400">⇄</span>
          <span>{item.to}</span>
        </button>
      ))}
    </div>
  );
};
