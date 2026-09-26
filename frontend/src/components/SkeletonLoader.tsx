import React from "react";

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
