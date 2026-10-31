import React, { useState } from 'react';
import { AdaptiveQuestion } from '../../types';
import { HelpCircle, AlertTriangle, ShieldCheck, ArrowRight, SkipForward, PhoneCall } from 'lucide-react';

interface AdaptiveQuestionViewProps {
  question: AdaptiveQuestion;
  questionNumber: number;
  totalAnswered: number;
  onSubmitAnswer: (factName: string, value: string, rawResponse?: any) => Promise<void>;
  isSubmitting: boolean;
  onFinishEarly?: () => void;
}

export const AdaptiveQuestionView: React.FC<AdaptiveQuestionViewProps> = ({
  question,
  questionNumber,
  totalAnswered,
  onSubmitAnswer,
  isSubmitting,
  onFinishEarly
}) => {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [showRedFlagAlert, setShowRedFlagAlert] = useState<boolean>(false);

  const handleSelectOption = async (factValue: string, isRedFlag?: boolean) => {
    setSelectedOption(factValue);
    if (isRedFlag && factValue === 'TRUE') {
      setShowRedFlagAlert(true);
    }
    await onSubmitAnswer(question.target_fact_name, factValue, { selected_option: factValue });
    setSelectedOption(null);
  };

  const handleSkip = async () => {
    await onSubmitAnswer(question.target_fact_name, 'UNKNOWN', { skipped: true });
    setSelectedOption(null);
  };

  return (
    <div className="space-y-6">
      {/* Progress & Safety Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-carbon-border pb-4">
        <div className="flex items-center gap-2">
          <span className="w-7 h-7 rounded-lg bg-signal/20 border border-signal/40 text-signal text-xs font-bold flex items-center justify-center">
            {questionNumber}
          </span>
          <div>
            <span className="text-xs font-semibold text-mist">Clarifying Diagnostic Question</span>
            <span className="text-[11px] text-mist-muted ml-2 font-mono">
              ({totalAnswered} answered)
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {question.is_safety_critical && (
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-alert/15 text-alert border border-alert/30">
              <AlertTriangle className="w-3 h-3" />
              Safety-Critical Screening
            </span>
          )}
          {question.evidence_provenance && (
            <span className="text-[10px] text-mist-muted font-mono hidden md:inline-block">
              Ref: {question.evidence_provenance}
            </span>
          )}
        </div>
      </div>

      {/* Immediate Red Flag Warning Banner */}
      {showRedFlagAlert && (
        <div className="p-4 rounded-xl glass-panel-alert border border-alert text-mist space-y-2 animate-bounce">
          <div className="flex items-center gap-2 text-alert font-bold text-sm">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            CRITICAL RED FLAG DETECTED
          </div>
          <p className="text-xs text-mist leading-relaxed">
            The symptom you reported meets emergency referral criteria. Please do not wait to finish this assessment. Contact emergency medical services immediately.
          </p>
          <div className="pt-2">
            <a
              href="tel:112"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-alert text-white text-xs font-bold shadow-lg hover:opacity-90"
            >
              <PhoneCall className="w-4 h-4" />
              Call Emergency Dispatch (112 / 911)
            </a>
          </div>
        </div>
      )}

      {/* Question Prompt Card */}
      <div className="p-5 sm:p-6 rounded-2xl glass-panel space-y-4">
        <h2 className="text-lg sm:text-xl font-bold text-mist leading-snug">
          {question.prompt}
        </h2>

        {question.subtext && (
          <div className="p-3 rounded-xl surface-card text-xs text-mist-muted flex items-start gap-2.5">
            <HelpCircle className="w-4 h-4 text-signal shrink-0 mt-0.5" />
            <span className="leading-relaxed">{question.subtext}</span>
          </div>
        )}

        {/* Answer Options */}
        <div className="pt-2 space-y-2.5">
          {question.options && question.options.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {question.options.map((opt) => {
                const isSelected = selectedOption === opt.fact_value;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    disabled={isSubmitting}
                    onClick={() => handleSelectOption(opt.fact_value, opt.is_red_flag)}
                    className={`p-4 rounded-xl border text-left font-medium transition-all flex items-center justify-between gap-3 ${
                      isSelected
                        ? 'bg-signal/20 border-signal text-signal ring-2 ring-signal/30'
                        : opt.is_red_flag
                        ? 'surface-card border-carbon-border hover:border-alert/50 text-mist hover:bg-alert/5'
                        : 'surface-card border-carbon-border hover:border-signal/50 text-mist'
                    } disabled:opacity-50`}
                  >
                    <span className="text-sm font-semibold">{opt.label}</span>
                    <ArrowRight className="w-4 h-4 text-mist-muted shrink-0" />
                  </button>
                );
              })}
            </div>
          ) : (
            /* Fallback Boolean Yes / No */
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                disabled={isSubmitting}
                onClick={() => handleSelectOption('TRUE')}
                className="p-4 rounded-xl border border-carbon-border hover:border-signal hover:bg-signal/15 text-mist font-semibold text-sm transition-all"
              >
                Yes
              </button>
              <button
                type="button"
                disabled={isSubmitting}
                onClick={() => handleSelectOption('FALSE')}
                className="p-4 rounded-xl border border-carbon-border hover:border-signal hover:bg-signal/15 text-mist font-semibold text-sm transition-all"
              >
                No
              </button>
            </div>
          )}
        </div>

        {/* Footer Actions: Skip or Complete Early */}
        <div className="pt-4 border-t border-carbon-border flex items-center justify-between text-xs">
          <button
            type="button"
            disabled={isSubmitting}
            onClick={handleSkip}
            className="flex items-center gap-1.5 text-mist-muted hover:text-mist transition-colors py-1.5 px-3 rounded-lg hover:bg-carbon"
          >
            <SkipForward className="w-3.5 h-3.5" />
            <span>I am not sure / Skip question</span>
          </button>

          {totalAnswered >= 3 && onFinishEarly && (
            <button
              type="button"
              disabled={isSubmitting}
              onClick={onFinishEarly}
              className="text-signal hover:underline font-medium"
            >
              Analyze with current findings →
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

