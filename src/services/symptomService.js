import { commonSymptomChips, bodyAreas, redFlagTriggers } from "../data/mockData";
import { apiRequest } from "./apiClient";

export const symptomService = {
  async getCommonSymptoms() {
    const res = await apiRequest("/symptoms/common");
    return res || commonSymptomChips;
  },

  async getBodyAreas() {
    const res = await apiRequest("/symptoms/body-areas");
    return res || bodyAreas;
  },

  // Critical safety triage check
  checkForRedFlags(text = "", symptoms = []) {
    const lowerText = text.toLowerCase();
    const symptomsJoined = symptoms.map((s) => (typeof s === "string" ? s : s.label || "").toLowerCase()).join(" ");
    const combined = `${lowerText} ${symptomsJoined}`;

    const matchedTriggers = redFlagTriggers.filter((trigger) => combined.includes(trigger.toLowerCase()));

    // Also check for specific high-risk combinations
    const hasChestPain = combined.includes("chest") && (combined.includes("pain") || combined.includes("pressure") || combined.includes("tightness"));
    const hasBreathIssue = combined.includes("shortness of breath") || combined.includes("difficulty breathing");
    const hasNeuroIssue = combined.includes("droop") || combined.includes("slurred") || combined.includes("numbness on one side") || combined.includes("worst headache of life");

    const isEmergency = matchedTriggers.length > 0 || (hasChestPain && hasBreathIssue) || hasNeuroIssue;

    return {
      isEmergency,
      matchedTriggers,
      reason: isEmergency
        ? "Potential high-risk clinical symptoms detected (e.g., cardiopulmonary or acute neurological warning signs) which necessitate immediate medical evaluation."
        : null,
    };
  },

  // Generates smart contextual follow-up questions based on selected body area & symptoms
  async generateFollowUpQuestions(symptomData) {
    const res = await apiRequest("/assessment/follow-up", {
      method: "POST",
      body: JSON.stringify(symptomData),
    });

    if (res && res.questions) return res.questions;

    // Smart contextual fallback generator
    const { primarySymptoms = [], bodyArea = "head" } = symptomData;
    const sStr = primarySymptoms.map(s => typeof s === 'string' ? s : s.label).join(", ").toLowerCase();

    const questions = [];

    if (sStr.includes("head") || bodyArea === "head") {
      questions.push({
        id: "q1",
        question: "Is this headache sudden and described as the most severe headache you've ever experienced ('thunderclap')?",
        hint: "Sudden explosive onset requires immediate emergency evaluation.",
        isCriticalSafety: true
      });
      questions.push({
        id: "q2",
        question: "Have you noticed any visual changes like flashing lights, blind spots, or double vision?",
        hint: "Visual disturbances help differentiate aura migraines from tension headaches."
      });
      questions.push({
        id: "q3",
        question: "Is there marked neck stiffness preventing your chin from touching your chest?",
        hint: "Neck rigidity can indicate meningeal irritation.",
        isCriticalSafety: true
      });
      questions.push({
        id: "q4",
        question: "Have you been experiencing prolonged screen time or poor posture over the past 24–48 hours?",
        hint: "Helps assess tension and ergonomic cervical strain."
      });
    } else if (sStr.includes("chest") || bodyArea === "chest") {
      questions.push({
        id: "q1",
        question: "Does the chest discomfort radiate to your left arm, jaw, neck, or back?",
        hint: "Classic cardiac radiation patterns require urgent evaluation.",
        isCriticalSafety: true
      });
      questions.push({
        id: "q2",
        question: "Are you feeling shortness of breath, unexplained cold sweats, or lightheadedness?",
        hint: "Systemic cardiopulmonary signs.",
        isCriticalSafety: true
      });
      questions.push({
        id: "q3",
        question: "Does the pain get sharper when you take a deep breath or cough?",
        hint: "Pleuro-musculoskeletal indicators."
      });
    } else if (sStr.includes("abdomen") || sStr.includes("stomach") || bodyArea === "abdomen") {
      questions.push({
        id: "q1",
        question: "Is the abdominal pain sharp, rigid to the touch, or localized sharply in the lower right area?",
        hint: "Can signal acute appendicitis or peritoneal irritation.",
        isCriticalSafety: true
      });
      questions.push({
        id: "q2",
        question: "Have you experienced repeated vomiting, inability to keep liquids down, or black stools?",
        hint: "Helps evaluate dehydration risk and gastrointestinal bleeding.",
        isCriticalSafety: true
      });
      questions.push({
        id: "q3",
        question: "Did the symptoms begin following a specific meal, travel, or change in diet?",
        hint: "Helps assess foodborne or digestive flare factors."
      });
    } else {
      // General fallbacks
      questions.push({
        id: "q1",
        question: "Have you experienced any shortness of breath or sudden difficulty breathing?",
        hint: "Key vital symptom check.",
        isCriticalSafety: true
      });
      questions.push({
        id: "q2",
        question: "Has your body temperature been measured above 38.5°C (101.3°F)?",
        hint: "Signals systemic inflammatory or infectious response."
      });
      questions.push({
        id: "q3",
        question: "Are your symptoms progressively worsening, or have they stabilized?",
        hint: "Helps determine trajectory and care urgency."
      });
      questions.push({
        id: "q4",
        question: "Have you had difficulty staying hydrated or keeping normal meals down?",
        hint: "Assesses hydration and metabolic resilience."
      });
    }

    return questions;
  }
};
