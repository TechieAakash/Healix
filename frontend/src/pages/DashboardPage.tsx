import React, { useEffect, useState } from 'react';
import { 
  Sparkles, 
  Activity, 
  FileText, 
  ArrowRight, 
  ShieldAlert, 
  CheckCircle2, 
  Clock, 
  Plus,
  ShieldCheck,
  Stethoscope,
  ChevronRight
} from 'lucide-react';
import { api } from '../services/api';
import { User, AssessmentSummary, TimelineObservation } from '../types';

interface DashboardPageProps {
  user: User;
  navigate: (route: string, param?: string) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ user, navigate }) => {
  const [assessments, setAssessments] = useState<AssessmentSummary[]>([]);
  const [observations, setObservations] = useState<TimelineObservation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [aData, oData] = await Promise.all([
          api.listAssessments(),
          api.getTimeline()
        ]);
        setAssessments(aData);
        setObservations(oData);
      } catch (err) {
        console.error('Failed to load dashboard data', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
      {/* Welcome Banner */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-carbon-border relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-signal/15 border border-signal/30 text-signal text-xs font-mono font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Intelligent Health Companion</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-mist">
            Welcome back, {user.full_name}
          </h1>
          <p className="text-xs sm:text-sm text-mist-muted max-w-xl leading-relaxed">
            Assess symptoms in natural English, receive evidence-backed clinical guidance, and maintain your personal health records.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => navigate('assessment-new')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-signal text-void font-bold text-xs hover:opacity-90 shadow-md transition-all"
          >
            <Plus className="w-4 h-4 stroke-[3]" />
            <span>New Symptom Assessment</span>
          </button>
          <button
            onClick={() => navigate('timeline')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-carbon border border-carbon-border text-mist font-semibold text-xs hover:border-signal/40 transition-colors"
          >
            <Activity className="w-4 h-4 text-signal" />
            <span>Health Timeline</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Recent Assessments & Health Intelligence */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Recent Assessments */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-mist flex items-center gap-2">
              <Activity className="w-5 h-5 text-signal" />
              <span>Recent Symptom Assessments</span>
            </h2>
            <button
              onClick={() => navigate('assessment-new')}
              className="text-xs font-semibold text-signal hover:underline"
            >
              + Start Assessment
            </button>
          </div>

          {loading ? (
            <div className="glass-panel p-8 rounded-2xl text-center text-xs text-mist-muted">
              Loading your previous assessments...
            </div>
          ) : assessments.length === 0 ? (
            <div className="glass-panel p-10 rounded-2xl text-center space-y-4 border border-dashed border-carbon-border">
              <div className="w-12 h-12 rounded-full bg-signal/15 border border-signal/30 flex items-center justify-center text-signal mx-auto">
                <Stethoscope className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-mist">No assessments completed yet</h3>
                <p className="text-xs text-mist-muted mt-1 max-w-sm mx-auto leading-relaxed">
                  Describe what symptoms you are experiencing to start your first clinical guidance assessment.
                </p>
              </div>
              <button
                onClick={() => navigate('assessment-new')}
                className="px-5 py-2.5 rounded-xl bg-signal text-void text-xs font-bold hover:opacity-90 transition-all inline-flex items-center gap-2"
              >
                <span>Start Symptom Assessment</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {assessments.map((a) => (
                <div
                  key={a.id}
                  onClick={() => navigate('assessment-detail', a.id)}
                  className="glass-panel p-5 rounded-2xl border border-carbon-border hover:border-signal/50 cursor-pointer transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      {a.emergency_flagged ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold px-2.5 py-0.5 rounded bg-alert text-white">
                          <ShieldAlert className="w-3 h-3" />
                          EMERGENCY RED FLAG
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold px-2.5 py-0.5 rounded bg-signal/20 text-signal border border-signal/30">
                          <CheckCircle2 className="w-3 h-3" />
                          EVALUATED
                        </span>
                      )}
                      <span className="text-[11px] font-mono text-mist-muted">
                        {new Date(a.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-mist group-hover:text-signal transition-colors">
                      {a.primary_complaint}
                    </h3>

                    {a.top_conclusion && (
                      <p className="text-xs text-mist-muted line-clamp-1">
                        Finding: {a.top_conclusion}
                      </p>
                    )}
                  </div>

                  <div className="flex items-center gap-2 self-end sm:self-center text-xs font-semibold text-mist-muted group-hover:text-signal">
                    <span>View Assessment</span>
                    <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Col: Timeline & Clinical Guidance Standards */}
        <div className="space-y-6">
          {/* Health Timeline Feed Widget */}
          <div className="glass-panel p-6 rounded-2xl border border-carbon-border space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-mist flex items-center gap-2">
                <Clock className="w-4 h-4 text-signal" />
                <span>Health Timeline</span>
              </h3>
              <button
                onClick={() => navigate('timeline')}
                className="text-[11px] font-semibold text-signal hover:underline"
              >
                View History
              </button>
            </div>

            {observations.length === 0 ? (
              <p className="text-xs text-mist-muted leading-relaxed">
                No observations logged yet. Previous evaluations and symptom notes will appear here chronologically.
              </p>
            ) : (
              <div className="space-y-3">
                {observations.slice(0, 3).map((obs) => (
                  <div key={obs.id} className="p-3 rounded-xl surface-card space-y-1">
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="text-mist font-semibold truncate">{obs.title}</span>
                      <span className={`px-1.5 py-0.2 rounded text-[10px] font-mono font-bold ${
                        obs.severity === 'CRITICAL' ? 'bg-alert text-white' : 'bg-signal/20 text-signal'
                      }`}>
                        {obs.severity}
                      </span>
                    </div>
                    {obs.notes && (
                      <p className="text-[11px] text-mist-muted line-clamp-2">{obs.notes}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Clinical Decision Support Standards Box */}
          <div className="glass-panel p-6 rounded-2xl border border-carbon-border space-y-3">
            <div className="flex items-center gap-2 text-signal text-xs font-semibold uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4" />
              <span>Evidence-Informed Engine</span>
            </div>
            <h3 className="text-sm font-bold text-mist">
              Clinical Guidelines & Red-Flag Safeguards
            </h3>
            <p className="text-xs text-mist-muted leading-relaxed">
              Healix evaluates symptom patterns against verified international clinical policies (including ACEP neurovascular guidelines, AHA cardiac pathways, and IDSA standards).
            </p>
            <div className="pt-1 border-t border-carbon-border text-[11px] text-mist-muted flex items-center justify-between">
              <span>Deterministic Rule Base v1.2</span>
              <span className="text-signal font-mono font-bold">100% Traceable</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
