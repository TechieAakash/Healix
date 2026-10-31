import React, { useState } from 'react';
import { AnatomicalLocation } from '../../types';
import { MapPin, Check, Sparkles } from 'lucide-react';

interface AnatomicalRegionSelectorProps {
  locations: AnatomicalLocation[];
  selectedLocationIds: string[];
  onToggleLocation: (id: string) => void;
}

const SYSTEM_LABELS: Record<string, string> = {
  HEAD: 'Head & Neck',
  CHEST: 'Chest & Lungs',
  ABDOMEN: 'Abdomen & Pelvis',
  SPINE: 'Spine & Back',
  EXTREMITIES: 'Limbs & Joints',
  GENERAL: 'Generalized'
};

export const AnatomicalRegionSelector: React.FC<AnatomicalRegionSelectorProps> = ({
  locations,
  selectedLocationIds,
  onToggleLocation,
}) => {
  const [activeSystem, setActiveSystem] = useState<string>('HEAD');

  // Group locations by system
  const systems = Array.from(new Set(locations.map(l => l.system)));
  const currentLocations = locations.filter(l => l.system === activeSystem);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-mist flex items-center gap-2">
            <MapPin className="w-4 h-4 text-signal" />
            Anatomical Body Region Selector
          </h3>
          <p className="text-xs text-mist-muted">
            Pinpoint where your symptoms are localized to help differential accuracy.
          </p>
        </div>
        {selectedLocationIds.length > 0 && (
          <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-signal/15 text-signal border border-signal/30">
            {selectedLocationIds.length} selected
          </span>
        )}
      </div>

      {/* System Tabs */}
      <div className="flex flex-wrap gap-1.5 p-1 rounded-xl glass-panel">
        {systems.map((sys) => {
          const countInSys = locations.filter(l => l.system === sys && selectedLocationIds.includes(l.id)).length;
          const isActive = activeSystem === sys;
          return (
            <button
              key={sys}
              type="button"
              onClick={() => setActiveSystem(sys)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
                isActive
                  ? 'bg-signal/20 text-signal border border-signal/40 shadow-sm font-semibold'
                  : 'text-mist-muted hover:text-mist hover:bg-carbon'
              }`}
            >
              <span>{SYSTEM_LABELS[sys] || sys}</span>
              {countInSys > 0 && (
                <span className="w-4 h-4 rounded-full bg-signal text-void text-[10px] font-bold flex items-center justify-center">
                  {countInSys}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Location Grid for Active System */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
        {currentLocations.map((loc) => {
          const isSelected = selectedLocationIds.includes(loc.id);
          return (
            <button
              key={loc.id}
              type="button"
              onClick={() => onToggleLocation(loc.id)}
              className={`p-3 rounded-xl border text-left transition-all flex items-start justify-between gap-2 ${
                isSelected
                  ? 'bg-signal/15 border-signal text-mist shadow-sm'
                  : 'surface-card border-carbon-border hover:border-carbon-border-strong text-mist-muted hover:text-mist'
              }`}
            >
              <div>
                <div className={`text-xs font-semibold ${isSelected ? 'text-signal' : 'text-mist'}`}>
                  {loc.name}
                </div>
                <div className="text-[11px] text-mist-muted line-clamp-1 mt-0.5">
                  {loc.description}
                </div>
              </div>
              <div
                className={`w-5 h-5 rounded-md flex items-center justify-center shrink-0 border transition-all ${
                  isSelected
                    ? 'bg-signal border-signal text-void'
                    : 'border-carbon-border'
                }`}
              >
                {isSelected && <Check className="w-3.5 h-3.5 stroke-[3]" />}
              </div>
            </button>
          );
        })}
      </div>

      {/* Selected tags chip preview */}
      {selectedLocationIds.length > 0 && (
        <div className="pt-2 flex flex-wrap items-center gap-1.5">
          <span className="text-[11px] text-mist-muted">Selected locations:</span>
          {selectedLocationIds.map(id => {
            const l = locations.find(loc => loc.id === id);
            if (!l) return null;
            return (
              <span
                key={id}
                onClick={() => onToggleLocation(id)}
                className="cursor-pointer text-xs px-2.5 py-0.5 rounded-full bg-signal/10 border border-signal/30 text-signal hover:bg-alert/20 hover:text-alert hover:border-alert/40 transition-colors flex items-center gap-1"
                title="Click to remove"
              >
                {l.name}
                <span className="text-[10px]">×</span>
              </span>
            );
          })}
        </div>
      )}
    </div>
  );
};

