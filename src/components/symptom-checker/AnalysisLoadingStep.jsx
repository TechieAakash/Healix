import React, { useState, useEffect } from "react";
import { Check, Loader2, ShieldCheck, Cpu } from "lucide-react";
import { motion } from "framer-motion";

export function AnalysisLoadingStep({ onComplete }) {
  const [currentStage, setCurrentStage] = useState(0);

  const stages = [
    {
      title: "Understanding your symptoms",
      desc: "Structuring reported sensations, timeline, and anatomical areas",
    },
    {
      title: "Reviewing relevant clinical literature",
      desc: "Querying evidence-grounded medical indexes (Mayo Clinic, WHO, NHS)",
    },
    {
      title: "Synthesizing triage & next-step guidance",
      desc: "Evaluating urgency thresholds and preparing your personalized health summary",
    },
  ];

  useEffect(() => {
    const timer1 = setTimeout(() => setCurrentStage(1), 800);
    const timer2 = setTimeout(() => setCurrentStage(2), 1600);
    const timer3 = setTimeout(() => {
      if (onComplete) onComplete();
    }, 2400);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
    };
  }, [onComplete]);

  return (
    <div className="max-w-xl mx-auto py-12 px-4 text-center">
      {/* Subtle pulsing indicator */}
      <div className="relative w-20 h-20 mx-auto mb-6 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full bg-teal-100/60 animate-ping" />
        <div className="w-16 h-16 rounded-2xl bg-teal-700 text-white flex items-center justify-center shadow-lg shadow-teal-600/30 relative z-10">
          <Cpu className="w-8 h-8 animate-pulse" />
        </div>
      </div>

      <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
        Analyzing your information...
      </h2>
      <p className="text-sm text-slate-500 mt-2 max-w-md mx-auto">
        Evaluating symptom patterns against verified clinical knowledge bases to provide clear, actionable guidance.
      </p>

      {/* Structured animated stages */}
      <div className="mt-10 bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs text-left space-y-5">
        {stages.map((stage, idx) => {
          const isDone = idx < currentStage;
          const isCurrent = idx === currentStage;
          const isPending = idx > currentStage;

          return (
            <motion.div
              key={stage.title}
              initial={{ opacity: 0.7 }}
              animate={{ opacity: isPending ? 0.4 : 1 }}
              className="flex items-start gap-3.5"
            >
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5 text-xs transition-colors ${
                  isDone
                    ? "bg-teal-700 text-white"
                    : isCurrent
                    ? "bg-teal-100 text-teal-800 border border-teal-300"
                    : "bg-slate-100 text-slate-500 border border-slate-200"
                }`}
              >
                {isDone ? (
                  <Check className="w-3.5 h-3.5 stroke-[3]" />
                ) : isCurrent ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-teal-700" />
                ) : (
                  <span className="w-2 h-2 rounded-full bg-slate-300" />
                )}
              </div>

              <div>
                <h4
                  className={`text-sm font-semibold transition-colors ${
                    isCurrent
                      ? "text-slate-900"
                      : isDone
                      ? "text-teal-900"
                      : "text-slate-500"
                  }`}
                >
                  {stage.title}
                </h4>
                <p className="text-xs text-slate-500 mt-0.5">{stage.desc}</p>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="mt-8 flex items-center justify-center gap-2 text-xs text-slate-500">
        <ShieldCheck className="w-4 h-4 text-teal-700" />
        <span>Evidence-grounded retrieval • No definitive disease diagnosis claimed</span>
      </div>
    </div>
  );
}
