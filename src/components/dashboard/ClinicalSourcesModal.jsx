import React from "react";
import { Modal } from "../common/Modal";
import { Button } from "../common/Button";
import { Badge } from "../common/Badge";
import {
  BookOpen,
  ExternalLink,
  ShieldCheck,
  CheckCircle2,
  Database,
  Cpu,
  BotMessageSquare,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

export function ClinicalSourcesModal({ isOpen, onClose }) {
  const navigate = useNavigate();

  const sourcesList = [
    {
      name: "Mayo Clinic",
      citationsCount: 4,
      topics: "Tension Headaches, Dehydration, Abdominal Pain Triage",
      url: "https://www.mayoclinic.org",
      authority: "Mayo Foundation for Medical Education and Research",
      badge: "Clinical Peer-Reviewed",
    },
    {
      name: "World Health Organization (WHO)",
      citationsCount: 3,
      topics: "Headache Disorders Fact Sheet, Primary Care Guidelines",
      url: "https://www.who.int",
      authority: "United Nations Global Health Observatory",
      badge: "International Standard",
    },
    {
      name: "National Health Service (NHS UK)",
      citationsCount: 3,
      topics: "Clinical Knowledge Summaries (CKS), Cough & Hydration",
      url: "https://www.nhs.uk",
      authority: "UK National Institute for Health and Care Excellence",
      badge: "Public Health System",
    },
    {
      name: "American Academy of Family Physicians (AAFP)",
      citationsCount: 2,
      topics: "Evidence-Based Adult Symptom Assessment & Cough Algorithms",
      url: "https://www.aafp.org",
      authority: "American Board of Family Medicine",
      badge: "Clinical Specialty",
    },
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Verified Medical Sources & Knowledge Bases"
      subtitle="12 Verified clinical guidelines grounding Healix AI triage summaries"
      maxWidth="max-w-2xl"
    >
      <div className="space-y-6">
        {/* RAG Grounding Architecture Banner */}
        <div className="p-4 bg-teal-50 rounded-2xl border border-teal-200/80 space-y-2">
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-teal-700" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-teal-950">
              Retrieval-Augmented Generation (RAG) in Healthcare
            </h4>
          </div>
          <p className="text-xs text-teal-900 leading-relaxed">
            Healix does not rely on raw AI memory. When you describe symptoms, our system retrieves validated medical guidance from curated clinical registries before formatting explanations. This virtually eliminates hallucinations and guarantees clinical grounding.
          </p>
        </div>

        {/* Sources Catalog List */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Curated Clinical Knowledge Bases
            </h4>
            <span className="text-[11px] font-semibold text-teal-800 bg-teal-50 px-2 py-0.5 rounded-md border border-teal-200">
              12 Active Citations
            </span>
          </div>

          <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
            {sourcesList.map((source, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 hover:border-slate-300 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-900">{source.name}</span>
                    <Badge variant="teal" size="sm">
                      {source.badge}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-600">
                    <strong className="text-slate-700">Covered Topics:</strong> {source.topics}
                  </p>
                  <p className="text-[11px] text-slate-400">
                    Authority: {source.authority}
                  </p>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <span className="text-xs font-bold text-teal-700 bg-white px-2 py-1 rounded-lg border border-slate-200">
                    {source.citationsCount} Citations
                  </span>
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 text-slate-400 hover:text-teal-700 hover:bg-white rounded-lg border border-transparent hover:border-slate-200 transition-all"
                    title="Open Source Library"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Verification Guarantee */}
        <div className="p-3 bg-slate-100 rounded-xl border border-slate-200 text-[11px] text-slate-500 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-teal-600 shrink-0" />
          <span>
            All sources are reviewed according to evidence-based medicine criteria (GRADE framework).
          </span>
        </div>

        {/* Bottom Actions */}
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
              navigate("/assistant");
            }}
            icon={BotMessageSquare}
          >
            Ask AI with Citations
          </Button>
        </div>
      </div>
    </Modal>
  );
}
