import React from "react";
import { Outlet, Link } from "react-router-dom";
import { ArrowUpRight, ShieldAlert } from "lucide-react";
import { Navbar } from "../components/common/Navbar";
import { HealixLogo } from "../components/common/HealixLogo";

const CURRENT_YEAR = new Date().getFullYear();

export function PublicLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-white font-sans">
      <Navbar />
      <main className="flex-1"><Outlet /></main>
      <div className="border-y border-emerald-100 bg-emerald-50/70 px-5 py-3 text-xs text-emerald-950 sm:px-8">
        <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-2 sm:flex-row sm:items-center">
          <p className="flex items-center gap-2"><ShieldAlert className="h-4 w-4 shrink-0 text-emerald-700" /><span><strong>Health information only.</strong> Healix is not a doctor. In an emergency, contact local emergency services.</span></p>
          <Link to="/symptom-checker" className="shrink-0 font-semibold text-emerald-800 hover:text-emerald-950">Start assessment <ArrowUpRight className="ml-1 inline h-3.5 w-3.5" /></Link>
        </div>
      </div>
      <footer className="bg-white px-5 py-5 sm:px-8">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="flex flex-col items-center gap-1 sm:items-start"><HealixLogo size={29} textClassName="text-base font-bold text-emerald-950" /><span className="text-[10px] text-slate-500">Health. Smarter.</span></div>
          <nav aria-label="Footer navigation" className="flex flex-wrap justify-center gap-x-6 gap-y-2 text-[11px] text-slate-500">
            <Link to="/#overview" className="hover:text-emerald-800">Overview</Link>
            <Link to="/#features" className="hover:text-emerald-800">Features</Link>
            <Link to="/assistant" className="hover:text-emerald-800">AI Assistant</Link>
            <Link to="/#about" className="hover:text-emerald-800">About</Link>
            <Link to="/login" className="hover:text-emerald-800">Log in</Link>
          </nav>
          <p className="text-[10px] text-slate-400">© {CURRENT_YEAR} Healix. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
