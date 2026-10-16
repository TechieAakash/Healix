import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { assessmentService } from "../services/assessmentService";
import { authService } from "../services/authService";
import { ReportSection } from "../components/reports/ReportSection";
import { UrgencyIndicator } from "../components/common/UrgencyIndicator";
import { Button } from "../components/common/Button";
import {
  Printer,
  Download,
  ArrowLeft,
  HeartPulse,
  ShieldCheck,
  Calendar,
  User,
  FileText,
  Activity,
  AlertTriangle,
  Info,
  CheckCircle2,
} from "lucide-react";

export function ReportPage() {
  const { id } = useParams();
  const [assessment, setAssessment] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(authService.getCurrentUser());
    const data = assessmentService.getAssessmentById(id);
    setAssessment(data);
  }, [id]);

  if (!assessment) {
    return (
      <div className="max-w-3xl mx-auto py-12 text-center text-slate-500">
        Loading printable medical summary...
      </div>
    );
  }

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadPdf = () => {
    // Standard trigger for browser PDF print dialog
    window.print();
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-16">
      {/* Top Bar with Navigation & Actions (hidden in print) */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 no-print">
        <Link
          to={`/assessment/${assessment.id}`}
          className="text-xs font-semibold text-slate-600 hover:text-slate-900 inline-flex items-center gap-1.5"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Assessment Summary
        </Link>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={handleDownloadPdf}
            icon={Download}
          >
            Download PDF
          </Button>
          <Button
            variant="teal"
            size="sm"
            onClick={handlePrint}
            icon={Printer}
          >
            Print Report
          </Button>
        </div>
      </div>

      {/* ================= PRINTABLE CLINICAL DOCUMENT ================= */}
      <div className="bg-white rounded-3xl border border-slate-200/90 p-8 sm:p-12 shadow-sm printable-card space-y-8 text-slate-900">
        {/* Document Header */}
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-6 border-b-2 border-slate-900 pb-6">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-teal-600 flex items-center justify-center text-white">
                <HeartPulse className="w-5 h-5" />
              </div>
              <span className="font-extrabold text-2xl tracking-tight text-slate-900">
                Healix
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                Clinical Intake Brief
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Patient-Prepared Symptom Summary for Healthcare Consultations
            </p>
          </div>

          <div className="text-left sm:text-right text-xs space-y-1">
            <p className="font-mono text-slate-400">REF: {assessment.id}</p>
            <p className="text-slate-600">
              Generated: <span className="font-semibold text-slate-900">{assessment.date}</span>
            </p>
            <p className="text-teal-700 font-semibold">Status: Intake Completed</p>
          </div>
        </div>

        {/* Section 1: Patient-Provided Information */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs">
          <div>
            <span className="text-slate-400 block font-medium">Patient Name</span>
            <span className="font-bold text-slate-900 mt-0.5 block">{user?.fullName || "Aakash Sharma"}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Date of Birth</span>
            <span className="font-semibold text-slate-800 mt-0.5 block">{user?.dateOfBirth || "1996-08-14"}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Primary Symptom</span>
            <span className="font-semibold text-slate-800 mt-0.5 block">{assessment.primarySymptom}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Emergency Contact</span>
            <span className="font-semibold text-slate-800 mt-0.5 block">{user?.emergencyContact?.name || "Priya Sharma"}</span>
          </div>
        </div>

        {/* Section 2: Symptoms & Timeline */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100 pb-2 flex items-center gap-2">
            <Activity className="w-4 h-4 text-teal-600" />
            1. Reported Symptoms & Timeline
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="p-3 bg-white border border-slate-200 rounded-xl">
              <span className="text-slate-400 block">Symptom Cluster</span>
              <div className="flex flex-wrap gap-1 mt-1.5">
                {assessment.symptoms?.map((s, i) => (
                  <span key={i} className="px-2 py-0.5 bg-slate-100 font-semibold rounded text-slate-800">
                    {typeof s === "string" ? s : s.label}
                  </span>
                ))}
              </div>
            </div>
            <div className="p-3 bg-white border border-slate-200 rounded-xl">
              <span className="text-slate-400 block">Onset & Duration</span>
              <span className="font-semibold text-slate-800 mt-1 block">
                {assessment.duration || "Recent"} (Frequency: {assessment.frequency || "Intermittent"})
              </span>
            </div>
            <div className="p-3 bg-white border border-slate-200 rounded-xl">
              <span className="text-slate-400 block">Reported Severity</span>
              <span className="font-semibold text-slate-800 mt-1 block">
                {assessment.severity || "Mild to Moderate"}
              </span>
            </div>
          </div>
        </div>

        {/* Section 3: Follow-Up Answers */}
        {assessment.followUpSummary && assessment.followUpSummary.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100 pb-2 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-teal-600" />
              2. Clinical Intake Responses
            </h3>
            <div className="divide-y divide-slate-100 border border-slate-200 rounded-xl overflow-hidden text-xs">
              {assessment.followUpSummary.map((item, idx) => (
                <div key={idx} className="p-3 bg-white flex items-center justify-between gap-4">
                  <span className="text-slate-700 font-medium">{item.question}</span>
                  <span className="font-bold text-slate-900 bg-slate-100 px-2.5 py-1 rounded-md shrink-0">
                    {item.answer}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Section 4: Urgency Assessment */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100 pb-2 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-teal-600" />
            3. Urgency Guidance Level
          </h3>
          <UrgencyIndicator
            level={assessment.urgencyLevel}
            title={assessment.urgencyTitle}
            description={assessment.urgencyDescription}
          />
        </div>

        {/* Section 5: Possible Explanations */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100 pb-2">
            4. Informational Possibilities (To Discuss with Clinician)
          </h3>
          <div className="space-y-3">
            {assessment.possibleExplanations?.map((exp, idx) => (
              <div key={idx} className="p-4 border border-slate-200 rounded-xl text-xs space-y-1.5">
                <div className="flex items-center justify-between">
                  <h4 className="font-bold text-slate-900 text-sm">{exp.title}</h4>
                  <span className="text-[11px] font-semibold text-teal-700 px-2 py-0.5 bg-teal-50 rounded border border-teal-200">
                    {exp.matchLevel}
                  </span>
                </div>
                <p className="text-slate-600 leading-relaxed">{exp.description}</p>
                {exp.clinicalInsight && (
                  <p className="text-slate-500 italic mt-1">
                    Differential note: {exp.clinicalInsight}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Section 6: Warning Signs & Red Flags */}
        <div className="p-4 bg-amber-50 rounded-2xl border border-amber-200 space-y-2 text-xs">
          <h4 className="font-bold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
            5. Clinical Warning Signs ("Red Flags")
          </h4>
          <ul className="space-y-1 text-slate-800 list-disc pl-5">
            {assessment.warningSignsToWatch?.map((sign, idx) => (
              <li key={idx}>{sign}</li>
            ))}
          </ul>
        </div>

        {/* Section 7: Medical Sources */}
        <div className="pt-2 text-xs text-slate-500 space-y-1">
          <p className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">
            6. Evidence Grounding & Knowledge Bases:
          </p>
          <p>
            {assessment.sources?.map((s) => (typeof s === "object" ? s.name : s)).join(" • ")}
          </p>
        </div>

        {/* Legal Disclaimer Box */}
        <div className="p-4 bg-slate-100 rounded-xl text-[11px] text-slate-500 leading-relaxed border border-slate-200">
          <strong>LEGAL & CLINICAL NOTICE:</strong> This document was prepared by Healix, an AI-powered health informational triage tool. This summary does not constitute an official diagnosis, clinical evaluation, or prescription. Please present this summary to your doctor or licensed healthcare practitioner for professional examination.
        </div>
      </div>
    </div>
  );
}
