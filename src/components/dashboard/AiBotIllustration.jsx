import React from "react";

export function AiBotIllustration({ className = "w-40 h-28" }) {
  return (
    <svg
      viewBox="0 0 200 140"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Soft botanical leaves in background */}
      <path
        d="M170 120 C185 85 175 45 150 30 C155 60 145 95 130 115 Z"
        fill="#a7d7b8"
        opacity="0.7"
      />
      <path
        d="M185 130 C200 100 195 65 170 50 C175 80 165 110 150 125 Z"
        fill="#82c79b"
        opacity="0.6"
      />
      <path
        d="M130 135 C115 105 125 70 150 55 C145 85 155 115 170 130 Z"
        fill="#5cae7c"
        opacity="0.4"
      />
      <path
        d="M110 135 C100 115 110 90 130 80 C125 100 135 120 145 130 Z"
        fill="#3d9961"
        opacity="0.3"
      />

      {/* Robot Antenna */}
      <circle cx="95" cy="40" r="5" fill="#059669" />
      <rect x="93" y="44" width="4" height="12" rx="2" fill="#047857" />

      {/* Robot Head Body */}
      <rect
        x="60"
        y="54"
        width="70"
        height="54"
        rx="20"
        fill="#ffffff"
        stroke="#059669"
        strokeWidth="3.5"
      />

      {/* Screen Face */}
      <rect
        x="68"
        y="62"
        width="54"
        height="38"
        rx="14"
        fill="#e6f7ef"
      />

      {/* Smiling Friendly Eyes */}
      <path
        d="M78 77 C78 73 84 73 84 77"
        stroke="#047857"
        strokeWidth="3"
        strokeLinecap="round"
      />
      <path
        d="M106 77 C106 73 112 73 112 77"
        stroke="#047857"
        strokeWidth="3"
        strokeLinecap="round"
      />

      {/* Cute Smile */}
      <path
        d="M91 85 C93 88 97 88 99 85"
        stroke="#047857"
        strokeWidth="2.5"
        strokeLinecap="round"
      />

      {/* Blushing cheeks */}
      <ellipse cx="76" cy="85" rx="3.5" ry="2" fill="#fca5a5" opacity="0.6" />
      <ellipse cx="114" cy="85" rx="3.5" ry="2" fill="#fca5a5" opacity="0.6" />

      {/* Cute Ears / Side nubs */}
      <rect x="54" y="70" width="6" height="14" rx="3" fill="#059669" />
      <rect x="130" y="70" width="6" height="14" rx="3" fill="#059669" />
    </svg>
  );
}
