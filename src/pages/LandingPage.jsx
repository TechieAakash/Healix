import React from "react";
import { Link } from "react-router-dom";
import {
  Activity,
  ArrowRight,
  Brain,
  CheckCircle2,
  ClipboardList,
  Heart,
  MessageCircle,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  Users,
  Zap,
} from "lucide-react";
import { HealixLogo } from "../components/common/HealixLogo";

const features = [
  {
    icon: MessageCircle,
    title: "AI Health Assistant",
    description: "Get answers to health questions and practical guidance, available whenever you need it.",
    to: "/assistant",
  },
  {
    icon: ClipboardList,
    title: "Health Assessment",
    description: "Check your symptoms with a guided intake and clear, safety-first next steps.",
    to: "/symptom-checker",
  },
  {
    icon: TrendingUp,
    title: "Health Insights",
    description: "See patterns in your health information and follow changes over time.",
    to: "/insights",
  },
  {
    icon: Heart,
    title: "Personalized Care Plans",
    description: "Build healthier routines with suggestions shaped around your goals and habits.",
    to: "/care-plan",
  },
];

function DashboardPreview() {
  return (
    <div className="relative mx-auto w-full max-w-[650px]">
      <div className="absolute -inset-8 rounded-[3rem] bg-emerald-200/50 blur-3xl" />
      <div className="absolute -left-8 top-12 hidden h-56 w-24 -rotate-12 rounded-full bg-emerald-100/90 blur-xl lg:block" />
      <div className="relative overflow-hidden rounded-2xl border border-emerald-100 bg-white/95 p-2 shadow-[0_28px_80px_-28px_rgba(5,100,75,0.35)] sm:p-3">
        <div className="flex items-center gap-1.5 border-b border-emerald-50 px-2 pb-2">
          <span className="h-2 w-2 rounded-full bg-rose-400" />
          <span className="h-2 w-2 rounded-full bg-amber-400" />
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          <span className="ml-2 text-[10px] font-medium text-slate-400">Healix · Health overview</span>
        </div>
        <div className="grid min-h-[320px] grid-cols-[112px_1fr] sm:grid-cols-[138px_1fr]">
          <aside className="flex flex-col border-r border-emerald-50 px-2 py-3 sm:px-3">
            <HealixLogo size={22} textClassName="text-sm font-bold text-emerald-950" />
            <div className="mt-5 space-y-1 text-[10px] font-medium text-slate-500">
              <div className="rounded-lg bg-emerald-50 px-2 py-2 text-emerald-800"><Activity className="mr-1 inline h-3 w-3" /> Overview</div>
              <div className="px-2 py-2"><ClipboardList className="mr-1 inline h-3 w-3" /> Assessment</div>
              <div className="px-2 py-2"><MessageCircle className="mr-1 inline h-3 w-3" /> Assistant</div>
              <div className="px-2 py-2"><Heart className="mr-1 inline h-3 w-3" /> Care plan</div>
            </div>
            <div className="mt-auto rounded-lg bg-emerald-50/80 p-2 text-[9px] text-emerald-900">
              <span className="font-semibold">Your health, in focus</span><br />Private and personal
            </div>
          </aside>
          <div className="min-w-0 p-3 sm:p-4">
            <div className="flex items-start justify-between gap-2">
              <div><p className="text-[9px] font-medium text-slate-400">YOUR OVERVIEW</p><h2 className="mt-1 text-sm font-bold text-slate-900 sm:text-base">A clearer view of your health</h2></div>
              <span className="rounded-full bg-emerald-50 px-2 py-1 text-[9px] text-emerald-800">Today</span>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4">
              {[[Heart, "Heart rate", "72 bpm"], [Activity, "SpO₂", "98%"], [Zap, "Sleep", "7h 42m"], [TrendingUp, "Steps", "8,432"]].map(([Icon, label, value]) => (
                <div key={label} className="rounded-xl border border-emerald-100/90 bg-white p-2 sm:p-2.5">
                  <Icon className="h-3.5 w-3.5 text-emerald-700" />
                  <p className="mt-2 text-[9px] text-slate-400">{label}</p>
                  <p className="text-xs font-bold text-slate-800 sm:text-sm">{value}</p>
                </div>
              ))}
            </div>
            <Link to="/assistant" className="mt-3 flex items-center justify-between gap-3 rounded-xl bg-gradient-to-r from-emerald-50 to-teal-50 p-3 transition hover:from-emerald-100 hover:to-teal-100">
              <div className="flex items-center gap-2"><span className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-emerald-700"><Brain className="h-4 w-4" /></span><div><p className="text-[10px] font-bold text-slate-800">Health Assistant</p><p className="text-[9px] text-slate-500">Ask a question or explore guidance</p></div></div>
              <span className="rounded-full bg-emerald-700 px-2.5 py-1 text-[9px] font-semibold text-white">Chat now <ArrowRight className="ml-1 inline h-3 w-3" /></span>
            </Link>
            <div className="mt-3 rounded-xl border border-emerald-100/90 p-3">
              <div className="flex items-center justify-between"><div><p className="text-[10px] font-bold text-slate-800">Health trends</p><p className="text-[9px] text-slate-400">Your activity over time</p></div><span className="rounded-full bg-emerald-50 px-2 py-1 text-[9px] font-semibold text-emerald-700">View insights</span></div>
              <svg viewBox="0 0 440 90" className="mt-2 h-16 w-full" role="img" aria-label="Illustrative upward health trend">
                <defs><linearGradient id="trendFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#10b981" stopOpacity=".2"/><stop offset="1" stopColor="#10b981" stopOpacity="0"/></linearGradient></defs>
                <path d="M0 69 L40 58 L80 62 L120 43 L160 49 L200 34 L240 42 L280 24 L320 30 L360 12 L400 20 L440 8 L440 90 L0 90 Z" fill="url(#trendFill)" />
                <path d="M0 69 L40 58 L80 62 L120 43 L160 49 L200 34 L240 42 L280 24 L320 30 L360 12 L400 20 L440 8" fill="none" stroke="#059669" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <div className="flex justify-between text-[8px] text-slate-400"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function LandingPage() {
  return (
    <div className="bg-white text-slate-900">
      <section id="overview" className="relative overflow-hidden bg-gradient-to-br from-[#f5fffc] via-white to-[#e9faf5]">
        <div className="mx-auto grid max-w-7xl items-center gap-10 px-5 py-12 sm:px-8 sm:py-16 lg:grid-cols-2 lg:gap-12 lg:px-10 lg:py-12">
          <div className="relative z-10 text-center lg:text-left">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50/80 px-3 py-1.5 text-[11px] font-semibold text-emerald-800"><Sparkles className="h-3.5 w-3.5" /> A smarter health companion</div>
            <h1 className="text-4xl font-extrabold leading-[1.08] tracking-tight text-slate-950 sm:text-5xl lg:text-[3.5rem]">Better Health.<br /><span className="text-emerald-800">Brighter You.</span></h1>
            <p className="mx-auto mt-5 max-w-lg text-sm leading-6 text-slate-600 sm:text-base lg:mx-0">Get health insights, understand symptoms, and discover practical next steps—all in one place.</p>
            <div className="mt-7 flex flex-col justify-center gap-3 sm:flex-row lg:justify-start">
              <Link to="/symptom-checker" className="inline-flex items-center justify-center gap-2 rounded-full bg-emerald-700 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800">Get Started <ArrowRight className="h-4 w-4" /></Link>
              <a href="#features" className="inline-flex items-center justify-center rounded-full border border-emerald-700 px-6 py-3 text-sm font-semibold text-emerald-800 transition hover:bg-emerald-50">Explore Features</a>
            </div>
            <div className="mx-auto mt-8 flex max-w-md items-center justify-center divide-x divide-emerald-200 text-left lg:mx-0 lg:justify-start">
              {[[Users, "10K+", "Active users"], [CheckCircle2, "4.8/5", "App rating"], [Zap, "24/7", "Health support"]].map(([Icon, value, label]) => <div key={label} className="flex flex-1 items-center gap-2 px-3 first:pl-0 last:pr-0"><span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-800"><Icon className="h-4 w-4" /></span><span><strong className="block text-xs font-bold text-slate-800">{value}</strong><span className="text-[9px] text-slate-500 sm:text-[10px]">{label}</span></span></div>)}
            </div>
          </div>
          <div className="relative py-2 sm:px-3"><DashboardPreview /></div>
        </div>
      </section>

      <section id="features" className="mx-auto grid max-w-7xl gap-4 px-5 py-8 sm:grid-cols-2 sm:px-8 sm:py-10 lg:grid-cols-4 lg:px-10">
        {features.map(({ icon: Icon, title, description, to }) => <Link key={title} to={to} className="group flex min-h-[185px] flex-col rounded-xl border border-emerald-100 bg-white p-5 transition hover:-translate-y-1 hover:border-emerald-300 hover:shadow-lg hover:shadow-emerald-900/5"><span className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 transition group-hover:bg-emerald-100"><Icon className="h-5 w-5" /></span><h2 className="text-sm font-bold text-emerald-950">{title}</h2><p className="mt-2 flex-1 text-xs leading-5 text-slate-500">{description}</p><ArrowRight className="mt-3 h-4 w-4 text-emerald-800 transition group-hover:translate-x-1" /></Link>)}
      </section>

      <section id="about" className="bg-gradient-to-r from-[#f2fcf9] via-[#f8fffd] to-[#effbf7] px-5 py-10 sm:px-8 sm:py-12">
        <div className="mx-auto max-w-6xl">
          <div className="text-center"><span className="rounded-full border border-emerald-100 bg-white px-3 py-1 text-[10px] font-semibold text-emerald-700">How it works</span><h2 className="mt-3 text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">Your health journey, <span className="text-emerald-800">simplified</span></h2></div>
          <div className="mt-8 grid gap-5 md:grid-cols-3">
            {[[ClipboardList, "Assess", "Share what you’re experiencing and complete a guided assessment."], [Brain, "Understand", "Get clear, safety-first information and personalized insights."], [TrendingUp, "Improve", "Explore care guidance and build healthier habits over time."]].map(([Icon, title, description], index) => <div key={title} className="flex items-start gap-3 rounded-xl border border-emerald-100/80 bg-white/70 p-4"><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-sm font-bold text-emerald-900">{index + 1}</span><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-emerald-50 text-emerald-700"><Icon className="h-4 w-4" /></span><div><h3 className="text-sm font-bold text-slate-900">{title}</h3><p className="mt-1 text-xs leading-5 text-slate-500">{description}</p></div><ArrowRight className="mt-2 hidden h-4 w-4 shrink-0 text-emerald-700 md:block" /></div>)}
          </div>
          <div id="safety" className="mt-7 flex flex-col items-center justify-between gap-3 rounded-xl border border-emerald-100 bg-white/70 px-4 py-3 text-center sm:flex-row sm:text-left"><p className="flex items-center gap-2 text-xs text-slate-600"><ShieldCheck className="h-4 w-4 shrink-0 text-emerald-700" /> Healix offers health information and triage support; it does not replace a qualified clinician.</p><Link to="/symptom-checker" className="shrink-0 text-xs font-semibold text-emerald-800 hover:text-emerald-950">Start a symptom check <ArrowRight className="ml-1 inline h-3 w-3" /></Link></div>
        </div>
      </section>
    </div>
  );
}
