import { mockAssessments } from "../data/mockData";
import { apiRequest } from "./apiClient";

export const assessmentService = {
  // Analyze symptom assessment
  async analyzeAssessment(payload) {
    const apiRes = await apiRequest("/assessment/result", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    if (apiRes) return apiRes;

    // Simulate realistic AI + RAG triage generation
    await new Promise((resolve) => setTimeout(resolve, 2200));

    const {
      description = "",
      structuredSymptoms = [],
      bodyArea = "head",
      duration = "Few days",
      severity = "Mild",
      frequency = "Comes and goes",
      answers = {},
      hasRedFlags = false,
    } = payload;

    const symptomLabels = structuredSymptoms.map((s) => (typeof s === "string" ? s : s.label));
    if (symptomLabels.length === 0 && description) {
      symptomLabels.push("Unspecified Symptom");
    }

    // Determine urgency level
    let urgencyLevel = "routine";
    let urgencyTitle = "Routine Care Recommended";
    let urgencyDescription =
      "Your reported symptoms align with commonly managed conditions that can be evaluated at a routine clinic visit. Continue monitoring at home.";

    if (hasRedFlags || severity === "Severe") {
      urgencyLevel = "urgent";
      urgencyTitle = "Prompt Medical Evaluation Advised";
      urgencyDescription =
        "Given the reported severity or notable symptom combinations, an in-person clinical assessment by a doctor or urgent care center within 12–24 hours is advised.";
    }

    // Dynamic possible explanations grounded in clinical literature
    const possibleExplanations = [];
    const textJoined = `${description} ${symptomLabels.join(" ")}`.toLowerCase();

    if (textJoined.includes("head") || bodyArea === "head") {
      possibleExplanations.push({
        title: "Tension-type Cephalea / Headache",
        matchLevel: "High Relevance",
        description:
          "Diffuse, bilateral mild-to-moderate band-like discomfort frequently triggered by physical or emotional stress, eye fatigue, dehydration, or prolonged neck muscle contraction.",
        matchedSymptoms: symptomLabels.filter((s) => /head|fatigue|neck/i.test(s)),
        clinicalInsight: "Characteristically non-pulsatile and without significant photophobia.",
      });
      possibleExplanations.push({
        title: "Sleep Disruption & Hydration Deficit",
        matchLevel: "Moderate Relevance",
        description:
          "Mild subclinical fluid deficit combined with irregular circadian rest cycles, which can manifest as dull cranial heaviness and reduced alertness.",
        matchedSymptoms: symptomLabels.filter((s) => /fatigue|tired/i.test(s)),
        clinicalInsight: "Generally responds well to restorative sleep and oral rehydration.",
      });
      possibleExplanations.push({
        title: "Cervicogenic Strain / Postural Discomfort",
        matchLevel: "Possible Factor",
        description:
          "Referred cranial sensation arising from chronic tension in the trapezius or suboccipital musculature after prolonged workstation use.",
        matchedSymptoms: ["Neck stiffness", "Headache"],
        clinicalInsight: "Often alleviated by ergonomic adjustments and gentle cervical mobility stretches.",
      });
    } else if (textJoined.includes("chest") || bodyArea === "chest") {
      possibleExplanations.push({
        title: "Musculoskeletal Chest Wall Strain (Costochondritis)",
        matchLevel: "Common Consideration",
        description:
          "Localized discomfort in the cartilage connecting the ribs to the breastbone. Frequently tender to direct palpation and aggravated by twisting or deep inhalation.",
        matchedSymptoms: ["Chest discomfort"],
        clinicalInsight: "Must always be differentiated from cardiac etiology by an in-person physician.",
      });
      possibleExplanations.push({
        title: "Gastroesophageal Reflux Discomfort",
        matchLevel: "Moderate Relevance",
        description:
          "Gastric acid irritation of the esophageal lining producing substernal sensation, often worse after meals or when lying supine.",
        matchedSymptoms: ["Chest discomfort", "Stomach pain"],
        clinicalInsight: "Commonly associated with an acidic or sour taste in the mouth.",
      });
    } else if (textJoined.includes("cough") || textJoined.includes("throat") || bodyArea === "throat") {
      possibleExplanations.push({
        title: "Upper Respiratory Viral Irritation",
        matchLevel: "High Relevance",
        description:
          "Transient inflammation of the pharyngeal and tracheal passages following seasonal viral contact, typically self-limiting in healthy adults.",
        matchedSymptoms: symptomLabels.filter((s) => /cough|throat|fever/i.test(s)),
        clinicalInsight: "Expected duration is typically 7 to 10 days.",
      });
    } else {
      possibleExplanations.push({
        title: "Transient Functional Fatigue & Physical Strain",
        matchLevel: "High Relevance",
        description:
          "A non-specific constellation of mild physical symptoms secondary to cumulative fatigue, mild physiological stressors, or recovery from exertion.",
        matchedSymptoms: symptomLabels,
        clinicalInsight: "Monitoring symptom trajectory over the next 48 hours is standard practice.",
      });
    }

    const newAssessment = {
      id: `asm_${Date.now()}`,
      date: "Today, Oct 2, 2026",
      timestamp: new Date().toISOString(),
      symptoms: symptomLabels.length ? symptomLabels : ["General discomfort"],
      primarySymptom: symptomLabels.slice(0, 2).join(" & ") || "Reported symptoms",
      bodyArea,
      duration,
      severity,
      frequency,
      urgencyLevel,
      urgencyTitle,
      urgencyDescription,
      status: "Completed",
      possibleExplanations,
      selfCareGuidance: [
        "Prioritize scheduled rest in a quiet, temperate environment.",
        "Ensure consistent hydration (water and clear broths, minimizing excessive caffeine).",
        "Keep a concise log of symptom timing, triggers, and changes.",
        "Refrain from unprescribed medications or strenuous physical workouts until fully resolved.",
      ],
      warningSignsToWatch: [
        "Sudden, unbearable progression in pain or severe new symptoms",
        "Onset of shortness of breath, chest pressure, or lightheadedness",
        "Persistent high fever exceeding 38.5°C (101.3°F)",
        "New neurological signs (sudden numbness, weakness, confusion, or speech changes)",
      ],
      sources: [
        {
          name: "Mayo Clinic",
          topic: "Clinical Decision & Symptom Assessment",
          url: "https://www.mayoclinic.org",
          retrievalDate: "October 2026",
          authority: "Evidence-Based Clinical Summaries",
        },
        {
          name: "World Health Organization (WHO)",
          topic: "Triage Principles & Primary Care Standards",
          url: "https://www.who.int",
          retrievalDate: "2026",
          authority: "WHO Primary Healthcare Technical Series",
        },
        {
          name: "National Health Service (NHS UK)",
          topic: "Health Information & Self-Management Guidance",
          url: "https://www.nhs.uk",
          retrievalDate: "2026",
          authority: "NHS Clinical Guidelines Framework",
        },
      ],
    };

    // Store in history
    this.saveToStorage(newAssessment);
    return newAssessment;
  },

  getAllAssessments() {
    try {
      const stored = localStorage.getItem("healix_assessments");
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.error("Storage error:", e);
    }
    // Default to mock data
    return mockAssessments;
  },

  getAssessmentById(id) {
    const list = this.getAllAssessments();
    return list.find((a) => a.id === id) || mockAssessments[0];
  },

  saveToStorage(assessment) {
    const list = this.getAllAssessments();
    const updated = [assessment, ...list.filter((a) => a.id !== assessment.id)];
    localStorage.setItem("healix_assessments", JSON.stringify(updated));
    return updated;
  },
};
