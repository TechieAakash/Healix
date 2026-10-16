import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/common/Sidebar";
import { Header } from "../components/common/Header";
import { MobileNavigation } from "../components/common/MobileNavigation";
import { ShieldCheck, Lock } from "lucide-react";

export function AppLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Desktop Sidebar */}
      <Sidebar className="hidden md:flex" />

      {/* Mobile Drawer & Bottom Bar */}
      <MobileNavigation
        isOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
      />

      {/* Main App Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header onMobileMenuToggle={() => setMobileMenuOpen(true)} />

        <main className="flex-1 overflow-y-auto pb-20 md:pb-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            <Outlet />
          </div>

          {/* Persistent security reassurance banner in footer */}
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-8 flex items-center justify-between text-xs text-slate-400 border-t border-slate-200/60 mt-8">
            <div className="flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-teal-600" />
              <span>Your health information is private, client-encrypted, and stored securely.</span>
            </div>
            <div className="flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
              <span>Healix v1.0.4 • Clinical Triage Assistant</span>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
