import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import { assessmentService } from "../services/assessmentService";
import { Button } from "../components/common/Button";
import { Card, CardHeader } from "../components/common/Card";
import { HealthMetricCard } from "../components/dashboard/HealthMetricCard";
import { AssessmentCard } from "../components/dashboard/AssessmentCard";
import { HealthActivityChart } from "../components/dashboard/HealthActivityChart";
import { HealthInsightsCard } from "../components/dashboard/HealthInsightsCard";
import { TriageStatusModal } from "../components/dashboard/TriageStatusModal";
import { ClinicalSourcesModal } from "../components/dashboard/ClinicalSourcesModal";
import { SkeletonLoader } from "../components/common/SkeletonLoader";
import {
  Stethoscope,
  ArrowRight,
  ShieldCheck,
  Activity,
  Calendar,
  Sparkles,
  BotMessageSquare,
  History,
  Clock,
  HeartPulse,
} from "lucide-react";

export function DashboardPage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);

  // Interactive modal states for metric cards
  const [showTriageModal, setShowTriageModal] = useState(false);
  const [showSourcesModal, setShowSourcesModal] = useState(false);

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    setUser(currentUser);
    const data = assessmentService.getAllAssessments();
    setAssessments(data);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <SkeletonLoader type="text" count={3} />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <SkeletonLoader type="card" count={3} />
        </div>
      </div>
    );
  }

  const latestAssessment = assessments[0];
  const previousAssessments = assessments.slice(1, 4);

  return (
    <div className="space-y-8">
      {/* ================= GREETING HEADER ================= */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6 sm:p-8 rounded-3xl shadow-md relative overflow-hidden">
        {/* Glow accent */}
        <div className="absolute top-0 right-0 w-80 h-80 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 space-y-1.5">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-teal-500/20 text-teal-300 text-xs font-semibold mb-1">
            <HeartPulse className="w-3.5 h-3.5 text-teal-400" />
            <span>Health Triage Companion</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Good morning, {user?.name || "Aakash"}
          </h1>
          <p className="text-sm text-slate-300 max-w-xl">
            How are you feeling today? Healix is ready to assist you in evaluating symptoms, identifying warning signs, and guiding care choices.
          </p>
        </div>

        <div className="relative z-10 flex flex-wrap items-center gap-3">
          <Link to="/symptom-checker">
            <Button
              variant="teal"
              size="lg"
              icon={Stethoscope}
              className="shadow-lg shadow-teal-900/40"
            >
              Start Symptom Check
            </Button>
          </Link>
          <Link to="/assistant">
            <Button
              variant="secondary"
              size="lg"
              icon={BotMessageSquare}
              className="bg-slate-800 text-white hover:bg-slate-700 border border-slate-700"
            >
              Ask Assistant
            </Button>
          </Link>
        </div>
      </div>

      {/* ================= QUICK METRICS ROW (All Cards Fully Interactive) ================= */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Total Assessments -> Clicks to /history */}
        <HealthMetricCard
          title="Total Assessments"
          value={assessments.length}
          subtitle="Documented evaluations"
          icon={Activity}
          badgeText="View all in history"
          to="/history"
        />

        {/* Card 2: Last Check-in -> Clicks to view latest assessment summary report */}
        <HealthMetricCard
          title="Last Check-in"
          value={
            latestAssessment?.date
              ? latestAssessment.date.includes(",")
                ? latestAssessment.date.split(",")[0]
                : latestAssessment.date
              : "Today"
          }
          subtitle={latestAssessment?.primarySymptom || "Headache & fatigue"}
          icon={Calendar}
          badgeText="Report generated"
          to={latestAssessment ? `/assessment/${latestAssessment.id}` : "/symptom-checker"}
        />

        {/* Card 3: Triage Status -> Clicks to open Triage & Safety Protocol Modal */}
        <HealthMetricCard
          title="Triage Status"
          value={
            latestAssessment?.urgencyLevel === "emergency"
              ? "Emergency"
              : latestAssessment?.urgencyLevel === "urgent"
              ? "Urgent"
              : "Routine"
          }
          subtitle={latestAssessment?.urgencyTitle || "No emergency red flags"}
          icon={ShieldCheck}
          badgeText="Safety engine active"
          onClick={() => setShowTriageModal(true)}
        />

        {/* Card 4: Clinical Citations -> Clicks to open Verified Medical Sources Modal */}
        <HealthMetricCard
          title="Clinical Citations"
          value="12 Verified"
          subtitle="Mayo, WHO & NHS linked"
          icon={Sparkles}
          badgeText="Grounding active"
          onClick={() => setShowSourcesModal(true)}
        />
      </div>

      {/* ================= MAIN DASHBOARD GRID ================= */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Recent Assessment & Activity Chart (8 cols) */}
        <div className="lg:col-span-8 space-y-8">
          {/* Card 1: Recent Assessment */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900 tracking-tight">
                Recent Assessment
              </h2>
              <Link
                to="/symptom-checker"
                className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center gap-1"
              >
                New check-in <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {latestAssessment ? (
              <AssessmentCard assessment={latestAssessment} />
            ) : (
              <div className="p-8 text-center bg-white rounded-2xl border border-slate-200">
                <p className="text-sm text-slate-500">No assessments logged yet.</p>
                <div className="mt-3">
                  <Link to="/symptom-checker">
                    <Button variant="teal" size="sm">
                      Start your first check
                    </Button>
                  </Link>
                </div>
              </div>
            )}
          </div>

          {/* Card 2: Health Activity Chart */}
          <Card padding="default">
            <CardHeader
              title="Health Activity & Symptom Trajectory"
              subtitle="Weekly check-ins, fatigue reports, and discomfort index over the past 8 weeks"
              action={
                <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700">
                  Past 8 Weeks
                </span>
              }
            />
            <HealthActivityChart />
            <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between text-xs text-slate-400 gap-2">
              <p>Visualizing self-reported trends over time to assist clinical discussions.</p>
              <span className="text-teal-700 font-medium">Updated Oct 2, 2026</span>
            </div>
          </Card>

          {/* Card 3: Previous Assessments list */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900 tracking-tight">
                Previous Assessments
              </h2>
              <Link
                to="/history"
                className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center gap-1"
              >
                View all history <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="space-y-3">
              {previousAssessments.map((asm) => (
                <AssessmentCard key={asm.id} assessment={asm} compact />
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Health Insights & Safety Reminder (4 cols) */}
        <div className="lg:col-span-4 space-y-6">
          {/* Card 4: Health Insights */}
          <HealthInsightsCard />

          {/* Quick AI Assistant Card */}
          <Card padding="default" className="border-teal-100 bg-teal-50/40">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-xl bg-teal-600 text-white">
                <BotMessageSquare className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900">
                  Ask Healix Assistant
                </h3>
                <p className="text-[11px] text-slate-500">24/7 Clinical Q&A</p>
              </div>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed mb-4">
              Have questions about hydration, tension triggers, or what symptoms to track before a doctor's visit?
            </p>
            <Link to="/assistant">
              <Button variant="outline" size="sm" className="w-full bg-white text-teal-800 border-teal-200">
                Start Health Conversation
              </Button>
            </Link>
          </Card>

          {/* Clinical Safety Card */}
          <Card padding="default" className="border-slate-200 bg-slate-50/80">
            <div className="flex items-center gap-2 mb-2">
              <ShieldCheck className="w-4 h-4 text-teal-600" />
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Patient Safety Reassurance
              </h4>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Healix does not diagnose diseases. In case of severe chest pain, sudden numbness, or shortness of breath, please call <strong>911 / 112</strong> immediately.
            </p>
          </Card>
        </div>
      </div>

      {/* ================= INTERACTIVE MODALS FOR QUICK METRICS ================= */}
      {/* 1. Triage Status & Protocol Modal */}
      <TriageStatusModal
        isOpen={showTriageModal}
        onClose={() => setShowTriageModal(false)}
        latestAssessment={latestAssessment}
      />

      {/* 2. Clinical Citations & Knowledge Bases Modal */}
      <ClinicalSourcesModal
        isOpen={showSourcesModal}
        onClose={() => setShowSourcesModal(false)}
      />
    </div>
  );
}
