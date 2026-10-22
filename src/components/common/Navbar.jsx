import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { HealixLogo } from "./HealixLogo";

const links = [
  { label: "Overview", to: "/#overview" },
  { label: "Features", to: "/#features" },
  { label: "AI Assistant", to: "/assistant" },
  { label: "About", to: "/#about" },
];

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-emerald-100/80 bg-white/95 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-5 sm:px-8 lg:px-10">
        <Link to="/" aria-label="Healix home"><HealixLogo size={30} textClassName="text-lg font-bold tracking-tight text-emerald-950" /></Link>
        <nav aria-label="Main navigation" className="hidden items-center gap-7 md:flex">
          {links.map((link, index) => <Link key={link.label} to={link.to} className={`border-b-2 py-[17px] text-[11px] font-medium transition ${index === 0 ? "border-emerald-700 text-emerald-800" : "border-transparent text-slate-500 hover:border-emerald-300 hover:text-emerald-800"}`}>{link.label}</Link>)}
        </nav>
        <div className="hidden items-center gap-2.5 md:flex">
          <Link to="/login" className="rounded-xl border border-emerald-600 px-4 py-2 text-[11px] font-semibold text-emerald-800 transition hover:bg-emerald-50">Log in</Link>
          <Link to="/symptom-checker" className="rounded-xl bg-emerald-700 px-4 py-2 text-[11px] font-semibold text-white transition hover:bg-emerald-800">Get Started</Link>
        </div>
        <button type="button" onClick={() => setMobileMenuOpen((open) => !open)} className="rounded-lg p-2 text-emerald-900 hover:bg-emerald-50 md:hidden" aria-label={mobileMenuOpen ? "Close navigation menu" : "Open navigation menu"} aria-expanded={mobileMenuOpen}>
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>
      {mobileMenuOpen && <nav aria-label="Mobile navigation" className="space-y-1 border-t border-emerald-100 bg-white px-5 py-3 md:hidden">
        {links.map((link) => <Link key={link.label} to={link.to} onClick={() => setMobileMenuOpen(false)} className="block rounded-lg px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-emerald-50 hover:text-emerald-800">{link.label}</Link>)}
        <div className="flex gap-2 border-t border-emerald-50 pt-3">
          <Link to="/login" onClick={() => setMobileMenuOpen(false)} className="flex-1 rounded-lg border border-emerald-600 px-3 py-2.5 text-center text-sm font-semibold text-emerald-800">Log in</Link>
          <Link to="/symptom-checker" onClick={() => setMobileMenuOpen(false)} className="flex-1 rounded-lg bg-emerald-700 px-3 py-2.5 text-center text-sm font-semibold text-white">Get Started</Link>
        </div>
      </nav>}
    </header>
  );
}
