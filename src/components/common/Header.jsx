import React, { useState } from "react";
import {
  Search,
  Bell,
  HelpCircle,
  Menu,
  X,
  ShieldAlert,
  ChevronDown,
  Info,
  CheckCircle2,
} from "lucide-react";
import { authService } from "../../services/authService";
import { useNavigate } from "react-router-dom";
import { Modal } from "./Modal";

export function Header({ onMobileMenuToggle }) {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showHelpModal, setShowHelpModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/history?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <>
      <header className="h-16 bg-white border-b border-slate-200/80 px-4 sm:px-8 flex items-center justify-between gap-4 sticky top-0 z-30">
        {/* Mobile menu button + App title */}
        <div className="flex items-center gap-3">
          <button
            onClick={onMobileMenuToggle}
            className="md:hidden p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors"
            aria-label="Open navigation menu"
          >
            <Menu className="w-5 h-5" />
          </button>

          {/* Search bar */}
          <form onSubmit={handleSearchSubmit} className="relative hidden sm:block w-64 lg:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              placeholder="Search symptoms, assessments, or notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 hover:border-slate-300 focus:border-teal-600 focus:bg-white text-xs text-slate-900 rounded-xl pl-9 pr-3.5 py-2 transition-all outline-none"
            />
          </form>
        </div>

        {/* Right action items */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Clinical Safety Indicator */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-200/60 text-teal-800 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
            <span>RAG Medical Grounding Active</span>
          </div>

          {/* Help & Safety guidelines */}
          <button
            onClick={() => setShowHelpModal(true)}
            className="p-2 text-slate-500 hover:text-teal-700 hover:bg-slate-100 rounded-xl transition-colors cursor-pointer relative"
            title="Safety Guidelines & Help"
          >
            <HelpCircle className="w-5 h-5" />
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors cursor-pointer relative"
              title="Notifications"
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-teal-600"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-slate-200 py-3 z-50">
                <div className="px-4 pb-2 border-b border-slate-100 flex items-center justify-between">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-700">
                    Notifications
                  </span>
                  <span className="text-[11px] text-teal-600 font-medium">Mark all read</span>
                </div>
                <div className="divide-y divide-slate-100 max-h-64 overflow-y-auto">
                  <div className="p-3.5 hover:bg-slate-50 transition-colors">
                    <p className="text-xs font-medium text-slate-900">
                      Assessment Completed: Headache & Fatigue
                    </p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Your summary report is ready with 3 curated clinical citations.
                    </p>
                    <span className="text-[10px] text-slate-400 mt-1 block">2 hours ago</span>
                  </div>
                  <div className="p-3.5 hover:bg-slate-50 transition-colors">
                    <p className="text-xs font-medium text-slate-900">
                      Hydration & Rest Reminder
                    </p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Remember to take a 15-minute visual break away from backlit displays.
                    </p>
                    <span className="text-[10px] text-slate-400 mt-1 block">5 hours ago</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="h-6 w-px bg-slate-200 mx-1"></div>

          {/* User quick profile */}
          <div
            onClick={() => navigate("/settings")}
            className="flex items-center gap-2 pl-1 cursor-pointer group"
          >
            <div className="w-8 h-8 rounded-xl bg-slate-900 text-white font-semibold text-xs flex items-center justify-center group-hover:bg-teal-700 transition-colors">
              {user.name ? user.name[0].toUpperCase() : "A"}
            </div>
            <div className="hidden sm:block text-left">
              <span className="text-xs font-semibold text-slate-800 block leading-tight">
                {user.name || "Aakash"}
              </span>
              <span className="text-[11px] text-slate-400 block">Personal Profile</span>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400 hidden sm:block group-hover:text-slate-700 transition-colors" />
          </div>
        </div>
      </header>

      {/* Safety & Help Modal */}
      <Modal
        isOpen={showHelpModal}
        onClose={() => setShowHelpModal(false)}
        title="Healix Clinical Safety & Guidance Principles"
        subtitle="How Healix helps you navigate healthcare safely"
      >
        <div className="space-y-4 text-sm text-slate-600">
          <div className="p-4 bg-teal-50/60 rounded-xl border border-teal-200/70 text-slate-800 flex items-start gap-3">
            <Info className="w-5 h-5 text-teal-700 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-teal-950 text-xs">Our Triage Philosophy</p>
              <p className="text-xs text-teal-900 mt-0.5 leading-relaxed">
                Healix is designed as an educational and triage assistant. It structures your symptoms, flags potential warning indicators, and grounds information in authoritative medical sources (Mayo Clinic, WHO, NHS).
              </p>
            </div>
          </div>

          <div className="space-y-2.5">
            <h4 className="font-semibold text-slate-900 text-xs uppercase tracking-wider">
              Essential Safety Rules:
            </h4>
            <ul className="space-y-2 text-xs">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                <span>
                  <strong>No definitive diagnosis:</strong> Healix never claims that you have a specific illness. Only licensed physicians can provide clinical diagnosis.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                <span>
                  <strong>Immediate emergency priority:</strong> If potential red-flag symptoms (like chest pressure radiating to the arm or acute numbness) are detected, emergency medical instructions take precedence.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                <span>
                  <strong>Data privacy:</strong> Your health history is stored securely and never shared with third-party advertisers.
                </span>
              </li>
            </ul>
          </div>

          <div className="pt-3 border-t border-slate-100 flex justify-end">
            <button
              onClick={() => setShowHelpModal(false)}
              className="px-4 py-2 bg-slate-900 text-white rounded-xl text-xs font-semibold hover:bg-slate-800 transition-colors"
            >
              Understood
            </button>
          </div>
        </div>
      </Modal>
    </>
  );
}
