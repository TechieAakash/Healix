import React from "react";

export function HealixLogo({ size = 32, showText = true, textClassName = "text-xl font-bold text-emerald-950 tracking-tight" }) {
  return (
    <div className="flex items-center gap-2.5 select-none">
      <svg
        width={size}
        height={size}
        viewBox="0 0 36 36"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="shrink-0"
      >
        {/* 4 Petals arranged in a clover/cross layout as seen in the Healix UI */}
        <circle cx="13" cy="13" r="5.5" fill="#047857" />
        <circle cx="23" cy="13" r="5.5" fill="#059669" />
        <circle cx="13" cy="23" r="5.5" fill="#10b981" />
        <circle cx="23" cy="23" r="5.5" fill="#047857" />
        <circle cx="18" cy="18" r="3" fill="#065f46" />
      </svg>
      {showText && <span className={textClassName}>Healix</span>}
    </div>
  );
}
