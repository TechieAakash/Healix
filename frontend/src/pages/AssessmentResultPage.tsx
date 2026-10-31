import React, { useEffect, useState } from 'react';
import { 
  Sparkles, 
  FileText, 
  ArrowRight, 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowLeft, 
  Download, 
  PhoneCall, 
  Clock, 
  Stethoscope, 
  HeartHandshake,
  ShieldCheck,
  Check
} from 'lucide-react';
import { api } from '../services/api';

interface AssessmentResultPageProps {
  assessmentId: string;
  navigate: (route: string, param?: string) => void;
}

export const AssessmentResultPage: React.FC<AssessmentResultPageProps> = ({ assessmentId, navigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [generatingReport, setGeneratingReport] = useState(false);

  useEffect(() => {
    async function fetchResult() {
      try {
        const res = await api.getAssessment(assessmentId);
        setData(res);
      } catch (err) {
        console.error('Failed to load assessment', err);
      } finally {
        setLoading(false);
      }
    }
    fetchResult();
  }, [assessmentId]);

  const handleGenerateReport = async () => {
    setGeneratingReport(true);
    try {
      await api.generateReport(assessmentId);
      navigate('reports');
    } catch (err: any) {
      alert(err.message || 'Report generation failed');
    } finally {
      setGeneratingReport(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-8 h-8 border-2 border-signal border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-mist-muted font-mono">Retrieving verified assessment results...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <AlertTriangle className="w-8 h-8 text-alert mx-auto" />
        <p className="text-sm font-semibold text-mist">Assessment record could not be loaded.</p>
        <button
          onClick={() => navigate('dashboard')}
          className="text-xs text-signal hover:underline"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  const isEmergency = data.emergency_flagged || data.recommendation_tier === 'EMERGENCY' || data.conclusions?.some((c: any) => c.recommendation_tier === 'EMERGENCY');
  const isUrgent = !isEmergency && (data.recommendation_tier === 'URGENT' || data.conclusions?.some((c: any) => c.recommendation_tier === 'URGENT_EVALUATION'));

  const getTierDisplay = () => {
    if (isEmergency) {
      return {
        badge: 'CRITICAL EMERGENCY RED FLAG',
        title: 'Emergency Medical Care Recommended Immediately',
        color: 'glass-panel-alert border-alert',
        badgeColor: 'bg-alert text-white font-bold',
        icon: ShieldAlert,
        action: 'Dial 112 / 911 or go to the nearest emergency room immediately.'
      };
    }
    if (isUrgent) {
      return {
        badge: 'URGENT MEDICAL EVALUATION',
        title: 'Prompt Clinical Evaluation Advised (Within 24 Hours)',
        color: 'bg-amber/10 border-amber/40',
        badgeColor: 'bg-amber text-void font-bold',
        icon: AlertTriangle,
        action: 'Contact an urgent care center or primary care provider today.'
      };
    }
    return {
      badge: 'ROUTINE CARE / CLINICAL CONSULTATION',
      title: 'Standard Consultation & Symptom Monitoring',
      color: 'glass-panel-mint border-mint/40',
      badgeColor: 'bg-mint text-void font-bold',
      icon: CheckCircle2,
      action: 'Schedule a routine outpatient consultation with your healthcare provider if symptoms persist.'
    };
  };

  const tier = getTierDisplay();
  const TierIcon = tier.icon;

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-8 animate-fade-in">
      {/* Top Bar Navigation */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('dashboard')}
          className="flex items-center gap-2 text-xs font-semibold text-mist-muted hover:text-mist transition-colors py-2 px-3 rounded-lg hover:bg-carbon"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </button>

        <button
          onClick={handleGenerateReport}
          disabled={generatingReport}
          className="px-4 py-2 rounded-xl bg-signal text-void text-xs font-bold hover:opacity-90 transition-all flex items-center gap-2 shadow-sm"
        >
          <Download className="w-4 h-4" />
          <span>{generatingReport ? 'Compiling Report...' : 'Download Clinical Report'}</span>
        </button>
      </div>

      {/* Emergency Immediate Action Banner */}
      {isEmergency && (
        <div className="p-6 rounded-2xl bg-alert/20 border-2 border-alert text-mist space-y-4 animate-signal-pulse">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-alert flex items-center justify-center text-white shrink-0">
                <ShieldAlert className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-extrabold text-alert">
                  CRITICAL CLINICAL ALERT: IMMEDIATE ATTENTION REQUIRED
                </h3>
                <p className="text-xs text-mist leading-relaxed mt-0.5">
                  Your reported symptom pattern flags high risk for acute conditions that require immediate in-person evaluation.
                </p>
              </div>
            </div>

            <a
              href="tel:112"
              className="px-5 py-3 rounded-xl bg-alert text-white font-extrabold text-xs flex items-center gap-2 shadow-lg hover:brightness-110"
            >
              <PhoneCall className="w-4 h-4" />
              <span>Call Emergency Dispatch (112 / 911)</span>
            </a>
          </div>
        </div>
      )}

      {/* Hero Assessment Summary Card */}
      <div className={`p-6 sm:p-8 rounded-3xl border ${tier.color} space-y-4`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono tracking-wider ${tier.badgeColor}`}>
            <TierIcon className="w-4 h-4" />
            {tier.badge}
          </span>
          <span className="text-xs text-mist-muted font-mono">
            Assessment ID: {assessmentId.substring(0, 8)} • Verified Engine v1.2
          </span>
        </div>

        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-mist tracking-tight">
            {tier.title}
          </h1>
          <p className="text-xs sm:text-sm text-mist-muted mt-1">
            Primary Reported Concern: <span className="text-mist font-semibold">"{data.primary_complaint}"</span>
          </p>
        </div>

        <div className="p-4 rounded-xl surface-card text-xs text-mist flex items-start gap-3">
          <Stethoscope className="w-5 h-5 text-signal shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="block text-mist font-semibold mb-0.5">Recommended Next Action:</strong>
            {tier.action}
          </div>
        </div>
      </div>

      {/* Clinical Narrative Summary (Gemini + Rule Verification) */}
      {data.gemini_narrative && (
        <div className="p-6 rounded-2xl glass-panel border border-signal/30 space-y-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-signal uppercase tracking-wider">
            <Sparkles className="w-4 h-4 text-signal" />
            <span>Clinical Summary Narrative</span>
          </div>

          <p className="text-sm text-mist leading-relaxed font-sans whitespace-pre-line">
            {data.gemini_narrative}
          </p>
        </div>
      )}

      {/* Verified Findings & Clinical Considerations */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-mist flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-signal" />
            <span>Possible Clinical Explanations & Observations</span>
          </h2>
          <span className="text-xs text-mist-muted">
            {data.conclusions?.length || 0} findings evaluated
          </span>
        </div>

        {(!data.conclusions || data.conclusions.length === 0) ? (
          <div className="glass-panel p-6 rounded-2xl text-center space-y-3 border border-carbon-border">
            <Stethoscope className="w-8 h-8 text-signal mx-auto" />
            <h3 className="text-sm font-bold text-mist">Outpatient Symptom Monitoring Advised</h3>
            <p className="text-xs text-mist-muted max-w-md mx-auto leading-relaxed">
              No acute emergency red flags were detected for this combination of symptoms. Continue routine self-monitoring, rest, stay hydrated, and contact a primary care physician if your symptoms worsen or persist.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {data.conclusions.map((c: any) => (
              <div key={c.id} className="glass-panel p-6 rounded-2xl border border-carbon-border space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-pulse">
                      [{c.rule_id}]
                    </span>
                    <span className="text-xs font-mono text-mist-muted uppercase">
                      • {c.category}
                    </span>
                  </div>

                  <span className={`text-xs font-mono font-bold px-2.5 py-0.5 rounded ${
                    c.recommendation_tier === 'EMERGENCY'
                      ? 'bg-alert text-white font-bold'
                      : c.recommendation_tier === 'URGENT_EVALUATION'
                      ? 'bg-amber text-void'
                      : 'bg-signal/20 text-signal border border-signal/30'
                  }`}>
                    {c.recommendation_tier}
                  </span>
                </div>

                <h3 className="text-base font-bold text-mist">{c.summary}</h3>

                {c.detailed_explanation && (
                  <p className="text-xs text-mist-muted leading-relaxed">
                    {c.detailed_explanation}
                  </p>
                )}

                {/* Actionable Steps */}
                {c.actionable_steps && c.actionable_steps.length > 0 && (
                  <div className="pt-3 border-t border-carbon-border space-y-2">
                    <span className="text-[11px] font-mono text-signal uppercase font-bold block">
                      Recommended Practical Steps:
                    </span>
                    <ul className="space-y-1.5 text-xs text-mist">
                      {c.actionable_steps.map((st: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2.5">
                          <Check className="w-3.5 h-3.5 text-signal shrink-0 mt-0.5 stroke-[3]" />
                          <span className="leading-relaxed">{st}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Non-Diagnostic Clinical Safety Notice */}
      <div className="p-5 rounded-2xl glass-panel space-y-2">
        <div className="flex items-center gap-2 text-xs font-bold text-mist">
          <ShieldCheck className="w-4 h-4 text-signal shrink-0" />
          <span>Clinical Safety Notice & Limitations</span>
        </div>
        <p className="text-[11px] text-mist-muted leading-relaxed">
          Healix is an AI-assisted clinical decision-support and symptom assessment tool. It does not provide formal medical diagnoses, write prescriptions, or replace in-person consultation with a qualified healthcare professional. If you experience severe shortness of breath, sudden severe chest pain, loss of consciousness, or sudden neurological deficits, call 112 / 911 immediately.
        </p>
      </div>
    </div>
  );
};
