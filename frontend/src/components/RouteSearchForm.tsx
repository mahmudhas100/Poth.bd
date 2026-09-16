"use client";

import React from "react";
import { SearchIcon, MapPinIcon } from "@animateicons/react/lucide";
import { NavigationIcon, ChevronDownIcon, ChevronUpIcon, SwapIcon } from "@/components/ui/Icons";
import { AutocompleteInput } from "@/components/AutocompleteInput";
import { RecentSearches } from "@/components/RecentSearches";
import { Stop } from "@/types/transit";

interface RouteSearchFormProps {
  fromStop: string;
  setFromStop: (val: string) => void;
  toStop: string;
  setToStop: (val: string) => void;
  stops: Stop[];
  loading: boolean;
  isSearchExpanded: boolean;
  setIsSearchExpanded: (val: boolean) => void;
  hasSearched: boolean;
  recentSearches: { from: string; to: string }[];
  onSearch: (e: React.FormEvent) => void;
  onSwap: () => void;
}

export const RouteSearchForm: React.FC<RouteSearchFormProps> = ({
  fromStop,
  setFromStop,
  toStop,
  setToStop,
  stops,
  loading,
  isSearchExpanded,
  setIsSearchExpanded,
  hasSearched,
  recentSearches,
  onSearch,
  onSwap,
}) => {
  return (
    <section
      className={`shrink-0 animate-in slide-in-from-bottom-10 duration-700 delay-150 fade-in fill-mode-both relative z-20 transition-all duration-500 ${
        isSearchExpanded ? "mb-6 md:mb-10" : "mb-3"
      }`}
    >
      <div className="bg-white/40 backdrop-blur-2xl rounded-3xl border border-white/60 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
        <form
          onSubmit={onSearch}
          className={`flex flex-col relative transition-all duration-500 ${
            isSearchExpanded ? "p-5 sm:p-6 md:p-8" : "py-3.5 px-5"
          }`}
        >
          {/* Collapsed Summary Header */}
          {!isSearchExpanded && hasSearched && (
            <div
              onClick={() => setIsSearchExpanded(true)}
              className="flex justify-between items-center cursor-pointer animate-in fade-in duration-300"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-accent/10 flex items-center justify-center text-accent">
                  <SearchIcon size={14} />
                </div>
                <p className="font-bengali font-bold text-slate-800 text-base sm:text-lg">
                  {fromStop} <span className="text-slate-400 mx-1">⇄</span> {toStop}
                </p>
              </div>
            </div>
          )}

          {/* Input Fields Container */}
          <div
            className={`transition-all duration-500 ease-in-out ${
              isSearchExpanded ? "max-h-[500px] opacity-100 overflow-visible" : "max-h-0 opacity-0 overflow-hidden"
            }`}
          >
            <div
              className={`flex flex-col md:flex-row gap-5 md:gap-8 relative transition-all duration-500 ${
                isSearchExpanded ? "pb-5 md:pb-8" : "pb-0"
              }`}
            >
              <div className="flex-1 flex flex-col gap-2">
                <label className="text-[10px] font-extrabold uppercase tracking-[0.2em] text-slate-500 pl-1">
                  কোথা থেকে
                </label>
                <AutocompleteInput
                  value={fromStop}
                  onChange={setFromStop}
                  options={stops}
                  placeholder="যেমন: এয়ারপোর্ট"
                  icon={<NavigationIcon size={20} />}
                />
              </div>

              {/* Desktop Swap Button */}
              <button
                type="button"
                onClick={onSwap}
                className="hidden md:flex absolute left-1/2 top-1/2 -translate-x-1/2 translate-y-[2px] z-10 w-9 h-9 rounded-full bg-white border border-slate-200 shadow-sm items-center justify-center text-slate-400 hover:text-accent hover:border-accent/50 hover:scale-110 active:scale-95 transition-all focus:outline-none focus:ring-2 focus:ring-accent/20"
                title="Swap destinations"
              >
                <SwapIcon size={16} />
              </button>

              {/* Mobile Swap Button */}
              <div className="flex-1 flex flex-col gap-2 relative">
                <button
                  type="button"
                  onClick={onSwap}
                  className="md:hidden absolute -top-6 left-1/2 -translate-x-1/2 z-10 w-9 h-9 rounded-full bg-white border border-slate-200 shadow-sm flex items-center justify-center text-slate-400 hover:text-accent hover:border-accent/50 hover:scale-110 active:scale-95 transition-all focus:outline-none focus:ring-2 focus:ring-accent/20"
                >
                  <SwapIcon size={16} className="rotate-90" />
                </button>
                <label className="text-[10px] font-extrabold uppercase tracking-[0.2em] text-slate-500 pl-1 md:pl-2">
                  কোথায় যাবেন
                </label>
                <AutocompleteInput
                  value={toStop}
                  onChange={setToStop}
                  options={stops}
                  placeholder="যেমন: মতিঝিল"
                  icon={<MapPinIcon size={20} />}
                />
              </div>
            </div>
          </div>

          {/* Submit Button & Recent Chips */}
          <div
            className={`transition-all duration-500 ease-in-out ${
              isSearchExpanded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4 max-h-0 overflow-hidden m-0"
            }`}
          >
            <RecentSearches
              searches={recentSearches}
              onSelect={(from, to) => {
                setFromStop(from);
                setToStop(to);
              }}
            />

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full flex justify-center items-center gap-2 group"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <SearchIcon size={20} className="animate-spin" /> লোডিং...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <SearchIcon size={20} className="group-hover:scale-110 transition-transform" /> ভাড়া দেখুন
                </span>
              )}
            </button>
          </div>

          {/* Collapser / Expander Button */}
          {hasSearched && (
            <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 z-30">
              <button
                type="button"
                onClick={() => setIsSearchExpanded(!isSearchExpanded)}
                className="bg-white border border-slate-200 text-slate-400 hover:text-accent shadow-sm rounded-full p-1.5 transition-all hover:scale-110 active:scale-95"
              >
                {isSearchExpanded ? <ChevronUpIcon size={18} /> : <ChevronDownIcon size={18} />}
              </button>
            </div>
          )}
        </form>
      </div>
    </section>
  );
};
