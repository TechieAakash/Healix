import React from 'react';
import { ArrowRight, Cpu, Network, ShieldCheck, Database, GitBranch, Terminal } from 'lucide-react';

export const HowItWorksPage: React.FC<{ navigate: (route: string) => void }> = ({ navigate }) => {
  const steps = [
    {
      num: '01',
      title: 'Typed Fact Extraction & 5-Valued Logic',
      desc: 'User inputs are converted into typed Fact objects evaluated under 5-valued logic: TRUE, FALSE, UNKNOWN, NOT_ASKED, NOT_APPLICABLE. A missing answer is never assumed negative.',
      icon: Database
    },
    {
      num: '02',
      title: 'Emergency Red-Flag Short-Circuit',
      desc: 'Before standard triage rules execute, high-priority emergency conditions (e.g. thunderclap onset, meningism triad) are evaluated. If triggered, the system immediately halts and routes to emergency care.',
      icon: ShieldCheck
    },
    {
      num: '03',
      title: 'Forward Chaining & Conflict Resolution',
      desc: 'Satisfied rules compete in a production system conflict resolution loop: Priority Level -> Specificity Score -> Recency -> Refractoriness. The winning rule fires, asserting derived observations into working memory.',
      icon: Cpu
    },
    {
      num: '04',
      title: 'Clinical Guidance & Narrative Generation',
      desc: 'The verified conclusions and rule firings are synthesized into structured clinical advice, actionable next steps, and a consultation summary with evidence citations.',
      icon: Network
    }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 space-y-16">
      <div className="text-center space-y-3">
        <div className="text-xs font-mono text-signal uppercase tracking-wider font-semibold">
          System Architecture
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-mist">
          How the Healix Inference Pipeline Works
        </h1>
        <p className="text-sm text-mist-muted max-w-2xl mx-auto leading-relaxed">
          Healix combines classic expert system production rules with verified clinical guidelines, ensuring mathematical and clinical transparency.
        </p>
      </div>

      <div className="space-y-6">
        {steps.map((s) => {
          const Icon = s.icon;
          return (
            <div key={s.num} className="glass-panel p-6 sm:p-8 rounded-2xl flex flex-col sm:flex-row items-start gap-6 border border-carbon-border hover:border-signal/40 transition-colors">
              <div className="w-12 h-12 rounded-xl bg-signal/10 border border-signal/30 flex items-center justify-center text-signal font-mono font-bold text-lg shrink-0">
                {s.num}
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4 text-signal" />
                  <h3 className="text-lg font-bold text-mist">{s.title}</h3>
                </div>
                <p className="text-sm text-mist-muted leading-relaxed">{s.desc}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="glass-panel-glow p-8 rounded-3xl text-center space-y-4">
        <h2 className="text-xl font-bold text-mist">Ready to experience explainable clinical triage?</h2>
        <p className="text-xs text-mist-muted max-w-md mx-auto">
          Start an assessment to receive personalized, evidence-informed guidance.
        </p>
        <button
          onClick={() => navigate('assessment-new')}
          className="px-6 py-2.5 rounded-xl bg-signal text-void font-bold text-sm hover:bg-signal/90 transition-all inline-flex items-center gap-2"
        >
          <span>Start Assessment</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

