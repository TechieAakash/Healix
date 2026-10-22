import React, { useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import {
  Stethoscope,
  ArrowRight,
  ShieldAlert,
  AlertTriangle,
  RotateCcw,
  Loader2,
  FileText,
  LogIn,
  ChevronRight,
} from "lucide-react";
import { assessmentService } from "../services/assessmentService";
import { authService } from "../services/authService";
import { UrgencyIndicator } from "../components/common/UrgencyIndicator";
import { Button } from "../components/common/Button";

const COMMON_SYMPTOM_OPTIONS = [
  "Headache",
  "Fever",
  "Cough",
  "Sore Throat",
  "Stomach Pain",
  "Fatigue",
  "Shortness of Breath",
  "Chest Discomfort",
  "Dizziness",
  "Body Aches",
  "Skin Rash",
  "Nausea",
];

const BODY_AREAS = [
  { id: "head", label: "Head & Neck" },
  { id: "chest", label: "Chest & Respiratory" },
  { id: "abdomen", label: "Stomach & Abdomen" },
  { id: "musculoskeletal", label: "Arms, Legs & Back" },
  { id: "skin", label: "Skin & General" },
];

export function SymptomCheckerPage() {
  const [searchParams] = useSearchParams();
  const isAuthenticated = authService.isAuthenticated();

  // Inputs: initialize with URL query parameter ?initial=... or saved draft if present
  const [symptomText, setSymptomText] = useState(() => {
    const draft = assessmentService.getDraftLocally();
    return searchParams.get("initial") || (draft ? draft.description || "" : "");
  });
  const [selectedChips, setSelectedChips] = useState(() => {
    const draft = assessmentService.getDraftLocally();
    return draft && Array.isArray(draft.symptoms) ? draft.symptoms : [];
  });
  const [bodyArea, setBodyArea] = useState(() => {
    const draft = assessmentService.getDraftLocally();
    return draft?.bodyArea || "head";
  });
  const [severity, setSeverity] = useState(() => {
    const draft = assessmentService.getDraftLocally();
    return draft?.severity || 5;
  });
  const [duration, setDuration] = useState(() => {
    const draft = assessmentService.getDraftLocally();
    return draft?.duration || "1-3 days";
  });

  // Workflow states: 'input' | 'questions' | 'analyzing' | 'result' | 'error' | 'auth_required'
  const [stage, setStage] = useState("input");
  const [assessmentId, setAssessmentId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleToggleChip = (chip) => {
    if (selectedChips.includes(chip)) {
      setSelectedChips(selectedChips.filter((c) => c !== chip));
    } else {
      setSelectedChips([...selectedChips, chip]);
    }
  };

  const saveCurrentDraft = () => {
    assessmentService.saveDraftLocally({
      description: symptomText.trim(),
      symptoms: selectedChips,
      bodyArea,
      severity,
      duration,
    });
  };

  const handleStartAssessment = async (e) => {
    if (e) e.preventDefault();
    const query = symptomText.trim();
    if (!query && selectedChips.length === 0) {
      setErrorMessage("Please describe your symptoms or select at least one symptom option.");
      return;
    }

    setErrorMessage("");

    // If user is not authenticated, save draft and prompt sign in
    if (!authService.isAuthenticated()) {
      saveCurrentDraft();
      setStage("auth_required");
      return;
    }

    setIsSubmitting(true);
    try {
      // Step 1: Create real assessment session on FastAPI backend
      const initRes = await assessmentService.createAssessment({
        description: query,
        // The backend creates structured records from symptom_data. Sending
        // chip names in both fields previously persisted every selected item twice.
        symptoms: [],
        symptom_data: selectedChips.map((name) => ({
          name,
          severity,
          body_location: bodyArea,
          duration,
        })),
      });

      // Clear draft upon successful creation
      assessmentService.clearDraftLocally();

      const newId = initRes.assessment_id;
      setAssessmentId(newId);

      // Step 2: Request adaptive follow-up questions
      const generatedQuestions = await assessmentService.getFollowUpQuestions(newId);
      if (generatedQuestions && generatedQuestions.length > 0) {
        setQuestions(generatedQuestions);
        setStage("questions");
      } else {
        // Direct analysis if no further follow-up required
        await executeAnalysis(newId);
      }
    } catch (err) {
      if (err.isUnauthorized) {
        // A token can be present in local storage after the backend session has
        // expired. Preserve the intake before sending the user through login so
        // that the checker resumes with the same symptoms afterward.
        saveCurrentDraft();
        setErrorMessage("Please sign in to complete a personalized clinical assessment.");
        setStage("auth_required");
      } else {
        setErrorMessage(err.message || "Failed to initialize symptom assessment. Please try again.");
        setStage("error");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAnswerChange = (questionId, value) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleSubmitAnswersAndAnalyze = async () => {
    if (!assessmentId) return;
    const unanswered = questions.filter((question) => !String(answers[question.id] || "").trim());
    if (unanswered.length) {
      setErrorMessage("Please answer each question or choose ‘Not sure’ to continue.");
      return;
    }
    setIsSubmitting(true);
    setErrorMessage("");
    try {
      // Submit each answered question to backend
      for (const [qId, ans] of Object.entries(answers)) {
        if (ans) {
          await assessmentService.submitAnswer(assessmentId, qId, ans);
        }
      }
      const nextQuestions = await assessmentService.getFollowUpQuestions(assessmentId);
      if (nextQuestions.length > 0) {
        setQuestions(nextQuestions);
        setAnswers({});
      } else {
        await executeAnalysis(assessmentId);
      }
    } catch (err) {
      console.error("[SymptomChecker] Analysis execution failed:", err);
      if (err.isUnauthorized) {
        saveCurrentDraft();
        setErrorMessage("Your session expired. Sign in again to continue the assessment.");
        setStage("auth_required");
      } else {
        setErrorMessage(err.message || "Triage analysis could not be completed.");
        setStage("error");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const executeAnalysis = async (targetId) => {
    setStage("analyzing");
    try {
      const res = await assessmentService.analyzeAssessment(targetId);
      setAnalysisResult(res);
      setStage("result");
    } catch (err) {
      console.error("[SymptomChecker] Analysis error:", err);
      if (err.isUnauthorized) {
        saveCurrentDraft();
        setErrorMessage("Your session expired. Sign in again to continue the assessment.");
        setStage("auth_required");
      } else {
        setErrorMessage(err.message || "Unable to complete safety triage analysis.");
        setStage("error");
      }
    }
  };

  const handleReset = () => {
    setStage("input");
    setAssessmentId(null);
    setQuestions([]);
    setAnswers({});
    setAnalysisResult(null);
    setErrorMessage("");
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Page Title & Medical Notice */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
            <Stethoscope className="w-7 h-7 text-emerald-700" />
            Symptom Checker
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Python-based safety triage and clear next-step health information.
          </p>
        </div>

        {!isAuthenticated && (
          <Link to="/login" className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200 hover:bg-emerald-100 transition-colors">
            <LogIn className="w-3.5 h-3.5" />
            Sign in to save assessment history
          </Link>
        )}
      </div>

      {/* Main Interactive Stage */}
      {stage === "input" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Form */}
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 sm:p-7 border border-slate-200/80 shadow-xs space-y-6">
            <form onSubmit={handleStartAssessment} className="space-y-5">
              {/* Narrative description */}
              <div>
                <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
                  What are you experiencing? <span className="text-emerald-700">*</span>
                </label>
                <textarea
                  rows={3}
                  value={symptomText}
                  onChange={(e) => setSymptomText(e.target.value)}
                  placeholder="Describe your symptoms in natural language (e.g. 'Dull temple headache since yesterday, feels worse when looking at computer screen')..."
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 text-xs sm:text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-700 focus:ring-1 focus:ring-emerald-700"
                />
              </div>

              {/* Symptom Chips */}
              <div className="space-y-2.5">
                <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Select related symptoms (optional)
                </label>
                <div className="flex flex-wrap gap-2">
                  {COMMON_SYMPTOM_OPTIONS.map((symptom) => {
                    const isSelected = selectedChips.includes(symptom);
                    return (
                      <button
                        key={symptom}
                        type="button"
                        onClick={() => handleToggleChip(symptom)}
                        className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer ${
                          isSelected
                            ? "bg-emerald-50 border-emerald-600 text-emerald-900 font-semibold shadow-2xs"
                            : "bg-white border-slate-200 text-slate-600 hover:border-slate-300 hover:bg-slate-50"
                        }`}
                      >
                        {symptom}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Body Area & Duration */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Primary Body Area
                  </label>
                  <select
                    value={bodyArea}
                    onChange={(e) => setBodyArea(e.target.value)}
                    className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 text-slate-800 bg-white focus:outline-none focus:border-emerald-700"
                  >
                    {BODY_AREAS.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Duration
                  </label>
                  <select
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}
                    className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 text-slate-800 bg-white focus:outline-none focus:border-emerald-700"
                  >
                    <option value="Less than 24 hours">Less than 24 hours</option>
                    <option value="1-3 days">1 to 3 days</option>
                    <option value="4-7 days">4 to 7 days</option>
                    <option value="More than a week">More than a week</option>
                  </select>
                </div>
              </div>

              {/* Severity Scale */}
              <div className="pt-2">
                <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-1.5">
                  <span>Discomfort Severity</span>
                  <span className="text-emerald-800 font-bold">{severity} / 10 ({severity >= 8 ? "Severe" : severity >= 4 ? "Moderate" : "Mild"})</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={severity}
                  onChange={(e) => setSeverity(Number(e.target.value))}
                  className="w-full accent-emerald-700 h-2 bg-slate-200 rounded-lg cursor-pointer"
                />
              </div>

              {errorMessage && (
                <div className="p-3 bg-red-50 text-red-700 text-xs rounded-xl border border-red-200 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0" />
                  <span>{errorMessage}</span>
                </div>
              )}

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full sm:w-auto px-6 py-2.5 bg-[#065f46] hover:bg-[#064e3b] text-white text-xs sm:text-sm font-semibold rounded-xl shadow-xs transition-colors cursor-pointer flex items-center justify-center gap-2 disabled:opacity-60"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Initializing Assessment...
                    </>
                  ) : (
                    <>
                      Check Symptoms
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Right Info Box */}
          <div className="space-y-4">
            <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-4">
              <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-800 flex items-center justify-center font-bold">
                <ShieldAlert className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-bold text-slate-900">
                Safety First Protocol
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Healix immediately checks for acute red-flag symptoms such as sudden severe chest pressure, slurred speech, or breathing distress.
              </p>
              <div className="p-3 bg-slate-50 rounded-xl text-[11px] text-slate-500 border border-slate-100 leading-relaxed">
                <strong>Notice:</strong> This application provides health information and triage guidance, not clinical medical diagnosis.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stage: Follow-up Questions */}
      {stage === "questions" && (
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200/80 shadow-xs space-y-6 max-w-2xl mx-auto">
          <div className="space-y-1">
            <span className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider bg-emerald-50 px-2.5 py-0.5 rounded-md border border-emerald-200">
              Step 2: Follow-up Questions
            </span>
            <h2 className="text-lg font-bold text-slate-900 pt-1">
              Please answer a few brief clarifying questions
            </h2>
            <p className="text-xs text-slate-500">
              These details help our deterministic triage engine refine clinical context.
            </p>
          </div>

          <div className="space-y-5 divide-y divide-slate-100">
            {questions.map((q, idx) => (
              <div key={q.id} className="pt-4 first:pt-0 space-y-2.5">
                <p className="text-xs sm:text-sm font-semibold text-slate-800">
                  {idx + 1}. {q.question}
                </p>
                {q.reasoning && (
                  <p className="text-[11px] leading-relaxed text-slate-500">
                    Why we ask: {q.reasoning}
                  </p>
                )}
                {q.options && q.options.length > 0 ? (
                  <div className="space-y-1.5">
                    {q.options.map((opt) => (
                      <label
                        key={opt}
                        className={`flex items-center gap-2.5 p-2.5 rounded-xl border text-xs cursor-pointer transition-colors ${
                          answers[q.id] === opt
                            ? "bg-emerald-50 border-emerald-600 text-emerald-950 font-medium"
                            : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50"
                        }`}
                      >
                        <input
                          type="radio"
                          name={`q_${q.id}`}
                          value={opt}
                          checked={answers[q.id] === opt}
                          onChange={() => handleAnswerChange(q.id, opt)}
                          className="accent-emerald-700"
                        />
                        <span>{opt}</span>
                      </label>
                    ))}
                  </div>
                ) : (
                  <input
                    type="text"
                    value={answers[q.id] || ""}
                    onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                    placeholder="Your answer..."
                    className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 text-slate-900"
                  />
                )}
              </div>
            ))}
          </div>

          {errorMessage && (
            <div className="p-3 bg-red-50 text-red-700 text-xs rounded-xl border border-red-200">
              {errorMessage}
            </div>
          )}

          <div className="flex items-center justify-between pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={handleReset}
              className="text-xs font-semibold text-slate-500 hover:text-slate-800 cursor-pointer"
            >
              Start Over
            </button>
            <button
              type="button"
              onClick={handleSubmitAnswersAndAnalyze}
              disabled={isSubmitting}
              className="px-6 py-2.5 bg-[#065f46] hover:bg-[#064e3b] text-white text-xs sm:text-sm font-semibold rounded-xl shadow-xs transition-colors cursor-pointer flex items-center gap-2 disabled:opacity-60"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  Save Answers & Continue
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Stage: Analyzing Animation */}
      {stage === "analyzing" && (
        <div className="bg-white rounded-2xl p-12 border border-slate-200/80 shadow-xs text-center space-y-4 max-w-lg mx-auto">
          <Loader2 className="w-10 h-10 text-emerald-700 animate-spin mx-auto" />
          <h3 className="text-base font-bold text-slate-900">
            Evaluating Symptoms & Safety Rules
          </h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Applying deterministic safety rules and preparing general next-step guidance...
          </p>
        </div>
      )}

      {/* Stage: Result */}
      {stage === "result" && analysisResult && (
        <div className="space-y-6 animate-in fade-in max-w-4xl mx-auto">
          {/* Urgency Indicator Card */}
          <UrgencyIndicator
            level={analysisResult.urgency_level}
            description={analysisResult.summary}
          />

          {/* Detailed Observations */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200/80 shadow-xs space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Retrieved Health Information
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Educational passages selected from Healix’s local health reference library. They are not diagnoses.
                </p>
              </div>

              {assessmentId && (
                <Link
                  to={`/assessment/${assessmentId}`}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-800 text-xs font-semibold hover:bg-emerald-100 border border-emerald-200 transition-colors"
                >
                  <FileText className="w-3.5 h-3.5" />
                  View Full Clinical Brief
                </Link>
              )}
            </div>

            {/* Possible explanations */}
            {analysisResult.possible_explanations && analysisResult.possible_explanations.length > 0 && (
              <div className="space-y-3">
                {analysisResult.possible_explanations.map((exp, idx) => (
                  <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-1.5 text-xs">
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-slate-900 text-sm">{exp.title}</h4>
                      {exp.match_level && (
                        <span className="px-2 py-0.5 bg-emerald-100 text-emerald-900 font-semibold rounded text-[10px]">
                          {exp.match_level}
                        </span>
                      )}
                    </div>
                    <p className="text-slate-600 leading-relaxed">{exp.description}</p>
                  </div>
                ))}
              </div>
            )}
            {(!analysisResult.possible_explanations || analysisResult.possible_explanations.length === 0) && (
              <p className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-xs text-slate-600">
                No relevant reference passage was available for these symptoms. Add the symptoms, how long they have been present, and how severe they feel. Safety guidance below still reflects the deterministic urgency review.
              </p>
            )}

            {/* Warning signs & Red flags */}
            {analysisResult.warning_signs && analysisResult.warning_signs.length > 0 && (
              <div className="p-4 bg-amber-50/80 rounded-2xl border border-amber-200/80 space-y-2 text-xs">
                <h4 className="font-bold text-amber-950 uppercase tracking-wider flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  Warning Signs to Monitor
                </h4>
                <ul className="space-y-1 text-slate-800 list-disc list-inside">
                  {analysisResult.warning_signs.map((sign, idx) => (
                    <li key={idx}>{sign}</li>
                  ))}
                </ul>
              </div>
            )}

            {analysisResult.reasoning_trace?.length > 0 && (
              <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-4 space-y-2 text-xs">
                <h4 className="font-bold text-amber-950">Why this was flagged</h4>
                <ul className="space-y-2 text-slate-700">
                  {analysisResult.reasoning_trace.map((item, idx) => (
                    <li key={`${item.rule_id}-${idx}`}>
                      <span className="font-semibold">{item.rule_id}:</span> {item.conclusion}
                      <span className="block text-[11px] text-slate-500">
                        Matched: {item.matched_facts.map((fact) => String(fact.value).replaceAll("_", " ")).join(", ")}. {item.source} ({item.reference})
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {analysisResult.condition_ranking?.length > 0 && (
              <div className="rounded-xl border border-emerald-200 bg-emerald-50/50 p-4 space-y-3 text-xs">
                <h4 className="font-bold text-emerald-950">Dataset pattern matches</h4>
                <p className="text-slate-600">These are matches to synthetic DDXPlus examples, not diagnoses. The safety review above always controls urgency.</p>
                <ol className="space-y-2">
                  {analysisResult.condition_ranking.map((item, idx) => (
                    <li key={`${item.condition}-${idx}`} className="flex items-center justify-between gap-3 rounded-lg bg-white/80 p-2.5">
                      <span className="font-semibold text-slate-800">{idx + 1}. {item.condition}</span>
                      <span className="shrink-0 text-emerald-800">{Math.round(item.probability * 100)}% dataset match · {item.confidence_band}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}

            {/* General Self-Care Guidance */}
            {analysisResult.general_guidance && analysisResult.general_guidance.length > 0 && (
              <div className="space-y-2 text-xs">
                <h4 className="font-bold text-slate-900 uppercase tracking-wider">
                  Self-Care Next Steps
                </h4>
                <ul className="space-y-1.5 text-slate-700 list-disc list-inside">
                  {analysisResult.general_guidance.map((g, idx) => (
                    <li key={idx}>{g}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Disclaimer */}
            <div className="p-3 bg-slate-50 rounded-xl text-[11px] text-slate-500 leading-relaxed border border-slate-200">
              <strong>Medical Disclaimer:</strong> {analysisResult.disclaimer || "Healix is an informational triage tool, not a doctor. Please consult a licensed physician."}
            </div>

            {/* Action Bar */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-slate-100">
              <button
                type="button"
                onClick={handleReset}
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 cursor-pointer"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                New Symptom Check
              </button>

              {assessmentId && (
                <Link to={`/assessment/${assessmentId}`}>
                  <Button variant="primary" size="sm" icon={ChevronRight} iconPosition="right">
                    Open Patient Summary Report
                  </Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Stage: Auth Required */}
      {stage === "auth_required" && (
        <div className="bg-white rounded-2xl p-8 border border-slate-200 text-center space-y-4 max-w-lg mx-auto shadow-sm">
          <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-700 flex items-center justify-center mx-auto">
            <LogIn className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">
            Sign In to Process Assessment
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Your symptom notes and selections have been saved. Please sign in or register to securely process your clinical assessment and view personalized guidance.
          </p>
          <div className="flex items-center justify-center gap-3 pt-2">
            <button
              type="button"
              onClick={() => setStage("input")}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl transition-colors cursor-pointer"
            >
              Back to Draft
            </button>
            <Link to="/login?redirect=/symptoms">
              <Button variant="primary" size="sm" icon={LogIn} iconPosition="left">
                Sign In to Continue
              </Button>
            </Link>
          </div>
        </div>
      )}

      {/* Stage: Error */}
      {stage === "error" && (
        <div className="bg-white rounded-2xl p-8 border border-slate-200 text-center space-y-4 max-w-lg mx-auto">
          <div className="w-12 h-12 rounded-full bg-red-50 text-red-600 flex items-center justify-center mx-auto">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">
            Assessment Request Error
          </h3>
          <p className="text-xs text-slate-600">
            {errorMessage || "An unexpected error occurred while communicating with the health assessment engine."}
          </p>
          <div className="flex items-center justify-center gap-3 pt-2">
            <button
              onClick={handleReset}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl transition-colors cursor-pointer"
            >
              Start Over
            </button>
            <button
              onClick={handleStartAssessment}
              className="px-4 py-2 bg-[#065f46] hover:bg-[#064e3b] text-white text-xs font-semibold rounded-xl transition-colors cursor-pointer"
            >
              Retry Check
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
