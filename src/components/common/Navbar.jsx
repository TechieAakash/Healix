import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { HeartPulse, Menu, X, ArrowRight, ShieldCheck } from "lucide-react";
import { Button } from "./Button";

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20 group-hover:bg-teal-500 transition-colors">
            <HeartPulse className="w-6 h-6" />
          </div>
          <div>
            <span className="font-bold text-xl text-slate-900 tracking-tight flex items-center gap-1.5">
              Healix
            </span>
            <p className="text-[11px] text-slate-500 font-medium">
              Understand your health. Take the next step.
            </p>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-8">
          <a
            href="#features"
            className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
          >
            Capabilities
          </a>
          <a
            href="#how-it-works"
            className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
          >
            How It Works
          </a>
          <a
            href="#safety"
            className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors flex items-center gap-1.5"
          >
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            Safety First
          </a>
        </nav>

        {/* CTA Buttons */}
        <div className="hidden md:flex items-center gap-3">
          <Link to="/login">
            <Button variant="ghost" size="sm">
              Sign In
            </Button>
          </Link>
          <Link to="/symptom-checker">
            <Button variant="teal" size="sm" icon={ArrowRight} iconPosition="right">
              Check My Symptoms
            </Button>
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 text-slate-600 hover:text-slate-900 rounded-xl"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile menu dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-b border-slate-200 px-4 pt-2 pb-6 space-y-3">
          <a
            href="#features"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-medium text-slate-700 hover:text-teal-600"
          >
            Capabilities
          </a>
          <a
            href="#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-medium text-slate-700 hover:text-teal-600"
          >
            How It Works
          </a>
          <a
            href="#safety"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-medium text-slate-700 hover:text-teal-600"
          >
            Safety First
          </a>
          <div className="pt-4 border-t border-slate-100 flex flex-col gap-2">
            <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="outline" className="w-full">
                Sign In
              </Button>
            </Link>
            <Link to="/symptom-checker" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="teal" className="w-full">
                Check My Symptoms
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
