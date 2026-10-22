import React, { useState } from "react";
import {
  Search,
  Bell,
  Menu,
  Sun,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

function getFormattedDate() {
  return new Date().toLocaleDateString("en-GB", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function Header({ onMobileMenuToggle }) {
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [dateLabel] = useState(getFormattedDate);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/reports?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <>
      <header className="h-16 bg-white border-b border-slate-200/80 px-4 sm:px-8 flex items-center justify-between gap-4 sticky top-0 z-30">
        {/* Mobile menu button + Search bar */}
        <div className="flex items-center gap-3 flex-1 max-w-md">
          <button
            onClick={onMobileMenuToggle}
            className="md:hidden p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors"
            aria-label="Open navigation menu"
          >
            <Menu className="w-5 h-5" />
          </button>

          {/* Search bar matching "Search anything..." */}
          <form onSubmit={handleSearchSubmit} className="relative w-full">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              placeholder="Search anything..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200/90 hover:border-slate-300 focus:border-emerald-600 focus:bg-white text-xs sm:text-sm text-slate-800 placeholder-slate-400 rounded-xl pl-10 pr-4 py-2 transition-all outline-none"
            />
          </form>
        </div>

        {/* Right header items: Bell + Weather widget */}
        <div className="flex items-center gap-4 shrink-0">
          {/* Notifications Bell */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors cursor-pointer relative"
              title="Notifications"
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-emerald-600 ring-2 ring-white"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-slate-200 py-3 z-50">
                <div className="px-4 pb-2 border-b border-slate-100 flex items-center justify-between">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-700">
                    Notifications
                  </span>
                  <span className="text-[11px] text-emerald-700 font-medium cursor-pointer">Mark all read</span>
                </div>
                <div className="divide-y divide-slate-100 max-h-64 overflow-y-auto">
                  <div className="p-3.5 hover:bg-slate-50 transition-colors">
                    <p className="text-xs font-medium text-slate-900">
                      Health Assessment Completed
                    </p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Your summary report is ready with personalized wellness tips.
                    </p>
                    <span className="text-[10px] text-slate-400 mt-1 block">2 hours ago</span>
                  </div>
                  <div className="p-3.5 hover:bg-slate-50 transition-colors">
                    <p className="text-xs font-medium text-slate-900">
                      Hydration & Rest Reminder
                    </p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Keep up your hydration goal! 6 of 8 glasses completed.
                    </p>
                    <span className="text-[10px] text-slate-400 mt-1 block">4 hours ago</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Date & Weather widget */}
          <div className="hidden sm:flex items-center gap-2.5 pl-3 border-l border-slate-200">
            <div className="w-8 h-8 rounded-full bg-amber-50 flex items-center justify-center text-amber-500 shrink-0">
              <Sun className="w-4 h-4 fill-amber-400 text-amber-500" />
            </div>
            <div className="text-right">
              <span className="text-xs font-medium text-slate-900 block leading-tight">
                {dateLabel}
              </span>
              <span className="text-[11px] text-slate-500 block">
                22°C · New Delhi
              </span>
            </div>
          </div>
        </div>
      </header>
    </>
  );
}
