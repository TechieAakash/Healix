import React from "react";

export function SkeletonLoader({ type = "card", count = 1, className = "" }) {
  const items = Array.from({ length: count }, (_, i) => i);

  if (type === "card") {
    return (
      <div className={`space-y-4 ${className}`}>
        {items.map((i) => (
          <div
            key={i}
            className="p-6 bg-white rounded-2xl border border-slate-200/80 animate-pulse space-y-3"
          >
            <div className="flex items-center justify-between">
              <div className="h-4 bg-slate-200 rounded-md w-1/3"></div>
              <div className="h-4 bg-slate-200 rounded-full w-20"></div>
            </div>
            <div className="h-3 bg-slate-100 rounded-md w-3/4"></div>
            <div className="h-3 bg-slate-100 rounded-md w-1/2"></div>
            <div className="pt-2 flex gap-2">
              <div className="h-6 bg-slate-100 rounded-full w-16"></div>
              <div className="h-6 bg-slate-100 rounded-full w-20"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (type === "chart") {
    return (
      <div className={`p-6 bg-white rounded-2xl border border-slate-200/80 animate-pulse space-y-4 ${className}`}>
        <div className="h-4 bg-slate-200 rounded-md w-1/4"></div>
        <div className="h-48 bg-slate-100 rounded-xl w-full"></div>
      </div>
    );
  }

  return (
    <div className={`space-y-2 animate-pulse ${className}`}>
      {items.map((i) => (
        <div key={i} className="h-4 bg-slate-200 rounded-md w-full"></div>
      ))}
    </div>
  );
}
