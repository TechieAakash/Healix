import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  Download,
  Calendar,
  ChevronDown,
  Heart,
  Droplet,
  Moon,
  Footprints,
  Scale,
  ClipboardList,
  Stethoscope,
  HeartPulse,
  CheckCircle2,
} from "lucide-react";

export function ReportsOverviewPage() {
  const [activeTab, setActiveTab] = useState("Health Overview");
  const [timeRange, setTimeRange] = useState("Last 4 Weeks");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [downloadToast, setDownloadToast] = useState(false);

  const tabs = ["Health Overview", "Lab Reports", "Trends", "Downloads"];

  const keyMetrics = [
    { label: "Heart Rate", value: "72 bpm", icon: Heart },
    { label: "SpO2", value: "98%", icon: Droplet },
    { label: "Sleep", value: "7h 42m", icon: Moon },
    { label: "Steps", value: "8,432", icon: Footprints },
    { label: "Weight", value: "72 kg", icon: Scale },
  ];

  const recentActivity = [
    {
      title: "Health Assessment",
      sub: "Completed • 2 days ago",
      icon: ClipboardList,
      color: "text-emerald-700 bg-emerald-50",
      link: "/assessment/asm_101",
    },
    {
      title: "Symptom Check",
      sub: "Headache • 4 days ago",
      icon: Stethoscope,
      color: "text-teal-700 bg-teal-50",
      link: "/symptom-checker",
    },
    {
      title: "Care Plan Updated",
      sub: "3 days ago",
      icon: HeartPulse,
      color: "text-emerald-700 bg-emerald-50",
      link: "/care-plan",
    },
  ];

  const handleDownload = () => {
    setDownloadToast(true);
    setTimeout(() => {
      setDownloadToast(false);
      // Trigger a print or simulated PDF download
      window.print();
    }, 800);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Toast Alert */}
      {downloadToast && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-2 bg-emerald-800 text-white px-4 py-2.5 rounded-xl shadow-lg text-xs font-semibold animate-in fade-in slide-in-from-top-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-300" />
          <span>Generating and downloading medical brief PDF...</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Reports
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Review detailed health metrics, laboratory summaries, and historical trends.
          </p>
        </div>

        {/* Date Filter Dropdown */}
        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-2 px-3.5 py-2 bg-white border border-slate-200 rounded-xl text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors shadow-xs"
          >
            <Calendar className="w-3.5 h-3.5 text-slate-500" />
            <span>{timeRange}</span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </button>

          {dropdownOpen && (
            <div className="absolute right-0 mt-1.5 w-40 bg-white border border-slate-200 rounded-xl shadow-lg py-1 z-20 text-xs">
              {["Last 7 Days", "Last 4 Weeks", "Last 3 Months", "Last Year"].map((opt) => (
                <button
                  key={opt}
                  onClick={() => {
                    setTimeRange(opt);
                    setDropdownOpen(false);
                  }}
                  className={`w-full text-left px-3.5 py-2 hover:bg-emerald-50 transition-colors ${
                    timeRange === opt ? "text-emerald-800 font-semibold bg-emerald-50/50" : "text-slate-700"
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-1 border-b border-slate-200 pb-2 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
              activeTab === tab
                ? "bg-emerald-50 text-emerald-800"
                : "text-slate-500 hover:text-slate-900 hover:bg-slate-50"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* 3 Columns: Health Score, Key Metrics, Recent Activity */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Card 1: Health Score */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs flex flex-col items-center justify-between text-center">
          <h2 className="text-sm font-bold text-slate-900 tracking-tight self-start">
            Health Score
          </h2>

          <div className="my-6 relative flex items-center justify-center">
            {/* Circular Gauge Ring */}
            <svg className="w-36 h-36" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="42"
                stroke="#e2e8f0"
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="50"
                cy="50"
                r="42"
                stroke="#059669"
                strokeWidth="8"
                strokeDasharray="264"
                strokeDashoffset={264 - (264 * 82) / 100}
                strokeLinecap="round"
                fill="none"
                transform="rotate(-90 50 50)"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-extrabold text-slate-900">82</span>
              <span className="text-[10px] text-slate-400 font-medium">/ 100</span>
            </div>
          </div>

          <div className="space-y-1">
            <span className="inline-block px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-full">
              Good
            </span>
            <p className="text-xs text-slate-500 pt-1">Your health is on track!</p>
          </div>
        </div>

        {/* Card 2: Key Metrics Table */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 tracking-tight">
            Key Metrics
          </h2>

          <div className="divide-y divide-slate-100">
            {keyMetrics.map((km, idx) => {
              const Icon = km.icon;
              return (
                <div key={idx} className="flex items-center justify-between py-2.5">
                  <div className="flex items-center gap-2.5">
                    <Icon className="w-4 h-4 text-emerald-700" />
                    <span className="text-xs text-slate-600 font-medium">{km.label}</span>
                  </div>
                  <span className="text-xs font-bold text-slate-900">{km.value}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Card 3: Recent Activity */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 tracking-tight">
            Recent Activity
          </h2>

          <div className="space-y-3">
            {recentActivity.map((act, idx) => {
              const Icon = act.icon;
              return (
                <Link
                  key={idx}
                  to={act.link}
                  className="flex items-start gap-3 p-2 rounded-xl hover:bg-slate-50 transition-colors"
                >
                  <div className={`w-8 h-8 rounded-lg ${act.color} flex items-center justify-center shrink-0 mt-0.5`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-semibold text-slate-900">{act.title}</h3>
                    <p className="text-[11px] text-slate-400 mt-0.5">{act.sub}</p>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </div>

      {/* Bottom Download Banner Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900">Download Report</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Get a detailed health report in PDF format
          </p>
        </div>

        <button
          onClick={handleDownload}
          className="flex items-center gap-2 px-5 py-2.5 bg-[#065f46] hover:bg-[#064e3b] text-white text-xs sm:text-sm font-semibold rounded-xl shadow-xs transition-colors cursor-pointer shrink-0"
        >
          <Download className="w-4 h-4" />
          <span>Download</span>
        </button>
      </div>
    </div>
  );
}
