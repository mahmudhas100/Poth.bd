"use client";

import React from "react";
import { SearchIcon, MoveRightIcon } from "@animateicons/react/lucide";
import { BusIcon, NavigationIcon, RouteDistanceIcon, ShareIcon, MapPinIcon } from "@/components/ui/Icons";
import { DirectFareResult, TransitResult, SuggestionResult } from "@/types/transit";
import { getGoogleMapsDirectionUrl } from "@/lib/maps";

interface DirectRouteCardProps {
  route: DirectFareResult;
  onOpenStops: (stops: string[], title: string) => void;
  onShare: (fromBn: string, toBn: string, fromEn: string, toEn: string, routeName: string, distance: number, fare: number) => void;
  animationClass?: string;
}

export const DirectRouteCard: React.FC<DirectRouteCardProps> = ({
  route,
  onOpenStops,
  onShare,
  animationClass = "",
}) => {
  return (
    <div className={`transit-card ${animationClass}`}>
      <div className="space-y-5">
        <div className="flex flex-row items-center justify-between gap-3 sm:gap-5">
          <div className="space-y-2 min-w-0 flex-1">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 bg-blue-50 text-accent rounded-md font-bold text-[9px] uppercase tracking-widest font-display">
              <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
              Direct Route
            </div>
            <h3 className="text-xl sm:text-2xl md:text-3xl leading-tight font-bengali font-bold text-slate-900 truncate whitespace-normal">
              {route.from_stop_bn} ⇄ {route.to_stop_bn}
            </h3>
            <div className="flex flex-col gap-1.5">
              <p className="text-slate-600 text-sm sm:text-[15px] font-bengali font-semibold bg-slate-50 px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg inline-flex w-fit border border-slate-100 items-center">
                <BusIcon size={14} className="mr-2 text-slate-400 shrink-0" /> {route.route_name}
              </p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <RouteDistanceIcon size={14} className="text-slate-400 shrink-0" />
                <p className="text-slate-500 text-xs sm:text-sm font-bengali font-medium">
                  <span className="font-display font-bold text-slate-700">{route.distance_km}</span> কি.মি. দূরত্ব
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-col items-end justify-center shrink-0">
            <div className="text-4xl sm:text-5xl md:text-6xl fare-number-accent whitespace-nowrap">
              <span className="text-2xl sm:text-3xl opacity-50 font-bengali font-normal mr-1">৳</span>
              {route.fare}
            </div>
            <p className="text-slate-400 text-[9px] uppercase tracking-[0.2em] font-display font-bold mt-1 whitespace-nowrap">
              Total Fare
            </p>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onOpenStops(route.stops, "Route Map")}
            className="flex-1 py-3.5 bg-slate-50/50 hover:bg-blue-50 border border-slate-200/60 rounded-xl text-xs font-bold uppercase tracking-widest text-slate-500 hover:text-accent hover:border-blue-200 transition-all flex items-center justify-center gap-2 group font-display"
          >
            <NavigationIcon size={14} className="group-hover:-translate-y-0.5 transition-transform" />
            View All Stops
          </button>
          <a
            href={getGoogleMapsDirectionUrl(route.from_stop, route.to_stop)}
            target="_blank"
            rel="noopener noreferrer"
            className="px-3.5 sm:px-4 py-3.5 bg-slate-50/50 hover:bg-emerald-50 border border-slate-200/60 rounded-xl text-slate-500 hover:text-emerald-600 hover:border-emerald-200 transition-all flex items-center justify-center gap-1.5 group font-display"
            title="গুগল ম্যাপে ডিরেকশন দেখুন (Google Maps)"
          >
            <MapPinIcon size={15} className="group-hover:scale-110 text-emerald-600 transition-transform" />
            <span className="text-xs font-bold uppercase tracking-wider hidden sm:inline text-emerald-700">Maps</span>
          </a>
          <button
            onClick={() =>
              onShare(
                route.from_stop_bn,
                route.to_stop_bn,
                route.from_stop,
                route.to_stop,
                route.route_name,
                route.distance_km,
                route.fare
              )
            }
            className="px-3.5 sm:px-4 py-3.5 bg-slate-50/50 hover:bg-blue-50 border border-slate-200/60 rounded-xl text-slate-400 hover:text-accent hover:border-blue-200 transition-all flex items-center justify-center"
            title="Share Fare Details"
          >
            <ShareIcon size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

interface TransitRouteCardProps {
  result: TransitResult;
  onOpenStops: (stops: string[], title: string) => void;
  onShare: (fromBn: string, toBn: string, fromEn: string, toEn: string, routeName: string, distance: number, fare: number) => void;
  animationClass?: string;
}

export const TransitRouteCard: React.FC<TransitRouteCardProps> = ({
  result,
  onOpenStops,
  onShare,
  animationClass = "",
}) => {
  return (
    <div className={`transit-card ${animationClass}`}>
      <div className="space-y-6">
        <div className="flex flex-row items-center justify-between gap-3 sm:gap-4 border-b border-slate-100 pb-6">
          <div className="space-y-2 min-w-0 flex-1">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 bg-amber-50 text-amber-600 rounded-md font-bold text-[9px] uppercase tracking-widest font-display">
              <div className="w-1.5 h-1.5 rounded-full bg-amber-500" />
              Transit Required
            </div>
            <h3 className="text-xl sm:text-2xl md:text-3xl leading-tight font-bengali font-bold text-slate-900 truncate whitespace-normal">
              {result.leg1.from_stop_bn} <MoveRightIcon className="inline opacity-30 mx-0.5 sm:mx-1" size={20} /> {result.leg2.to_stop_bn}
            </h3>
            <div className="flex flex-wrap items-center gap-x-2 gap-y-1 mt-1 text-slate-500 text-xs sm:text-sm font-bengali font-medium">
              <div className="flex items-center">
                <span className="font-bold text-amber-600 bg-amber-50 px-1 sm:px-2 py-0.5 rounded mr-1">
                  {result.transfer_at_bn}
                </span>
                -এ বাস বদলান
              </div>
              <span className="text-slate-300 hidden sm:inline">•</span>
              <div className="flex items-center gap-1.5">
                <RouteDistanceIcon size={14} className="text-slate-400 shrink-0" />
                <span>
                  মোট <span className="font-display font-bold text-slate-700">{result.total_distance_km}</span> কি.মি.
                </span>
              </div>
            </div>
          </div>
          <div className="flex flex-col items-end justify-center shrink-0">
            <div className="text-4xl sm:text-5xl md:text-6xl fare-number-accent whitespace-nowrap">
              <span className="text-2xl sm:text-3xl opacity-50 font-bengali font-normal mr-1">৳</span>
              {result.total_fare}
            </div>
            <p className="text-slate-400 text-[9px] uppercase tracking-[0.2em] font-display font-bold mt-1 whitespace-nowrap">
              Total Fare
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-2 relative">
          <div className="absolute left-[27px] top-8 bottom-8 w-0.5 bg-slate-200 z-0" />

          {/* Leg 1 */}
          <div
            onClick={() => onOpenStops(result.leg1.stops, `Leg 1: ${result.leg1.route_name}`)}
            className="bg-white border border-slate-100 p-4 rounded-2xl flex justify-between items-center cursor-pointer hover:border-accent/30 hover:shadow-md transition-all group relative z-10"
          >
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 border border-blue-100 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                1
              </div>
              <div>
                <h4 className="font-bold text-lg font-bengali text-slate-800">
                  {result.leg1.from_stop_bn} ⇄ {result.leg1.to_stop_bn}
                </h4>
                <p className="text-sm text-slate-500 font-bengali font-medium">
                  রুট: {result.leg1.route_name}
                </p>
              </div>
            </div>
            <div className="text-xl sm:text-2xl fare-number text-slate-600 whitespace-nowrap shrink-0">
              ৳{result.leg1.fare}
            </div>
          </div>

          <div className="flex justify-center py-2 relative z-10">
            <div className="bg-amber-100/50 backdrop-blur-sm border border-amber-200/50 text-[10px] font-bold text-amber-700 px-4 py-1.5 rounded-full uppercase tracking-widest font-display shadow-sm">
              Change at {result.transfer_at_bn}
            </div>
          </div>

          {/* Leg 2 */}
          <div
            onClick={() => onOpenStops(result.leg2.stops, `Leg 2: ${result.leg2.route_name}`)}
            className="bg-white border border-slate-100 p-4 rounded-2xl flex justify-between items-center cursor-pointer hover:border-emerald-500/30 hover:shadow-md transition-all group relative z-10"
          >
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0 border border-emerald-100 group-hover:bg-emerald-500 group-hover:text-white transition-colors">
                2
              </div>
              <div>
                <h4 className="font-bold text-lg font-bengali text-slate-800">
                  {result.leg2.from_stop_bn} ⇄ {result.leg2.to_stop_bn}
                </h4>
                <p className="text-sm text-slate-500 font-bengali font-medium">
                  রুট: {result.leg2.route_name}
                </p>
              </div>
            </div>
            <div className="text-xl sm:text-2xl fare-number text-slate-600 whitespace-nowrap shrink-0">
              ৳{result.leg2.fare}
            </div>
          </div>
        </div>

        <div className="flex gap-2">
          <a
            href={getGoogleMapsDirectionUrl(
              result.leg1.from_stop,
              result.leg2.to_stop
            )}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 py-3 bg-slate-50/50 hover:bg-emerald-50 border border-slate-200/60 rounded-xl text-xs font-bold uppercase tracking-widest text-slate-500 hover:text-emerald-600 hover:border-emerald-200 transition-all flex items-center justify-center gap-2 group font-display"
            title="গুগল ম্যাপে ট্রানজিট ডিরেকশন দেখুন (Google Maps)"
          >
            <MapPinIcon size={14} className="group-hover:scale-110 text-emerald-600 transition-transform" />
            Maps Direction
          </a>
          <button
            onClick={() =>
              onShare(
                result.leg1.from_stop_bn,
                result.leg2.to_stop_bn,
                result.leg1.from_stop,
                result.leg2.to_stop,
                `Transit via ${result.transfer_at_bn}`,
                result.total_distance_km,
                result.total_fare
              )
            }
            className="px-4 py-3 bg-slate-50/50 hover:bg-amber-50 border border-slate-200/60 rounded-xl text-xs font-bold uppercase tracking-widest text-slate-500 hover:text-amber-600 hover:border-amber-200 transition-all flex items-center justify-center gap-2 group font-display"
            title="Share Transit Details"
          >
            <ShareIcon size={14} className="group-hover:scale-110 transition-transform" />
            <span className="hidden sm:inline">Share</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export const SuggestionBanner: React.FC<{ suggestion: SuggestionResult }> = ({ suggestion }) => (
  <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-b border-amber-100 p-5 -mx-6 -mt-6 mb-6 flex items-start gap-4">
    <div className="bg-amber-500 p-1.5 rounded-full text-white shadow-sm shrink-0">
      <SearchIcon size={14} />
    </div>
    <div className="space-y-1">
      <p className="text-[10px] font-extrabold text-amber-800 leading-none uppercase tracking-[0.2em] font-display">
        Suggestion
      </p>
      <p className="text-sm text-amber-900 font-bengali leading-tight font-medium">
        {suggestion.message}
      </p>
    </div>
  </div>
);

export const SkeletonLoader: React.FC = () => (
  <div className="space-y-6 pt-2">
    {[1, 2, 3].map((i) => (
      <div
        key={i}
        className="bg-white/40 border border-white/60 p-5 rounded-3xl animate-pulse flex flex-col gap-5 shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
      >
        <div className="flex justify-between items-start gap-4">
          <div className="space-y-3 flex-1">
            <div className="h-4 w-20 bg-slate-200/60 rounded-md"></div>
            <div className="h-8 w-3/4 bg-slate-200/80 rounded-lg"></div>
            <div className="h-6 w-1/2 bg-slate-200/60 rounded-lg"></div>
          </div>
          <div className="space-y-2 flex flex-col items-end">
            <div className="h-10 w-16 bg-slate-200/80 rounded-lg"></div>
            <div className="h-3 w-12 bg-slate-200/60 rounded-md"></div>
          </div>
        </div>
        <div className="h-12 w-full bg-slate-200/40 rounded-xl mt-2"></div>
      </div>
    ))}
  </div>
);
