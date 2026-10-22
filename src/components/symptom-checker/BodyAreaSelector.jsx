import React from "react";
import { bodyAreas } from "../../data/mockData";
import { Brain, Heart, Shield, Move, Activity, User, Mic } from "lucide-react";

export function BodyAreaSelector({ selectedArea, onSelectArea }) {
  const iconMap = {
    head: Brain,
    throat: Mic,
    chest: Heart,
    abdomen: Shield,
    back: Activity,
    limbs: Move,
    general: User,
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Interactive Stylized Body Schematic SVG */}
        <div className="lg:col-span-5 flex flex-col items-center justify-center p-6 bg-slate-50/80 rounded-2xl border border-slate-200">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4">
            Interactive Body Hotspots
          </p>

          <div className="relative w-48 h-80 flex items-center justify-center select-none">
            {/* SVG Silhouette */}
            <svg
              viewBox="0 0 200 340"
              className="w-full h-full drop-shadow-xs transition-all"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Head */}
              <circle
                cx="100"
                cy="36"
                r="24"
                className={`transition-all cursor-pointer ${
                  selectedArea === "head"
                    ? "fill-teal-500 stroke-teal-700 stroke-2"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("head")}
              />

              {/* Neck & Throat */}
              <rect
                x="92"
                y="60"
                width="16"
                height="14"
                rx="3"
                className={`transition-all cursor-pointer ${
                  selectedArea === "throat"
                    ? "fill-teal-500 stroke-teal-700 stroke-2"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("throat")}
              />

              {/* Chest */}
              <path
                d="M 66 74 C 70 74 130 74 134 74 C 142 86 142 120 130 130 C 115 132 85 132 70 130 C 58 120 58 86 66 74 Z"
                className={`transition-all cursor-pointer ${
                  selectedArea === "chest"
                    ? "fill-teal-500 stroke-teal-700 stroke-2"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("chest")}
              />

              {/* Abdomen */}
              <path
                d="M 72 133 C 80 133 120 133 128 133 C 132 155 132 180 124 190 C 112 192 88 192 76 190 C 68 180 68 155 72 133 Z"
                className={`transition-all cursor-pointer ${
                  selectedArea === "abdomen"
                    ? "fill-teal-500 stroke-teal-700 stroke-2"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("abdomen")}
              />

              {/* Arms (Left & Right) */}
              <path
                d="M 58 82 C 45 105 38 140 34 180 C 31 190 35 195 40 190 C 46 150 52 115 62 90 Z"
                className={`transition-all cursor-pointer ${
                  selectedArea === "limbs"
                    ? "fill-teal-500 stroke-teal-700"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("limbs")}
              />
              <path
                d="M 142 82 C 155 105 162 140 166 180 C 169 190 165 195 160 190 C 154 150 148 115 138 90 Z"
                className={`transition-all cursor-pointer ${
                  selectedArea === "limbs"
                    ? "fill-teal-500 stroke-teal-700"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("limbs")}
              />

              {/* Legs (Left & Right) */}
              <path
                d="M 78 194 C 84 235 84 275 80 320 C 78 328 88 330 92 322 C 98 280 100 240 96 194 Z"
                className={`transition-all cursor-pointer ${
                  selectedArea === "limbs"
                    ? "fill-teal-500 stroke-teal-700"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("limbs")}
              />
              <path
                d="M 104 194 C 100 240 102 280 108 322 C 112 330 122 328 120 320 C 116 275 116 235 122 194 Z"
                className={`transition-all cursor-pointer ${
                  selectedArea === "limbs"
                    ? "fill-teal-500 stroke-teal-700"
                    : "fill-slate-200 hover:fill-teal-200 stroke-slate-300"
                }`}
                onClick={() => onSelectArea("limbs")}
              />
            </svg>

            {/* Quick Helper Floating Badges */}
            <div className="absolute bottom-2 text-center text-[11px] text-slate-500 font-medium">
              Click any zone or list on the right
            </div>
          </div>
        </div>

        {/* Body Area Cards Grid */}
        <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-3">
          {bodyAreas.map((area) => {
            const Icon = iconMap[area.id] || User;
            const isSelected = selectedArea === area.id;

            return (
              <button
                type="button"
                key={area.id}
                onClick={() => onSelectArea(area.id)}
                className={`text-left p-3.5 rounded-xl border transition-all cursor-pointer flex items-start gap-3 ${
                  isSelected
                    ? "border-teal-600 bg-teal-50/70 ring-2 ring-teal-500/20 shadow-xs"
                    : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/60"
                }`}
              >
                <div
                  className={`p-2 rounded-lg shrink-0 ${
                    isSelected ? "bg-teal-700 text-white" : "bg-slate-100 text-slate-600"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>
                <div>
                  <h4
                    className={`text-xs font-semibold ${
                      isSelected ? "text-teal-900" : "text-slate-900"
                    }`}
                  >
                    {area.label}
                  </h4>
                  <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">
                    {area.description}
                  </p>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
