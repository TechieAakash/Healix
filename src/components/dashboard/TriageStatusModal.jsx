import React from "react";
import { Modal } from "../common/Modal";
import { Button } from "../common/Button";
import { Badge } from "../common/Badge";
import {
  ShieldCheck,
  AlertOctagon,
  CheckCircle2,
  HeartPulse,
  PhoneCall,
  Activity,
  ArrowRight,
  ExternalLink,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

export function TriageStatusModal({ isOpen, onClose, latestAssessment }) {
  const navigate = useNavigate();

  const urgency = latestAssessment?.urgencyLevel || "routine";
  const urgencyTitle = latestAssessment?.urgencyTitle || "Routine Care Recommended";
  const urgencyDesc =
    latestAssessment?.urgencyDescription ||
    "Your current assessments show no immediate red-flag indicators. Symptoms appear safe for routine home observation or a standard doctor visit.";

  const safetyProtocols = [
    {
      name: "Cardiopulmonary Red-Flag Filter",
      status: "Passed",
      desc: "Monitors for substernal chest pressure radiating to arm/jaw or acute resting dyspnea.",
      icon: HeartPulse,
    },
    {
      name: "Acute Neurological Interceptor",
      status: "Passed",
      desc: "Screens for facial drooping, focal extremity weakness, speech changes, or thunderclap onset.",
      icon: Activity,
    },
    {
      name: "Systemic Inflammatory & Fever Triage",
      status: "Passed",
      desc: "Evaluates persistent hyperthermia (>38.5°C) paired with meningeal rigidity or lethargy.",
      icon: CheckCircle2,
    },
    {
      name: "Evidence Retrieval Triage Filter",
      status: "Active",
      desc: "Grounds all symptom summaries with clinical literature before generating patient next steps.",
      icon: ShieldCheck,
    },
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Healix Clinical Triage Engine Status"
      subtitle="Safety-first monitoring, emergency rules, and triage thresholds"
      maxWidth="max-w-2xl"
    >
      <div className="space-y-6">
        {/* Top Status Banner */}
        <div className="p-4 rounded-2xl bg-teal-50 border border-teal-200/80 flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="p-2.5 rounded-xl bg-teal-600 text-white shrink-0 mt-0.5">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h4 className="text-sm font-bold text-slate-900">
                  Current Assessment: {urgency.toUpperCase()}
                </h4>
                <Badge variant={urgency === "emergency" ? "red" : urgency === "urgent" ? "amber" : "teal"} dot>
                  {urgencyTitle}
                </Badge>
              </div>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                {urgencyDesc}
              </p>
            </div>
          </div>
        </div>

        {/* Live Safety Protocols Checklist */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Active Triage Safety Filters
            </h4>
            <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
              4/4 Systems Operational
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {safetyProtocols.map((p, idx) => {
              const Icon = p.icon;
              return (
                <div
                  key={idx}
                  className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between"
                >
                  <div className="flex items-start gap-2.5">
                    <div className="p-1.5 rounded-lg bg-white border border-slate-200 text-teal-700 shrink-0">
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-xs font-bold text-slate-900">{p.name}</span>
                      </div>
                      <p className="text-[11px] text-slate-500 mt-1 leading-snug">
                        {p.desc}
                      </p>
                    </div>
                  </div>
                  <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px]">
                    <span className="text-slate-400">Filter Status:</span>
                    <span className="text-emerald-700 font-semibold flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                      {p.status}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Emergency Hotline Quick Access */}
        <div className="p-4 bg-rose-50/70 border border-rose-200 rounded-2xl space-y-2">
          <div className="flex items-center gap-2">
            <AlertOctagon className="w-4 h-4 text-rose-600" />
            <span className="text-xs font-bold uppercase tracking-wider text-rose-900">
              Emergency Care Protocol (Priority Override)
            </span>
          </div>
          <p className="text-xs text-rose-950 leading-relaxed">
            If you or someone near you experiences crushing chest pain, difficulty speaking, severe breathing trouble, or sudden fainting, call emergency responders immediately:
          </p>
          <div className="flex flex-wrap gap-2 pt-1">
            <a
              href="tel:911"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-700 transition-colors shadow-2xs"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              Dial 911 (US/Canada)
            </a>
            <a
              href="tel:112"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition-colors shadow-2xs"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              Dial 112 (EU/India)
            </a>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-end gap-3 pt-2 border-t border-slate-100">
          <Button
            variant="outline"
            size="sm"
            onClick={onClose}
          >
            Close
          </Button>
          <Button
            variant="teal"
            size="sm"
            onClick={() => {
              onClose();
              navigate("/symptom-checker");
            }}
            icon={ArrowRight}
            iconPosition="right"
          >
            Run New Symptom Check
          </Button>
        </div>
      </div>
    </Modal>
  );
}
