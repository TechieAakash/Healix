import React from "react";

export function ReportSection({
  title,
  icon: Icon,
  badge,
  children,
  className = "",
}) {
  return (
    <div
      className={`bg-white rounded-2xl border border-slate-200 p-6 shadow-xs ${className}`}
    >
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
        <div className="flex items-center gap-2.5">
          {Icon && (
            <div className="p-1.5 rounded-lg bg-teal-50 text-teal-700">
              <Icon className="w-4 h-4" />
            </div>
          )}
          <h3 className="text-base font-bold text-slate-900 tracking-tight">
            {title}
          </h3>
        </div>
        {badge && <div>{badge}</div>}
      </div>
      <div>{children}</div>
    </div>
  );
}
