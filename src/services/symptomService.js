import { commonSymptomChips, bodyAreas } from "../data/mockData";

/**
 * Service for symptom metadata and reference options.
 * Note: Clinical safety, red-flag detection, and urgency triage are strictly performed
 * server-side by the deterministic Python triage engine.
 */
export const symptomService = {
  getCommonSymptoms() {
    return commonSymptomChips;
  },

  getBodyAreas() {
    return bodyAreas;
  },
};
