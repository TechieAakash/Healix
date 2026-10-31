import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { LandingPage } from './pages/LandingPage';
import { HowItWorksPage } from './pages/HowItWorksPage';
import { AboutPage } from './pages/AboutPage';
import { AuthPage } from './pages/AuthPages';
import { DashboardPage } from './pages/DashboardPage';
import { NewAssessmentPage } from './pages/NewAssessmentPage';
import { AssessmentResultPage } from './pages/AssessmentResultPage';
import { TimelinePage } from './pages/TimelinePage';
import { ReportsPage } from './pages/ReportsPage';
import { ThemeProvider } from './context/ThemeContext';
import { api } from './services/api';
import { User } from './types';
import { ShieldCheck, Activity } from 'lucide-react';

export const AppContent: React.FC = () => {
  const [currentRoute, setCurrentRoute] = useState<string>('landing');
  const [routeParam, setRouteParam] = useState<string | undefined>(undefined);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('healix_token');
    if (token) {
      api.getMe()
        .then((userData) => {
          setUser(userData);
          if (currentRoute === 'landing' || currentRoute === 'login' || currentRoute === 'register') {
            setCurrentRoute('dashboard');
          }
        })
        .catch(() => {
          localStorage.removeItem('healix_token');
          setUser(null);
        });
    }
  }, []);

  const navigate = (route: string, param?: string) => {
    setCurrentRoute(route);
    setRouteParam(param);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleAuthSuccess = (token: string, userData: any) => {
    localStorage.setItem('healix_token', token);
    setUser(userData);
    setCurrentRoute('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('healix_token');
    setUser(null);
    setCurrentRoute('landing');
  };

  return (
    <div className="min-h-screen flex flex-col bg-void text-mist transition-colors duration-200">
      <Navbar
        currentRoute={currentRoute}
        navigate={navigate}
        user={user}
        onLogout={handleLogout}
      />

      <main className="flex-1">
        {currentRoute === 'landing' && <LandingPage navigate={navigate} />}
        {currentRoute === 'how-it-works' && <HowItWorksPage navigate={navigate} />}
        {currentRoute === 'about' && <AboutPage navigate={navigate} />}
        {currentRoute === 'login' && (
          <AuthPage mode="login" navigate={navigate} onAuthSuccess={handleAuthSuccess} />
        )}
        {currentRoute === 'register' && (
          <AuthPage mode="register" navigate={navigate} onAuthSuccess={handleAuthSuccess} />
        )}
        {currentRoute === 'dashboard' && user && (
          <DashboardPage user={user} navigate={navigate} />
        )}
        {currentRoute === 'assessment-new' && (
          <NewAssessmentPage navigate={navigate} />
        )}
        {currentRoute === 'assessment-detail' && routeParam && (
          <AssessmentResultPage assessmentId={routeParam} navigate={navigate} />
        )}
        {currentRoute === 'timeline' && <TimelinePage />}
        {currentRoute === 'reports' && <ReportsPage navigate={navigate} />}
      </main>

      {/* Global Clinical Platform Footer */}
      <footer className="border-t border-carbon-border glass-panel py-10 px-4 mt-auto">
        <div className="max-w-6xl mx-auto space-y-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-mist-muted">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-lg bg-signal/15 border border-signal/30 flex items-center justify-center text-signal">
                <Activity className="w-3.5 h-3.5" />
              </div>
              <span className="font-extrabold text-mist tracking-tight">HEALIX</span>
              <span>• Intelligent Symptom Assessment & Clinical Guidance Platform</span>
            </div>

            <div className="flex items-center gap-5 text-xs font-medium">
              <button onClick={() => navigate('how-it-works')} className="hover:text-mist transition-colors">Clinical Architecture</button>
              <button onClick={() => navigate('about')} className="hover:text-mist transition-colors">Safety Standards</button>
              <button onClick={() => navigate(user ? 'assessment-new' : 'login')} className="text-signal hover:underline">Start Assessment</button>
            </div>
          </div>

          <div className="p-4 rounded-xl surface-card text-[11px] text-mist-muted flex items-start gap-3">
            <ShieldCheck className="w-4 h-4 text-signal shrink-0 mt-0.5" />
            <p className="leading-relaxed">
              <strong>Medical Disclaimer:</strong> Healix is an AI-assisted symptom assessment and decision-support tool. It does not provide medical diagnoses, write drug prescriptions, or replace formal consultation with a licensed healthcare practitioner. For life-threatening emergencies, dial 911 / 112 immediately.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
};
