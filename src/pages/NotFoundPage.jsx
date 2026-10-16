import React from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/common/Button";
import { HeartPulse, Home, Stethoscope } from "lucide-react";

export function NotFoundPage() {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center p-6 space-y-4">
      <div className="w-16 h-16 rounded-3xl bg-teal-50 text-teal-700 flex items-center justify-center">
        <HeartPulse className="w-8 h-8" />
      </div>
      <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
        Page Not Found
      </h1>
      <p className="text-sm text-slate-500 max-w-sm">
        The health information page you requested does not exist or has been moved.
      </p>
      <div className="pt-2 flex items-center gap-3">
        <Link to="/">
          <Button variant="outline" size="sm" icon={Home}>
            Healix Home
          </Button>
        </Link>
        <Link to="/dashboard">
          <Button variant="teal" size="sm" icon={Stethoscope}>
            Go to Dashboard
          </Button>
        </Link>
      </div>
    </div>
  );
}
