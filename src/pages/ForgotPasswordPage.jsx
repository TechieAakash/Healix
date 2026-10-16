import React, { useState } from "react";
import { Link } from "react-router-dom";
import { authService } from "../services/authService";
import { Button } from "../components/common/Button";
import { Input } from "../components/common/FormControls";
import { Card } from "../components/common/Card";
import { HeartPulse, Mail, ArrowLeft, CheckCircle2 } from "lucide-react";

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) {
      setError("Please enter a valid email address");
      return;
    }

    setIsLoading(true);
    setError("");
    try {
      await authService.resetPassword(email);
      setSubmitted(true);
    } catch (err) {
      setError("Could not process reset. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[75vh] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link to="/" className="inline-flex items-center gap-2.5 mb-6">
          <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
            <HeartPulse className="w-6 h-6" />
          </div>
          <span className="font-bold text-2xl text-slate-900 tracking-tight">Healix</span>
        </Link>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          Reset your password
        </h2>
        <p className="mt-2 text-xs sm:text-sm text-slate-500">
          Enter your registered email to receive secure recovery instructions.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card padding="default" className="shadow-lg border-slate-200">
          {submitted ? (
            <div className="py-6 text-center space-y-4">
              <div className="w-12 h-12 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-900">Check your inbox</h3>
              <p className="text-xs text-slate-500 leading-relaxed">
                If an account exists for <strong>{email}</strong>, we've sent password reset instructions.
              </p>
              <div className="pt-2">
                <Link to="/login">
                  <Button variant="outline" size="sm" className="w-full">
                    Return to Login
                  </Button>
                </Link>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Email Address"
                type="email"
                placeholder="aakash@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={error}
                icon={Mail}
                required
              />

              <div className="pt-2">
                <Button
                  type="submit"
                  variant="teal"
                  size="md"
                  className="w-full"
                  isLoading={isLoading}
                >
                  Send Reset Link
                </Button>
              </div>

              <div className="text-center pt-2">
                <Link
                  to="/login"
                  className="text-xs text-slate-500 hover:text-slate-800 inline-flex items-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  Back to Sign In
                </Link>
              </div>
            </form>
          )}
        </Card>
      </div>
    </div>
  );
}
