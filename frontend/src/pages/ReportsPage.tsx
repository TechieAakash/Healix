import React, { useEffect, useState } from 'react';
import { FileText, Download, ShieldCheck, Printer, ArrowLeft, QrCode } from 'lucide-react';
import { api } from '../services/api';
import { ReportItem } from '../types';

export const ReportsPage: React.FC<{ navigate: (route: string) => void }> = ({ navigate }) => {
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [selectedReport, setSelectedReport] = useState<ReportItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadReports() {
      try {
        const data = await api.listReports();
        setReports(data);
        if (data.length > 0) {
          setSelectedReport(data[0]);
        }
      } catch (err) {
        console.error('Failed to load reports', err);
      } finally {
        setLoading(false);
      }
    }
    loadReports();
  }, []);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-signal/10 border border-signal/30 text-signal text-xs font-mono font-medium">
            <FileText className="w-3.5 h-3.5" />
            <span>Audit-Proof Reports</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-mist mt-1">
            Clinical Summary Documents
          </h1>
          <p className="text-xs sm:text-sm text-mist-muted">
            Cryptographically hashed consultation summaries designed to share with healthcare professionals.
          </p>
        </div>

        {selectedReport && (
          <button
            onClick={handlePrint}
            className="px-4 py-2 rounded-xl bg-signal text-void font-bold text-xs hover:bg-signal/90 transition-all flex items-center gap-2 self-start sm:self-auto shadow-md shadow-signal/20"
          >
            <Printer className="w-4 h-4" />
            <span>Print / Save as PDF</span>
          </button>
        )}
      </div>

      {loading ? (
        <div className="glass-panel p-8 rounded-2xl text-center text-xs text-mist-muted">
          Loading report vault...
        </div>
      ) : reports.length === 0 ? (
        <div className="glass-panel p-10 rounded-2xl text-center space-y-4">
          <FileText className="w-10 h-10 text-mist-muted mx-auto" />
          <h3 className="text-sm font-bold text-mist">No clinical reports generated yet</h3>
          <p className="text-xs text-mist-muted max-w-sm mx-auto">
            Complete a health assessment and click "Generate Report" to produce an audit-verified medical summary document.
          </p>
          <button
            onClick={() => navigate('assessment-new')}
            className="px-5 py-2 rounded-xl bg-signal text-void font-bold text-xs hover:bg-signal/90"
          >
            Start Assessment
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Reports Sidebar */}
          <div className="space-y-3">
            <h3 className="text-xs font-mono uppercase text-mist-muted font-bold tracking-wider">
              Generated Reports ({reports.length})
            </h3>
            <div className="space-y-2">
              {reports.map((rep) => {
                const isSelected = selectedReport?.id === rep.id;
                return (
                  <div
                    key={rep.id}
                    onClick={() => setSelectedReport(rep)}
                    className={`p-4 rounded-2xl border cursor-pointer transition-all ${
                      isSelected
                        ? 'glass-panel-glow border-signal/50 text-mist'
                        : 'glass-panel border-carbon-border text-mist-muted hover:text-mist hover:border-carbon-border/80'
                    }`}
                  >
                    <div className="text-xs font-bold truncate">{rep.title}</div>
                    <div className="flex items-center justify-between text-[10px] font-mono mt-2 text-mist-muted">
                      <span>{new Date(rep.created_at).toLocaleDateString()}</span>
                      <span className="truncate max-w-[100px] text-signal font-mono">
                        #{rep.checksum_sha256.slice(0, 8)}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Printable Report View (A4 layout) */}
          <div className="lg:col-span-2">
            {selectedReport && (
              <div className="glass-panel p-8 sm:p-10 rounded-3xl border border-carbon-border space-y-6 print:bg-white print:text-black print:border-none print:p-0 print:shadow-none">
                {/* Header */}
                <div className="flex items-start justify-between border-b border-carbon-border pb-6 print:border-gray-300">
                  <div className="space-y-1">
                    <div className="text-xs font-mono font-bold text-signal print:text-black uppercase tracking-widest">
                      HEALIX CLINICAL DECISION-SUPPORT REPORT
                    </div>
                    <h2 className="text-xl font-extrabold text-mist print:text-black">
                      {selectedReport.title}
                    </h2>
                    <div className="text-xs font-mono text-mist-muted print:text-gray-600">
                      Generated: {new Date(selectedReport.created_at).toLocaleString()} • KB: {selectedReport.report_data.kb_version}
                    </div>
                  </div>

                  <div className="p-2 rounded-xl glass-panel text-center print:border-gray-300">
                    <QrCode className="w-12 h-12 text-signal print:text-black mx-auto" />
                    <span className="text-[9px] font-mono text-mist-muted print:text-gray-500 block mt-1">
                      AUDIT VERIFIED
                    </span>
                  </div>
                </div>

                {/* Primary Complaint */}
                <div className="space-y-1">
                  <div className="text-[11px] font-mono uppercase text-mist-muted print:text-gray-600 font-bold">
                    Primary Symptom / Complaint
                  </div>
                  <p className="text-sm font-semibold text-mist print:text-black">
                    "{selectedReport.report_data.primary_complaint}"
                  </p>
                </div>

                {/* Conclusions */}
                <div className="space-y-3">
                  <div className="text-[11px] font-mono uppercase text-signal print:text-black font-bold">
                    Rule Engine Inferred Conclusions
                  </div>
                  <div className="space-y-3">
                    {selectedReport.report_data.conclusions?.map((c: any, i: number) => (
                      <div key={i} className="p-4 rounded-xl glass-panel print:border-gray-200 print:bg-gray-50 space-y-1.5">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-mono font-bold text-pulse print:text-black">
                            [{c.rule_id}] {c.category}
                          </span>
                          <span className="text-[11px] font-mono font-bold text-signal print:text-black">
                            {c.tier}
                          </span>
                        </div>
                        <div className="text-sm font-bold text-mist print:text-black">{c.summary}</div>
                        <div className="text-[11px] font-mono text-mist-muted print:text-gray-500">
                          Certainty / Confidence: {Math.round(c.confidence * 100)}%
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Cryptographic SHA-256 Checksum */}
                <div className="p-4 rounded-xl glass-panel font-mono text-xs space-y-1 print:border-gray-300 print:bg-gray-100">
                  <div className="text-[10px] uppercase text-mist-muted print:text-gray-600">
                    Cryptographic Integrity Signature (SHA-256)
                  </div>
                  <div className="text-signal print:text-black break-all text-[11px]">
                    {selectedReport.checksum_sha256}
                  </div>
                </div>

                {/* Clinical Disclaimer Footer */}
                <div className="pt-4 border-t border-carbon-border print:border-gray-300 text-[10px] text-mist-muted print:text-gray-500 leading-relaxed">
                  <strong>Clinical Notice:</strong> {selectedReport.report_data.clinical_disclaimer}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

