import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  Home,
  ClipboardList,
  MessageSquare,
  FileBarChart2,
  HeartPulse,
  Settings,
  X,
  LogOut,
  ChevronRight,
  Stethoscope,
} from "lucide-react";
import { authService } from "../../services/authService";
import { HealixLogo } from "./HealixLogo";

export function MobileNavigation({ isOpen, onClose }) {
  const navigate = useNavigate();
  const user = authService.getCurrentUser() || {};

  const handleLogout = () => {
    authService.logout();
    onClose();
    navigate("/login");
  };

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
    <>
      {/* Mobile Drawer */}
      {isOpen && (
        <div className="fixed inset-0 z-50 md:hidden flex">
          <div
            className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs"
            onClick={onClose}
          />
          <div className="relative w-72 max-w-[80vw] bg-white text-slate-800 h-full flex flex-col justify-between p-6 shadow-2xl z-10">
            <div>
              <div className="flex items-center justify-between pb-5 border-b border-slate-100">
                <HealixLogo size={28} />
                <button
                  onClick={onClose}
                  className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <nav className="mt-5 space-y-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                          isActive
                            ? "bg-emerald-50 text-emerald-800 font-semibold"
                            : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                        }`
                      }
                    >
                      <Icon className="w-4 h-4 shrink-0" />
                      <span>{item.label}</span>
                    </NavLink>
                  );
                })}
              </nav>
            </div>

            <div className="pt-4 border-t border-slate-100">
              <div
                onClick={() => {
                  onClose();
                  navigate("/settings");
                }}
                className="flex items-center justify-between p-2 rounded-xl hover:bg-slate-50 cursor-pointer"
              >
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-emerald-800 text-white font-bold text-xs flex items-center justify-center">
                    {user?.avatarInitials || "KA"}
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-slate-900">
                      {user?.fullName || "Krish Alagh"}
                    </p>
                    <p className="text-[10px] text-slate-400">View Profile</p>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-400" />
              </div>

              <button
                type="button"
                onClick={handleLogout}
                className="w-full mt-2 flex items-center justify-center gap-2 p-2 text-xs font-semibold text-red-600 hover:bg-red-50 rounded-xl transition-colors cursor-pointer"
              >
                <LogOut className="w-4 h-4" />
                Sign Out
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Bottom Navigation Bar */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200/80 px-2 py-2 flex items-center justify-around z-30 shadow-lg">
        {navItems.slice(0, 5).map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex flex-col items-center gap-1 py-1 px-2 rounded-lg text-[10px] font-medium transition-colors ${
                  isActive ? "text-emerald-700 font-semibold" : "text-slate-400 hover:text-slate-700"
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label.split(" ")[0]}</span>
            </NavLink>
          );
        })}
      </div>
    </>
  );
}
