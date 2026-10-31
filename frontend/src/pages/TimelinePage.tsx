import React, { useEffect, useState } from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { Activity, Plus, Clock, ShieldCheck, Sparkles, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import { TimelineObservation } from '../types';

export const TimelinePage: React.FC = () => {
  const [observations, setObservations] = useState<TimelineObservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [title, setTitle] = useState('');
  const [notes, setNotes] = useState('');
  const [severity, setSeverity] = useState('MILD');

  const fetchTimeline = async () => {
    try {
      const data = await api.getTimeline();
      setObservations(data);
    } catch (err) {
      console.error('Failed to load timeline', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimeline();
  }, []);

  const handleAddObservation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    try {
      await api.createObservation({ title, notes, severity });
      setTitle('');
      setNotes('');
      setShowAddModal(false);
      fetchTimeline();
    } catch (err: any) {
      alert(err.message || 'Failed to save observation');
    }
  };

  // Convert observations to numeric chart data
  const severityMap: Record<string, number> = {
    MILD: 1,
    MODERATE: 2,
    SEVERE: 3,
    CRITICAL: 4
  };

  const chartData = [...observations].reverse().map((obs, idx) => ({
    time: new Date(obs.recorded_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }),
    severityScore: severityMap[obs.severity] || 1,
    label: obs.title,
    severity: obs.severity
  }));

  return (
    <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-signal/10 border border-signal/30 text-signal text-xs font-mono font-medium">
            <Activity className="w-3.5 h-3.5" />
            <span>Longitudinal Record</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-mist mt-1">
            Personal Health Timeline
          </h1>
          <p className="text-xs sm:text-sm text-mist-muted">
            Chronological log of clinical assessments, symptom trends, and user notes.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 rounded-xl bg-signal text-void font-bold text-xs hover:bg-signal/90 transition-all flex items-center gap-2 self-start sm:self-auto shadow-md shadow-signal/20"
        >
          <Plus className="w-4 h-4" />
          <span>Log Health Note</span>
        </button>
      </div>

      {/* Visual Severity Trend Chart */}
      {chartData.length > 1 && (
        <div className="glass-panel p-6 rounded-3xl border border-carbon-border space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-mono font-bold text-signal uppercase tracking-wider">
              Symptom Severity Trend Curve
            </h2>
            <span className="text-[10px] font-mono text-mist-muted">
              Y-Axis: Mild (1) to Critical (4)
            </span>
          </div>

          <div className="h-56 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="severityGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="rgb(14,165,233)" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="rgb(14,165,233)" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.3} />
                <XAxis dataKey="time" fontSize={11} tickLine={false} />
                <YAxis
                  fontSize={11}
                  domain={[1, 4]}
                  ticks={[1, 2, 3, 4]}
                  tickFormatter={(val) => ['Mild', 'Mod', 'Sev', 'Crit'][val - 1]}
                  tickLine={false}
                />
                <Tooltip
                  content={({ payload }) => {
                    if (payload && payload.length) {
                      const d = payload[0].payload;
                      return (
                        <div className="glass-panel p-3 rounded-xl border border-carbon-border text-xs text-mist shadow-lg">
                          <div className="font-bold">{d.label}</div>
                          <div className="text-[11px] font-mono text-signal">Severity: {d.severity}</div>
                          <div className="text-[10px] text-mist-muted">{d.time}</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="severityScore"
                  stroke="rgb(14,165,233)"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#severityGrad)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Chronological Observation Feed */}
      <div className="space-y-4">
        <h2 className="text-sm font-bold text-mist flex items-center gap-2">
          <Clock className="w-4 h-4 text-signal" />
          <span>Chronological Episodes</span>
        </h2>

        {loading ? (
          <div className="glass-panel p-8 rounded-2xl text-center text-xs text-mist-muted">
            Loading timeline...
          </div>
        ) : observations.length === 0 ? (
          <div className="glass-panel p-8 rounded-2xl text-center text-xs text-mist-muted">
            No health observations recorded yet. Complete an assessment or log a quick note.
          </div>
        ) : (
          <div className="space-y-3">
            {observations.map((obs) => (
              <div key={obs.id} className="glass-panel p-5 rounded-2xl border border-carbon-border space-y-2">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-bold text-mist">{obs.title}</span>
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                      obs.severity === 'CRITICAL'
                        ? 'bg-alert text-void'
                        : obs.severity === 'SEVERE'
                          ? 'bg-alert/30 text-alert'
                          : 'bg-signal/20 text-signal border border-signal/30'
                    }`}>
                      {obs.severity}
                    </span>
                    <span className="text-xs font-mono text-mist-muted">
                      {new Date(obs.recorded_at).toLocaleDateString()} {new Date(obs.recorded_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
                {obs.notes && (
                  <p className="text-xs text-mist-muted leading-relaxed">{obs.notes}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Observation Modal */}
      {showAddModal && (
        <div className="fixed inset-0 modal-overlay z-50 flex items-center justify-center p-4">
          <div className="glass-panel max-w-md w-full p-6 rounded-3xl border border-carbon-border space-y-4">
            <h3 className="text-lg font-bold text-mist">Log New Health Observation</h3>
            <form onSubmit={handleAddObservation} className="space-y-3">
              <div>
                <label className="block text-xs font-mono text-mist-muted mb-1">Title / Event</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Mild headache following screen work"
                  className="w-full p-3 rounded-xl border border-carbon-border text-xs focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-mist-muted mb-1">Severity</label>
                <select
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                  className="w-full p-3 rounded-xl border border-carbon-border text-xs focus:outline-none"
                >
                  <option value="MILD">Mild</option>
                  <option value="MODERATE">Moderate</option>
                  <option value="SEVERE">Severe</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-mono text-mist-muted mb-1">Notes / Context</label>
                <textarea
                  rows={3}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Duration, triggers, self-care actions taken..."
                  className="w-full p-3 rounded-xl border border-carbon-border text-xs focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 text-xs font-mono text-mist-muted hover:text-mist"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-signal text-void font-bold text-xs hover:bg-signal/90"
                >
                  Save Note
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

