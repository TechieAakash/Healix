import React, { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

// Layouts
import { PublicLayout } from "./layouts/PublicLayout";
import { AppLayout } from "./layouts/AppLayout";
import { authService } from "./services/authService";

// Pages are loaded when their route is opened to keep the landing page bundle small.
const lazyPage = (load, name) => lazy(() => load().then((module) => ({ default: module[name] })));
const LandingPage = lazyPage(() => import("./pages/LandingPage"), "LandingPage");
const LoginPage = lazyPage(() => import("./pages/LoginPage"), "LoginPage");
const SignupPage = lazyPage(() => import("./pages/SignupPage"), "SignupPage");
const ForgotPasswordPage = lazyPage(() => import("./pages/ForgotPasswordPage"), "ForgotPasswordPage");
const DashboardPage = lazyPage(() => import("./pages/DashboardPage"), "DashboardPage");
const HealthInsightsPage = lazyPage(() => import("./pages/HealthInsightsPage"), "HealthInsightsPage");
const HealthAssessmentPage = lazyPage(() => import("./pages/HealthAssessmentPage"), "HealthAssessmentPage");
const CarePlanPage = lazyPage(() => import("./pages/CarePlanPage"), "CarePlanPage");
const SymptomCheckerPage = lazyPage(() => import("./pages/SymptomCheckerPage"), "SymptomCheckerPage");
const AssessmentResultPage = lazyPage(() => import("./pages/AssessmentResultPage"), "AssessmentResultPage");
const AiAssistantPage = lazyPage(() => import("./pages/AiAssistantPage"), "AiAssistantPage");
const HealthHistoryPage = lazyPage(() => import("./pages/HealthHistoryPage"), "HealthHistoryPage");
const ReportsOverviewPage = lazyPage(() => import("./pages/ReportsOverviewPage"), "ReportsOverviewPage");
const ReportPage = lazyPage(() => import("./pages/ReportPage"), "ReportPage");
const SettingsPage = lazyPage(() => import("./pages/SettingsPage"), "SettingsPage");
const NotFoundPage = lazyPage(() => import("./pages/NotFoundPage"), "NotFoundPage");

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div className="min-h-screen bg-slate-50" aria-label="Loading page" />}>
      <Routes>
        {/* Full Screen Standalone Auth Pages (Screens 1 & 2) */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />

        {/* Public Website Routes */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
        </Route>

        {/* Symptom Checker: accessible to both Guests and Authenticated users */}
        <Route
          path="/symptom-checker"
          element={authService.isAuthenticated() ? <AppLayout /> : <PublicLayout />}
        >
          <Route
            index
            element={
              authService.isAuthenticated() ? (
                <SymptomCheckerPage />
              ) : (
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
                  <SymptomCheckerPage />
                </div>
              )
            }
          />
        </Route>
        <Route path="/symptoms" element={<Navigate to="/symptom-checker" replace />} />

        {/* Authenticated Application Routes (Screens 3-10) */}
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/app" element={<Navigate to="/dashboard" replace />} />
          <Route path="/assessment" element={<HealthAssessmentPage />} />
          <Route path="/assessment/:id" element={<AssessmentResultPage />} />
          <Route path="/insights" element={<HealthInsightsPage />} />
          <Route path="/care-plan" element={<CarePlanPage />} />
          <Route path="/assistant" element={<AiAssistantPage />} />
          <Route path="/history" element={<HealthHistoryPage />} />
          <Route path="/reports" element={<ReportsOverviewPage />} />
          <Route path="/report/:id" element={<ReportPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* 404 Catch-All */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
