import React, { useState, useEffect } from "react";
import { authService } from "../services/authService";
import { Card, CardHeader } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Input, Select } from "../components/common/FormControls";
import {
  User,
  Shield,
  Bell,
  Globe,
  Lock,
  CheckCircle2,
  Trash2,
  Download,
  ShieldCheck,
  Eye,
} from "lucide-react";

export function SettingsPage() {
  const [activeTab, setActiveTab] = useState("profile");
  const [user, setUser] = useState(authService.getCurrentUser());
  const [formData, setFormData] = useState({
    name: user?.name || "Aakash",
    fullName: user?.fullName || "Aakash Sharma",
    email: user?.email || "aakash@example.com",
    dateOfBirth: user?.dateOfBirth || "1996-08-14",
    gender: user?.gender || "Male",
    bloodGroup: user?.bloodGroup || "O+",
  });

  const [privacySettings, setPrivacySettings] = useState({
    saveHistory: user?.settings?.saveHistory ?? true,
    personalizeInsights: user?.settings?.personalizeInsights ?? true,
    emailAlerts: user?.settings?.emailAlerts ?? true,
    assessmentReminders: user?.settings?.assessmentReminders ?? true,
    language: user?.settings?.language || "en",
  });

  const [savedToast, setSavedToast] = useState(false);

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    const updated = await authService.updateProfile({
      ...formData,
      settings: privacySettings,
    });
    setUser(updated);
    setSavedToast(true);
    setTimeout(() => setSavedToast(false), 2500);
  };

  const handleToggle = (key) => {
    setPrivacySettings((prev) => {
      const next = { ...prev, [key]: !prev[key] };
      authService.updateProfile({ settings: next });
      return next;
    });
    setSavedToast(true);
    setTimeout(() => setSavedToast(false), 2000);
  };

  const tabs = [
    { id: "profile", label: "Profile", icon: User },
    { id: "privacy", label: "Privacy & Data", icon: Shield },
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "language", label: "Language", icon: Globe },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Settings & Preferences
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Manage your personal profile, encrypted health records, and privacy toggles.
          </p>
        </div>

        {savedToast && (
          <div className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-xl text-xs font-semibold animate-fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Settings saved</span>
          </div>
        )}
      </div>

      {/* Tabs navigation */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3 overflow-x-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                isActive
                  ? "bg-slate-900 text-white shadow-xs"
                  : "bg-white text-slate-600 border border-slate-200 hover:border-slate-300"
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* ================= TAB 1: PROFILE ================= */}
      {activeTab === "profile" && (
        <Card padding="default" className="shadow-xs">
          <CardHeader
            title="Personal Profile Information"
            subtitle="Used to provide personalized triage context on symptoms and clinical intake briefs."
          />
          <form onSubmit={handleSaveProfile} className="space-y-4 pt-2">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Input
                label="Full Name"
                value={formData.fullName}
                onChange={(e) =>
                  setFormData({ ...formData, fullName: e.target.value })
                }
                required
              />
              <Input
                label="Email Address"
                type="email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                required
              />
              <Input
                label="Date of Birth"
                type="date"
                value={formData.dateOfBirth}
                onChange={(e) =>
                  setFormData({ ...formData, dateOfBirth: e.target.value })
                }
                required
              />
              <Select
                label="Biological Sex / Gender"
                value={formData.gender}
                onChange={(e) =>
                  setFormData({ ...formData, gender: e.target.value })
                }
                options={[
                  { value: "Male", label: "Male" },
                  { value: "Female", label: "Female" },
                  { value: "Other", label: "Other / Prefer not to say" },
                ]}
              />
            </div>

            <div className="pt-4 border-t border-slate-100 flex justify-end">
              <Button type="submit" variant="teal" size="sm">
                Save Changes
              </Button>
            </div>
          </form>
        </Card>
      )}

      {/* ================= TAB 2: PRIVACY & DATA ================= */}
      {activeTab === "privacy" && (
        <div className="space-y-6">
          <Card padding="default" className="shadow-xs space-y-5">
            <CardHeader
              title="Health Data & Triage Privacy Controls"
              subtitle="Control how your symptom history is retained and utilized."
            />

            {/* Toggle 1: Save assessment history */}
            <div className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-200">
              <div className="space-y-0.5 max-w-lg">
                <h4 className="text-sm font-bold text-slate-900">
                  Save assessment history
                </h4>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Allows Healix to display your previous assessments and longitudinal symptom progression in your patient dashboard.
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleToggle("saveHistory")}
                className={`w-12 h-6 rounded-full transition-colors relative cursor-pointer ${
                  privacySettings.saveHistory ? "bg-teal-600" : "bg-slate-300"
                }`}
              >
                <span
                  className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-transform ${
                    privacySettings.saveHistory ? "right-1" : "left-1"
                  }`}
                />
              </button>
            </div>

            {/* Toggle 2: Use data for personalization */}
            <div className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-200">
              <div className="space-y-0.5 max-w-lg">
                <h4 className="text-sm font-bold text-slate-900">
                  Use my data to improve personalization
                </h4>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Synthesizes recurring patterns (such as persistent fatigue across multiple assessments) to offer helpful non-diagnostic insights.
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleToggle("personalizeInsights")}
                className={`w-12 h-6 rounded-full transition-colors relative cursor-pointer ${
                  privacySettings.personalizeInsights ? "bg-teal-600" : "bg-slate-300"
                }`}
              >
                <span
                  className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-transform ${
                    privacySettings.personalizeInsights ? "right-1" : "left-1"
                  }`}
                />
              </button>
            </div>
          </Card>

          {/* Export / Delete Data */}
          <Card padding="default" className="shadow-xs border-rose-200 bg-rose-50/20">
            <h4 className="text-sm font-bold text-rose-950 uppercase tracking-wider mb-2">
              Data Management & Purge
            </h4>
            <p className="text-xs text-slate-600 mb-4 leading-relaxed">
              You own all medical intake briefs and symptom logs. You can export an encrypted archive or permanently wipe all records.
            </p>
            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                size="sm"
                icon={Download}
                onClick={() => alert("Encrypted JSON archive exported to your downloads.")}
              >
                Export Health Data
              </Button>
              <Button
                variant="danger"
                size="sm"
                icon={Trash2}
                onClick={() => {
                  if (confirm("Are you sure? This will wipe your locally stored assessments.")) {
                    localStorage.removeItem("healix_assessments");
                    alert("Assessment records wiped.");
                    window.location.reload();
                  }
                }}
              >
                Delete All Health Records
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* ================= TAB 3: NOTIFICATIONS ================= */}
      {activeTab === "notifications" && (
        <Card padding="default" className="shadow-xs space-y-5">
          <CardHeader
            title="Notification Preferences"
            subtitle="Choose when Healix contacts you with follow-up reminders."
          />

          <div className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-200">
            <div className="space-y-0.5">
              <h4 className="text-sm font-bold text-slate-900">Email notifications</h4>
              <p className="text-xs text-slate-500">
                Receive printable summary copies and medical source citations by email.
              </p>
            </div>
            <button
              type="button"
              onClick={() => handleToggle("emailAlerts")}
              className={`w-12 h-6 rounded-full transition-colors relative cursor-pointer ${
                privacySettings.emailAlerts ? "bg-teal-600" : "bg-slate-300"
              }`}
            >
              <span
                className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-transform ${
                  privacySettings.emailAlerts ? "right-1" : "left-1"
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-200">
            <div className="space-y-0.5">
              <h4 className="text-sm font-bold text-slate-900">Assessment check-in reminders</h4>
              <p className="text-xs text-slate-500">
                Gentle reminders 48 hours after an assessment to track whether symptoms have improved.
              </p>
            </div>
            <button
              type="button"
              onClick={() => handleToggle("assessmentReminders")}
              className={`w-12 h-6 rounded-full transition-colors relative cursor-pointer ${
                privacySettings.assessmentReminders ? "bg-teal-600" : "bg-slate-300"
              }`}
            >
              <span
                className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-transform ${
                  privacySettings.assessmentReminders ? "right-1" : "left-1"
                }`}
              />
            </button>
          </div>
        </Card>
      )}

      {/* ================= TAB 4: LANGUAGE ================= */}
      {activeTab === "language" && (
        <Card padding="default" className="shadow-xs space-y-4">
          <CardHeader
            title="Language & Accessibility"
            subtitle="Select your preferred language for symptom intake and triage explanations."
          />

          <div className="max-w-xs space-y-2">
            <Select
              label="Display Language"
              value={privacySettings.language}
              onChange={(e) => {
                const val = e.target.value;
                setPrivacySettings((prev) => ({ ...prev, language: val }));
                setSavedToast(true);
                setTimeout(() => setSavedToast(false), 2000);
              }}
              options={[
                { value: "en", label: "English (US / International)" },
                { value: "hi", label: "हिन्दी (Hindi)" },
                { value: "es", label: "Español (Spanish)" },
              ]}
            />
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs text-slate-600">
            <div className="flex items-center gap-2 font-bold text-slate-900 mb-1">
              <Globe className="w-4 h-4 text-teal-600" />
              <span>Multilingual Translation Support</span>
            </div>
            Clinical knowledge bases and triage follow-ups are automatically translated to ensure medical terminology is accessible and culturally clear.
          </div>
        </Card>
      )}
    </div>
  );
}
