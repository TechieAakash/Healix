import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import {
  KeyRound,
  Shield,
  HelpCircle,
  LogOut,
  ChevronRight,
  CheckCircle2,
  X,
} from "lucide-react";

export function SettingsPage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(authService.getCurrentUser());
  const [activeTab, setActiveTab] = useState("Profile");
  const [showEditModal, setShowEditModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [savedToast, setSavedToast] = useState(false);

  const [editForm, setEditForm] = useState({
    fullName: user?.fullName || "Krish Alagh",
    dateOfBirth: user?.dateOfBirth || "15 Jan 2006",
    gender: user?.gender || "Male",
    bloodGroup: user?.bloodGroup || "O+",
    height: user?.height || "178 cm",
    weight: user?.weight || "72 kg",
  });

  const tabs = ["Profile", "Health Data", "Notifications", "Preferences"];

  const handleSaveProfile = (e) => {
    e.preventDefault();
    const updated = authService.updateProfile({
      ...user,
      ...editForm,
      name: editForm.fullName.split(" ")[0],
    });
    setUser(updated);
    setShowEditModal(false);
    setSavedToast(true);
    setTimeout(() => setSavedToast(false), 2500);
  };

  const handleLogout = () => {
    authService.logout();
    navigate("/login");
  };

  const personalInfo = [
    { label: "Full Name", value: user?.fullName || "Krish Alagh" },
    { label: "Date of Birth", value: user?.dateOfBirth || "15 Jan 2006" },
    { label: "Gender", value: user?.gender || "Male" },
    { label: "Blood Group", value: user?.bloodGroup || "O+" },
    { label: "Height", value: user?.height || "178 cm" },
    { label: "Weight", value: user?.weight || "72 kg" },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Toast Alert */}
      {savedToast && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-2 bg-emerald-800 text-white px-4 py-2.5 rounded-xl shadow-lg text-xs font-semibold animate-in fade-in slide-in-from-top-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-300" />
          <span>Profile updated successfully</span>
        </div>
      )}

      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          Profile & Settings
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Manage your personal details and account configurations.
        </p>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-1 border-b border-slate-200 pb-2 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
              activeTab === tab
                ? "bg-emerald-50 text-emerald-800"
                : "text-slate-500 hover:text-slate-900 hover:bg-slate-50"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* User Profile Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-emerald-800 text-white font-bold text-lg flex items-center justify-center shrink-0 shadow-xs">
            {user?.avatarInitials || "KA"}
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">{user?.fullName || "Krish Alagh"}</h2>
            <p className="text-xs text-slate-400 mt-0.5">{user?.email || "krish@example.com"}</p>
          </div>
        </div>

        <button
          onClick={() => setShowEditModal(true)}
          className="px-4 py-2 border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:border-slate-300 transition-colors cursor-pointer self-start sm:self-auto"
        >
          Edit Profile
        </button>
      </div>

      {/* Personal Information Section */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-4">
        <h3 className="text-sm font-bold text-slate-900 tracking-tight">
          Personal Information
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-4 gap-x-8 pt-1">
          {personalInfo.map((info, idx) => (
            <div key={idx} className="space-y-1">
              <span className="text-[11px] font-medium text-slate-400 block">{info.label}</span>
              <span className="text-xs sm:text-sm font-semibold text-slate-800 block">{info.value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Account Settings Section */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-3">
        <h3 className="text-sm font-bold text-slate-900 tracking-tight">
          Account Settings
        </h3>

        <div className="divide-y divide-slate-100">
          {/* Change Password */}
          <button
            onClick={() => setShowPasswordModal(true)}
            className="w-full flex items-center justify-between py-3.5 hover:bg-slate-50/70 px-2 rounded-xl transition-colors text-left cursor-pointer group"
          >
            <div className="flex items-center gap-3">
              <KeyRound className="w-4 h-4 text-slate-500 group-hover:text-emerald-700" />
              <span className="text-xs sm:text-sm font-medium text-slate-700 group-hover:text-slate-900">
                Change Password
              </span>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-600 transition-transform group-hover:translate-x-0.5" />
          </button>

          {/* Privacy & Security */}
          <button
            onClick={() => alert("Privacy settings are managed under Client Encryption Mode.")}
            className="w-full flex items-center justify-between py-3.5 hover:bg-slate-50/70 px-2 rounded-xl transition-colors text-left cursor-pointer group"
          >
            <div className="flex items-center gap-3">
              <Shield className="w-4 h-4 text-slate-500 group-hover:text-emerald-700" />
              <span className="text-xs sm:text-sm font-medium text-slate-700 group-hover:text-slate-900">
                Privacy & Security
              </span>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-600 transition-transform group-hover:translate-x-0.5" />
          </button>

          {/* Help & Support */}
          <button
            onClick={() => navigate("/assistant")}
            className="w-full flex items-center justify-between py-3.5 hover:bg-slate-50/70 px-2 rounded-xl transition-colors text-left cursor-pointer group"
          >
            <div className="flex items-center gap-3">
              <HelpCircle className="w-4 h-4 text-slate-500 group-hover:text-emerald-700" />
              <span className="text-xs sm:text-sm font-medium text-slate-700 group-hover:text-slate-900">
                Help & Support
              </span>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-600 transition-transform group-hover:translate-x-0.5" />
          </button>

          {/* Log Out */}
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-between py-3.5 hover:bg-red-50/50 px-2 rounded-xl transition-colors text-left cursor-pointer group"
          >
            <div className="flex items-center gap-3">
              <LogOut className="w-4 h-4 text-rose-500" />
              <span className="text-xs sm:text-sm font-medium text-rose-600">
                Log Out
              </span>
            </div>
            <ChevronRight className="w-4 h-4 text-rose-300 transition-transform group-hover:translate-x-0.5" />
          </button>
        </div>
      </div>

      {/* Edit Profile Modal */}
      {showEditModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-200 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h4 className="text-sm font-bold text-slate-900">Edit Personal Information</h4>
              <button
                onClick={() => setShowEditModal(false)}
                className="p-1 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveProfile} className="space-y-3 mt-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Full Name</label>
                <input
                  type="text"
                  value={editForm.fullName}
                  onChange={(e) => setEditForm({ ...editForm, fullName: e.target.value })}
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Date of Birth</label>
                <input
                  type="text"
                  value={editForm.dateOfBirth}
                  onChange={(e) => setEditForm({ ...editForm, dateOfBirth: e.target.value })}
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Gender</label>
                  <select
                    value={editForm.gender}
                    onChange={(e) => setEditForm({ ...editForm, gender: e.target.value })}
                    className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none bg-white"
                  >
                    <option>Male</option>
                    <option>Female</option>
                    <option>Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Blood Group</label>
                  <input
                    type="text"
                    value={editForm.bloodGroup}
                    onChange={(e) => setEditForm({ ...editForm, bloodGroup: e.target.value })}
                    className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Height</label>
                  <input
                    type="text"
                    value={editForm.height}
                    onChange={(e) => setEditForm({ ...editForm, height: e.target.value })}
                    className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Weight</label>
                  <input
                    type="text"
                    value={editForm.weight}
                    onChange={(e) => setEditForm({ ...editForm, weight: e.target.value })}
                    className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:border-emerald-700 focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowEditModal(false)}
                  className="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-medium bg-[#065f46] hover:bg-[#064e3b] text-white rounded-xl shadow-xs"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Password Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl border border-slate-200 animate-in fade-in zoom-in-95">
            <h4 className="text-sm font-bold text-slate-900 mb-2">Change Password</h4>
            <div className="space-y-3">
              <input
                type="password"
                placeholder="Current password"
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl"
              />
              <input
                type="password"
                placeholder="New password"
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl"
              />
            </div>
            <div className="flex justify-end gap-2 pt-4">
              <button
                type="button"
                onClick={() => setShowPasswordModal(false)}
                className="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-xl"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowPasswordModal(false);
                  setSavedToast(true);
                  setTimeout(() => setSavedToast(false), 2000);
                }}
                className="px-4 py-2 text-xs font-medium bg-[#065f46] text-white rounded-xl"
              >
                Update
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
