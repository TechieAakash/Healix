import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  HeartPulse,
  ArrowRight,
  ShieldCheck,
  Sparkles,
  Stethoscope,
  HelpCircle,
  AlertTriangle,
  BookOpen,
  Activity,
  CheckCircle2,
  Clock,
  Lock,
  ChevronRight,
  FileCheck,
  Send,
} from "lucide-react";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { UrgencyIndicator } from "../components/common/UrgencyIndicator";
import { motion } from "framer-motion";

export function LandingPage() {
  const navigate = useNavigate();
  const [heroInput, setHeroInput] = useState("Headache and persistent fatigue after long computer work");

  const handleQuickCheck = (e) => {
    e.preventDefault();
    navigate(`/symptom-checker?initial=${encodeURIComponent(heroInput)}`);
  };

  const features = [
    {
      icon: Stethoscope,
      title: "AI Symptom Analysis",
      description:
        "Describe your symptoms in natural language. Our clinical reasoning engine organizes patterns without making premature assumptions.",
    },
    {
      icon: HelpCircle,
      title: "Smart Follow-up Questions",
      description:
        "Dynamic, context-aware inquiries refine symptom duration, severity, and location—mirroring a medical intake interview.",
    },
    {
      icon: AlertTriangle,
      title: "Safety-First Triage",
      description:
        "Continuous red-flag monitoring prioritizes genuine emergencies, directing you to immediate emergency care when warning signs appear.",
    },
    {
      icon: BookOpen,
      title: "Evidence-Grounded Information",
      description:
        "Every health insight is anchored in peer-reviewed clinical knowledge bases (Mayo Clinic, WHO, NHS) with transparent citations.",
    },
  ];

  const workflowSteps = [
    {
      step: "01",
      title: "Describe your symptoms",
      desc: "Speak or type in everyday plain language. Add structured symptoms like headache, fever, or fatigue with one tap.",
    },
    {
      step: "02",
      title: "Answer a few questions",
      desc: "Clarify timeline, severity, and specific body zones through a simple, guided conversational questionnaire.",
    },
    {
      step: "03",
      title: "Healix analyzes relevant information",
      desc: "Our RAG engine cross-references clinical literature to synthesize potential factors and rule out red flags.",
    },
    {
      step: "04",
      title: "Review your next-step guidance",
      desc: "Receive clear, responsible urgency recommendations: self-care tips, warning signs to monitor, and printable doctor reports.",
    },
  ];

  return (
    <div className="space-y-24 pb-16">
      {/* ================= HERO SECTION ================= */}
      <section className="relative pt-12 sm:pt-20 lg:pt-28 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Subtle decorative glow */}
        <div className="absolute top-10 left-1/2 -translate-x-1/2 w-96 h-96 bg-teal-200/20 blur-3xl rounded-full pointer-events-none -z-10" />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          {/* Left Column: Headlines & CTAs */}
          <div className="lg:col-span-6 space-y-6 text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-teal-50 border border-teal-200/80 text-teal-800 text-xs font-semibold">
              <ShieldCheck className="w-4 h-4 text-teal-600" />
              <span>Evidence-Grounded AI Health Triage</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.1]">
              Understand your symptoms. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-700 via-teal-600 to-slate-900">
                Know your next step.
              </span>
            </h1>

            <p className="text-base sm:text-lg text-slate-600 max-w-xl mx-auto lg:mx-0 leading-relaxed">
              An AI-powered health assistant that helps you understand symptoms, identify warning signs, and find reliable health information—supporting, not replacing, professional care.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <Link to="/symptom-checker" className="w-full sm:w-auto">
                <Button
                  variant="teal"
                  size="lg"
                  className="w-full sm:w-auto"
                  icon={ArrowRight}
                  iconPosition="right"
                >
                  Check My Symptoms
                </Button>
              </Link>
              <Link to="/assistant" className="w-full sm:w-auto">
                <Button variant="outline" size="lg" className="w-full sm:w-auto">
                  Explore Healix Assistant
                </Button>
              </Link>
            </div>

            <div className="pt-6 flex flex-wrap items-center justify-center lg:justify-start gap-6 text-xs text-slate-500">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Zero diagnostic claims</span>
              </div>
              <div className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-teal-600" />
                <span>Private & Encrypted</span>
              </div>
              <div className="flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-slate-700" />
                <span>Curated medical citations</span>
              </div>
            </div>
          </div>

          {/* Right Column: Hero Visual Card (Polished interactive preview) */}
          <div className="lg:col-span-6">
            <div className="relative bg-white rounded-3xl border border-slate-200 shadow-xl p-6 sm:p-8 space-y-6">
              {/* Card top bar */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                <div className="flex items-center gap-2.5">
                  <div className="w-3 h-3 rounded-full bg-rose-400" />
                  <div className="w-3 h-3 rounded-full bg-amber-400" />
                  <div className="w-3 h-3 rounded-full bg-emerald-400" />
                  <span className="text-xs font-semibold text-slate-500 ml-2">
                    Live Symptom Assessment Preview
                  </span>
                </div>
                <Badge variant="teal" dot>
                  Safety Engine Online
                </Badge>
              </div>

              {/* Symptom input preview */}
              <form onSubmit={handleQuickCheck} className="space-y-2">
                <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider block">
                  Describe what you're experiencing:
                </label>
                <div className="flex items-center gap-2 bg-slate-50 rounded-2xl border border-slate-200 p-2 focus-within:border-teal-600 focus-within:bg-white transition-all">
                  <input
                    type="text"
                    value={heroInput}
                    onChange={(e) => setHeroInput(e.target.value)}
                    className="flex-1 bg-transparent px-3 text-sm text-slate-800 outline-none"
                    placeholder="E.g., headache since yesterday and dry cough"
                  />
                  <Button variant="teal" size="sm" type="submit" icon={Send}>
                    Analyze
                  </Button>
                </div>
              </form>

              {/* AI Processing indicator simulation */}
              <div className="bg-slate-50/80 rounded-2xl p-4 border border-slate-200/80 flex items-center justify-between text-xs">
                <div className="flex items-center gap-3">
                  <span className="w-2.5 h-2.5 rounded-full bg-teal-600 animate-ping" />
                  <span className="text-slate-700 font-medium">
                    AI Triage: Cross-referencing clinical sources (Mayo Clinic / WHO)
                  </span>
                </div>
                <span className="text-teal-700 font-semibold">Active RAG</span>
              </div>

              {/* Urgency indicator preview */}
              <UrgencyIndicator
                level="routine"
                title="Routine Care Recommended"
                description="Reported indicators align with non-urgent postural strain. Hydration and screen-break hygiene suggested."
                compact={false}
              />

              {/* Health insight card */}
              <div className="p-4 rounded-2xl bg-teal-50/60 border border-teal-200/70 flex items-start gap-3">
                <Sparkles className="w-5 h-5 text-teal-700 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-xs font-bold text-teal-950 uppercase tracking-wider">
                    Evidence-Grounded Observation
                  </h4>
                  <p className="text-xs text-teal-900 mt-1 leading-relaxed">
                    "Tension-type headaches and eye strain often correlate with sustained cervical posture. Discuss persistent symptoms with your doctor."
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ================= FEATURE SECTION ================= */}
      <section id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <Badge variant="teal">Capabilities</Badge>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Your health, understood.
          </h2>
          <p className="text-base text-slate-600 leading-relaxed">
            Healix transforms ambiguous discomfort into structured, reliable clinical information with zero guesswork and strict medical boundaries.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feat) => {
            const Icon = feat.icon;
            return (
              <div
                key={feat.title}
                className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xs hover:shadow-md hover:border-slate-300 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="w-12 h-12 rounded-2xl bg-teal-50 text-teal-700 flex items-center justify-center mb-5 border border-teal-100">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-base font-bold text-slate-900 mb-2">
                    {feat.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    {feat.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ================= HOW IT WORKS ================= */}
      <section id="how-it-works" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-900 rounded-3xl text-white p-8 sm:p-12 lg:p-16 relative overflow-hidden">
          <div className="text-center max-w-2xl mx-auto space-y-3 mb-12">
            <span className="text-xs uppercase font-bold tracking-wider text-teal-400">
              Clear 4-Step Process
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              How Healix Works
            </h2>
            <p className="text-sm text-slate-400">
              From first symptom to clear clinical next steps in under 3 minutes.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 relative z-10">
            {workflowSteps.map((step) => (
              <div
                key={step.step}
                className="bg-slate-800/80 rounded-2xl p-6 border border-slate-700/80 flex flex-col justify-between"
              >
                <div>
                  <span className="text-2xl font-black text-teal-400 font-mono">
                    {step.step}
                  </span>
                  <h3 className="text-base font-bold text-white mt-3 mb-2">
                    {step.title}
                  </h3>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {step.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 text-center">
            <Link to="/symptom-checker">
              <Button variant="teal" size="lg" icon={ArrowRight} iconPosition="right">
                Start Your Free Symptom Check
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* ================= BUILT WITH SAFETY IN MIND ================= */}
      <section id="safety" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-teal-50/70 rounded-3xl border border-teal-200/90 p-8 sm:p-12">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-7 space-y-4">
              <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-teal-800">
                <ShieldCheck className="w-5 h-5 text-teal-600" />
                <span>Safety & Clinical Responsibility</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                Built with safety in mind. Not a doctor.
              </h2>
              <p className="text-sm text-slate-700 leading-relaxed">
                Healix provides health information and triage support, not medical diagnosis. We believe AI in healthcare should be a collaborative bridge between patients and clinicians, not an overconfident diagnostic tool.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div className="p-4 bg-white rounded-2xl border border-teal-100 shadow-2xs">
                  <h4 className="text-xs font-bold text-slate-900 uppercase">
                    Red-Flag Interception
                  </h4>
                  <p className="text-xs text-slate-600 mt-1">
                    Cardiopulmonary and acute neurological cues instantly trigger emergency priority screens with direct hotlines.
                  </p>
                </div>
                <div className="p-4 bg-white rounded-2xl border border-teal-100 shadow-2xs">
                  <h4 className="text-xs font-bold text-slate-900 uppercase">
                    Zero Hallucination Tolerance
                  </h4>
                  <p className="text-xs text-slate-600 mt-1">
                    Guidance is restricted to verified clinical sources like Mayo Clinic, NHS, and WHO guidelines.
                  </p>
                </div>
              </div>
            </div>

            <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-teal-200 shadow-sm space-y-4">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                Clinical Safety Checklist
              </h3>
              <ul className="space-y-3 text-xs text-slate-600">
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>Always phrases conditions as "possibilities to discuss with a doctor"</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>Provides printable doctor summaries formatted for appointments</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>Never hides emergency guidance behind registration or paywalls</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>End-to-end encrypted health history with full deletion control</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
