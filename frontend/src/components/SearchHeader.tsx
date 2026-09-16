"use client";

import React from "react";

interface SearchHeaderProps {
  isSearchExpanded: boolean;
  isOffline: boolean;
}

export const SearchHeader: React.FC<SearchHeaderProps> = ({
  isSearchExpanded,
  isOffline,
}) => {
  return (
    <div
      className={`transition-all duration-500 ease-in-out overflow-hidden ${
        isSearchExpanded ? "max-h-[500px] opacity-100 shrink-0" : "max-h-0 opacity-0 shrink-0 m-0"
      }`}
    >
      <header className="mb-6 md:mb-10 flex flex-col items-center md:items-start text-center md:text-left animate-in slide-in-from-bottom-8 duration-700 fade-in">
        <div className="flex flex-wrap items-center gap-2 mb-4">
          <div className="hidden sm:inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-accent/10 border border-accent/20 text-accent font-display font-bold text-[10px] uppercase tracking-widest">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-accent"></span>
            </span>
            BRTA Official Fare 2026
          </div>
          {isOffline && (
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-800 font-bengali font-semibold text-xs animate-pulse">
              <span className="w-2 h-2 rounded-full bg-amber-500" />
              অফলাইন মোড - ক্যাশ করা ডেটা ব্যবহৃত হচ্ছে
            </div>
          )}
        </div>

        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tighter uppercase font-display bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 drop-shadow-sm mb-2">
          Poth <span className="text-accent italic font-medium text-xl sm:text-2xl md:text-3xl lowercase relative sm:-top-2">.bd</span>
          <span className="text-slate-400 font-bengali font-semibold text-xl sm:text-2xl ml-2"> (পথ)</span>
        </h1>
        <p className="text-xs sm:text-base md:text-lg text-slate-600 leading-tight font-medium font-bengali mt-1 sm:mt-0">
          সঠিক রুট, নির্ভুল ভাড়া — আপনার ভ্রমণের সহজ পথ।
        </p>
      </header>
    </div>
  );
};
