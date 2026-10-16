import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Stethoscope,
  History,
  BotMessageSquare,
  Settings,
  X,
  FileText,
  LogOut,
  HeartPulse,
} from "lucide-react";
import { authService } from "../../services/authService";

export function MobileNavigation({ isOpen, onClose }) {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();

  const handleLogout = () => {
    authService.logout();
    onClose();
    navigate("/login");
  };

  const navItems = [
    { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
    { label: "Symptom Checker", to: "/symptom-checker", icon: Stethoscope },
    { label: "Health History", to: "/history", icon: History },
    { label: "AI Assistant", to: "/assistant", icon: BotMessageSquare },
    { label: "Reports", to: "/reports", icon: FileText },
    { label: "Settings", to: "/settings", icon: Settings },
  ];

  return (
    <>
      {/* Mobile Drawer (Hamburger open state) */}
      {isOpen && (
        <div className="fixed inset-0 z-50 md:hidden flex">
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs"
            onClick={onClose}
          />
          <div className="relative w-72 max-w-[80vw] bg-slate-900 text-white h-full flex flex-col justify-between p-6 shadow-2xl z-10">
            <div>
              <div className="flex items-center justify-between pb-6 border-b border-slate-800">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-teal-600 flex items-center justify-center text-white">
                    <HeartPulse className="w-5 h-5" />
                  </div>
                  <span className="font-bold text-lg text-white">Healix</span>
                </div>
                <button
                  onClick={onClose}
                  className="p-1.5 text-slate-400 hover:text-white rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <nav className="mt-6 space-y-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `flex items-center gap-3 px-3.5 py-3 rounded-xl text-sm font-medium transition-colors ${
                          isActive
                            ? "bg-teal-600 text-white font-semibold"
                            : "text-slate-400 hover:text-white hover:bg-slate-800"
                        }`
                      }
                    >
                      <Icon className="w-5 h-5" />
                      <span>{item.label}</span>
                    </NavLink>
                  );
                })}
              </nav>
            </div>

            <div className="pt-6 border-t border-slate-800">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-teal-700 text-white text-xs font-bold flex items-center justify-center">
                    {user.name ? user.name[0].toUpperCase() : "A"}
                  </div>
                  <div className="truncate">
                    <p className="text-xs font-semibold text-white truncate">{user.fullName || user.name}</p>
                    <p className="text-[10px] text-slate-400 truncate">{user.email}</p>
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-400 hover:text-rose-400"
                  title="Logout"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Sticky Mobile Bar for quick thumbs access */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-slate-200/90 flex items-center justify-around px-2 z-40 shadow-lg">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center py-1 px-3 text-[10px] font-medium transition-colors ${
              isActive ? "text-teal-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`
          }
        >
          <LayoutDashboard className="w-5 h-5 mb-0.5" />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/symptom-checker"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center py-1 px-3 text-[10px] font-medium transition-colors ${
              isActive ? "text-teal-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`
          }
        >
          <div className="relative">
            <Stethoscope className="w-5 h-5 mb-0.5" />
            <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-teal-500"></span>
          </div>
          <span>Check</span>
        </NavLink>

        <NavLink
          to="/assistant"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center py-1 px-3 text-[10px] font-medium transition-colors ${
              isActive ? "text-teal-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`
          }
        >
          <BotMessageSquare className="w-5 h-5 mb-0.5" />
          <span>Assistant</span>
        </NavLink>

        <NavLink
          to="/history"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center py-1 px-3 text-[10px] font-medium transition-colors ${
              isActive ? "text-teal-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`
          }
        >
          <History className="w-5 h-5 mb-0.5" />
          <span>History</span>
        </NavLink>
      </div>
    </>
  );
}
