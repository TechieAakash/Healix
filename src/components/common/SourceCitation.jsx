import React from "react";
import { ExternalLink, ShieldCheck } from "lucide-react";

export function SourceCitation({ sources = [], className = "" }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className={`rounded-2xl bg-slate-50/80 border border-slate-200/80 p-5 ${className}`}>
      <div className="flex items-center gap-2 mb-3">
        <ShieldCheck className="w-4 h-4 text-teal-700" />
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-700">
          Curated Medical Sources & Citations
        </h4>
      </div>
      <p className="text-xs text-slate-500 mb-3 leading-relaxed">
        These references were returned by the assessment workflow. They are provided for additional reading and do not replace professional medical advice.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {sources.map((src, idx) => {
          const isObj = typeof src === "object" && src !== null;
          const name = isObj ? src.name : src;
          const topic = isObj ? src.topic : "Clinical Guidance Documentation";
          const authority = isObj ? src.authority : "";
          const url = isObj && src.url ? src.url : "";
          const Tag = url ? "a" : "div";

          return (
            <Tag
              key={idx}
              {...(url ? { href: url, target: "_blank", rel: "noopener noreferrer" } : {})}
              className="flex flex-col justify-between p-3.5 bg-white rounded-xl border border-slate-200 hover:border-teal-500 hover:shadow-xs transition-all group"
            >
              <div>
                <div className="flex items-center justify-between text-xs font-semibold text-slate-900 group-hover:text-teal-700">
                  <span>{name}</span>
                  {url && <ExternalLink className="w-3 h-3 text-slate-500 group-hover:text-teal-700 transition-colors" />}
                </div>
                {topic && <p className="text-xs text-slate-600 mt-1 line-clamp-2">{topic}</p>}
              </div>
              {authority && (
                <div className="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                  <span>{authority}</span>
                </div>
              )}
            </Tag>
          );
        })}
      </div>
    </div>
  );
}
