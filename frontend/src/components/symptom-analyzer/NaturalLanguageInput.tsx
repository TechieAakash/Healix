import React, { useState } from 'react';
import { Sparkles, ArrowRight, CheckCircle2, ShieldAlert } from 'lucide-react';
import { ParseSymptomsResponse } from '../../types';

interface NaturalLanguageInputProps {
  freeText: string;
  onChangeFreeText: (text: string) => void;
  onAnalyze: () => Promise<void>;
  isAnalyzing: boolean;
  parseResult: ParseSymptomsResponse | null;
}

const EXAMPLE_PROMPTS = [
  "Throbbing headache on my right temple for two days with nausea, but no fever.",
  "Sudden crushing chest tightness radiating down left arm with shortness of breath.",
  "Sharp pain in the lower right abdomen since this morning with fever and loss of appetite.",
  "Runny nose, tickly sore throat and dry cough for 3 days without breathing difficulty."
];

export const NaturalLanguageInput: React.FC<NaturalLanguageInputProps> = ({
  freeText,
  onChangeFreeText,
  onAnalyze,
  isAnalyzing,
  parseResult
}) => {
  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-semibold text-mist flex items-center justify-between mb-1.5">
          <span className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-signal" />
            Describe What You Are Experiencing
          </span>
          <span className="text-xs text-mist-muted font-normal">
            Natural English, conversational details
          </span>
        </label>
        <p className="text-xs text-mist-muted mb-2">
          Tell us about your symptoms in your own words. Mention where it hurts, how it feels, how long it has lasted, and symptoms you explicitly do <em>not</em> have.
        </p>

        <div className="relative">
          <textarea
            value={freeText}
            onChange={(e) => onChangeFreeText(e.target.value)}
            rows={4}
            placeholder="e.g. I have had a pounding headache on the right side of my head for 2 days. It feels worse in bright lights and I feel sick, but I don't have a fever or neck stiffness..."
            className="w-full p-3.5 rounded-xl text-sm border border-carbon-border text-mist placeholder:text-mist-muted/50 focus:outline-none leading-relaxed resize-none"
          />

          <div className="flex items-center justify-between mt-2">
            <div className="text-[11px] text-mist-muted">
              {freeText.length > 0 ? `${freeText.length} characters` : 'Type or select an example below'}
            </div>

            <button
              type="button"
              onClick={onAnalyze}
              disabled={isAnalyzing || !freeText.trim()}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-signal text-void hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center gap-2 shadow-sm"
            >
              {isAnalyzing ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-void border-t-transparent rounded-full animate-spin" />
                  <span>Parsing Description...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Analyze My Description</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Example Prompt Chips */}
      <div className="pt-1">
        <span className="text-[11px] text-mist-muted block mb-1.5 font-medium">Try an example case:</span>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_PROMPTS.map((ex, i) => (
            <button
              key={i}
              type="button"
              onClick={() => onChangeFreeText(ex)}
              className="text-[11px] text-left px-2.5 py-1.5 rounded-lg surface-card-hover border border-carbon-border text-mist-muted hover:text-mist transition-colors line-clamp-1 max-w-md"
            >
              "{ex.length > 55 ? ex.substring(0, 52) + '...' : ex}"
            </button>
          ))}
        </div>
      </div>

      {/* Extracted NLP Summary Box */}
      {parseResult && (
        <div className="p-4 rounded-xl bg-signal/10 border border-signal/30 space-y-3 animate-fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-signal">
              <CheckCircle2 className="w-4 h-4 text-signal" />
              <span>Extracted Clinical Profile</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-signal/15 border border-signal/20">
                Confidence: {Math.round(parseResult.confidence * 100)}%
              </span>
            </div>
            {parseResult.source && (
              <span className="text-[10px] text-mist-muted font-mono">
                Engine: {parseResult.source === 'GEMINI_2_FLASH' ? 'Gemini 2.0 Flash' : 'Deterministic Rule Parser'}
              </span>
            )}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2.5 text-xs">
            <div className="p-2 rounded-lg surface-card">
              <span className="text-[10px] text-mist-muted block">Duration</span>
              <span className="font-medium text-mist">{parseResult.duration || 'Not specified'}</span>
            </div>
            <div className="p-2 rounded-lg surface-card">
              <span className="text-[10px] text-mist-muted block">Severity</span>
              <span className="font-medium text-mist">{parseResult.severity || 'Moderate'}</span>
            </div>
            <div className="p-2 rounded-lg surface-card">
              <span className="text-[10px] text-mist-muted block">Character</span>
              <span className="font-medium text-mist">{parseResult.character || 'Not specified'}</span>
            </div>
            <div className="p-2 rounded-lg surface-card">
              <span className="text-[10px] text-mist-muted block">Negated / Absent</span>
              <span className="font-medium text-mint">
                {parseResult.negated_facts.length > 0
                  ? parseResult.negated_facts.map(f => f.replace('symptom.', '').replace('_', ' ')).join(', ')
                  : 'None ruled out'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

