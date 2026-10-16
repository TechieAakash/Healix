import React from "react";

export function Card({
  children,
  className = "",
  padding = "default", // none | sm | default | lg
  hover = false,
  bordered = true,
  onClick,
  ...props
}) {
  const paddingStyles = {
    none: "",
    sm: "p-4",
    default: "p-6",
    lg: "p-8",
  };

  const hoverStyles = hover
    ? "transition-all duration-200 hover:shadow-md hover:border-slate-300 hover:-translate-y-0.5"
    : "";

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-2xl ${
        bordered ? "border border-slate-200/80" : ""
      } shadow-[0_1px_3px_rgba(15,23,42,0.04)] ${paddingStyles[padding]} ${hoverStyles} ${className} ${
        onClick ? "cursor-pointer" : ""
      }`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, action, className = "" }) {
  return (
    <div className={`flex items-start justify-between gap-4 mb-4 ${className}`}>
      <div>
        <h3 className="text-base font-semibold text-slate-900 tracking-tight">{title}</h3>
        {subtitle && <p className="text-sm text-slate-500 mt-0.5">{subtitle}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}
