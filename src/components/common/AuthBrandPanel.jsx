import React from "react";
import { Activity, Bot, HeartHandshake } from "lucide-react";
import { HealixLogo } from "./HealixLogo";

export function AuthBrandPanel() {
  const features = [
    {
      title: "Track your health",
      desc: "Get insights from your data",
      icon: Activity,
    },
    {
      title: "AI health assistant",
      desc: "Ask anything, anytime",
      icon: Bot,
    },
    {
      title: "Personalized care plans",
      desc: "Built for your goals",
      icon: HeartHandshake,
    },
  ];

  return (
    <div className="relative hidden lg:flex flex-col justify-between w-1/2 p-12 overflow-hidden bg-gradient-to-br from-[#e4f4ea] via-[#edf8f1] to-[#d8efe2]">
      {/* Nature / Mountain Mist Backdrop Graphic */}
      <div className="absolute inset-0 pointer-events-none opacity-60">
        <svg
          viewBox="0 0 600 800"
          className="w-full h-full object-cover"
          preserveAspectRatio="xMidYMax slice"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Layered distant misty hills */}
          <path
            d="M0 450 C120 420 220 480 340 440 C460 400 520 430 600 410 L600 800 L0 800 Z"
            fill="#cbe6d5"
            fillOpacity="0.45"
          />
          <path
            d="M0 520 C140 490 260 550 380 500 C480 460 540 510 600 490 L600 800 L0 800 Z"
            fill="#b5dbbe"
            fillOpacity="0.5"
          />
          <path
            d="M0 600 C150 570 240 630 390 580 C500 550 550 590 600 570 L600 800 L0 800 Z"
            fill="#9ccca7"
            fillOpacity="0.5"
          />
          {/* Botanical leaf silhouettes on foreground */}
          <path
            d="M-40 820 C-10 720 40 680 80 690 C120 700 80 770 40 820 Z"
            fill="#2d6a4f"
            fillOpacity="0.25"
          />
          <path
            d="M30 840 C70 730 140 700 170 730 C190 760 140 810 90 850 Z"
            fill="#1b4332"
            fillOpacity="0.2"
          />
        </svg>
      </div>

      {/* Top Brand Logo */}
      <div className="relative z-10">
        <HealixLogo size={36} textClassName="text-2xl font-bold text-emerald-950 tracking-tight" />
      </div>

      {/* Center Hero Copy + Feature List */}
      <div className="relative z-10 my-auto py-8 max-w-md">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-emerald-950 tracking-tight leading-tight">
          Better Health. Brighter You.
        </h1>
        <p className="mt-3 text-sm text-emerald-900/75 leading-relaxed">
          Your AI-powered health companion for a healthier, happier life.
        </p>

        <div className="mt-10 space-y-5">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div key={idx} className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-full bg-white/80 border border-emerald-200/80 shadow-xs flex items-center justify-center text-emerald-800 shrink-0">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-sm font-semibold text-emerald-950">{feat.title}</h2>
                  <p className="text-xs text-emerald-800/80">{feat.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Footer copyright */}
      <div className="relative z-10 text-xs text-emerald-900/60">
        © 2026 Healix Health. All rights reserved.
      </div>
    </div>
  );
}
