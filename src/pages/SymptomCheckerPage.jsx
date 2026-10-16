import React, { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { ProgressStepper } from "../components/symptom-checker/ProgressStepper";
import { BodyAreaSelector } from "../components/symptom-checker/BodyAreaSelector";
import { SafetyRedFlagModal } from "../components/symptom-checker/SafetyRedFlagModal";
import { AnalysisLoadingStep } from "../components/symptom-checker/AnalysisLoadingStep";
import { Button } from "../components/common/Button";
import { Card } from "../components/common/Card";
import { Badge } from "../components/common/Badge";
import { TextArea, Input } from "../components/common/FormControls";
import { commonSymptomChips } from "../data/mockData";
import { symptomService } from "../services/symptomService";
import { assessmentService } from "../services/assessmentService";
import {
  Mic,
  MicOff,
  Plus,
  X,
  ArrowRight,
  ArrowLeft,
  ShieldAlert,
  ShieldCheck,
  HelpCircle,
  Sparkles,
  CheckCircle2,
  Calendar,
  Activity,
  Layers,
} from "lucide-react";

export function SymptomCheckerPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  // Current Step: 1 = Symptoms, 2 = Details, 3 = Follow-up, 4 = Analysis
  const [currentStep, setCurrentStep] = useState(1);

  // Assessment Form State
  const [freeText, setFreeText] = useState(searchParams.get("initial") || "");
  const [selectedChips, setSelectedChips] = useState([
    { id: "headache", label: "Headache" },
    { id: "fatigue", label: "Fatigue" },
  ]);
  const [customSymptomInput, setCustomSymptomInput] = useState("");
  const [showAddCustom, setShowAddCustom] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  // Step 2 Details
  const [onset, setOnset] = useState("Few days");
  const [severity, setSeverity] = useState("Mild");
  const [frequency, setFrequency] = useState("Comes and goes");
  const [bodyArea, setBodyArea] = useState("head");

  // Step 3 Follow-up Questions State
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});

  // Safety Red Flag State
  const [isRedFlagDetected, setIsRedFlagDetected] = useState(false);
  const [redFlagReason, setRedFlagReason] = useState("");
  const [matchedTriggers, setMatchedTriggers] = useState([]);

  const steps = [
    { label: "Symptoms" },
    { label: "Details" },
    { label: "Follow-up" },
    { label: "Analysis" },
    { label: "Results" },
  ];

  // Perform continuous safety red-flag triage checks
  const performTriageSafetyCheck = (text, chips) => {
    const check = symptomService.checkForRedFlags(text, chips);
    if (check.isEmergency) {
      setIsRedFlagDetected(true);
      setRedFlagReason(check.reason);
      setMatchedTriggers(check.matchedTriggers);
    }
  };

  const handleToggleChip = (chip) => {
    const exists = selectedChips.find((c) => c.id === chip.id);
    let updated;
    if (exists) {
      updated = selectedChips.filter((c) => c.id !== chip.id);
    } else {
      updated = [...selectedChips, chip];
    }
    setSelectedChips(updated);
    performTriageSafetyCheck(freeText, updated);
  };

  const handleAddCustomSymptom = (e) => {
    e.preventDefault();
    if (!customSymptomInput.trim()) return;
    const newChip = {
      id: `custom_${Date.now()}`,
      label: customSymptomInput.trim(),
    };
    const updated = [...selectedChips, newChip];
    setSelectedChips(updated);
    setCustomSymptomInput("");
    setShowAddCustom(false);
    performTriageSafetyCheck(freeText, updated);
  };

  const toggleVoiceRecording = () => {
    if (!isRecording) {
      setIsRecording(true);
      setTimeout(() => {
        setFreeText((prev) =>
          prev
            ? `${prev}. I've also had a dull headache behind my eyes since yesterday morning.`
            : "I've had a headache since yesterday and feel tired."
        );
        setIsRecording(false);
      }, 1900);
    } else {
      setIsRecording(false);
    }
  };

  // Step 1 -> Step 2 validation
  const handleProceedToDetails = () => {
    if (!freeText.trim() && selectedChips.length === 0) {
      alert("Please describe what you are experiencing or select at least one symptom.");
      return;
    }
    performTriageSafetyCheck(freeText, selectedChips);
    setCurrentStep(2);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Step 2 -> Step 3 follow-up generation
  const handleProceedToFollowUp = async () => {
    const generated = await symptomService.generateFollowUpQuestions({
      primarySymptoms: selectedChips,
      bodyArea,
      description: freeText,
      severity,
    });
    setQuestions(generated);
    setCurrentQuestionIndex(0);
    setCurrentStep(3);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Step 3 answers
  const handleAnswerQuestion = (val) => {
    const currentQ = questions[currentQuestionIndex];
    if (!currentQ) return;

    // Check if user answered Yes to critical red-flag question
    if (currentQ.isCriticalSafety && val === "Yes") {
      setIsRedFlagDetected(true);
      setRedFlagReason("Positive confirmation of potential acute warning sign.");
      setMatchedTriggers([currentQ.question]);
    }

    setAnswers((prev) => ({ ...prev, [currentQ.id]: val }));

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      // Proceed to Step 4 Analysis
      setCurrentStep(4);
    }
  };

  // Step 4 Complete -> Navigate to results
  const handleAnalysisComplete = async () => {
    const result = await assessmentService.analyzeAssessment({
      description: freeText,
      structuredSymptoms: selectedChips,
      bodyArea,
      duration: onset,
      severity,
      frequency,
      answers,
      hasRedFlags: isRedFlagDetected,
    });
    navigate(`/assessment/${result.id}`);
  };

  return (
    <div className="max-w-4xl mx-auto py-4 sm:py-8 px-4 sm:px-6">
      {/* Progress Stepper */}
      <ProgressStepper steps={steps} currentStep={currentStep} />

      {/* Safety Red Flag Modal */}
      <SafetyRedFlagModal
        isOpen={isRedFlagDetected}
        onProceedAnyway={() => setIsRedFlagDetected(false)}
        detectedReason={redFlagReason}
        matchedTriggers={matchedTriggers}
      />

      {/* ================= STEP 1: SYMPTOMS ================= */}
      {currentStep === 1 && (
        <div className="space-y-6">
          <div className="text-center max-w-xl mx-auto space-y-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              What are you experiencing?
            </h1>
            <p className="text-sm text-slate-500">
              Describe your symptoms in your own words or select from common health indicators below.
            </p>
          </div>

          <Card padding="default" className="shadow-sm space-y-6">
            {/* Free-text input with Voice Input button */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-semibold text-slate-800">
                  Describe symptoms in your own words:
                </label>
                <button
                  type="button"
                  onClick={toggleVoiceRecording}
                  className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-xl transition-all cursor-pointer ${
                    isRecording
                      ? "bg-rose-100 text-rose-700 animate-pulse"
                      : "bg-slate-100 hover:bg-slate-200 text-slate-700"
                  }`}
                >
                  {isRecording ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5" />}
                  <span>{isRecording ? "Listening..." : "Voice Input"}</span>
                </button>
              </div>

              <TextArea
                rows={4}
                placeholder="E.g., I've had a headache since yesterday and feel tired..."
                value={freeText}
                onChange={(e) => {
                  setFreeText(e.target.value);
                  performTriageSafetyCheck(e.target.value, selectedChips);
                }}
                className="text-base"
              />
              <p className="text-[11px] text-slate-400">
                Tip: Mention when it started, what it feels like, or any related sensations.
              </p>
            </div>

            {/* Structured Symptoms Chips */}
            <div className="space-y-3 pt-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Quick Select & Structured Symptoms:
                </span>
                <button
                  type="button"
                  onClick={() => setShowAddCustom(true)}
                  className="text-xs text-teal-700 hover:text-teal-800 font-semibold inline-flex items-center gap-1 cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5" /> Add custom symptom
                </button>
              </div>

              <div className="flex flex-wrap gap-2">
                {commonSymptomChips.map((chip) => {
                  const isSelected = selectedChips.some((c) => c.id === chip.id);
                  return (
                    <button
                      key={chip.id}
                      type="button"
                      onClick={() => handleToggleChip(chip)}
                      className={`text-xs px-3 py-1.5 rounded-full border transition-all cursor-pointer font-medium flex items-center gap-1.5 ${
                        isSelected
                          ? "bg-teal-600 border-teal-600 text-white shadow-xs"
                          : "bg-slate-50 border-slate-200 text-slate-700 hover:border-slate-300 hover:bg-slate-100"
                      }`}
                    >
                      {isSelected && <CheckCircle2 className="w-3 h-3 stroke-[2.5]" />}
                      <span>{chip.label}</span>
                    </button>
                  );
                })}
              </div>

              {/* Add Custom Symptom input modal/bar */}
              {showAddCustom && (
                <form
                  onSubmit={handleAddCustomSymptom}
                  className="mt-3 p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center gap-2"
                >
                  <input
                    type="text"
                    placeholder="Enter symptom name (e.g. ringing in ears)..."
                    value={customSymptomInput}
                    onChange={(e) => setCustomSymptomInput(e.target.value)}
                    className="flex-1 text-xs bg-white border border-slate-200 rounded-lg px-3 py-1.5 outline-none focus:border-teal-600"
                    autoFocus
                  />
                  <Button variant="teal" size="sm" type="submit">
                    Add
                  </Button>
                  <button
                    type="button"
                    onClick={() => setShowAddCustom(false)}
                    className="p-1.5 text-slate-400 hover:text-slate-700"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </form>
              )}
            </div>

            {/* Next Step Action */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <span className="text-xs text-slate-400">
                Step 1 of 5 • Safety triage active
              </span>
              <Button
                variant="teal"
                size="md"
                onClick={handleProceedToDetails}
                icon={ArrowRight}
                iconPosition="right"
              >
                Continue to Details
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* ================= STEP 2: SYMPTOM DETAILS ================= */}
      {currentStep === 2 && (
        <div className="space-y-6">
          <div className="text-center max-w-xl mx-auto space-y-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Symptom Details & Location
            </h1>
            <p className="text-sm text-slate-500">
              Providing timeline and anatomical context helps refine informational matching.
            </p>
          </div>

          <Card padding="default" className="shadow-sm space-y-8">
            {/* Timeline: When did it start? */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
                <Calendar className="w-4 h-4 text-teal-600" />
                When did it start?
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {["Today", "Few days", "1–2 weeks", "More than 2 weeks"].map((opt) => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setOnset(opt)}
                    className={`p-3 rounded-xl border text-xs font-semibold text-center transition-all cursor-pointer ${
                      onset === opt
                        ? "border-teal-600 bg-teal-50 text-teal-900 ring-2 ring-teal-500/20 shadow-xs"
                        : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            {/* Severity: Mild, Moderate, Severe */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
                <Activity className="w-4 h-4 text-teal-600" />
                Severity level:
              </label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { label: "Mild", desc: "Noticeable but easily tolerated" },
                  { label: "Moderate", desc: "Interferes with normal tasks" },
                  { label: "Severe", desc: "Incapacitating or unbearable" },
                ].map((sev) => (
                  <button
                    key={sev.label}
                    type="button"
                    onClick={() => {
                      setSeverity(sev.label);
                      if (sev.label === "Severe") {
                        performTriageSafetyCheck("severe pain", selectedChips);
                      }
                    }}
                    className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                      severity === sev.label
                        ? "border-teal-600 bg-teal-50 text-teal-900 ring-2 ring-teal-500/20 shadow-xs"
                        : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
                    }`}
                  >
                    <p className="text-xs font-bold">{sev.label}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">{sev.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Frequency: Constant, Occasional, Comes and goes */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-teal-600" />
                Frequency:
              </label>
              <div className="grid grid-cols-3 gap-3">
                {["Constant", "Occasional", "Comes and goes"].map((freq) => (
                  <button
                    key={freq}
                    type="button"
                    onClick={() => setFrequency(freq)}
                    className={`p-3 rounded-xl border text-xs font-semibold text-center transition-all cursor-pointer ${
                      frequency === freq
                        ? "border-teal-600 bg-teal-50 text-teal-900 ring-2 ring-teal-500/20 shadow-xs"
                        : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
                    }`}
                  >
                    {freq}
                  </button>
                ))}
              </div>
            </div>

            {/* Location: Body-area selector */}
            <div className="space-y-3 pt-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-600">
                Primary Body Location:
              </label>
              <BodyAreaSelector
                selectedArea={bodyArea}
                onSelectArea={(area) => setBodyArea(area)}
              />
            </div>

            {/* Navigation buttons */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <Button
                variant="outline"
                size="md"
                onClick={() => setCurrentStep(1)}
                icon={ArrowLeft}
              >
                Back to Symptoms
              </Button>
              <Button
                variant="teal"
                size="md"
                onClick={handleProceedToFollowUp}
                icon={ArrowRight}
                iconPosition="right"
              >
                Continue to Follow-up
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* ================= STEP 3: FOLLOW-UP QUESTIONS ================= */}
      {currentStep === 3 && (
        <div className="space-y-6">
          <div className="text-center max-w-xl mx-auto space-y-2">
            <Badge variant="teal">Intake Clarification</Badge>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              A few follow-up questions
            </h1>
            <p className="text-sm text-slate-500">
              Healix asks targeted questions to better understand clinical warning indicators.
            </p>
          </div>

          {questions.length > 0 && (
            <Card padding="lg" className="shadow-md space-y-8">
              {/* Question progress counter */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                  Question {currentQuestionIndex + 1} of {questions.length}
                </span>
                <span className="text-xs text-slate-400">
                  {Math.round(((currentQuestionIndex + 1) / questions.length) * 100)}% completed
                </span>
              </div>

              {/* Conversational Prompt */}
              <div className="space-y-4">
                <div className="p-4 bg-teal-50/70 rounded-2xl border border-teal-100 text-teal-950 flex items-start gap-3">
                  <div className="w-8 h-8 rounded-xl bg-teal-600 text-white flex items-center justify-center shrink-0">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-teal-700">
                      Healix Assistant:
                    </span>
                    <h3 className="text-base sm:text-lg font-bold text-slate-900 mt-1">
                      {questions[currentQuestionIndex]?.question}
                    </h3>
                    {questions[currentQuestionIndex]?.hint && (
                      <p className="text-xs text-teal-900 mt-1 leading-relaxed">
                        {questions[currentQuestionIndex]?.hint}
                      </p>
                    )}
                  </div>
                </div>

                {/* Yes, No, Not sure response buttons */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3">
                  {["Yes", "No", "Not sure"].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleAnswerQuestion(option)}
                      className="p-4 rounded-xl border border-slate-200 bg-white hover:border-teal-600 hover:bg-teal-50/40 text-slate-800 font-bold text-sm text-center transition-all cursor-pointer shadow-xs active:scale-[0.98]"
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              {/* Navigation buttons */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    if (currentQuestionIndex > 0) {
                      setCurrentQuestionIndex((prev) => prev - 1);
                    } else {
                      setCurrentStep(2);
                    }
                  }}
                  icon={ArrowLeft}
                >
                  Back
                </Button>
                <span className="text-xs text-slate-400">
                  Tap any option above to advance
                </span>
              </div>
            </Card>
          )}
        </div>
      )}

      {/* ================= STEP 4: AI ANALYSIS LOADING ================= */}
      {currentStep === 4 && (
        <AnalysisLoadingStep onComplete={handleAnalysisComplete} />
      )}
    </div>
  );
}
