import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Stethoscope,
  History,
  BotMessageSquare,
  FileText,
  Settings,
  LogOut,
  ShieldCheck,
  Activity,
  HeartPulse,
} from "lucide-react";
import { authService } from "../../services/authService";

export function Sidebar({ className = "" }) {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();

  const handleLogout = () => {
    authService.logout();
    navigate("/login");
  };

  const navItems = [
    { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
    { label: "Symptom Checker", to: "/symptom-checker", icon: Stethoscope, badge: "AI" },
    { label: "Health History", to: "/history", icon: History },
    { label: "AI Assistant", to: "/assistant", icon: BotMessageSquare },
    { label: "Reports", to: "/reports", icon: FileText },
    { label: "Settings", to: "/settings", icon: Settings },
  ];

  return (
    <aside
      className={`w-64 bg-slate-900 text-slate-300 flex flex-col justify-between shrink-0 select-none border-r border-slate-800 ${className}`}
    >
      {/* Brand Header */}
      <div>
        <div className="p-6 pb-5 flex items-center justify-between border-b border-slate-800/80">
          <NavLink to="/dashboard" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20 group-hover:bg-teal-500 transition-colors">
              <HeartPulse className="w-6 h-6" />
            </div>
            <div>
              <span className="font-bold text-lg text-white tracking-tight flex items-center gap-1.5">
                Healix
                <span className="text-[10px] uppercase font-semibold tracking-wider px-1.5 py-0.5 rounded bg-teal-950 text-teal-400 border border-teal-800">
                  AI Triage
                </span>
              </span>
              <p className="text-[11px] text-slate-400 -mt-0.5">Clinical Intelligence</p>
            </div>
          </NavLink>
        </div>

        {/* Navigation Links */}
        <nav className="p-4 space-y-1.5 mt-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? "bg-teal-600 text-white font-semibold shadow-sm shadow-teal-600/30"
                      : "text-slate-400 hover:text-white hover:bg-slate-800/70"
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-5 h-5 shrink-0" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-teal-500/20 text-teal-300">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Safety Notice & User Profile */}
      <div className="p-4 border-t border-slate-800/80 space-y-4">
        {/* Safety Disclaimer Widget */}
        <div className="p-3 bg-slate-800/60 rounded-xl border border-slate-800 text-[11px] text-slate-400 leading-relaxed flex items-start gap-2.5">
          <ShieldCheck className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
          <span>
            <strong className="text-slate-200">Not a doctor:</strong> Healix offers triage information, not clinical diagnosis.
          </span>
        </div>

        {/* User Card */}
        <div className="flex items-center justify-between pt-2">
          <div
            onClick={() => navigate("/settings")}
            className="flex items-center gap-3 min-w-0 cursor-pointer group"
          >
            <div className="w-9 h-9 rounded-xl bg-teal-700 text-white font-bold flex items-center justify-center shrink-0 border border-teal-500/30 group-hover:ring-2 group-hover:ring-teal-400 transition-all">
              {user.name ? user.name[0].toUpperCase() : "A"}
            </div>
            <div className="truncate">
              <p className="text-sm font-medium text-white truncate group-hover:text-teal-300 transition-colors">
                {user.fullName || user.name || "Aakash"}
              </p>
              <p className="text-xs text-slate-400 truncate">{user.email || "aakash@example.com"}</p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            title="Log out"
            className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-xl transition-colors cursor-pointer"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
