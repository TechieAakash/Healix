import React from "react";
import { Modal } from "../common/Modal";
import { Button } from "../common/Button";
import { AlertOctagon, PhoneCall, MapPin, ArrowRight, ShieldCheck } from "lucide-react";

export function SafetyRedFlagModal({
  isOpen,
  onProceedAnyway,
  detectedReason,
  matchedTriggers = [],
}) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={() => {}} // Disallow accidental backdrop dismissal without making a choice
      showClose={false}
      maxWidth="max-w-xl"
    >
      <div className="space-y-6">
        {/* Emergency Alert Banner */}
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center shrink-0 border border-rose-200">
            <AlertOctagon className="w-7 h-7" />
          </div>
          <div>
            <span className="text-[11px] uppercase tracking-wider font-bold text-rose-700 bg-rose-50 px-2.5 py-0.5 rounded-full border border-rose-200">
              Immediate Safety Advisory
            </span>
            <h3 className="text-xl font-bold text-slate-900 mt-1">
              Important: Please seek immediate medical attention.
            </h3>
          </div>
        </div>

        {/* Clinical Rationale (Carefully phrased, non-alarmist, no definitive diagnostic claims) */}
        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-slate-700 space-y-3">
          <p className="text-sm leading-relaxed">
            Some symptoms you have reported (e.g.{" "}
            <strong>
              {matchedTriggers.length > 0
                ? matchedTriggers.join(", ")
                : "cardiopulmonary, neurological, or sudden severe indicators"}
            </strong>
            ) can sometimes require urgent in-person medical evaluation.
          </p>
          <p className="text-xs text-slate-500 leading-relaxed">
            <strong>Healix cannot determine the specific cause of your symptoms</strong> and cannot replace emergency clinical care. For your safety, emergency assessment takes strict priority over any automated informational report.
          </p>
        </div>

        {/* Emergency Immediate Action Guide */}
        <div className="bg-rose-50/70 rounded-2xl p-4 border border-rose-200 space-y-2">
          <h4 className="text-xs font-bold text-rose-900 uppercase tracking-wider flex items-center gap-1.5">
            <PhoneCall className="w-4 h-4 text-rose-600" />
            Recommended Immediate Actions:
          </h4>
          <ul className="text-xs text-rose-950 space-y-1.5 pl-5 list-disc">
            <li>Call your regional emergency hotline immediately (e.g., <strong>911</strong> in the US/Canada, <strong>112</strong> in the EU/India, <strong>999</strong> in the UK).</li>
            <li>If someone is with you, notify them right away and have them accompany you to the nearest Emergency Room.</li>
            <li>Do not attempt to drive yourself if you are feeling faint, confused, or severely breathless.</li>
          </ul>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          <a
            href="tel:911"
            className="flex-1"
          >
            <Button
              variant="danger"
              className="w-full text-sm font-semibold py-3"
              icon={PhoneCall}
            >
              Call Emergency Services (911 / 112)
            </Button>
          </a>

          <Button
            variant="outline"
            onClick={onProceedAnyway}
            className="flex-1 text-slate-700 border-slate-300 hover:bg-slate-100 text-xs py-3"
            icon={ArrowRight}
            iconPosition="right"
          >
            I understand, continue for information
          </Button>
        </div>

        <div className="flex items-center justify-center gap-1.5 text-[11px] text-slate-400">
          <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
          <span>Healix Safety Triage System • Priority Protection Active</span>
        </div>
      </div>
    </Modal>
  );
}
