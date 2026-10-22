import React from "react";
import { Sparkles } from "lucide-react";

export function SuggestedQuestions({ onSelectQuestion, questions = [] }) {
  const defaultQuestions = [
    "Could it be dehydration?",
    "When should I see a doctor?",
    "What information should I track?",
    "How does tension headache differ from a migraine?",
  ];

  const list = questions.length > 0 ? questions : defaultQuestions;

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500">
        <Sparkles className="w-3.5 h-3.5 text-teal-700" />
        <span>Suggested clinical questions:</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {list.map((q, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => onSelectQuestion(q)}
            className="text-xs px-3 py-1.5 rounded-xl bg-white border border-slate-200 text-slate-700 hover:border-teal-500 hover:text-teal-800 hover:bg-teal-50/50 transition-all text-left shadow-2xs cursor-pointer"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
