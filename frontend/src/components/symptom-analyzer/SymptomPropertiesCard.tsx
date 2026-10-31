import React from 'react';
import { Clock, Gauge, Zap } from 'lucide-react';

interface SymptomPropertiesCardProps {
  duration: string;
  severity: string;
  character: string;
  onChangeDuration: (v: string) => void;
  onChangeSeverity: (v: string) => void;
  onChangeCharacter: (v: string) => void;
}

const DURATION_CHOICES = [
  "< 24 Hours",
  "1-3 Days",
  "4-7 Days",
  "1-3 Weeks",
  "> 1 Month"
];

const SEVERITY_CHOICES = [
  { id: "Mild", label: "Mild", sub: "Noticeable but does not disrupt routine", color: "text-mint border-mint/40 bg-mint/10" },
  { id: "Moderate", label: "Moderate", sub: "Disrupts regular tasks, uncomfortable", color: "text-amber border-amber/40 bg-amber/10" },
  { id: "Severe", label: "Severe", sub: "Incapacitating or unbearable intensity", color: "text-alert border-alert/40 bg-alert/10" }
];

const CHARACTER_CHOICES = [
  "Pulsating / Throbbing",
  "Pressing / Tight Band",
  "Sharp / Stabbing",
  "Dull / Aching",
  "Burning / Reflux",
  "Explosive / Thunderclap",
  "Constant Pressure",
  "Cramping / Spasmodic"
];

export const SymptomPropertiesCard: React.FC<SymptomPropertiesCardProps> = ({
  duration,
  severity,
  character,
  onChangeDuration,
  onChangeSeverity,
  onChangeCharacter
}) => {
  return (
    <div className="p-4 sm:p-5 rounded-2xl glass-panel space-y-5">
      <div>
        <h3 className="text-sm font-semibold text-mist flex items-center gap-2">
          <Gauge className="w-4 h-4 text-signal" />
          Symptom Properties & Character
        </h3>
        <p className="text-xs text-mist-muted">
          Clinical parameters help calibrate rule certainty and risk thresholds.
        </p>
      </div>

      {/* Severity Selector */}
      <div className="space-y-2">
        <label className="text-xs font-semibold text-mist flex items-center gap-1.5">
          <Gauge className="w-3.5 h-3.5 text-signal" />
          Overall Intensity / Severity
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          {SEVERITY_CHOICES.map((choice) => {
            const isSelected = severity === choice.id;
            return (
              <button
                key={choice.id}
                type="button"
                onClick={() => onChangeSeverity(choice.id)}
                className={`p-3 rounded-xl border text-left transition-all ${
                  isSelected
                    ? `${choice.color} shadow-sm ring-1 ring-current`
                    : 'surface-card border-carbon-border hover:border-carbon-border-strong text-mist-muted hover:text-mist'
                }`}
              >
                <div className="text-xs font-bold">{choice.label}</div>
                <div className="text-[11px] opacity-80 mt-0.5 line-clamp-1">{choice.sub}</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Duration Selector */}
      <div className="space-y-2">
        <label className="text-xs font-semibold text-mist flex items-center gap-1.5">
          <Clock className="w-3.5 h-3.5 text-signal" />
          Duration (How long has this lasted?)
        </label>
        <div className="flex flex-wrap gap-2">
          {DURATION_CHOICES.map((d) => {
            const isSelected = duration === d;
            return (
              <button
                key={d}
                type="button"
                onClick={() => onChangeDuration(d)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  isSelected
                    ? 'bg-signal/20 text-signal border border-signal font-semibold shadow-sm'
                    : 'surface-card border border-carbon-border text-mist-muted hover:text-mist'
                }`}
              >
                {d}
              </button>
            );
          })}
        </div>
      </div>

      {/* Character / Sensation */}
      <div className="space-y-2">
        <label className="text-xs font-semibold text-mist flex items-center gap-1.5">
          <Zap className="w-3.5 h-3.5 text-signal" />
          Pain Quality / Sensation
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {CHARACTER_CHOICES.map((c) => {
            const isSelected = character === c;
            return (
              <button
                key={c}
                type="button"
                onClick={() => onChangeCharacter(c)}
                className={`p-2.5 rounded-xl border text-xs text-left transition-all ${
                  isSelected
                    ? 'bg-signal/15 border-signal text-signal font-semibold'
                    : 'surface-card border-carbon-border hover:border-carbon-border-strong text-mist-muted hover:text-mist'
                }`}
              >
                {c}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

