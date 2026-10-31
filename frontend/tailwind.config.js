function withOpacity(variableName) {
  return ({ opacityValue }) => {
    if (opacityValue !== undefined) {
      return `rgb(var(${variableName}) / ${opacityValue})`;
    }
    return `rgb(var(${variableName}))`;
  };
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        void: withOpacity('--bg-primary'),
        carbon: withOpacity('--bg-surface'),
        'carbon-elevated': withOpacity('--bg-surface-elevated'),
        'carbon-glass': 'var(--bg-glass-style)',
        'carbon-border': withOpacity('--border-color'),
        'carbon-border-strong': withOpacity('--border-strong'),
        signal: withOpacity('--accent-teal'),
        'signal-glow': 'rgba(var(--accent-teal) / 0.22)',
        mint: withOpacity('--accent-mint'),
        'mint-glow': 'rgba(var(--accent-mint) / 0.20)',
        amber: withOpacity('--accent-amber'),
        'amber-glow': 'rgba(var(--accent-amber) / 0.20)',
        pulse: withOpacity('--pulse-indigo'),
        mist: withOpacity('--text-primary'),
        'mist-muted': withOpacity('--text-muted'),
        alert: withOpacity('--accent-rose'),
        'alert-glow': 'rgba(var(--accent-rose) / 0.25)'
      },
      backdropBlur: {
        xs: '2px',
        glass: '16px',
        deep: '24px'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace']
      }
    },
  },
  plugins: [],
}
