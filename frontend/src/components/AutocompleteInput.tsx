"use client";

import React, { useState, useEffect, useRef } from "react";
import { XIcon } from "@animateicons/react/lucide";
import { Stop } from "@/types/transit";

interface AutocompleteInputProps {
  value: string;
  onChange: (val: string) => void;
  options: Stop[];
  placeholder: string;
  icon: React.ReactNode;
}

const BN_TO_EN_DIGITS: Record<string, string> = {
  "০": "0", "১": "1", "২": "2", "৩": "3", "৪": "4",
  "৫": "5", "৬": "6", "৭": "7", "৮": "8", "৯": "9",
};

/**
 * Normalizes text for transit search:
 * - Maps Bengali digits to English
 * - Converts hyphens, underscores, slashes, brackets to spaces
 * - Collapses extra whitespace and lowercases
 */
function normalizeText(text: string): string {
  if (!text) return "";
  let s = text.toLowerCase();
  s = s.replace(/[০-৯]/g, (d) => BN_TO_EN_DIGITS[d] || d);
  s = s.replace(/[-_./(),&+\\]/g, " ");
  return s.replace(/\s+/g, " ").trim();
}

/**
 * Calculate relevance score between target string and search query.
 */
function getMatchScore(target: string, query: string): number {
  if (!target || !query) return 0;
  if (target === query) return 1000;
  if (target.startsWith(query)) return 500;
  const words = target.split(" ");
  if (words.some((w) => w.startsWith(query))) return 300;
  if (target.includes(query)) return 100;

  // Space-collapsed check (e.g. "mirpur10" vs "mirpur 10")
  const compactTarget = target.replace(/\s+/g, "");
  const compactQuery = query.replace(/\s+/g, "");
  if (compactTarget === compactQuery) return 900;
  if (compactTarget.startsWith(compactQuery)) return 400;
  if (compactTarget.includes(compactQuery)) return 80;

  return 0;
}

interface ScoredStop {
  stop: Stop;
  score: number;
  matchedAlias?: string;
}

export const AutocompleteInput: React.FC<AutocompleteInputProps> = ({
  value,
  onChange,
  options,
  placeholder,
  icon,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filteredOptions, setFilteredOptions] = useState<ScoredStop[]>([]);
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const rawQ = value.trim();
    if (!rawQ) {
      setFilteredOptions([]);
      setSelectedIndex(-1);
      return;
    }

    const normQ = normalizeText(rawQ);
    const scored: ScoredStop[] = [];

    for (const opt of options) {
      const normEn = normalizeText(opt.name_en);
      const normBn = normalizeText(opt.name_bn);

      const scoreEn = getMatchScore(normEn, normQ);
      const scoreBn = getMatchScore(normBn, normQ);

      let bestScore = Math.max(scoreEn, scoreBn);
      let matchedAlias: string | undefined = undefined;

      if (opt.aliases && opt.aliases.length > 0) {
        for (const alias of opt.aliases) {
          const normAlias = normalizeText(alias);
          const aliasScore = getMatchScore(normAlias, normQ);
          if (aliasScore > 0) {
            const adjustedScore = aliasScore - 50; // slight preference to primary names
            if (adjustedScore > bestScore) {
              bestScore = adjustedScore;
              matchedAlias = alias;
            }
          }
        }
      }

      if (bestScore > 0) {
        scored.push({
          stop: opt,
          score: bestScore,
          matchedAlias,
        });
      }
    }

    // Sort by highest relevance score first, then shorter English name
    scored.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.stop.name_en.length - b.stop.name_en.length;
    });

    setFilteredOptions(scored.slice(0, 10));
    setSelectedIndex(-1);
  }, [value, options]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isOpen || filteredOptions.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev < filteredOptions.length - 1 ? prev + 1 : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : filteredOptions.length - 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const target = selectedIndex >= 0 && selectedIndex < filteredOptions.length
        ? filteredOptions[selectedIndex].stop
        : filteredOptions[0].stop;
      onChange(target.name_en);
      setIsOpen(false);
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  };

  /**
   * Utility to highlight matching query text safely inside stop names
   */
  const renderHighlightedText = (text: string, query: string) => {
    if (!query.trim()) return text;
    try {
      const cleanQ = query.trim().replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const pattern = cleanQ.split(/\s+/).join("[-\\s]+");
      const regex = new RegExp(`(${pattern})`, "gi");
      const parts = text.split(regex);
      return (
        <span>
          {parts.map((part, i) =>
            regex.test(part) ? (
              <span key={i} className="text-accent font-extrabold underline decoration-accent/30 decoration-2">
                {part}
              </span>
            ) : (
              part
            )
          )}
        </span>
      );
    } catch {
      return text;
    }
  };

  return (
    <div className="relative" ref={wrapperRef}>
      <div className="search-input-wrapper group relative">
        <div className="pl-5 text-accent transition-transform group-focus-within:scale-110">
          {icon}
        </div>
        <input
          type="text"
          placeholder={placeholder}
          className="search-input pr-10"
          value={value}
          onChange={(e) => {
            onChange(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          onKeyDown={handleKeyDown}
        />
        {value && (
          <button
            type="button"
            onClick={() => {
              onChange("");
              setIsOpen(false);
            }}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-1 rounded-full transition-colors"
            title="Clear text"
          >
            <XIcon size={16} />
          </button>
        )}
      </div>

      {isOpen && filteredOptions.length > 0 && (
        <div className="absolute z-50 w-full mt-2 bg-white/95 backdrop-blur-xl border border-white rounded-2xl shadow-[0_10px_40px_-10px_rgba(0,0,0,0.1)] overflow-hidden max-h-80 overflow-y-auto animate-in fade-in slide-in-from-top-2 duration-200">
          {filteredOptions.map(({ stop: opt, matchedAlias }, idx) => (
            <div
              key={opt.id}
              className={`px-5 py-3 cursor-pointer transition-colors border-b border-border/50 last:border-0 flex justify-between items-center ${
                idx === selectedIndex ? "bg-accent/15 text-accent font-bold" : "hover:bg-accent/5 text-foreground/90"
              }`}
              onMouseEnter={() => setSelectedIndex(idx)}
              onClick={() => {
                onChange(opt.name_en);
                setIsOpen(false);
              }}
            >
              <div className="flex flex-col text-left">
                <span className="font-bengali font-semibold text-sm leading-snug">
                  {renderHighlightedText(opt.name_bn, value)}
                </span>
                {matchedAlias && (
                  <span className="text-[11px] text-accent/80 font-normal">
                    {renderHighlightedText(matchedAlias, value)}
                  </span>
                )}
              </div>
              <span className="font-display text-xs text-foreground/50 ml-3 shrink-0">
                {renderHighlightedText(opt.name_en, value)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
