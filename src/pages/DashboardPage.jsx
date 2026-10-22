import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import {
  Heart,
  Droplet,
  Moon,
  Footprints,
  Bot,
  ClipboardPen,
  FileText,
  Activity,
  HeartPulse,
  X,
  CheckCircle2,
} from "lucide-react";
import { AiBotIllustration } from "../components/dashboard/AiBotIllustration";

export function DashboardPage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(authService.getCurrentUser());
  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [metricUpdates, setMetricUpdates] = useState({
    heartRate: "72",
    spo2: "98",
    sleep: "7h 42m",
    steps: "8,432",
    weight: "72",
  });
  const [updateSavedToast, setUpdateSavedToast] = useState(false);

  const handleSaveMetrics = (e) => {
    e.preventDefault();
    const updatedUser = {
      ...user,
      metrics: {
        ...user.metrics,
        heartRate: `${metricUpdates.heartRate} bpm`,
        spo2: `${metricUpdates.spo2}%`,
        sleep: metricUpdates.sleep,
        steps: metricUpdates.steps,
        weight: `${metricUpdates.weight} kg`,
      },
    };
    authService.updateProfile(updatedUser);
    setUser(updatedUser);
    setShowUpdateModal(false);
    setUpdateSavedToast(true);
    setTimeout(() => setUpdateSavedToast(false), 2500);
  };

  const metrics = [
    {
      id: "heart-rate",
      title: "Heart Rate",
      value: user?.metrics?.heartRate || "72 bpm",
      subtext: user?.metrics?.heartRateRange || "Normal range: 60 - 100",
      icon: Heart,
      iconColor: "text-emerald-700",
      iconBg: "bg-emerald-50",
    },
    {
      id: "spo2",
      title: "SpO2",
      value: user?.metrics?.spo2 || "98%",
      subtext: user?.metrics?.spo2Range || "Normal range: 95 - 100",
      icon: Droplet,
      iconColor: "text-emerald-700",
      iconBg: "bg-emerald-50",
    },
    {
      id: "sleep",
      title: "Sleep",
      value: user?.metrics?.sleep || "7h 42m",
      subtext: user?.metrics?.sleepSub || "Last night",
      icon: Moon,
      iconColor: "text-emerald-700",
      iconBg: "bg-emerald-50",
    },
    {
      id: "steps",
      title: "Steps",
      value: user?.metrics?.steps || "8,432",
      subtext: user?.metrics?.stepsSub || "Today",
      icon: Footprints,
      iconColor: "text-emerald-700",
      iconBg: "bg-emerald-50",
    },
  ];

  const quickActions = [
    {
      label: "Log Symptoms",
      desc: "Record current symptoms",
      icon: ClipboardPen,
      onClick: () => navigate("/symptom-checker"),
    },
    {
      label: "View Reports",
      desc: "Check lab results and summary",
      icon: FileText,
      onClick: () => navigate("/reports"),
    },
    {
      label: "Update Health Data",
      desc: "Vitals and activity check-in",
      icon: Activity,
      onClick: () => setShowUpdateModal(true),
    },
    {
      label: "Build Care Plan",
      desc: "Custom daily wellness goals",
      icon: HeartPulse,
      onClick: () => navigate("/care-plan"),
    },
  ];

  return (
    <div className="space-y-7 max-w-6xl mx-auto">
      {/* Toast Notification */}
      {updateSavedToast && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-2 bg-emerald-800 text-white px-4 py-2.5 rounded-xl shadow-lg text-xs font-semibold animate-in fade-in slide-in-from-top-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-300" />
          <span>Health data updated successfully</span>
        </div>
      )}

      {/* Greeting Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          Good morning, {user?.name || "Krrish"}
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Here's a quick look at your health today.
        </p>
      </div>

      {/* 4 Metric Cards in a Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div
              key={metric.id}
              className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs hover:border-slate-300 transition-all"
            >
              <div className="flex items-center gap-2.5 mb-3">
                <div className={`w-8 h-8 rounded-lg ${metric.iconBg} flex items-center justify-center shrink-0`}>
                  <Icon className={`w-4 h-4 ${metric.iconColor}`} />
                </div>
                <span className="text-xs font-medium text-slate-600">{metric.title}</span>
              </div>
              <div className="space-y-1">
                <p className="text-2xl font-bold text-slate-900 tracking-tight">{metric.value}</p>
                <p className="text-[11px] text-slate-400">{metric.subtext}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Featured AI Health Assistant Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#eef7f2] via-[#e5f4ec] to-[#d8efe2] border border-[#cbe6d5] p-6 sm:p-7 flex flex-col sm:flex-row items-center justify-between gap-6 shadow-xs">
        <div className="space-y-3 z-10 text-left w-full sm:w-auto">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-800 text-white flex items-center justify-center shadow-xs">
              <Bot className="w-4 h-4" />
            </div>
            <h2 className="text-lg font-bold text-emerald-950 tracking-tight">
              AI Health Assistant
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-emerald-900/80 max-w-md leading-relaxed">
            Ask questions, get personalized advice, and more.
          </p>
          <div className="pt-1">
            <Link to="/assistant">
              <button className="px-5 py-2.5 bg-[#065f46] hover:bg-[#064e3b] text-white text-xs sm:text-sm font-semibold rounded-xl shadow-xs transition-colors cursor-pointer">
                Chat Now
              </button>
            </Link>
          </div>
        </div>

        {/* AI Robot with Botanical illustration on right */}
        <div className="relative z-10 shrink-0 select-none">
          <AiBotIllustration className="w-36 sm:w-48 h-28 sm:h-32" />
        </div>
      </div>

      {/* Quick Actions Section */}
      <div className="space-y-3.5">
        <h3 className="text-sm font-bold text-slate-900 tracking-tight">
          Quick Actions
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
          {quickActions.map((action, idx) => {
            const Icon = action.icon;
            return (
              <button
                key={idx}
                onClick={action.onClick}
                className="flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-200/80 hover:border-emerald-600/50 hover:shadow-xs transition-all text-left cursor-pointer group"
              >
                <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0 group-hover:bg-emerald-800 group-hover:text-white transition-colors">
                  <Icon className="w-4 h-4" />
                </div>
                <div className="min-w-0">
                  <p className="text-xs font-semibold text-slate-800 group-hover:text-emerald-900 transition-colors">
                    {action.label}
                  </p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Quick Action Modal: Update Health Data */}
      {showUpdateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-200 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-800 flex items-center justify-center">
                  <Activity className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900">Update Health Data</h4>
                  <p className="text-[11px] text-slate-500">Record your latest health vitals</p>
                </div>
              </div>
              <button
                onClick={() => setShowUpdateModal(false)}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveMetrics} className="space-y-3.5 mt-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Heart Rate (bpm)
                </label>
                <input
                  type="number"
                  value={metricUpdates.heartRate}
                  onChange={(e) => setMetricUpdates({ ...metricUpdates, heartRate: e.target.value })}
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  SpO2 Oxygen (%)
                </label>
                <input
                  type="number"
                  value={metricUpdates.spo2}
                  onChange={(e) => setMetricUpdates({ ...metricUpdates, spo2: e.target.value })}
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Daily Steps
                </label>
                <input
                  type="text"
                  value={metricUpdates.steps}
                  onChange={(e) => setMetricUpdates({ ...metricUpdates, steps: e.target.value })}
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Weight (kg)
                </label>
                <input
                  type="number"
                  value={metricUpdates.weight}
                  onChange={(e) => setMetricUpdates({ ...metricUpdates, weight: e.target.value })}
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowUpdateModal(false)}
                  className="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-medium bg-[#065f46] hover:bg-[#064e3b] text-white rounded-xl shadow-xs"
                >
                  Save Metrics
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
