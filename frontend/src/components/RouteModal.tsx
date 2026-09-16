"use client";

import React from "react";
import { XIcon } from "@animateicons/react/lucide";
import { BusIcon } from "@/components/ui/Icons";

interface RouteModalProps {
  isOpen: boolean;
  onClose: () => void;
  stops: string[];
  title: string;
}

export const RouteModal: React.FC<RouteModalProps> = ({
  isOpen,
  onClose,
  stops,
  title,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-md animate-in fade-in duration-300">
      <div className="bg-white/95 backdrop-blur-2xl w-full max-w-md rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh] border border-white slide-in-from-bottom-4 animate-in duration-500">
        <div className="p-6 border-b border-border/50 flex justify-between items-center bg-white/50">
          <h3 className="font-display font-extrabold text-xl uppercase tracking-tight text-slate-800 flex items-center gap-2">
            <BusIcon size={20} className="text-accent" />
            {title}
          </h3>
          <button
            onClick={onClose}
            className="p-2 bg-slate-100 hover:bg-slate-200 rounded-full transition-colors text-slate-500 hover:text-slate-900"
          >
            <XIcon size={20} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-8 relative">
          {/* SVG Visual Track Line */}
          <div className="absolute left-[43px] top-10 bottom-12 w-1 bg-gradient-to-b from-blue-500 via-indigo-400 to-emerald-400 rounded-full opacity-30" />

          <div className="space-y-8 relative z-10">
            {stops.map((stop, idx) => {
              const isStart = idx === 0;
              const isEnd = idx === stops.length - 1;
              const isMiddle = !isStart && !isEnd;

              return (
                <div key={idx} className="flex items-start gap-5">
                  <div className="relative pt-1">
                    {/* Node Circle */}
                    <div
                      className={`w-6 h-6 rounded-full border-4 flex items-center justify-center shadow-sm bg-white ${
                        isStart
                          ? "border-blue-500"
                          : isEnd
                          ? "border-emerald-500"
                          : "border-slate-300 w-4 h-4 ml-1 mt-1"
                      }`}
                    >
                      {(isStart || isEnd) && (
                        <div
                          className={`w-2 h-2 rounded-full ${
                            isStart ? "bg-blue-500" : "bg-emerald-500"
                          }`}
                        />
                      )}
                    </div>
                  </div>

                  <div className={`space-y-0.5 ${isMiddle ? "pt-0.5 opacity-70" : ""}`}>
                    <p
                      className={`font-bengali text-lg leading-none ${
                        !isMiddle ? "font-bold text-slate-900 text-xl" : "font-medium text-slate-600"
                      }`}
                    >
                      {stop}
                    </p>
                    {isStart && (
                      <p className="text-[10px] uppercase font-bold text-blue-500 tracking-widest font-display">
                        Journey Start
                      </p>
                    )}
                    {isEnd && (
                      <p className="text-[10px] uppercase font-bold text-emerald-500 tracking-widest font-display">
                        Destination
                      </p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="p-5 bg-slate-50/80 border-t border-border/50">
          <button
            onClick={onClose}
            className="w-full py-4 bg-slate-900 text-white font-display font-bold uppercase tracking-widest text-sm rounded-xl hover:bg-slate-800 transition-colors shadow-lg shadow-slate-900/20 active:scale-95"
          >
            Close Route Map
          </button>
        </div>
      </div>
    </div>
  );
};
