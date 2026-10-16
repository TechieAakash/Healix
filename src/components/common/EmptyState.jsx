import React from "react";
import { FolderSearch, PlusCircle, AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "./Button";

export function EmptyState({
  title = "No assessments found",
  description = "You haven't conducted any symptom checks yet. Describe your symptoms to get started.",
  actionLabel = "Start Assessment",
  onAction,
  icon: Icon = FolderSearch,
  className = "",
}) {
  return (
    <div
      className={`flex flex-col items-center justify-center p-12 text-center bg-white rounded-2xl border border-dashed border-slate-300 ${className}`}
    >
      <div className="w-14 h-14 rounded-2xl bg-teal-50 text-teal-700 flex items-center justify-center mb-4">
        <Icon className="w-7 h-7" />
      </div>
      <h3 className="text-base font-semibold text-slate-900">{title}</h3>
      <p className="text-sm text-slate-500 mt-1.5 max-w-sm leading-relaxed">
        {description}
      </p>
      {onAction && (
        <div className="mt-5">
          <Button variant="teal" onClick={onAction} icon={PlusCircle}>
            {actionLabel}
          </Button>
        </div>
      )}
    </div>
  );
}

export function ErrorState({
  title = "Something went wrong",
  message = "We were unable to load this health data. Please try again.",
  onRetry,
  className = "",
}) {
  return (
    <div
      className={`flex flex-col items-center justify-center p-8 text-center bg-rose-50/50 rounded-2xl border border-rose-200 ${className}`}
    >
      <div className="w-12 h-12 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center mb-3">
        <AlertCircle className="w-6 h-6" />
      </div>
      <h3 className="text-sm font-semibold text-rose-900">{title}</h3>
      <p className="text-xs text-rose-700 mt-1 max-w-sm leading-relaxed">
        {message}
      </p>
      {onRetry && (
        <div className="mt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={onRetry}
            icon={RefreshCw}
            className="border-rose-200 text-rose-800 hover:bg-rose-50"
          >
            Retry
          </Button>
        </div>
      )}
    </div>
  );
}
