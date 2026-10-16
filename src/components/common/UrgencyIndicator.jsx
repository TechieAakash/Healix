import React from "react";
import { CheckCircle2, AlertTriangle, AlertOctagon, Info } from "lucide-react";

export function UrgencyIndicator({
  level = "routine", // 'routine' | 'urgent' | 'emergency'
  title,
  description,
  showIcon = true,
  compact = false,
  className = "",
}) {
  const configs = {
    routine: {
      badgeClass: "bg-emerald-50 text-emerald-800 border-emerald-200",
      iconClass: "text-emerald-600",
      defaultTitle: "Routine Care / Self-Monitoring",
      defaultDesc: "Symptoms appear typical for home observation and routine follow-up with your primary doctor if they do not improve.",
      icon: CheckCircle2,
      borderClass: "border-l-emerald-500",
      bgSubtle: "bg-emerald-50/50",
    },
    urgent: {
      badgeClass: "bg-amber-50 text-amber-900 border-amber-200",
      iconClass: "text-amber-600",
      defaultTitle: "Prompt Medical Attention Recommended",
      defaultDesc: "We recommend scheduling an appointment with your healthcare provider or visiting an urgent care clinic within 12–24 hours.",
      icon: AlertTriangle,
      borderClass: "border-l-amber-500",
      bgSubtle: "bg-amber-50/50",
    },
    emergency: {
      badgeClass: "bg-rose-50 text-rose-900 border-rose-300",
      iconClass: "text-rose-600",
      defaultTitle: "Immediate Emergency Evaluation Required",
      defaultDesc: "Potential warning signs detected. Please call emergency services (e.g. 911 / 112) or go to the nearest emergency department right away.",
      icon: AlertOctagon,
      borderClass: "border-l-rose-600",
      bgSubtle: "bg-rose-50/70",
    },
  };

  const config = configs[level] || configs.routine;
  const Icon = config.icon;
  const displayTitle = title || config.defaultTitle;
  const displayDesc = description || config.defaultDesc;

  if (compact) {
    return (
      <span
        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${config.badgeClass} ${className}`}
      >
        <Icon className={`w-3.5 h-3.5 ${config.iconClass}`} />
        <span>{displayTitle}</span>
      </span>
    );
  }

  return (
    <div
      className={`rounded-2xl p-5 border border-slate-200/80 border-l-4 ${config.borderClass} ${config.bgSubtle} ${className}`}
    >
      <div className="flex items-start gap-3.5">
        {showIcon && (
          <div className="mt-0.5 shrink-0 p-2 rounded-xl bg-white shadow-sm border border-slate-200/60">
            <Icon className={`w-5 h-5 ${config.iconClass}`} />
          </div>
        )}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-500">
              Urgency Assessment
            </span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full font-medium border ${config.badgeClass}`}
            >
              {level.toUpperCase()}
            </span>
          </div>
          <h4 className="text-base font-semibold text-slate-900">{displayTitle}</h4>
          <p className="text-sm text-slate-600 mt-1 leading-relaxed">{displayDesc}</p>
        </div>
      </div>
    </div>
  );
}
