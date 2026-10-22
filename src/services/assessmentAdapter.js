/**
 * Assessment Adapter.
 * Maps FastAPI backend snake_case schemas to UI view models, ensuring consistent
 * property naming, urgency levels, dates, and clear separation of real vs demo data.
 */

export function mapUrgencyLevel(level) {
  if (!level) return "routine";
  const lower = String(level).toLowerCase();
  if (lower === "emergency") return "emergency";
  if (lower === "urgent") return "urgent";
  if (lower === "unknown") return "unknown";
  return "routine";
}

export function getUrgencyMetadata(level) {
  const normalized = mapUrgencyLevel(level);
  switch (normalized) {
    case "emergency":
      return {
        level: "emergency",
        title: "Immediate Emergency Care Required",
        description:
          "Reported symptoms may indicate an acute medical emergency. Please contact your local emergency services or proceed to the nearest emergency room immediately.",
      };
    case "urgent":
      return {
        level: "urgent",
        title: "Prompt Medical Evaluation Advised",
        description:
          "Your reported symptoms warrant an in-person clinical assessment by a physician or urgent care clinic within 12–24 hours.",
      };
    case "unknown":
      return {
        level: "unknown",
        title: "Further Clarification Needed",
        description:
          "Healix could not identify specific medical patterns from the provided text. Please provide more detail or consult a healthcare professional.",
      };
    case "routine":
    default:
      return {
        level: "routine",
        title: "Routine Care Recommended",
        description:
          "Your symptoms appear consistent with non-emergent routine conditions. Monitor symptoms and schedule a routine checkup if they persist.",
      };
  }
}

export function formatDate(dateString) {
  if (!dateString) return "Recently";
  try {
    const d = new Date(dateString);
    if (isNaN(d.getTime())) return "Recently";
    return d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch {
    return "Recently";
  }
}

/**
 * Transforms an assessment object from GET /api/v1/assessments/{id}
 * into the complete UI view model expected by AssessmentResultPage & ReportPage.
 */
export function adaptAssessmentToViewModel(assessment) {
  if (!assessment) return null;

  const urgencyMeta = getUrgencyMetadata(assessment.urgency_level);
  const report = assessment.report || {};

  const symptomsList = (assessment.symptoms || []).map((s) => (typeof s === "string" ? s : s.name));
  const primarySymptom = symptomsList.slice(0, 2).join(" & ") || assessment.user_description || "Health Assessment";

  const rawExplanations = report.possible_explanations || [];
  const possibleExplanations = rawExplanations.map((item) => ({
    title: item.title || "Health Observation",
    matchLevel: item.match_level || item.matchLevel || "Clinical Consideration",
    description: item.description || "",
    clinicalInsight: item.clinical_note || item.clinicalInsight || item.reasoning || "",
    matchedSymptoms: item.relevant_symptoms || item.matchedSymptoms || [],
  }));

  const rawSources = report.sources || [];
  const sources = rawSources.map((src) => ({
    name: src.organization || src.name || src.source || "Source",
    topic: src.topic || src.title || "",
    url: src.url || "",
    authority: src.organization || src.authority || "",
  }));

  const followUpSummary = (assessment.follow_up_questions || []).flatMap((q) =>
    (q.answers || []).map((a) => ({
      question: q.question,
      answer: a.answer,
    }))
  );

  return {
    id: assessment.id,
    date: formatDate(assessment.created_at),
    timestamp: assessment.created_at,
    status: assessment.status === "COMPLETED" ? "Completed" : assessment.status,
    symptoms: symptomsList.length ? symptomsList : ["Reported symptoms"],
    primarySymptom,
    userDescription: assessment.user_description || "",
    urgencyLevel: urgencyMeta.level,
    urgencyTitle: urgencyMeta.title,
    urgencyDescription: urgencyMeta.description,
    summary: report.summary || assessment.summary || urgencyMeta.description,
    possibleExplanations,
    selfCareGuidance: report.general_guidance || [
      "Prioritize scheduled rest in a quiet, temperate environment.",
      "Ensure consistent oral hydration with water and light electrolytes.",
      "Monitor symptom trajectory and keep a concise log of changes.",
    ],
    warningSignsToWatch: report.warning_signs || [
      "Sudden, unbearable progression in symptom severity",
      "Onset of shortness of breath, chest pressure, or lightheadedness",
      "Persistent high fever exceeding 38.5°C (101.3°F)",
    ],
    sources,
    reasoningTrace: report.reasoning_trace || [],
    conditionRanking: report.condition_ranking || [],
    followUpSummary,
    isRealData: true,
  };
}
