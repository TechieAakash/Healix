import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import { Button } from "../components/common/Button";
import { Input } from "../components/common/FormControls";
import { Card } from "../components/common/Card";
import { HeartPulse, Mail, Lock, ArrowRight, ShieldCheck, CheckCircle2 } from "lucide-react";

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const validate = () => {
    const errs = {};
    if (!email.trim()) {
      errs.email = "Email address is required";
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errs.email = "Please enter a valid email address";
    }
    if (!password) {
      errs.password = "Password is required";
    } else if (password.length < 6) {
      errs.password = "Password must be at least 6 characters";
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setErrors({});
    try {
      await authService.login(email, password);
      setSuccess(true);
      setTimeout(() => {
        navigate("/dashboard");
      }, 700);
    } catch (err) {
      setErrors({ form: err.message || "Failed to log in. Please check your credentials." });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = () => {
    setEmail("aakash@example.com");
    setPassword("healix1234");
  };

  return (
    <div className="min-h-[80vh] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link to="/" className="inline-flex items-center gap-2.5 mb-6">
          <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
            <HeartPulse className="w-6 h-6" />
          </div>
          <span className="font-bold text-2xl text-slate-900 tracking-tight">Healix</span>
        </Link>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          Welcome back to Healix
        </h2>
        <p className="mt-2 text-xs sm:text-sm text-slate-500">
          Access your personalized symptom history and clinical summaries.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card padding="default" className="shadow-lg border-slate-200">
          {success ? (
            <div className="py-8 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Signed In Successfully</h3>
              <p className="text-xs text-slate-500">Redirecting to your dashboard...</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {errors.form && (
                <div className="p-3 bg-rose-50 text-rose-700 text-xs rounded-xl border border-rose-200">
                  {errors.form}
                </div>
              )}

              <Input
                label="Email Address"
                type="email"
                placeholder="aakash@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={errors.email}
                icon={Mail}
                required
              />

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-sm font-medium text-slate-700">
                    Password <span className="text-rose-500">*</span>
                  </label>
                  <Link
                    to="/forgot-password"
                    className="text-xs text-teal-700 hover:text-teal-800 font-medium"
                  >
                    Forgot password?
                  </Link>
                </div>
                <Input
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  error={errors.password}
                  icon={Lock}
                  required
                />
              </div>

              <div className="pt-2">
                <Button
                  type="submit"
                  variant="teal"
                  size="md"
                  className="w-full"
                  isLoading={isLoading}
                  icon={ArrowRight}
                  iconPosition="right"
                >
                  Continue
                </Button>
              </div>

              {/* Quick Demo Fill button */}
              <div className="text-center pt-2">
                <button
                  type="button"
                  onClick={handleDemoLogin}
                  className="text-xs text-slate-500 hover:text-slate-800 underline underline-offset-4 cursor-pointer"
                >
                  Fill with demo account (Aakash)
                </button>
              </div>

              {/* Social Login Placeholders */}
              <div className="pt-4 mt-4 border-t border-slate-100">
                <p className="text-[11px] text-center text-slate-400 uppercase tracking-wider mb-3">
                  Or continue with
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    className="flex items-center justify-center gap-2 py-2 px-3 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors"
                  >
                    <svg className="w-4 h-4" viewBox="0 0 24 24">
                      <path
                        fill="#4285F4"
                        d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.65v3h3.88c2.27-2.09 3.66-5.17 3.66-9.09z"
                      />
                      <path
                        fill="#34A853"
                        d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.1A11.996 11.996 0 0012 24z"
                      />
                      <path
                        fill="#FBBC05"
                        d="M5.28 14.32c-.25-.72-.38-1.49-.38-2.32 0-.83.13-1.6.38-2.32V6.58H1.25A11.996 11.996 0 000 12c0 1.92.45 3.74 1.25 5.42l4.03-3.1z"
                      />
                      <path
                        fill="#EA4335"
                        d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.39 0 3.45 2.64 1.25 6.58l4.03 3.1c.95-2.83 3.6-4.93 6.72-4.93z"
                      />
                    </svg>
                    Google
                  </button>
                  <button
                    type="button"
                    className="flex items-center justify-center gap-2 py-2 px-3 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors"
                  >
                    <svg className="w-4 h-4 fill-current text-slate-900" viewBox="0 0 24 24">
                      <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.63-.76 1.06-1.82.94-2.87-.91.04-2.02.6-2.67 1.36-.58.67-.99 1.76-.85 2.78 1.02.08 2.05-.51 2.58-1.27z" />
                    </svg>
                    Apple
                  </button>
                </div>
              </div>
            </form>
          )}

          <div className="mt-6 text-center text-xs text-slate-500">
            Don't have an account?{" "}
            <Link to="/signup" className="text-teal-700 font-semibold hover:text-teal-800">
              Create an account
            </Link>
          </div>
        </Card>

        <div className="mt-6 text-center flex items-center justify-center gap-1.5 text-xs text-slate-400">
          <ShieldCheck className="w-4 h-4 text-teal-600" />
          <span>Encrypted patient credentials</span>
        </div>
      </div>
    </div>
  );
}
