import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { CheckCircle2, XCircle, AlertTriangle, HelpCircle, ShieldAlert, Cpu, Sparkles } from 'lucide-react';
import { GraphNodeData } from '../../types';

export const FactNode: React.FC<{ data: GraphNodeData; selected?: boolean }> = ({ data, selected }) => {
  const isTrue = data.state === 'ACTIVE' || data.metadata?.value === 'TRUE';
  const isEmergency = data.metadata?.fact_name?.toLowerCase().includes('red_flag') || data.metadata?.fact_name?.toLowerCase().includes('thunderclap');

  return (
    <div className={`px-4 py-3 rounded-xl min-w-[200px] transition-all duration-200 ${
      selected ? 'ring-2 ring-signal shadow-lg shadow-signal/20' : ''
    } ${
      isEmergency 
        ? 'bg-alert/15 border border-alert/50 text-mist' 
        : isTrue 
          ? 'glass-panel border border-signal/40 text-mist' 
          : 'glass-panel border border-carbon-border text-mist-muted'
    }`}>
      <Handle type="source" position={Position.Right} className="!bg-signal !w-3 !h-3 !border-void" />
      <div className="flex items-center gap-2 mb-1">
        {isEmergency ? (
          <ShieldAlert className="w-4 h-4 text-alert" />
        ) : isTrue ? (
          <CheckCircle2 className="w-4 h-4 text-signal" />
        ) : (
          <HelpCircle className="w-4 h-4 text-mist-muted" />
        )}
        <span className="text-[10px] uppercase font-mono tracking-wider font-semibold text-signal">
          Fact • {data.metadata?.source || 'Reported'}
        </span>
      </div>
      <div className="font-semibold text-sm leading-tight text-mist">{data.label}</div>
      {data.sublabel && (
        <div className="text-[11px] font-mono mt-1 text-mist-muted">{data.sublabel}</div>
      )}
    </div>
  );
};

export const RuleNode: React.FC<{ data: GraphNodeData; selected?: boolean }> = ({ data, selected }) => {
  const isFired = data.state === 'FIRED';
  const isSkipped = data.state === 'SKIPPED';

  return (
    <div className={`px-4 py-3 rounded-xl min-w-[240px] transition-all duration-200 ${
      selected ? 'ring-2 ring-pulse shadow-lg shadow-pulse/20' : ''
    } ${
      isFired
        ? 'glass-panel border border-pulse/60 text-mist'
        : 'glass-panel opacity-60 text-mist-muted'
    }`}>
      <Handle type="target" position={Position.Left} className="!bg-pulse !w-3 !h-3 !border-void" />
      <Handle type="source" position={Position.Right} className="!bg-pulse !w-3 !h-3 !border-void" />
      <div className="flex items-center justify-between gap-2 mb-1">
        <div className="flex items-center gap-1.5">
          <Cpu className={`w-4 h-4 ${isFired ? 'text-pulse' : 'text-mist-muted'}`} />
          <span className="text-[10px] uppercase font-mono tracking-wider font-semibold text-pulse">
            Rule • Pri: {data.metadata?.priority || 500}
          </span>
        </div>
        <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
          isFired ? 'bg-signal/20 text-signal' : 'bg-carbon-border text-mist-muted'
        }`}>
          {isFired ? 'FIRED' : 'UNSATISFIED'}
        </span>
      </div>
      <div className="font-semibold text-sm leading-tight text-mist">{data.label}</div>
      {data.sublabel && (
        <div className="text-[11px] font-mono mt-1 text-mist-muted">{data.sublabel}</div>
      )}
    </div>
  );
};

export const ConclusionNode: React.FC<{ data: GraphNodeData; selected?: boolean }> = ({ data, selected }) => {
  const tier = data.metadata?.tier || 'CONSULT_PHYSICIAN';
  const isEmergency = tier === 'EMERGENCY';

  return (
    <div className={`px-5 py-4 rounded-xl min-w-[260px] transition-all duration-200 ${
      selected ? 'ring-2 ring-signal shadow-xl shadow-signal/30' : ''
    } ${
      isEmergency
        ? 'bg-alert/20 border-2 border-alert text-mist animate-signal-pulse'
        : 'glass-panel border border-signal/50 text-mist'
    }`}>
      <Handle type="target" position={Position.Left} className="!bg-signal !w-3 !h-3 !border-void" />
      <div className="flex items-center justify-between gap-2 mb-1">
        <div className="flex items-center gap-1.5">
          <Sparkles className={`w-4 h-4 ${isEmergency ? 'text-alert' : 'text-signal'}`} />
          <span className={`text-[10px] uppercase font-mono tracking-wider font-semibold ${
            isEmergency ? 'text-alert' : 'text-signal'
          }`}>
            Conclusion • {tier}
          </span>
        </div>
        {data.metadata?.confidence && (
          <span className="text-[10px] font-mono text-mist-muted">
            {Math.round(data.metadata.confidence * 100)}% Conf
          </span>
        )}
      </div>
      <div className="font-bold text-sm leading-snug text-mist">{data.label}</div>
      {data.sublabel && (
        <div className="text-[11px] font-mono mt-1 text-mist-muted">{data.sublabel}</div>
      )}
    </div>
  );
};

export const SafetyNode: React.FC<{ data: GraphNodeData; selected?: boolean }> = ({ data, selected }) => {
  return (
    <div className={`px-5 py-4 rounded-xl min-w-[260px] bg-alert/20 border-2 border-alert text-mist transition-all duration-200 ${
      selected ? 'ring-2 ring-alert shadow-xl shadow-alert/40' : ''
    }`}>
      <Handle type="target" position={Position.Left} className="!bg-alert !w-3 !h-3 !border-void" />
      <Handle type="source" position={Position.Right} className="!bg-alert !w-3 !h-3 !border-void" />
      <div className="flex items-center gap-2 mb-1">
        <ShieldAlert className="w-5 h-5 text-alert animate-bounce" />
        <span className="text-[10px] uppercase font-mono tracking-wider font-bold text-alert">
          EMERGENCY RED FLAG
        </span>
      </div>
      <div className="font-bold text-sm text-mist">{data.label}</div>
      {data.sublabel && (
        <div className="text-[11px] font-mono mt-1 text-alert">{data.sublabel}</div>
      )}
    </div>
  );
};

