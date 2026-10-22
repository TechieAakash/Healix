import { apiRequest } from "./apiClient";
import { adaptAssessmentToViewModel } from "./assessmentAdapter";
import { mockAssessments } from "../data/mockData";

export const assessmentService = {
  /**
   * Initializes a real assessment on the FastAPI backend.
   * @param {Object} params
   * @param {string} params.description - Patient symptom description
   * @param {Array<string>} params.symptoms - List of symptom names or symptom IDs
   * @param {Array<Object>} [params.symptom_data] - Detailed symptom metadata (severity, location, duration)
   */
  async createAssessment({ description = "", symptoms = [], symptom_data = null }) {
    const payload = {
      description,
      symptoms,
      ...(symptom_data ? { symptom_data } : {}),
    };
    const res = await apiRequest("/assessments", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    return res; // { assessment_id, status }
  },

  /**
   * Generates or fetches context-aware follow-up triage questions from backend.
   */
  async getFollowUpQuestions(assessmentId) {
    const res = await apiRequest(`/assessments/${assessmentId}/questions`, {
      method: "POST",
    });
    return res.questions || [];
  },

  /**
   * Submits an answer to a specific follow-up question.
   */
  async submitAnswer(assessmentId, questionId, answer) {
    const res = await apiRequest(`/assessments/${assessmentId}/answers`, {
      method: "POST",
      body: JSON.stringify({
        question_id: questionId,
        answer: String(answer),
      }),
    });
    return res;
  },

  /**
   * Executes deterministic safety triage & RAG analysis on the backend.
   */
  async analyzeAssessment(assessmentId) {
    const res = await apiRequest(`/assessments/${assessmentId}/analyze`, {
      method: "POST",
    });
    return res;
  },

  /**
   * Retrieves full details, questions, answers, and clinical report for an assessment.
   */
  async getAssessmentById(id) {
    try {
      const raw = await apiRequest(`/assessments/${id}`);
      if (raw) {
        return adaptAssessmentToViewModel(raw);
      }
    } catch (err) {
      // If it's a known mock ID (e.g., asm_101), return the mock template
      const mock = mockAssessments.find((a) => a.id === id);
      if (mock) {
        return { ...mock, isDemo: true };
      }
      throw err;
    }
    return null;
  },

  /**
   * Lists patient assessments timeline.
   */
  async getAllAssessments(page = 1, pageSize = 20) {
    try {
      const res = await apiRequest(`/assessments?page=${page}&page_size=${pageSize}`);
      if (res && res.items) {
        return res.items.map((item) => adaptAssessmentToViewModel(item));
      }
    } catch (err) {
      // In offline/unauthenticated mock mode, fallback to mock data
      console.warn("[assessmentService] Backend assessments unavailable, using local mock data:", err.message);
      return mockAssessments.map((a) => ({ ...a, isDemo: true }));
    }
    return [];
  },

  /**
   * Saves local offline assessment (used for unauthenticated drafts).
   */
  saveDraftLocally(draft) {
    localStorage.setItem("healix_draft_assessment", JSON.stringify(draft));
  },

  getDraftLocally() {
    try {
      const stored = localStorage.getItem("healix_draft_assessment");
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  },

  clearDraftLocally() {
    localStorage.removeItem("healix_draft_assessment");
  },
};
