import React, { useState, useMemo } from 'react';
import { SymptomDefinition } from '../../types';
import { Search, Activity, AlertTriangle, Check } from 'lucide-react';

interface SymptomTagSelectorProps {
  symptoms: SymptomDefinition[];
  selectedSymptomIds: string[];
  onToggleSymptom: (id: string) => void;
}

const SYSTEM_NAMES: Record<string, string> = {
  ALL: 'All Pathways',
  NEUROLOGICAL: 'Head & Brain',
  RESPIRATORY: 'Respiratory',
  DIGESTIVE: 'Digestive & Belly',
  MUSCULOSKELETAL: 'Bones & Muscles',
  GENERAL: 'General & Constitutional'
};

export const SymptomTagSelector: React.FC<SymptomTagSelectorProps> = ({
  symptoms,
  selectedSymptomIds,
  onToggleSymptom
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeSystem, setActiveSystem] = useState('ALL');

  const filteredSymptoms = useMemo(() => {
    return symptoms.filter((s) => {
      const matchesSearch =
        s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.synonyms.some(syn => syn.toLowerCase().includes(searchTerm.toLowerCase())) ||
        s.description.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesSystem = activeSystem === 'ALL' || s.system === activeSystem;
      return matchesSearch && matchesSystem;
    });
  }, [symptoms, searchTerm, activeSystem]);

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h3 className="text-sm font-semibold text-mist flex items-center gap-2">
            <Activity className="w-4 h-4 text-signal" />
            Clinical Symptom Tags
          </h3>
          <p className="text-xs text-mist-muted">
            Select one or more symptoms that best match what you are feeling.
          </p>
        </div>

        {/* Search bar */}
        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-mist-muted" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search symptoms or aliases..."
            className="w-full pl-8 pr-3 py-1.5 rounded-lg text-xs border border-carbon-border text-mist placeholder:text-mist-muted/60 focus:outline-none"
          />
        </div>
      </div>

      {/* System Category Tabs */}
      <div className="flex flex-wrap gap-1.5 p-1 rounded-xl glass-panel">
        {['ALL', 'NEUROLOGICAL', 'RESPIRATORY', 'DIGESTIVE', 'MUSCULOSKELETAL', 'GENERAL'].map((sys) => {
          const isActive = activeSystem === sys;
          const count = sys === 'ALL' 
            ? selectedSymptomIds.length 
            : symptoms.filter(s => s.system === sys && selectedSymptomIds.includes(s.id)).length;

          return (
            <button
              key={sys}
              type="button"
              onClick={() => setActiveSystem(sys)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
                isActive
                  ? 'bg-signal/20 text-signal border border-signal/40 font-semibold shadow-sm'
                  : 'text-mist-muted hover:text-mist hover:bg-carbon'
              }`}
            >
              <span>{SYSTEM_NAMES[sys] || sys}</span>
              {count > 0 && (
                <span className="w-4 h-4 rounded-full bg-signal text-void text-[10px] font-bold flex items-center justify-center">
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Symptoms Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
        {filteredSymptoms.map((sym) => {
          const isSelected = selectedSymptomIds.includes(sym.id);
          return (
            <button
              key={sym.id}
              type="button"
              onClick={() => onToggleSymptom(sym.id)}
              className={`p-3 rounded-xl border text-left transition-all flex flex-col justify-between gap-2 ${
                isSelected
                  ? 'bg-signal/15 border-signal text-mist shadow-sm ring-1 ring-signal/30'
                  : 'surface-card border-carbon-border hover:border-carbon-border-strong text-mist-muted hover:text-mist'
              }`}
            >
              <div className="flex items-start justify-between gap-2 w-full">
                <span className={`text-xs font-semibold ${isSelected ? 'text-signal' : 'text-mist'}`}>
                  {sym.name}
                </span>
                <div className="flex items-center gap-1">
                  {sym.is_emergency_candidate && (
                    <span title="Red-flag screening candidate" className="text-amber">
                      <AlertTriangle className="w-3.5 h-3.5" />
                    </span>
                  )}
                  <div
                    className={`w-4 h-4 rounded flex items-center justify-center shrink-0 border ${
                      isSelected
                        ? 'bg-signal border-signal text-void'
                        : 'border-carbon-border'
                    }`}
                  >
                    {isSelected && <Check className="w-3 h-3 stroke-[3]" />}
                  </div>
                </div>
              </div>

              <p className="text-[11px] text-mist-muted line-clamp-2 leading-relaxed">
                {sym.description}
              </p>

              {sym.synonyms.length > 0 && (
                <div className="text-[10px] text-mist-muted/70 flex flex-wrap gap-1 mt-1">
                  {sym.synonyms.slice(0, 3).map((syn, idx) => (
                    <span key={idx} className="bg-carbon px-1.5 py-0.5 rounded border border-carbon-border">
                      {syn}
                    </span>
                  ))}
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Selected tags chip preview */}
      {selectedSymptomIds.length > 0 && (
        <div className="pt-2 flex flex-wrap items-center gap-1.5">
          <span className="text-[11px] text-mist-muted">Selected symptoms:</span>
          {selectedSymptomIds.map(id => {
            const sym = symptoms.find(s => s.id === id);
            if (!sym) return null;
            return (
              <span
                key={id}
                onClick={() => onToggleSymptom(id)}
                className="cursor-pointer text-xs px-2.5 py-0.5 rounded-full bg-signal/10 border border-signal/30 text-signal hover:bg-alert/20 hover:text-alert hover:border-alert/40 transition-colors flex items-center gap-1"
                title="Click to remove"
              >
                {sym.name}
                <span className="text-[10px]">×</span>
              </span>
            );
          })}
        </div>
      )}
    </div>
  );
};

