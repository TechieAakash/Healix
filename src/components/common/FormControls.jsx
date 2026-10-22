import React, { useId } from "react";

export function Input({
  label,
  id,
  type = "text",
  error,
  helperText,
  icon: Icon,
  className = "",
  containerClassName = "",
  required = false,
  ...props
}) {
  const generatedId = useId();
  const inputId = id || generatedId;

  return (
    <div className={`w-full ${containerClassName}`}>
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-slate-700 mb-1.5"
        >
          {label} {required && <span className="text-teal-500">*</span>}
        </label>
      )}
      <div className="relative rounded-xl shadow-xs">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
            <Icon className="w-4 h-4" />
          </div>
        )}
        <input
          id={inputId}
          type={type}
          className={`block w-full rounded-xl border bg-white text-slate-900 placeholder:text-slate-500 text-sm transition-all focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600 disabled:bg-slate-50 disabled:text-slate-500 py-2.5 ${
            Icon ? "pl-10 pr-3.5" : "px-3.5"
          } ${
            error
              ? "border-teal-400 text-teal-900 focus:border-teal-500 focus:ring-teal-500/20"
              : "border-slate-200 hover:border-slate-300"
          } ${className}`}
          {...props}
        />
      </div>
      {error && <p className="mt-1 text-xs text-teal-600 font-medium">{error}</p>}
      {!error && helperText && (
        <p className="mt-1 text-xs text-slate-500">{helperText}</p>
      )}
    </div>
  );
}

export function TextArea({
  label,
  id,
  error,
  helperText,
  rows = 4,
  className = "",
  containerClassName = "",
  required = false,
  ...props
}) {
  const generatedId = useId();
  const inputId = id || generatedId;

  return (
    <div className={`w-full ${containerClassName}`}>
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-slate-700 mb-1.5"
        >
          {label} {required && <span className="text-teal-500">*</span>}
        </label>
      )}
      <textarea
        id={inputId}
        rows={rows}
        className={`block w-full rounded-xl border bg-white text-slate-900 placeholder:text-slate-500 text-sm transition-all focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600 disabled:bg-slate-50 disabled:text-slate-500 px-3.5 py-2.5 resize-y ${
          error
            ? "border-teal-400 text-teal-900 focus:border-teal-500 focus:ring-teal-500/20"
            : "border-slate-200 hover:border-slate-300"
        } ${className}`}
        {...props}
      />
      {error && <p className="mt-1 text-xs text-teal-600 font-medium">{error}</p>}
      {!error && helperText && (
        <p className="mt-1 text-xs text-slate-500">{helperText}</p>
      )}
    </div>
  );
}

export function Select({
  label,
  id,
  options = [],
  error,
  helperText,
  className = "",
  containerClassName = "",
  ...props
}) {
  const generatedId = useId();
  const inputId = id || generatedId;

  return (
    <div className={`w-full ${containerClassName}`}>
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-slate-700 mb-1.5"
        >
          {label}
        </label>
      )}
      <select
        id={inputId}
        className={`block w-full rounded-xl border bg-white text-slate-900 text-sm transition-all focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600 px-3.5 py-2.5 ${
          error
            ? "border-teal-400 text-teal-900"
            : "border-slate-200 hover:border-slate-300"
        } ${className}`}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-xs text-teal-600 font-medium">{error}</p>}
      {!error && helperText && (
        <p className="mt-1 text-xs text-slate-500">{helperText}</p>
      )}
    </div>
  );
}
