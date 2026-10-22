import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  Home,
  ClipboardList,
  MessageSquare,
  FileBarChart2,
  HeartPulse,
  Settings,
  ChevronRight,
  Stethoscope,
} from "lucide-react";
import { authService } from "../../services/authService";
import { HealixLogo } from "./HealixLogo";

export function Sidebar({ className = "" }) {
  const navigate = useNavigate();
  const user = authService.getCurrentUser() || {};

  const navItems = [
    { label: "Overview", to: "/dashboard", icon: Home },
    { label: "Symptom Checker", to: "/symptom-checker", icon: Stethoscope },
    { label: "Health Assessment", to: "/assessment", icon: ClipboardList },
    { label: "AI Assistant", to: "/assistant", icon: MessageSquare },
    { label: "Reports", to: "/reports", icon: FileBarChart2 },
    { label: "Care Plan", to: "/care-plan", icon: HeartPulse },
    { label: "Settings", to: "/settings", icon: Settings },
  ];

  return (
    <aside
      className={`w-64 bg-white text-slate-700 flex flex-col justify-between shrink-0 select-none border-r border-slate-200/80 shadow-[1px_0_4px_rgba(0,0,0,0.02)] ${className}`}
    >
      {/* Brand Header */}
      <div>
        <div className="p-6 pb-6 flex items-center justify-between">
          <NavLink to="/dashboard" className="flex items-center gap-2 group">
            <HealixLogo size={32} textClassName="text-xl font-bold text-emerald-950 tracking-tight" />
          </NavLink>
        </div>

        {/* Navigation Links */}
        <nav className="px-3.5 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-emerald-50 text-emerald-800 font-semibold"
                      : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon className={`w-4 h-4 shrink-0 ${isActive ? "text-emerald-700" : "text-slate-500"}`} />
                    <span>{item.label}</span>
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* User Profile Pill at Bottom */}
      <div className="p-4 border-t border-slate-100">
        <div
          onClick={() => navigate("/settings")}
          className="flex items-center justify-between p-2 rounded-xl hover:bg-slate-50 cursor-pointer transition-colors group"
        >
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-9 h-9 rounded-full bg-emerald-800 text-white font-semibold text-xs flex items-center justify-center shrink-0 shadow-xs">
              {user.avatarInitials || (user.fullName ? user.fullName.split(" ").map(n => n[0]).join("") : "??")}
            </div>
            <div className="truncate text-left">
              <p className="text-sm font-medium text-slate-900 truncate">
                {user.fullName || user.name || "Krish Alagh"}
              </p>
              <p className="text-[11px] text-slate-400 truncate">View Profile</p>
            </div>
          </div>
          <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-600 transition-colors shrink-0" />
        </div>
      </div>
    </aside>
  );
}
