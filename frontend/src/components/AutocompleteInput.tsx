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

export const AutocompleteInput: React.FC<AutocompleteInputProps> = ({
  value,
  onChange,
  options,
  placeholder,
  icon,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filteredOptions, setFilteredOptions] = useState<Stop[]>([]);
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (value.trim()) {
      const q = value.toLowerCase();
      const filtered = options
        .filter((o) => o.name_en.toLowerCase().includes(q) || o.name_bn.includes(q))
        .slice(0, 5);
      setFilteredOptions(filtered);
      setSelectedIndex(-1);
    } else {
      setFilteredOptions([]);
      setSelectedIndex(-1);
    }
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
      if (selectedIndex >= 0 && selectedIndex < filteredOptions.length) {
        e.preventDefault();
        onChange(filteredOptions[selectedIndex].name_en);
        setIsOpen(false);
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  };

  /**
   * Utility to highlight matching query text inside stop names
   */
  const renderHighlightedText = (text: string, query: string) => {
    if (!query.trim()) return text;
    const parts = text.split(new RegExp(`(${query})`, "gi"));
    return (
      <span>
        {parts.map((part, i) =>
          part.toLowerCase() === query.toLowerCase() ? (
            <span key={i} className="text-accent font-extrabold underline decoration-accent/30 decoration-2">
              {part}
            </span>
          ) : (
            part
          )
        )}
      </span>
    );
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
        <div className="absolute z-50 w-full mt-2 bg-white/95 backdrop-blur-xl border border-white rounded-2xl shadow-[0_10px_40px_-10px_rgba(0,0,0,0.1)] overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
          {filteredOptions.map((opt, idx) => (
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
              <span className="font-bengali font-semibold">
                {renderHighlightedText(opt.name_bn, value)}
              </span>
              <span className="font-display text-xs text-foreground/40">
                {renderHighlightedText(opt.name_en, value)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
