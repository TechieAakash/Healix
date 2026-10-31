import React from 'react';
import { ArrowRight, ShieldCheck, Network, Brain, Activity, Lock, Cpu, Sparkles, CheckCircle2 } from 'lucide-react';

interface LandingPageProps {
  navigate: (route: string) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ navigate }) => {
  return (
    <div className="space-y-24 py-12">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto px-4 space-y-6">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-signal/10 border border-signal/30 text-signal text-xs font-mono font-medium">
          <Sparkles className="w-3.5 h-3.5 text-signal" />
          <span>Deterministic AI • Fully Traceable • Medical Trust</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-mist leading-[1.15]">
          Understand your health.<br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-signal via-pulse to-mist">
            Understand the intelligence behind it.
          </span>
        </h1>

        <p className="text-base sm:text-lg text-mist-muted max-w-2xl mx-auto leading-relaxed">
          Healix replaces opaque, hallucination-prone black-box LLMs with a formal, deterministic production rule expert system. Every conclusion is logically auditable through an interactive knowledge graph.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <button
            onClick={() => navigate('assessment-new')}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-signal text-void font-bold text-sm hover:opacity-90 hover:scale-[1.02] shadow-lg transition-all"
          >
            <span>Start Symptom Assessment</span>
            <ArrowRight className="w-4 h-4" />
          </button>
          <button
            onClick={() => navigate('how-it-works')}
            className="flex items-center gap-2 px-6 py-3 rounded-xl glass-panel border-carbon-border text-mist font-semibold text-sm hover:border-signal/50 transition-all"
          >
            <Activity className="w-4 h-4 text-signal" />
            <span>How Clinical Reasoning Works</span>
          </button>
        </div>

        {/* Clinical Disclaimer Banner */}
        <div className="max-w-2xl mx-auto mt-6 p-3.5 rounded-xl glass-panel text-xs text-mist-muted flex items-center justify-center gap-2">
          <ShieldCheck className="w-4 h-4 text-signal shrink-0" />
          <span>
            <strong>Safety Notice:</strong> Healix is an educational decision-support platform and does not provide formal medical diagnoses or drug prescriptions.
          </span>
        </div>
      </section>

      {/* Signature Feature Preview: The Explainability Knowledge Graph */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="glass-panel p-8 rounded-3xl relative overflow-hidden border border-carbon-border/80">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div>
              <div className="text-xs font-mono text-signal uppercase tracking-wider font-semibold">
                Signature Feature
              </div>
              <h2 className="text-2xl font-bold text-mist mt-1">
                Interactive Reasoning Trace & Knowledge Graph
              </h2>
              <p className="text-sm text-mist-muted mt-1 max-w-xl">
                Unlike generative AI chats, Healix constructs a formal Directed Acyclic Graph (DAG) for every assessment run, proving exactly which facts fired which rules.
              </p>
            </div>
            <button
              onClick={() => navigate('assessment-new')}
              className="px-4 py-2 rounded-xl bg-carbon border border-signal/40 text-signal font-semibold text-xs hover:bg-signal/10 transition-colors"
            >
              Try Interactive Triage
            </button>
          </div>

          {/* Graphical Pipeline Mockup */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
            <div className="glass-panel p-5 rounded-2xl border border-signal/30 space-y-3">
              <div className="flex items-center gap-2 text-xs font-mono font-semibold text-signal">
                <CheckCircle2 className="w-4 h-4" />
                <span>USER-REPORTED FACTS</span>
              </div>
              <div className="space-y-2 text-xs font-mono">
                <div className="p-2.5 rounded-lg glass-panel text-mist">
                  Headache.Unilateral == TRUE
                </div>
                <div className="p-2.5 rounded-lg glass-panel text-mist">
                  Headache.Throbbing == TRUE
                </div>
                <div className="p-2.5 rounded-lg glass-panel text-mist">
                  Photophobia == TRUE
                </div>
              </div>
            </div>

            <div className="glass-panel p-5 rounded-2xl border border-pulse/30 space-y-3">
              <div className="flex items-center gap-2 text-xs font-mono font-semibold text-pulse">
                <Cpu className="w-4 h-4" />
                <span>RULE ENGINE MATCH</span>
              </div>
              <div className="space-y-2 text-xs font-mono">
                <div className="p-2.5 rounded-lg glass-panel border border-pulse/30 text-pulse font-semibold">
                  RULE_MIGRAINE_042 [Pri: 500]
                </div>
                <div className="p-2 rounded glass-panel text-[11px] text-mist-muted">
                  Antecedent conditions satisfied under 5-valued Kleene logic.
                </div>
              </div>
            </div>

            <div className="glass-panel p-5 rounded-2xl border border-signal/40 space-y-3">
              <div className="flex items-center gap-2 text-xs font-mono font-semibold text-signal">
                <Sparkles className="w-4 h-4" />
                <span>CAUSAL CONCLUSION</span>
              </div>
              <div className="p-3 rounded-lg bg-signal/10 border border-signal/30 text-xs text-mist font-medium">
                Benign Neurovascular Pattern (Consistent with Migraine criteria).
              </div>
              <div className="text-[11px] font-mono text-mist-muted">
                Confidence: 92% • Tier: CONSULT_PHYSICIAN
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Differentiators: Rule-Based vs Black-Box LLM */}
      <section className="max-w-5xl mx-auto px-4">
        <div className="text-center space-y-2 mb-12">
          <div className="text-xs font-mono text-signal uppercase tracking-wider font-semibold">
            Architectural Philosophy
          </div>
          <h2 className="text-3xl font-bold text-mist">Why Rule-Based AI Outperforms LLMs in Triage</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="glass-panel p-6 rounded-2xl border-l-4 border-alert/80 space-y-4">
            <h3 className="text-lg font-bold text-alert flex items-center gap-2">
              <span>Generic Generative LLMs</span>
            </h3>
            <ul className="space-y-2.5 text-xs text-mist-muted leading-relaxed">
              <li className="flex items-start gap-2">
                <span className="text-alert font-bold">✕</span>
                <span>Stochastic & Hallucination-Prone: Same symptoms can produce conflicting recommendations.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-alert font-bold">✕</span>
                <span>Black-box opacity: Cannot prove why an observation was asserted or excluded.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-alert font-bold">✕</span>
                <span>Interprets missing questions as negative answers, creating severe clinical bias.</span>
              </li>
            </ul>
          </div>

          <div className="glass-panel p-6 rounded-2xl border-l-4 border-signal space-y-4">
            <h3 className="text-lg font-bold text-signal flex items-center gap-2">
              <span>Healix Deterministic Engine</span>
            </h3>
            <ul className="space-y-2.5 text-xs text-mist leading-relaxed">
              <li className="flex items-start gap-2">
                <span className="text-signal font-bold">✓</span>
                <span>100% Deterministic: Exact reproducible execution trace for identical inputs.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-signal font-bold">✓</span>
                <span>Causal Explainability: Inspect both "Why Fired" and "Why Not Fired" conditions.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-signal font-bold">✓</span>
                <span>5-Valued Clinical Logic: Rigorously distinguishes True, False, Unknown, and Not Asked.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
};

