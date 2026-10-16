import React from "react";
import { Card } from "../common/Card";
import { Sparkles, ShieldCheck, ArrowRight, Lightbulb } from "lucide-react";
import { Link } from "react-router-dom";

export function HealthInsightsCard() {
  return (
    <Card className="bg-gradient-to-br from-teal-900 via-slate-900 to-slate-950 text-white border-0 shadow-lg relative overflow-hidden">
      {/* Background soft glow */}
      <div className="absolute -top-16 -right-16 w-48 h-48 rounded-full bg-teal-500/10 blur-3xl pointer-events-none" />

      <div className="flex items-center gap-2 mb-3">
        <span className="p-1.5 rounded-lg bg-teal-500/20 text-teal-300">
          <Sparkles className="w-4 h-4" />
        </span>
        <span className="text-xs uppercase tracking-wider font-semibold text-teal-300">
          Synthesized Pattern Insight
        </span>
      </div>

      <h3 className="text-lg font-bold text-white tracking-tight">
        Recurring pattern noted: Mild fatigue with evening onset
      </h3>

      <p className="text-xs text-slate-300 mt-2 leading-relaxed">
        Your last 2 assessments noted reports of fatigue accompanying head pressure after extended screen use. While not a diagnosis, chronic fatigue may relate to sleep hygiene, hydration, or postural neck strain.
      </p>

      {/* Safety notice boundary */}
      <div className="mt-4 p-3 rounded-xl bg-white/5 border border-white/10 flex items-start gap-2.5 text-[11px] text-slate-300">
        <ShieldCheck className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
        <p>
          <strong>Informational insight only:</strong> This observation is not a medical diagnosis. Mention this recurring pattern to your physician at your next annual check-up.
        </p>
      </div>

      <div className="mt-5 pt-3 border-t border-white/10 flex items-center justify-between">
        <Link
          to="/assistant"
          className="text-xs text-teal-300 hover:text-teal-200 font-semibold flex items-center gap-1.5 transition-colors"
        >
          Discuss with AI Assistant <ArrowRight className="w-3.5 h-3.5" />
        </Link>
        <span className="text-[11px] text-slate-400">Based on recent 4 weeks</span>
      </div>
    </Card>
  );
}
