import React, { useState } from "react";
import { Outlet, Navigate } from "react-router-dom";
import { Sidebar } from "../components/common/Sidebar";
import { Header } from "../components/common/Header";
import { MobileNavigation } from "../components/common/MobileNavigation";
import { authService } from "../services/authService";

export function AppLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Synchronously redirect unauthenticated users without blank screen
  if (!authService.isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex h-screen bg-[#f8fafc] overflow-hidden font-sans">
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

        <main className="flex-1 overflow-y-auto pb-16 md:pb-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
