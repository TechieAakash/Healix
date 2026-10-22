import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  User,
  Activity,
  HeartPulse,
  Stethoscope,
  CheckCircle2,
  ChevronRight,
  ChevronLeft,
} from "lucide-react";

import { assessmentService } from "../services/assessmentService";

export function HealthAssessmentPage() {
  const navigate = useNavigate();

  // Step 1 is the start - step 2 was previously default for mockup
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // Lifestyle question selections
  const [sleepHours, setSleepHours] = useState("7-8");
  const [exerciseDays, setExerciseDays] = useState("3-4");
  const [dietQuality, setDietQuality] = useState("Good");

  // Basic Info state
  const [age, setAge] = useState("20");
  const [gender, setGender] = useState("Male");
  const [height, setHeight] = useState("178");
  const [weight, setWeight] = useState("72");

  // Medical History & Symptoms
  const [medicalConditions] = useState(["None"]);
  const [currentSymptoms, setCurrentSymptoms] = useState("No acute symptoms today");

  const steps = [
    { number: 1, label: "Basic Info", icon: User },
    { number: 2, label: "Lifestyle", icon: Activity },
    { number: 3, label: "Medical History", icon: HeartPulse },
    { number: 4, label: "Symptoms", icon: Stethoscope },
    { number: 5, label: "Review", icon: CheckCircle2 },
  ];

  const handleNext = async () => {
    if (currentStep < 5) {
      setCurrentStep(currentStep + 1);
    } else {
      setIsSubmitting(true);
      setErrorMessage("");
      try {
        const description = `Health Assessment Intake: ${currentSymptoms}. Lifestyle: Sleep ${sleepHours}h, Exercise ${exerciseDays}d/wk, Diet: ${dietQuality}. Profile: ${gender}, ${age}y, ${height}cm, ${weight}kg. Known conditions: ${medicalConditions.join(", ")}.`;
        const res = await assessmentService.createAssessment({
          description,
          symptoms: currentSymptoms && currentSymptoms !== "No acute symptoms today" ? [currentSymptoms] : [],
        });
        const assessmentId = res.assessment_id;
        await assessmentService.analyzeAssessment(assessmentId);
        navigate(`/assessment/${assessmentId}`);
      } catch (err) {
        console.error("Failed to submit health assessment:", err);
        setErrorMessage(err.message || "Unable to submit health assessment. Please try again.");
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Health Assessment
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Complete your assessment to get personalized insights.
          </p>
        </div>

        {/* Step Indicator with Progress Bar */}
        <div className="w-full sm:w-44 space-y-1.5">
          <div className="flex justify-between text-xs font-semibold text-slate-600">
            <span>Step {currentStep} of 5</span>
          </div>
          <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-600 transition-all duration-300 rounded-full"
              style={{ width: `${(currentStep / 5) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Stepper Horizontal Navigation Bar */}
      <div className="bg-white rounded-2xl p-4 border border-slate-200/80 shadow-xs flex items-center justify-between overflow-x-auto">
        {steps.map((st) => {
          const Icon = st.icon;
          const isActive = currentStep === st.number;
          const isDone = currentStep > st.number;

          return (
            <button
              key={st.number}
              onClick={() => setCurrentStep(st.number)}
              className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl transition-all cursor-pointer whitespace-nowrap"
            >
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                  isActive
                    ? "bg-[#065f46] text-white"
                    : isDone
                    ? "bg-emerald-100 text-emerald-800"
                    : "bg-slate-100 text-slate-400"
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
              </div>
              <span
                className={`text-xs ${
                  isActive
                    ? "font-bold text-[#065f46]"
                    : isDone
                    ? "font-medium text-slate-700"
                    : "text-slate-400"
                }`}
              >
                {st.label}
              </span>
            </button>
          );
        })}
      </div>

      {/* Main Step Form Card */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200/80 shadow-xs">
        {/* Step 2: Lifestyle Questions (Mockup Screen 6) */}
        {currentStep === 2 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Lifestyle Questions
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Tell us about your daily habits and lifestyle.
              </p>
            </div>

            {/* Question 1: Sleep Hours */}
            <div className="space-y-2.5">
              <label className="block text-xs font-medium text-slate-700">
                How many hours do you sleep on average?
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {["< 5", "5-6", "7-8", "> 8"].map((opt) => {
                  const selected = sleepHours === opt;
                  return (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setSleepHours(opt)}
                      className={`py-2.5 px-4 rounded-xl text-xs font-medium border transition-all cursor-pointer text-center ${
                        selected
                          ? "bg-[#065f46] text-white border-[#065f46] shadow-xs"
                          : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50"
                      }`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Question 2: Exercise Days */}
            <div className="space-y-2.5">
              <label className="block text-xs font-medium text-slate-700">
                How many days per week do you exercise?
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {["0", "1-2", "3-4", "5+"].map((opt) => {
                  const selected = exerciseDays === opt;
                  return (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setExerciseDays(opt)}
                      className={`py-2.5 px-4 rounded-xl text-xs font-medium border transition-all cursor-pointer text-center ${
                        selected
                          ? "bg-[#065f46] text-white border-[#065f46] shadow-xs"
                          : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50"
                      }`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Question 3: Diet Quality */}
            <div className="space-y-2.5">
              <label className="block text-xs font-medium text-slate-700">
                How would you describe your diet?
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {["Poor", "Average", "Good", "Excellent"].map((opt) => {
                  const selected = dietQuality === opt;
                  return (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setDietQuality(opt)}
                      className={`py-2.5 px-4 rounded-xl text-xs font-medium border transition-all cursor-pointer text-center ${
                        selected
                          ? "bg-[#065f46] text-white border-[#065f46] shadow-xs"
                          : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50"
                      }`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Step 1: Basic Info */}
        {currentStep === 1 && (
          <div className="space-y-5">
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight">Basic Information</h2>
              <p className="text-xs text-slate-500 mt-0.5">Please confirm your baseline biometric profile.</p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Age</label>
                <input
                  type="number"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl text-xs"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Gender</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl text-xs bg-white"
                >
                  <option>Male</option>
                  <option>Female</option>
                  <option>Non-binary / Other</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Height (cm)</label>
                <input
                  type="number"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl text-xs"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Weight (kg)</label>
                <input
                  type="number"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl text-xs"
                />
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Medical History */}
        {currentStep === 3 && (
          <div className="space-y-5">
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight">Medical History</h2>
              <p className="text-xs text-slate-500 mt-0.5">Any known conditions, past treatments, or medication.</p>
            </div>
            <div className="space-y-3">
              {["No chronic conditions", "Hypertension", "Asthma", "Diabetes Type 2", "Thyroid disorder"].map((c) => (
                <label key={c} className="flex items-center gap-2.5 p-3 rounded-xl border border-slate-200 hover:bg-slate-50 cursor-pointer text-xs">
                  <input type="checkbox" defaultChecked={c === "No chronic conditions"} className="rounded text-emerald-700 focus:ring-emerald-700" />
                  <span>{c}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Symptoms */}
        {currentStep === 4 && (
          <div className="space-y-5">
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight">Current Symptoms</h2>
              <p className="text-xs text-slate-500 mt-0.5">Detail any active physical sensations or concerns.</p>
            </div>
            <textarea
              rows={4}
              value={currentSymptoms}
              onChange={(e) => setCurrentSymptoms(e.target.value)}
              className="w-full p-3.5 border border-slate-200 rounded-xl text-xs focus:border-emerald-700 focus:outline-none"
              placeholder="Describe symptoms..."
            />
          </div>
        )}

        {/* Step 5: Review */}
        {currentStep === 5 && (
          <div className="space-y-5">
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight">Review & Confirmation</h2>
              <p className="text-xs text-slate-500 mt-0.5">Please review your responses before generating recommendations.</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl space-y-2 text-xs">
              <p><strong>Sleep:</strong> {sleepHours} hours avg</p>
              <p><strong>Exercise:</strong> {exerciseDays} days per week</p>
              <p><strong>Diet:</strong> {dietQuality}</p>
              <p><strong>Profile:</strong> {gender}, {age} years, {height} cm, {weight} kg</p>
            </div>
          </div>
        )}

        {errorMessage && (
          <div className="p-3 bg-red-50 text-red-700 text-xs rounded-xl border border-red-200 mt-4">
            {errorMessage}
          </div>
        )}

        {/* Bottom Actions */}
        <div className="flex items-center justify-between pt-6 border-t border-slate-100 mt-8">
          {currentStep > 1 ? (
            <button
              type="button"
              disabled={isSubmitting}
              onClick={handleBack}
              className="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition-colors cursor-pointer disabled:opacity-50"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
          ) : <div />}

          <button
            type="button"
            disabled={isSubmitting}
            onClick={handleNext}
            className="flex items-center gap-1.5 px-6 py-2.5 bg-[#065f46] hover:bg-[#064e3b] text-white text-xs font-semibold rounded-xl shadow-xs transition-colors cursor-pointer ml-auto disabled:opacity-60"
          >
            <span>{isSubmitting ? "Analyzing..." : currentStep === 5 ? "Submit Assessment" : "Next"}</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
