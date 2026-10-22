import React from "react";
import { Bot, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

export function ChatMessage({ message }) {
  const isAssistant = message.sender === "assistant";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className={`flex items-start gap-3 sm:gap-4 ${
        isAssistant ? "justify-start" : "justify-end"
      }`}
    >
      {/* Assistant Avatar */}
      {isAssistant && (
        <div className="w-8 h-8 rounded-xl bg-teal-700 text-white flex items-center justify-center shrink-0 shadow-xs border border-teal-500/20">
          <Bot className="w-4 h-4" />
        </div>
      )}

      {/* Message Bubble */}
      <div
        className={`max-w-[85%] sm:max-w-2xl rounded-2xl p-4 sm:p-5 text-sm leading-relaxed ${
          isAssistant
            ? "bg-white text-slate-800 border border-slate-200/80 shadow-xs"
            : "bg-slate-900 text-white shadow-xs"
        }`}
      >
        {/* Render markdown-like paragraphs and bullets */}
        <div className="space-y-2 whitespace-pre-line text-sm">
          {message.text}
        </div>

        {/* Clinical source citations if present */}
        {isAssistant && message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-1.5 text-[11px] text-slate-500">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-700 shrink-0" />
            <span className="font-semibold text-slate-500">Sources:</span>
            {message.sources.map((src, i) => (
              <span
                key={i}
                className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-50 border border-slate-200 text-slate-600 text-[10px]"
              >
                {src}
              </span>
            ))}
          </div>
        )}

        <div
          className={`text-[10px] mt-2 flex items-center justify-end ${
            isAssistant ? "text-slate-500" : "text-slate-500"
          }`}
        >
          <span>{message.timestamp}</span>
        </div>
      </div>

      {/* User Avatar */}
      {!isAssistant && (
        <div className="w-8 h-8 rounded-xl bg-slate-900 text-white font-semibold text-xs flex items-center justify-center shrink-0">
          U
        </div>
      )}
    </motion.div>
  );
}
