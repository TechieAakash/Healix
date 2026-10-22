import React, { useState } from "react";
import {
  CheckCircle2,
  Circle,
  Plus,
  ChevronRight,
  Moon,
  Dumbbell,
  Heart,
  Apple,
} from "lucide-react";

export function CarePlanPage() {
  const [tasks, setTasks] = useState([
    {
      id: "t1",
      title: "Take your morning walk (20-25 mins)",
      sub: "Aim for 30 mins, brisk walk",
      completed: true,
    },
    {
      id: "t2",
      title: "Stay hydrated",
      sub: "Aim for 8-10 glasses of water",
      completed: false,
    },
    {
      id: "t3",
      title: "Follow healthy diet",
      sub: "Include fruits, vegetables, and whole grains",
      completed: false,
    },
    {
      id: "t4",
      title: "Get 7-8 hours of sleep",
      sub: "Maintain your sleep schedule",
      completed: false,
    },
  ]);

  const [recommendations] = useState([
    {
      id: "r1",
      title: "Improve Sleep Quality",
      sub: "Based on your sleep pattern",
      icon: Moon,
    },
    {
      id: "r2",
      title: "Build Strength & Endurance",
      sub: "Based on your activity data",
      icon: Dumbbell,
    },
    {
      id: "r3",
      title: "Manage Stress",
      sub: "Personalized breathing exercises",
      icon: Heart,
    },
    {
      id: "r4",
      title: "Healthy Eating Plan",
      sub: "Simple, sustainable meal ideas",
      icon: Apple,
    },
  ]);

  const [showNewPlanModal, setShowNewPlanModal] = useState(false);
  const [newPlanTitle, setNewPlanTitle] = useState("");
  const [newPlanSub, setNewPlanSub] = useState("");

  const toggleTask = (id) => {
    setTasks(
      tasks.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t))
    );
  };

  const handleAddNewPlan = (e) => {
    e.preventDefault();
    if (!newPlanTitle.trim()) return;
    setTasks([
      ...tasks,
      {
        id: `t_${Date.now()}`,
        title: newPlanTitle.trim(),
        sub: newPlanSub.trim() || "Daily wellness objective",
        completed: false,
      },
    ]);
    setNewPlanTitle("");
    setNewPlanSub("");
    setShowNewPlanModal(false);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Your Care Plan
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Personalized recommendations for your well-being.
          </p>
        </div>

        {/* [+ New Plan] Button */}
        <button
          onClick={() => setShowNewPlanModal(true)}
          className="flex items-center gap-1.5 px-4 py-2 bg-[#065f46] hover:bg-[#064e3b] text-white text-xs sm:text-sm font-semibold rounded-xl shadow-xs transition-colors cursor-pointer self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>New Plan</span>
        </button>
      </div>

      {/* Two Columns Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Today's Plan */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 tracking-tight">
            Today's Plan
          </h2>

          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                onClick={() => toggleTask(task.id)}
                className={`p-4 rounded-xl border transition-all cursor-pointer flex items-start gap-3.5 select-none ${
                  task.completed
                    ? "bg-[#f0fdf4] border-emerald-200 text-slate-800"
                    : "bg-white border-slate-200/80 hover:border-slate-300 text-slate-900"
                }`}
              >
                <div className="mt-0.5 shrink-0">
                  {task.completed ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-600 fill-emerald-100" />
                  ) : (
                    <Circle className="w-5 h-5 text-slate-300 hover:text-slate-400" />
                  )}
                </div>
                <div className="min-w-0">
                  <p
                    className={`text-xs sm:text-sm font-semibold ${
                      task.completed ? "line-through text-slate-500" : "text-slate-900"
                    }`}
                  >
                    {task.title}
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">{task.sub}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Recommended for You */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 tracking-tight">
            Recommended for You
          </h2>

          <div className="space-y-3">
            {recommendations.map((rec) => {
              const Icon = rec.icon;
              return (
                <div
                  key={rec.id}
                  className="p-4 rounded-xl border border-slate-200/80 hover:border-emerald-600/50 hover:bg-emerald-50/20 transition-all cursor-pointer flex items-center justify-between group"
                >
                  <div className="flex items-center gap-3.5 min-w-0">
                    <div className="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0 group-hover:bg-emerald-800 group-hover:text-white transition-colors">
                      <Icon className="w-4 h-4" />
                    </div>
                    <div className="truncate">
                      <p className="text-xs sm:text-sm font-semibold text-slate-900 group-hover:text-emerald-950 transition-colors truncate">
                        {rec.title}
                      </p>
                      <p className="text-xs text-slate-400 mt-0.5 truncate">{rec.sub}</p>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-700 transition-transform group-hover:translate-x-0.5 shrink-0 ml-2" />
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Modal: New Plan */}
      {showNewPlanModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-200 animate-in fade-in zoom-in-95">
            <h3 className="text-sm font-bold text-slate-900 mb-1">Add to Care Plan</h3>
            <p className="text-xs text-slate-500 mb-4">Set a custom goal or healthy habit</p>

            <form onSubmit={handleAddNewPlan} className="space-y-3.5">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Activity or Habit</label>
                <input
                  type="text"
                  value={newPlanTitle}
                  onChange={(e) => setNewPlanTitle(e.target.value)}
                  placeholder="e.g. 10 minutes evening mindfulness"
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Target or Frequency</label>
                <input
                  type="text"
                  value={newPlanSub}
                  onChange={(e) => setNewPlanSub(e.target.value)}
                  placeholder="e.g. Daily after dinner"
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowNewPlanModal(false)}
                  className="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-medium bg-[#065f46] hover:bg-[#064e3b] text-white rounded-xl shadow-xs"
                >
                  Add Plan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
