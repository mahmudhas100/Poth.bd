"use client";

import React, { useState, useRef, useEffect, useLayoutEffect, useCallback } from "react";
import { createPortal } from "react-dom";
import { InfoIcon } from "@/components/ui/Icons";

interface FareInfoBadgeProps {
  mode?: "bus" | "metro";
  distanceKm?: number;
  fare?: number;
  minFare?: number;
  maxFare?: number;
  className?: string;
  align?: "left" | "right";
}

export const FareInfoBadge: React.FC<FareInfoBadgeProps> = ({
  mode = "bus",
  distanceKm,
  fare,
  minFare,
  maxFare,
  className = "",
  align = "right",
}) => {
  const [mounted, setMounted] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const popoverRef = useRef<HTMLDivElement>(null);

  const [coords, setCoords] = useState<{ top: number; left: number; placeAbove: boolean }>({
    top: 0,
    left: 0,
    placeAbove: false,
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const calculatePosition = useCallback(() => {
    if (!buttonRef.current) return null;
    const rect = buttonRef.current.getBoundingClientRect();

    // Auto-close if button is scrolled completely out of viewport
    if (rect.bottom < -20 || rect.top > window.innerHeight + 20) {
      return null;
    }

    const popoverWidth = Math.min(288, window.innerWidth - 24);
    let left = align === "right" ? rect.right - popoverWidth : rect.left;
    const minLeft = 12;
    const maxLeft = window.innerWidth - popoverWidth - 12;
    left = Math.max(minLeft, Math.min(left, maxLeft));

    const popoverHeight = popoverRef.current?.offsetHeight || 260;
    const spaceBelow = window.innerHeight - rect.bottom;
    const spaceAbove = rect.top;

    const placeAbove = spaceBelow < popoverHeight + 16 && spaceAbove > spaceBelow;

    const top = placeAbove
      ? Math.max(12, rect.top - popoverHeight - 8)
      : Math.min(window.innerHeight - popoverHeight - 12, rect.bottom + 8);

    return { top, left, placeAbove };
  }, [align]);

  const updatePosition = useCallback(() => {
    const nextCoords = calculatePosition();
    if (!nextCoords) {
      setIsOpen(false);
      return;
    }
    setCoords(nextCoords);
  }, [calculatePosition]);

  // Use isomorphic layout effect so position is calculated before browser paint
  const useIsomorphicLayoutEffect = typeof window !== "undefined" ? useLayoutEffect : useEffect;

  useIsomorphicLayoutEffect(() => {
    if (isOpen) {
      updatePosition();
    }
  }, [isOpen, updatePosition]);

  useEffect(() => {
    if (!isOpen) return;

    const handleClickOutside = (e: MouseEvent | TouchEvent) => {
      const target = e.target as Node;
      if (buttonRef.current?.contains(target)) return;
      if (popoverRef.current?.contains(target)) return;
      setIsOpen(false);
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setIsOpen(false);
      }
    };

    const handleScrollOrResize = () => {
      updatePosition();
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("touchstart", handleClickOutside, { passive: true });
    document.addEventListener("keydown", handleKeyDown);
    window.addEventListener("scroll", handleScrollOrResize, true);
    window.addEventListener("resize", handleScrollOrResize);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("touchstart", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("scroll", handleScrollOrResize, true);
      window.removeEventListener("resize", handleScrollOrResize);
    };
  }, [isOpen, updatePosition]);

  const toggleOpen = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!isOpen) {
      const initial = calculatePosition();
      if (initial) {
        setCoords(initial);
      }
      setIsOpen(true);
    } else {
      setIsOpen(false);
    }
  };

  const isMetro = mode === "metro";

  return (
    <div className={`inline-flex items-center ${className}`}>
      <button
        ref={buttonRef}
        type="button"
        onClick={toggleOpen}
        aria-label="ভাড়ার সরকারি হিসাব ও উৎস দেখুন"
        aria-expanded={isOpen}
        aria-haspopup="dialog"
        title="সরকারি ভাড়ার প্রজ্ঞাপন ও হিসাব"
        className={`w-5 h-5 rounded-full flex items-center justify-center transition-all duration-200 focus:outline-none ${
          isOpen
            ? "text-accent bg-blue-50 scale-105 ring-2 ring-accent/20"
            : "text-slate-400 hover:text-accent hover:bg-slate-100/90 hover:scale-110 active:scale-95"
        }`}
      >
        <InfoIcon size={14} className="transition-colors duration-200" />
      </button>

      {/* Render popover via React Portal directly into document.body to bypass all parent overflow/stacking contexts */}
      {mounted &&
        isOpen &&
        createPortal(
          <div
            ref={popoverRef}
            style={
              {
                position: "fixed",
                top: `${coords.top}px`,
                left: `${coords.left}px`,
                width: "min(18rem, calc(100vw - 24px))",
                "--popover-translate": coords.placeAbove ? "4px" : "-4px",
              } as React.CSSProperties
            }
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-label="ভাড়ার সরকারি তথ্য ও প্রজ্ঞাপন"
            className={`z-[9999] bg-white/95 backdrop-blur-xl rounded-2xl border border-slate-200/90 shadow-2xl shadow-slate-900/20 p-3.5 text-left animate-popover ${
              coords.placeAbove ? "origin-bottom" : "origin-top"
            }`}
          >
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-100">
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-bold uppercase tracking-wider font-display text-slate-500">
                  {isMetro ? "মেট্রোরেল ভাড়া প্রজ্ঞাপন" : "বিআরটিএ সরকারি ভাড়ার চার্ট"}
                </span>
                <span
                  className={`text-[9px] font-bold px-1.5 py-0.5 rounded transition-colors ${
                    isMetro ? "bg-emerald-50 text-emerald-700" : "bg-blue-50 text-blue-700"
                  }`}
                >
                  {isMetro ? "DMTCL" : "BRTA Official"}
                </span>
              </div>
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  setIsOpen(false);
                }}
                className="w-5 h-5 -mr-1 rounded-full flex items-center justify-center text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors text-xs font-bold leading-none"
                aria-label="বন্ধ করুন"
                title="বন্ধ করুন"
              >
                ✕
              </button>
            </div>

            <div className="space-y-1.5 text-xs text-slate-600 font-bengali">
              {isMetro ? (
                <>
                  <p className="flex justify-between">
                    <span className="text-slate-400">উৎস:</span>
                    <span className="font-semibold text-slate-700">ডিএমটিসিএল (এমআরটি লাইন-৬)</span>
                  </p>
                  <p className="flex justify-between">
                    <span className="text-slate-400">ভাড়ার কাঠামো:</span>
                    <span className="font-semibold text-slate-700">স্টেশন দূরত্ব অনুযায়ী নির্ধারিত</span>
                  </p>
                  <p className="flex justify-between">
                    <span className="text-slate-400">সর্বনিম্ন ভাড়া:</span>
                    <span className="font-semibold text-slate-700">৳২০.০০ (সর্বোচ্চ ৳১০০)</span>
                  </p>

                  <a
                    href="https://dmtcl.gov.bd/pages/static-pages/6922df5f933eb65569e218ed"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] font-semibold text-emerald-600 hover:text-emerald-700 transition-colors group/link"
                  >
                    <span>অফিসিয়াল সময়সূচি ও চার্ট</span>
                    <span className="text-[10px] group-hover/link:translate-x-0.5 transition-transform">↗</span>
                  </a>
                </>
              ) : (
                <>
                  <p className="flex justify-between">
                    <span className="text-slate-400">গেজেট তারিখ:</span>
                    <span className="font-semibold text-slate-700">২২ সেপ্টেম্বর ২০২৬</span>
                  </p>
                  <p className="flex justify-between">
                    <span className="text-slate-400">ভাড়ার হার:</span>
                    <span className="font-semibold text-slate-700">২.৭০ টাকা / কি.মি. (ডিজেল)</span>
                  </p>
                  <p className="flex justify-between">
                    <span className="text-slate-400">সর্বনিম্ন ভাড়া:</span>
                    <span className="font-semibold text-slate-700">১০.০০ টাকা</span>
                  </p>

                  {distanceKm !== undefined && (
                    <div className="mt-2 pt-2 border-t border-slate-100 bg-slate-50/80 -mx-1 px-2.5 py-1.5 rounded-lg text-[11px] text-slate-500">
                      <p className="font-medium text-slate-700">
                        হিসাব: {distanceKm} কি.মি. × ২.৭০ = ৳{Math.round(distanceKm * 2.7)}
                      </p>
                      {fare !== undefined && fare === 10 && distanceKm * 2.7 < 10 && (
                        <p className="text-[10px] text-accent mt-0.5">* সরকারি সর্বনিম্ন ভাড়া ১০ টাকা প্রযোজ্য</p>
                      )}
                    </div>
                  )}

                  {minFare !== undefined && maxFare !== undefined && minFare !== maxFare && (
                    <div className="mt-2 pt-2 border-t border-slate-100 bg-slate-50/80 -mx-1 px-2.5 py-1.5 rounded-lg text-[11px] text-slate-500">
                      <p className="font-medium text-slate-700">
                        বিভিন্ন রুটের দূরত্ব অনুযায়ী ভাড়া ৳{minFare} থেকে ৳{maxFare}
                      </p>
                    </div>
                  )}

                  {/* Direct PDF Link */}
                  <a
                    href="https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-brta/2026/8/105993ce-3474-4649-bb30-be8f13767227.pdf"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] font-semibold text-accent hover:text-blue-700 transition-colors group/link"
                  >
                    <span>অফিসিয়াল বিআরটিএ চার্ট (PDF)</span>
                    <span className="text-[10px] group-hover/link:translate-x-0.5 transition-transform">↗</span>
                  </a>
                </>
              )}
            </div>
          </div>,
          document.body
        )}
    </div>
  );
};
