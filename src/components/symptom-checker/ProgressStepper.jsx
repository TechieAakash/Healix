import React from "react";
import { Check } from "lucide-react";

export function ProgressStepper({ steps = [], currentStep = 1 }) {
  return (
    <div className="w-full max-w-3xl mx-auto mb-8 sm:mb-12">
      <div className="relative flex items-center justify-between">
        {/* Progress connecting line */}
        <div className="absolute top-1/2 left-0 right-0 -translate-y-1/2 h-0.5 bg-slate-200 -z-0" />
        <div
          className="absolute top-1/2 left-0 -translate-y-1/2 h-0.5 bg-teal-700 transition-all duration-300 -z-0"
          style={{
            width: `${((Math.min(currentStep, steps.length) - 1) / (steps.length - 1)) * 100}%`,
          }}
        />

        {steps.map((step, idx) => {
          const stepNumber = idx + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;

          return (
            <div key={step.label} className="relative z-10 flex flex-col items-center">
              <div
                className={`w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center font-semibold text-xs sm:text-sm transition-all shadow-xs ${
                  isCompleted
                    ? "bg-teal-700 text-white"
                    : isCurrent
                    ? "bg-slate-900 text-white ring-4 ring-teal-100"
                    : "bg-white text-slate-500 border border-slate-300"
                }`}
              >
                {isCompleted ? <Check className="w-4 h-4 stroke-[3]" /> : stepNumber}
              </div>
              <span
                className={`absolute -bottom-6 text-[11px] sm:text-xs font-medium whitespace-nowrap transition-colors ${
                  isCurrent
                    ? "text-slate-900 font-bold"
                    : isCompleted
                    ? "text-teal-800"
                    : "text-slate-500"
                }`}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
