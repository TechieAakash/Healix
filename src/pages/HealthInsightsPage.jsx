import React, { useState } from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { ChevronDown, Calendar, Activity, Moon, Heart, Droplet, Scale } from "lucide-react";

export function HealthInsightsPage() {
  const [timeRange, setTimeRange] = useState("Last 4 Weeks");
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // Weekly steps data
  const activityData = [
    { day: "Mon", steps: 6800 },
    { day: "Tue", steps: 7900 },
    { day: "Wed", steps: 9400 },
    { day: "Thu", steps: 8200 },
    { day: "Fri", steps: 10100 },
    { day: "Sat", steps: 11200 },
    { day: "Sun", steps: 8432 },
  ];

  // Sleep trends data (Sep 10 to Sep 21)
  const sleepData = [
    { date: "Sep 10", hours: 7.2 },
    { date: "Sep 11", hours: 6.8 },
    { date: "Sep 12", hours: 8.0 },
    { date: "Sep 13", hours: 7.5 },
    { date: "Sep 14", hours: 6.9 },
    { date: "Sep 15", hours: 7.8 },
    { date: "Sep 16", hours: 8.2 },
    { date: "Sep 17", hours: 7.4 },
    { date: "Sep 18", hours: 7.9 },
    { date: "Sep 19", hours: 8.1 },
    { date: "Sep 20", hours: 7.6 },
    { date: "Sep 21", hours: 7.7 },
  ];

  // Heart rate trend data
  const heartRateData = [
    { day: "Mon", bpm: 74 },
    { day: "Tue", bpm: 71 },
    { day: "Wed", bpm: 73 },
    { day: "Thu", bpm: 70 },
    { day: "Fri", bpm: 75 },
    { day: "Sat", bpm: 69 },
    { day: "Sun", bpm: 72 },
  ];

  // Oxygen level trend data
  const oxygenData = [
    { day: "Mon", spo2: 98 },
    { day: "Tue", spo2: 98 },
    { day: "Wed", spo2: 99 },
    { day: "Thu", spo2: 97 },
    { day: "Fri", spo2: 98 },
    { day: "Sat", spo2: 99 },
    { day: "Sun", spo2: 98 },
  ];

  // Weight trend data
  const weightData = [
    { week: "W1", weight: 73.2 },
    { week: "W2", weight: 72.8 },
    { week: "W3", weight: 72.4 },
    { week: "W4", weight: 72.0 },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header with Title and Range Picker */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Health Insights
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Track your progress and spot trends over time.
          </p>
        </div>

        {/* Dropdown: Last 4 Weeks */}
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

      {/* Top 2 Cards: Weekly Activity & Sleep Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Weekly Activity */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
                <Activity className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-slate-900">Weekly Activity</h3>
                <p className="text-xs text-slate-400">8,432 steps avg. per day</p>
              </div>
            </div>
          </div>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={activityData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="activityGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#059669" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#059669" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="day" tick={{ fontSize: 11, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 11, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#ffffff", borderRadius: "12px", border: "1px solid #e2e8f0", fontSize: "12px" }}
                  formatter={(val) => [`${val.toLocaleString()} steps`, "Activity"]}
                />
                <Area type="monotone" dataKey="steps" stroke="#059669" strokeWidth={2.5} fillOpacity={1} fill="url(#activityGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sleep Trends */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
                <Moon className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-slate-900">Sleep Trends</h3>
                <p className="text-xs text-slate-400">avg. per night</p>
              </div>
            </div>
          </div>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sleepData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="date" tick={{ fontSize: 10, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 11, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#ffffff", borderRadius: "12px", border: "1px solid #e2e8f0", fontSize: "12px" }}
                  formatter={(val) => [`${val} hrs`, "Sleep"]}
                />
                <Bar dataKey="hours" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Bottom 3 Cards: Heart Rate, Oxygen Level, Weight Trend */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Heart Rate */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <Heart className="w-4 h-4" />
            </div>
            <div>
              <h4 className="text-xs font-medium text-slate-700">Heart Rate</h4>
              <p className="text-sm font-bold text-slate-900">72 bpm <span className="text-[10px] font-normal text-slate-400">avg. resting</span></p>
            </div>
          </div>

          <div className="h-32 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={heartRateData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f8fafc" />
                <XAxis dataKey="day" tick={{ fontSize: 10, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <YAxis domain={[60, 85]} tick={{ fontSize: 10, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#ffffff", borderRadius: "10px", border: "1px solid #e2e8f0", fontSize: "11px" }}
                  formatter={(val) => [`${val} bpm`, "HR"]}
                />
                <Line type="monotone" dataKey="bpm" stroke="#059669" strokeWidth={2} dot={{ r: 3, fill: "#059669" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Oxygen Level */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <Droplet className="w-4 h-4" />
            </div>
            <div>
              <h4 className="text-xs font-medium text-slate-700">Oxygen Level</h4>
              <p className="text-sm font-bold text-slate-900">98% <span className="text-[10px] font-normal text-slate-400">avg. SpO2</span></p>
            </div>
          </div>

          <div className="h-32 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={oxygenData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f8fafc" />
                <XAxis dataKey="day" tick={{ fontSize: 10, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <YAxis domain={[94, 100]} tick={{ fontSize: 10, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#ffffff", borderRadius: "10px", border: "1px solid #e2e8f0", fontSize: "11px" }}
                  formatter={(val) => [`${val}%`, "SpO2"]}
                />
                <Line type="monotone" dataKey="spo2" stroke="#059669" strokeWidth={2} dot={{ r: 3, fill: "#059669" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Weight Trend */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <Scale className="w-4 h-4" />
            </div>
            <div>
              <h4 className="text-xs font-medium text-slate-700">Weight Trend</h4>
              <p className="text-sm font-bold text-slate-900">72 kg <span className="text-[10px] font-normal text-slate-400">current weight</span></p>
            </div>
          </div>

          <div className="h-32 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={weightData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f8fafc" />
                <XAxis dataKey="week" tick={{ fontSize: 10, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <YAxis domain={[70, 75]} tick={{ fontSize: 10, fill: "#94a3b8" }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#ffffff", borderRadius: "10px", border: "1px solid #e2e8f0", fontSize: "11px" }}
                  formatter={(val) => [`${val} kg`, "Weight"]}
                />
                <Line type="monotone" dataKey="weight" stroke="#059669" strokeWidth={2} dot={{ r: 3, fill: "#059669" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
