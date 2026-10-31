import React from 'react';
import { X, CheckCircle2, XCircle, ShieldAlert, Cpu, Sparkles, BookOpen, ArrowRight } from 'lucide-react';
import { GraphNode } from '../../types';

interface NodeDetailDrawerProps {
  node: GraphNode | null;
  onClose: () => void;
}

export const NodeDetailDrawer: React.FC<NodeDetailDrawerProps> = ({ node, onClose }) => {
  if (!node) return null;

  const data = node.data;
  const meta = data.metadata || {};

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[450px] glass-panel backdrop-blur-2xl border-l border-carbon-border z-50 p-6 flex flex-col shadow-2xl transition-all duration-300 overflow-y-auto">
      <div className="flex items-center justify-between pb-4 border-b border-carbon-border">
        <div className="flex items-center gap-2">
          {data.node_type === 'FACT' && <CheckCircle2 className="w-5 h-5 text-signal" />}
          {data.node_type === 'RULE' && <Cpu className="w-5 h-5 text-pulse" />}
          {data.node_type === 'CONCLUSION' && <Sparkles className="w-5 h-5 text-signal" />}
          {data.node_type === 'SAFETY' && <ShieldAlert className="w-5 h-5 text-alert" />}
          <span className="text-xs uppercase font-mono font-bold tracking-wider text-signal">
            {data.node_type} INSPECTION
          </span>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-lg text-mist-muted hover:text-mist hover:bg-carbon-border/50 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="mt-6 space-y-6">
        <div>
          <h3 className="text-lg font-bold text-mist">{data.label}</h3>
          {data.sublabel && (
            <p className="text-xs font-mono text-mist-muted mt-1">{data.sublabel}</p>
          )}
        </div>

        {/* Fact details */}
        {data.node_type === 'FACT' && (
          <div className="glass-panel p-4 rounded-xl space-y-2 text-sm">
            <div className="flex justify-between font-mono text-xs text-mist-muted">
              <span>Fact Identifier:</span>
              <span className="text-mist">{meta.fact_name}</span>
            </div>
            <div className="flex justify-between font-mono text-xs text-mist-muted">
              <span>Logical State:</span>
              <span className="text-signal font-bold">{meta.value}</span>
            </div>
            <div className="flex justify-between font-mono text-xs text-mist-muted">
              <span>Data Source:</span>
              <span className="text-mist">{meta.source}</span>
            </div>
          </div>
        )}

        {/* Rule details & Why / Why Not */}
        {data.node_type === 'RULE' && (
          <>
            <div className="glass-panel p-4 rounded-xl space-y-2 text-sm">
              <div className="flex justify-between font-mono text-xs text-mist-muted">
                <span>Rule ID:</span>
                <span className="text-mist">{meta.rule_id}</span>
              </div>
              <div className="flex justify-between font-mono text-xs text-mist-muted">
                <span>Priority:</span>
                <span className="text-pulse font-bold">{meta.priority}</span>
              </div>
              <div className="flex justify-between font-mono text-xs text-mist-muted">
                <span>Category:</span>
                <span className="text-mist">{meta.category}</span>
              </div>
            </div>

            {/* If skipped: Why did this rule NOT fire? */}
            {data.state === 'SKIPPED' && meta.unsatisfied_conditions && (
              <div className="glass-panel-alert p-4 rounded-xl space-y-3">
                <div className="flex items-center gap-2 text-alert text-sm font-bold">
                  <XCircle className="w-4 h-4" />
                  Why did this rule NOT fire?
                </div>
                <div className="space-y-2">
                  {meta.unsatisfied_conditions.map((reason: string, idx: number) => (
                    <div key={idx} className="text-xs font-mono glass-panel p-2.5 rounded border border-alert/30 text-mist">
                      {reason}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* If fired: Why did this rule fire? */}
            {data.state === 'FIRED' && (
              <div className="glass-panel-glow p-4 rounded-xl space-y-2">
                <div className="flex items-center gap-2 text-signal text-sm font-bold">
                  <CheckCircle2 className="w-4 h-4" />
                  Why did this rule fire?
                </div>
                <p className="text-xs text-mist-muted leading-relaxed">
                  All antecedent conditions evaluated to <span className="text-signal font-mono">TRUE</span> under 5-valued logic in iteration {data.step}.
                </p>
              </div>
            )}
          </>
        )}

        {/* Conclusion details */}
        {data.node_type === 'CONCLUSION' && (
          <div className="space-y-4">
            <div className="glass-panel p-4 rounded-xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-mist-muted uppercase">Recommendation Tier</span>
                <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                  meta.tier === 'EMERGENCY' ? 'bg-alert text-white font-bold' : 'bg-signal/20 text-signal'
                }`}>
                  {meta.tier}
                </span>
              </div>
              {meta.detailed_explanation && (
                <p className="text-xs text-mist leading-relaxed border-t border-carbon-border pt-2">
                  {meta.detailed_explanation}
                </p>
              )}
            </div>

            {meta.actionable_steps && meta.actionable_steps.length > 0 && (
              <div className="glass-panel p-4 rounded-xl space-y-2">
                <h4 className="text-xs font-mono uppercase text-signal font-bold">Actionable Guidance</h4>
                <ul className="space-y-2">
                  {meta.actionable_steps.map((step: string, i: number) => (
                    <li key={i} className="text-xs text-mist flex items-start gap-2">
                      <ArrowRight className="w-3.5 h-3.5 text-signal shrink-0 mt-0.5" />
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Clinical Disclaimer */}
        <div className="p-3 rounded-lg glass-panel text-[11px] text-mist-muted flex items-start gap-2">
          <BookOpen className="w-4 h-4 text-signal shrink-0 mt-0.5" />
          <span>
            Every deduction is verifiable via formal production rules. Healix is an educational decision support system.
          </span>
        </div>
      </div>
    </div>
  );
};

