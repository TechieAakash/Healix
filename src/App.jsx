import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

// Layouts
import { PublicLayout } from "./layouts/PublicLayout";
import { AppLayout } from "./layouts/AppLayout";

// Pages
import { LandingPage } from "./pages/LandingPage";
import { LoginPage } from "./pages/LoginPage";
import { SignupPage } from "./pages/SignupPage";
import { ForgotPasswordPage } from "./pages/ForgotPasswordPage";
import { DashboardPage } from "./pages/DashboardPage";
import { SymptomCheckerPage } from "./pages/SymptomCheckerPage";
import { AssessmentResultPage } from "./pages/AssessmentResultPage";
import { AiAssistantPage } from "./pages/AiAssistantPage";
import { HealthHistoryPage } from "./pages/HealthHistoryPage";
import { ReportsOverviewPage } from "./pages/ReportsOverviewPage";
import { ReportPage } from "./pages/ReportPage";
import { SettingsPage } from "./pages/SettingsPage";
import { NotFoundPage } from "./pages/NotFoundPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Website Routes */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        </Route>

        {/* Authenticated Application Routes */}
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/app" element={<Navigate to="/dashboard" replace />} />
          <Route path="/symptom-checker" element={<SymptomCheckerPage />} />
          <Route path="/assessment/:id" element={<AssessmentResultPage />} />
          <Route path="/assistant" element={<AiAssistantPage />} />
          <Route path="/history" element={<HealthHistoryPage />} />
          <Route path="/reports" element={<ReportsOverviewPage />} />
          <Route path="/report/:id" element={<ReportPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* 404 Catch-All */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
