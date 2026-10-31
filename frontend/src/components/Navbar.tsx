import React, { useState } from 'react';
import { 
  Shield, 
  Sparkles, 
  Activity, 
  FileText, 
  Volume2, 
  VolumeX, 
  LogOut, 
  User as UserIcon,
  Sun,
  Moon,
  Type
} from 'lucide-react';
import { User } from '../types';
import { useTheme } from '../context/ThemeContext';

interface NavbarProps {
  currentRoute: string;
  navigate: (route: string) => void;
  user: User | null;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentRoute, navigate, user, onLogout }) => {
  const [ttsActive, setTtsActive] = useState(false);
  const { theme, toggleTheme, fontSize, setFontSize } = useTheme();

  const toggleTts = () => {
    if (!ttsActive) {
      if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance("Healix voice assistant enabled. Clinical guidance readouts active.");
        window.speechSynthesis.speak(u);
      }
      setTtsActive(true);
    } else {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setTtsActive(false);
    }
  };

  const cycleFontSize = () => {
    if (fontSize === 'sm') setFontSize('base');
    else if (fontSize === 'base') setFontSize('lg');
    else setFontSize('sm');
  };

  const navItems = user ? [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'assessment-new', label: 'Symptom Assessment', icon: Sparkles },
    { id: 'timeline', label: 'Health Timeline', icon: Activity },
    { id: 'reports', label: 'Clinical Reports', icon: FileText },
  ] : [
    { id: 'landing', label: 'Home', icon: Shield },
    { id: 'how-it-works', label: 'How It Works', icon: Activity },
    { id: 'about', label: 'Clinical Standards', icon: FileText },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-carbon-border glass-panel backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <div 
          onClick={() => navigate(user ? 'dashboard' : 'landing')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-xl bg-signal/15 border border-signal/40 flex items-center justify-center text-signal group-hover:scale-105 transition-transform">
            <Activity className="w-5 h-5 text-signal" />
          </div>
          <div>
            <span className="font-extrabold text-lg tracking-tight text-mist group-hover:text-signal transition-colors">
              HEALIX
            </span>
            <span className="hidden sm:inline-block ml-2 text-[10px] font-mono text-signal bg-signal/15 px-2 py-0.5 rounded-full border border-signal/25">
              CLINICAL GUIDANCE
            </span>
          </div>
        </div>

        {/* Navigation items */}
        <nav className="hidden md:flex items-center gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = currentRoute === item.id;
            return (
              <button
                key={item.id}
                onClick={() => navigate(item.id)}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  active 
                    ? 'bg-carbon-elevated border border-signal/50 text-signal font-semibold shadow-sm' 
                    : 'text-mist-muted hover:text-mist hover:bg-carbon'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${active ? 'text-signal' : 'text-mist-muted'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Action controls */}
        <div className="flex items-center gap-2">
          {/* Accessibility Font Size Toggle */}
          <button
            onClick={cycleFontSize}
            title={`Adjust text size (Current: ${fontSize.toUpperCase()})`}
            aria-label="Adjust text scaling"
            className="p-2 rounded-lg bg-carbon border border-carbon-border text-mist-muted hover:text-mist transition-colors flex items-center gap-1 text-xs font-mono font-semibold"
          >
            <Type className="w-3.5 h-3.5" />
            <span className="text-[11px] uppercase">{fontSize}</span>
          </button>

          {/* Theme Toggle (Dark / Light) */}
          <button
            onClick={toggleTheme}
            title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            aria-label="Toggle visual theme"
            className="p-2 rounded-lg bg-carbon border border-carbon-border text-mist-muted hover:text-mist transition-colors"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4 text-amber" /> : <Moon className="w-4 h-4 text-signal" />}
          </button>

          {/* TTS narrator toggle */}
          <button
            onClick={toggleTts}
            title={ttsActive ? 'Disable Audio Voice' : 'Enable Audio Voice Narrator'}
            aria-label="Toggle audio narrator"
            className={`p-2 rounded-lg border transition-colors ${
              ttsActive 
                ? 'bg-signal/20 border-signal text-signal' 
                : 'bg-carbon border-carbon-border text-mist-muted hover:text-mist'
            }`}
          >
            {ttsActive ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>

          {/* User Account / Auth buttons */}
          {user ? (
            <div className="flex items-center gap-2 pl-2 border-l border-carbon-border">
              <button 
                onClick={() => navigate('dashboard')}
                className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-carbon border border-carbon-border text-xs text-mist hover:border-signal/40 transition-colors"
              >
                <UserIcon className="w-3.5 h-3.5 text-signal" />
                <span className="max-w-[100px] truncate">{user.full_name}</span>
              </button>
              <button
                onClick={onLogout}
                title="Sign out"
                aria-label="Sign out"
                className="p-2 rounded-lg bg-carbon border border-carbon-border text-mist-muted hover:text-alert transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2 pl-2 border-l border-carbon-border">
              <button
                onClick={() => navigate('login')}
                className="px-3.5 py-1.5 text-xs font-semibold text-mist hover:text-signal transition-colors"
              >
                Sign In
              </button>
              <button
                onClick={() => navigate('register')}
                className="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-signal text-void hover:opacity-90 transition-opacity shadow-sm"
              >
                Get Started
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
