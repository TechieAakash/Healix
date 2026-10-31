import React from 'react';
import { ShieldCheck, Stethoscope, FileText, CheckCircle2, Lock, AlertTriangle, Cpu } from 'lucide-react';

export const AboutPage: React.FC<{ navigate: (route: string) => void }> = ({ navigate }) => {
  const standards = [
    {
      title: 'Neurovascular & Cephalea Standards',
      authority: 'American College of Emergency Physicians (ACEP) & ICHD-3',
      description: 'Rules for thunderclap cephalea, intracranial hemorrhage risk screening, and benign migraine differential patterns.',
      guarantee: 'Immediate red-flag trigger when sudden peak intensity (< 60s) is recorded.'
    },
    {
      title: 'Infectious & Meningeal Protocols',
      authority: 'Infectious Diseases Society of America (IDSA)',
      description: 'Meningeal irritation triad evaluation (nuchal rigidity, high pyrexia, and altered sensorium) for prompt clinical triage.',
      guarantee: 'Zero tolerance for unverified delays in suspected central nervous system infections.'
    },
    {
      title: 'Cardiopulmonary & Ischemic Pathways',
      authority: 'American Heart Association & American College of Cardiology (AHA/ACC)',
      description: 'Retrosternal crushing pressure, radiation to upper extremities, and acute dyspnea assessment.',
      guarantee: 'Direct priority routing to emergency dispatch (112/911) instructions.'
    },
    {
      title: 'Acute Abdominal & Surgical Triage',
      authority: 'World Society of Emergency Surgery (WSES)',
      description: 'Right Lower Quadrant localization, acute peritoneal signs, and appendicitis differential criteria.',
      guarantee: 'Clear surgical evaluation referral and fasting (NPO) precautions.'
    },
    {
      title: 'Self-Care & Preventive Boundaries',
      authority: 'World Health Organization (WHO) Supportive Care Guidance',
      description: 'Hydration wellness, sleep hygiene, and non-pharmacological support for mild, self-limiting viral episodes.',
      guarantee: 'Strict exclusion of drug prescribing or unverified pharmaceutical remedies.'
    }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 space-y-12 animate-fade-in">
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-signal/15 border border-signal/30 text-signal text-xs font-mono font-medium">
          <ShieldCheck className="w-4 h-4 text-signal" />
          <span>Evidence-Based Clinical Standards</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-mist">
          Clinical Guidance Principles & Safety Architecture
        </h1>
        <p className="text-sm text-mist-muted max-w-2xl mx-auto leading-relaxed">
          Healix combines classical deterministic reasoning with international medical policy standards to deliver reliable, auditable health assessments.
        </p>
      </div>

      {/* Core Principles */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 rounded-2xl border border-carbon-border space-y-3">
          <div className="w-9 h-9 rounded-xl bg-signal/15 border border-signal/30 flex items-center justify-center text-signal">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-mist">Deterministic Rule Engine</h3>
          <p className="text-xs text-mist-muted leading-relaxed">
            Unlike generative black-box LLMs that hallucinate, our custom production rule engine evaluates formal Boolean and 5-valued logic deterministically.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-carbon-border space-y-3">
          <div className="w-9 h-9 rounded-xl bg-signal/15 border border-signal/30 flex items-center justify-center text-signal">
            <Lock className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-mist">Privacy & Security by Design</h3>
          <p className="text-xs text-mist-muted leading-relaxed">
            All assessment data is encrypted at rest. We never share personal health indicators or assessment summaries with advertising brokers.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-carbon-border space-y-3">
          <div className="w-9 h-9 rounded-xl bg-signal/15 border border-signal/30 flex items-center justify-center text-signal">
            <Stethoscope className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-mist">Physician Decision Support</h3>
          <p className="text-xs text-mist-muted leading-relaxed">
            Healix generates structured, audit-ready clinical summaries designed to help users communicate symptoms clearly during professional consultations.
          </p>
        </div>
      </div>

      {/* Clinical Guidance Standards List */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-mist flex items-center gap-2">
          <FileText className="w-5 h-5 text-signal" />
          <span>Clinical Knowledge Base & Protocol Citations</span>
        </h2>

        <div className="space-y-3">
          {standards.map((s, i) => (
            <div key={i} className="glass-panel p-6 rounded-2xl border border-carbon-border space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <span className="text-sm font-bold text-mist">{s.title}</span>
                <span className="text-xs font-mono text-signal bg-signal/10 px-2 py-0.5 rounded border border-signal/20">
                  {s.authority}
                </span>
              </div>
              <p className="text-xs text-mist-muted leading-relaxed">{s.description}</p>
              <div className="text-xs text-mist font-medium pt-1 border-t border-carbon-border flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-mint shrink-0" />
                <span>Safeguard: {s.guarantee}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Safety Notice */}
      <div className="glass-panel p-6 rounded-2xl border-l-4 border-alert space-y-2">
        <div className="flex items-center gap-2 text-alert text-sm font-bold">
          <AlertTriangle className="w-5 h-5 text-alert" />
          <span>Strict Non-Diagnostic Clinical Boundary</span>
        </div>
        <p className="text-xs text-mist-muted leading-relaxed">
          Healix is designed as an explainable clinical decision-support tool. It does NOT provide formal medical diagnoses, prescribe medications, or replace emergency professional healthcare. In a medical emergency, contact emergency dispatch (112 / 911) immediately.
        </p>
      </div>
    </div>
  );
};
