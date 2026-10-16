import React from "react";

export function Badge({
  children,
  variant = "slate", // slate | teal | green | amber | red | blue
  size = "md", // sm | md
  dot = false,
  className = "",
}) {
  const variantStyles = {
    slate: "bg-slate-100 text-slate-700 border-slate-200/60",
    teal: "bg-teal-50 text-teal-700 border-teal-200/70",
    green: "bg-emerald-50 text-emerald-700 border-emerald-200/70",
    amber: "bg-amber-50 text-amber-800 border-amber-200/70",
    red: "bg-rose-50 text-rose-700 border-rose-200/70",
    blue: "bg-blue-50 text-blue-700 border-blue-200/70",
  };

  const dotStyles = {
    slate: "bg-slate-400",
    teal: "bg-teal-500",
    green: "bg-emerald-500",
    amber: "bg-amber-500",
    red: "bg-rose-500 animate-pulse",
    blue: "bg-blue-500",
  };

  const sizeStyles = {
    sm: "text-xs px-2 py-0.5 font-medium",
    md: "text-xs px-2.5 py-1 font-medium",
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
    >
      {dot && <span className={`w-1.5 h-1.5 rounded-full ${dotStyles[variant]}`} />}
      {children}
    </span>
  );
}
