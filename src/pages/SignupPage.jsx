import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import { Button } from "../components/common/Button";
import { Input } from "../components/common/FormControls";
import { Card } from "../components/common/Card";
import { HeartPulse, Mail, Lock, User, ArrowRight, ShieldCheck, CheckCircle2 } from "lucide-react";

export function SignupPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    termsAccepted: false,
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const validate = () => {
    const errs = {};
    if (!formData.name.trim()) errs.name = "Full name is required";
    if (!formData.email.trim()) {
      errs.email = "Email address is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errs.email = "Please enter a valid email address";
    }
    if (!formData.password) {
      errs.password = "Password is required";
    } else if (formData.password.length < 6) {
      errs.password = "Password must be at least 6 characters";
    }
    if (formData.password !== formData.confirmPassword) {
      errs.confirmPassword = "Passwords do not match";
    }
    if (!formData.termsAccepted) {
      errs.terms = "You must agree to the Terms of Service & Privacy Policy";
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
      await authService.signup(formData);
      setSuccess(true);
      setTimeout(() => {
        navigate("/dashboard");
      }, 900);
    } catch (err) {
      setErrors({ form: err.message || "Could not register account. Please try again." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link to="/" className="inline-flex items-center gap-2.5 mb-6">
          <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
            <HeartPulse className="w-6 h-6" />
          </div>
          <span className="font-bold text-2xl text-slate-900 tracking-tight">Healix</span>
        </Link>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          Create your Healix account
        </h2>
        <p className="mt-2 text-xs sm:text-sm text-slate-500">
          Track health observations and access AI triage guidance.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card padding="default" className="shadow-lg border-slate-200">
          {success ? (
            <div className="py-8 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Account Created!</h3>
              <p className="text-xs text-slate-500">Welcome to Healix. Directing to your dashboard...</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {errors.form && (
                <div className="p-3 bg-rose-50 text-rose-700 text-xs rounded-xl border border-rose-200">
                  {errors.form}
                </div>
              )}

              <Input
                label="Full Name"
                placeholder="Aakash Sharma"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                error={errors.name}
                icon={User}
                required
              />

              <Input
                label="Email Address"
                type="email"
                placeholder="aakash@example.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                error={errors.email}
                icon={Mail}
                required
              />

              <Input
                label="Create Password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                error={errors.password}
                icon={Lock}
                required
              />

              <Input
                label="Confirm Password"
                type="password"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                error={errors.confirmPassword}
                icon={Lock}
                required
              />

              {/* Terms of service checkbox */}
              <div className="pt-1">
                <label className="flex items-start gap-2.5 text-xs text-slate-600 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.termsAccepted}
                    onChange={(e) =>
                      setFormData({ ...formData, termsAccepted: e.target.checked })
                    }
                    className="mt-0.5 rounded border-slate-300 text-teal-600 focus:ring-teal-500"
                  />
                  <span>
                    By creating an account, you agree to Healix's{" "}
                    <span className="text-teal-700 font-medium underline">Terms of Service</span>{" "}
                    and acknowledge that Healix provides health information and triage, not medical diagnosis.
                  </span>
                </label>
                {errors.terms && (
                  <p className="mt-1 text-xs text-rose-600 font-medium">{errors.terms}</p>
                )}
              </div>

              <div className="pt-3">
                <Button
                  type="submit"
                  variant="teal"
                  size="md"
                  className="w-full"
                  isLoading={isLoading}
                  icon={ArrowRight}
                  iconPosition="right"
                >
                  Create Account
                </Button>
              </div>
            </form>
          )}

          <div className="mt-6 text-center text-xs text-slate-500">
            Already have an account?{" "}
            <Link to="/login" className="text-teal-700 font-semibold hover:text-teal-800">
              Sign in
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
