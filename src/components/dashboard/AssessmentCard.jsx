import React from "react";
import { Link } from "react-router-dom";
import { Card } from "../common/Card";
import { StatusBadge } from "../common/StatusBadge";
import { UrgencyIndicator } from "../common/UrgencyIndicator";
import { Button } from "../common/Button";
import { Calendar, Stethoscope, ChevronRight, FileText } from "lucide-react";

export function AssessmentCard({ assessment, compact = false }) {
  if (!assessment) return null;

  return (
    <Card
      hover
      padding={compact ? "sm" : "default"}
      className="transition-all"
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-emerald-50 text-emerald-700">
            <Stethoscope className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-slate-900 leading-tight">
              {assessment.primarySymptom || assessment.symptoms?.join(", ")}
            </h4>
            <div className="flex items-center gap-2 mt-0.5 text-xs text-slate-500">
              <span className="flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                {assessment.date}
              </span>
              <span>•</span>
              <span>Duration: {assessment.duration || "Recent"}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <StatusBadge status={assessment.status} />
          <UrgencyIndicator
            level={assessment.urgencyLevel}
            title={
              assessment.urgencyLevel === "emergency"
                ? "Emergency"
                : assessment.urgencyLevel === "urgent"
                ? "Urgent"
                : "Routine"
            }
            compact
          />
        </div>
      </div>

      {/* Symptom Tags */}
      <div className="pt-3">
        <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
          Reported Symptoms:
        </p>
        <div className="flex flex-wrap gap-1.5">
          {assessment.symptoms?.map((sym, idx) => (
            <span
              key={idx}
              className="text-xs px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 font-medium"
            >
              {typeof sym === "string" ? sym : sym.label}
            </span>
          ))}
        </div>
      </div>

      {/* Bottom CTA */}
      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
        <span className="text-xs text-slate-500 font-medium">
          {assessment.possibleExplanations?.length || 0} explanations explored
        </span>
        <div className="flex items-center gap-2">
          <Link to={`/report/${assessment.id}`}>
            <Button variant="ghost" size="sm" icon={FileText}>
              Print Report
            </Button>
          </Link>
          <Link to={`/assessment/${assessment.id}`}>
            <Button variant="outline" size="sm" icon={ChevronRight} iconPosition="right">
              View Summary
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
}
