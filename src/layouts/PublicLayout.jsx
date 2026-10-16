import React from "react";
import { Outlet, Link } from "react-router-dom";
import { Navbar } from "../components/common/Navbar";
import { HeartPulse, ShieldAlert, ArrowUpRight } from "lucide-react";

export function PublicLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 font-sans">
      <Navbar />

      <main className="flex-1">
        <Outlet />
      </main>

      {/* Safety Notice Banner */}
      <div className="bg-slate-900 text-slate-300 py-6 px-4 border-t border-slate-800">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
          <div className="flex items-center gap-3">
            <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0" />
            <p className="leading-relaxed">
              <strong>Medical Disclaimer:</strong> Healix is an artificial intelligence-driven health information and triage guidance assistant. It is <u>not</u> a doctor and does not provide formal medical diagnosis or treatment plans. In any emergency, immediately contact your local emergency services (e.g. 911 / 112).
            </p>
          </div>
          <Link
            to="/symptom-checker"
            className="shrink-0 text-teal-400 hover:text-teal-300 font-medium flex items-center gap-1"
          >
            Start Assessment <ArrowUpRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-slate-950 text-slate-400 py-12 px-4 sm:px-6 lg:px-8 border-t border-slate-900">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-teal-600 flex items-center justify-center text-white">
                <HeartPulse className="w-5 h-5" />
              </div>
              <span className="font-bold text-lg text-white">Healix</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Understand your health. Take the next step. Bringing clarity and safety to symptom navigation with AI and clinical RAG.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-3">
              Platform
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/symptom-checker" className="hover:text-white transition-colors">
                  Symptom Checker
                </Link>
              </li>
              <li>
                <Link to="/assistant" className="hover:text-white transition-colors">
                  AI Healthcare Assistant
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="hover:text-white transition-colors">
                  Patient Dashboard
                </Link>
              </li>
              <li>
                <Link to="/history" className="hover:text-white transition-colors">
                  Health History Log
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-3">
              Clinical Quality & Safety
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <a href="#safety" className="hover:text-white transition-colors">
                  Red-Flag Triage Engine
                </a>
              </li>
              <li>
                <a href="#sources" className="hover:text-white transition-colors">
                  Medical Grounding Sources
                </a>
              </li>
              <li>
                <a href="#privacy" className="hover:text-white transition-colors">
                  HIPAA & Privacy Standards
                </a>
              </li>
              <li>
                <a href="#disclaimer" className="hover:text-white transition-colors">
                  Clinical Disclaimer
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-3">
              Account & Support
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/login" className="hover:text-white transition-colors">
                  Sign In
                </Link>
              </li>
              <li>
                <Link to="/signup" className="hover:text-white transition-colors">
                  Create Free Account
                </Link>
              </li>
              <li>
                <Link to="/settings" className="hover:text-white transition-colors">
                  Settings & Preferences
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="max-w-7xl mx-auto pt-8 mt-8 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} Healix Health Technologies. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <span className="hover:text-slate-400 cursor-pointer">Privacy Policy</span>
            <span className="hover:text-slate-400 cursor-pointer">Terms of Service</span>
            <span className="hover:text-slate-400 cursor-pointer">Security Practices</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
