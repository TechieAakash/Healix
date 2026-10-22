import React from "react";
import { Card } from "../common/Card";
import { ArrowUpRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

export function HealthMetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  badgeText,
  className = "",
  onClick,
  to,
}) {
  const navigate = useNavigate();

  const handleClick = (e) => {
    if (onClick) {
      onClick(e);
    } else if (to) {
      navigate(to);
    }
  };

  const isClickable = !!(onClick || to);

  return (
    <Card
      padding="default"
      hover={isClickable}
      onClick={isClickable ? handleClick : undefined}
      className={`group transition-all select-none ${
        isClickable
          ? "cursor-pointer hover:border-teal-500 hover:shadow-md hover:-translate-y-0.5"
          : ""
      } ${className}`}
      role={isClickable ? "button" : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onKeyDown={(e) => {
        if (isClickable && (e.key === "Enter" || e.key === " ")) {
          e.preventDefault();
          handleClick(e);
        }
      }}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider group-hover:text-teal-700 transition-colors">
            {title}
          </p>
          <h3 className="text-2xl font-bold text-slate-900 mt-1">{value}</h3>
          {subtitle && (
            <p className="text-xs text-slate-500 mt-1 line-clamp-1">{subtitle}</p>
          )}
        </div>
        {Icon && (
          <div className="p-3 bg-teal-50 text-teal-700 rounded-2xl border border-teal-100/80 group-hover:bg-teal-700 group-hover:text-white transition-all shadow-2xs">
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      {badgeText && (
        <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
          <span className="text-slate-500 font-medium group-hover:text-teal-700 transition-colors">
            {badgeText}
          </span>
          <div className="w-6 h-6 rounded-full flex items-center justify-center bg-slate-50 group-hover:bg-teal-50 text-slate-500 group-hover:text-teal-700 transition-all">
            <ArrowUpRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </div>
        </div>
      )}
    </Card>
  );
}
