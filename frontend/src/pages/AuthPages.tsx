import React, { useState } from 'react';
import { Shield, Sparkles, AlertCircle, ArrowRight, Check } from 'lucide-react';
import { api } from '../services/api';

interface AuthPageProps {
  mode: 'login' | 'register';
  navigate: (route: string) => void;
  onAuthSuccess: (token: string, user: any) => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ mode, navigate, onAuthSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [dob, setDob] = useState('2001-04-12');
  const [sex, setSex] = useState('FEMALE');
  const [consent, setConsent] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === 'login') {
        const res = await api.login(email, password);
        onAuthSuccess(res.access_token, {
          id: res.user_id,
          email: res.email,
          full_name: res.full_name
        });
      } else {
        if (!consent) {
          setError('You must acknowledge the clinical safety disclaimer.');
          setLoading(false);
          return;
        }
        const res = await api.register({
          email,
          password,
          full_name: fullName,
          date_of_birth: dob,
          biological_sex: sex
        });
        onAuthSuccess(res.access_token, {
          id: res.user_id,
          email: res.email,
          full_name: res.full_name
        });
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const fillDemoCredentials = () => {
    setEmail('demo@healix.ai');
    setPassword('HealixDemo2026!');
  };

  return (
    <div className="max-w-md mx-auto px-4 py-16">
      <div className="glass-panel p-8 rounded-3xl border border-carbon-border space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-signal/10 border border-signal/30 text-signal text-xs font-mono">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Secure Access</span>
          </div>
          <h2 className="text-2xl font-bold text-mist">
            {mode === 'login' ? 'Welcome Back to Healix' : 'Create Your Health Vault'}
          </h2>
          <p className="text-xs text-mist-muted">
            {mode === 'login' ? 'Enter credentials to access your assessment timeline' : 'Deterministic explainable AI triage with tenant data protection'}
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-alert/15 border border-alert/40 text-mist text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-alert shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'register' && (
            <div>
              <label className="block text-xs font-mono text-mist-muted mb-1">Full Name</label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Ananya Sharma"
                className="w-full px-3.5 py-2.5 rounded-xl border border-carbon-border text-sm focus:outline-none focus:border-signal"
              />
            </div>
          )}

          <div>
            <label className="block text-xs font-mono text-mist-muted mb-1">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@example.com"
              className="w-full px-3.5 py-2.5 rounded-xl border border-carbon-border text-sm focus:outline-none focus:border-signal"
            />
          </div>

          <div>
            <label className="block text-xs font-mono text-mist-muted mb-1">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              className="w-full px-3.5 py-2.5 rounded-xl border border-carbon-border text-sm focus:outline-none focus:border-signal"
            />
          </div>

          {mode === 'register' && (
            <div className="space-y-3 pt-2">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-mono text-mist-muted mb-1">Birth Date</label>
                  <input
                    type="date"
                    value={dob}
                    onChange={(e) => setDob(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-carbon-border text-xs focus:outline-none focus:border-signal"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-mist-muted mb-1">Sex</label>
                  <select
                    value={sex}
                    onChange={(e) => setSex(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-carbon-border text-xs focus:outline-none focus:border-signal"
                  >
                    <option value="FEMALE">Female</option>
                    <option value="MALE">Male</option>
                    <option value="OTHER">Other / Prefer not to say</option>
                  </select>
                </div>
              </div>

              <label className="flex items-start gap-2 pt-2 cursor-pointer text-xs text-mist-muted">
                <input
                  type="checkbox"
                  checked={consent}
                  onChange={(e) => setConsent(e.target.checked)}
                  className="mt-0.5 rounded border-carbon-border text-signal focus:ring-signal"
                />
                <span>
                  I understand Healix is an educational decision-support tool, not an emergency doctor or licensed medical prescriber.
                </span>
              </label>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-signal text-void font-bold text-sm hover:bg-signal/90 disabled:opacity-50 transition-all flex items-center justify-center gap-2 shadow-lg shadow-signal/20 mt-4"
          >
            <span>{loading ? 'Processing...' : mode === 'login' ? 'Sign In' : 'Create Account'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {mode === 'login' && (
          <div className="pt-2 text-center">
            <button
              onClick={fillDemoCredentials}
              className="text-xs font-mono text-signal hover:underline"
            >
              ⚡ Fill 1-Click Demo Credentials (demo@healix.ai)
            </button>
          </div>
        )}

        <div className="pt-4 border-t border-carbon-border text-center text-xs text-mist-muted">
          {mode === 'login' ? (
            <span>
              Don't have an account?{' '}
              <button onClick={() => navigate('register')} className="text-signal font-semibold hover:underline">
                Register
              </button>
            </span>
          ) : (
            <span>
              Already registered?{' '}
              <button onClick={() => navigate('login')} className="text-signal font-semibold hover:underline">
                Sign In
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

