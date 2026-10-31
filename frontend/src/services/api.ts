import { 
  SymptomCatalogResponse, 
  ParseSymptomsResponse, 
  AdaptiveQuestionResponse,
  AssessmentDetail,
  AssessmentSummary
} from '../types';

const API_BASE = '/api/v1';

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('healix_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
}

export const api = {
  // Auth
  async login(email: string, password: string) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Login failed');
    }
    return res.json();
  },

  async register(data: { email: string; password: string; full_name: string; date_of_birth?: string; biological_sex?: string }) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...data, clinical_consent_acknowledged: true })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Registration failed');
    }
    return res.json();
  },

  async getMe() {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch user');
    return res.json();
  },

  // Symptom Catalog & NLP Parsing
  async getSymptomCatalog(): Promise<SymptomCatalogResponse> {
    const res = await fetch(`${API_BASE}/symptoms/catalog`);
    if (!res.ok) throw new Error('Failed to load symptom catalogue');
    return res.json();
  },

  async parseSymptoms(freeText: string): Promise<ParseSymptomsResponse> {
    const res = await fetch(`${API_BASE}/symptoms/parse`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ free_text: freeText })
    });
    if (!res.ok) throw new Error('Failed to analyze symptom description');
    return res.json();
  },

  // Assessments
  async startAssessment(data: {
    primary_complaint: string;
    symptom_ids?: string[];
    location_ids?: string[];
    duration?: string;
    severity?: string;
    character?: string;
  }): Promise<{ assessment_id: string; status: string; current_step: string; next_action: string }> {
    const res = await fetch(`${API_BASE}/assessments/start`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Failed to start assessment');
    }
    return res.json();
  },

  async getNextQuestion(assessment_id: string): Promise<AdaptiveQuestionResponse> {
    const res = await fetch(`${API_BASE}/assessments/${assessment_id}/next-question`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to retrieve next question');
    return res.json();
  },

  async submitAnswer(assessment_id: string, data: {
    question_id: string;
    fact_name: string;
    value: string;
    raw_response?: any;
  }) {
    const res = await fetch(`${API_BASE}/assessments/${assessment_id}/answer`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('Failed to record answer');
    return res.json();
  },

  async completeAssessment(assessment_id: string) {
    const res = await fetch(`${API_BASE}/assessments/${assessment_id}/complete`, {
      method: 'POST',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to complete assessment');
    return res.json();
  },

  async createAssessment(primary_complaint: string) {
    return this.startAssessment({ primary_complaint });
  },

  async evaluateAssessment(assessment_id: string, answers: Array<{ fact_name: string; value: string; raw_response?: any }>) {
    const res = await fetch(`${API_BASE}/assessments/${assessment_id}/evaluate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ answers })
    });
    if (!res.ok) throw new Error('Failed to evaluate assessment');
    return res.json();
  },

  async listAssessments(): Promise<AssessmentSummary[]> {
    const res = await fetch(`${API_BASE}/assessments`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to list assessments');
    return res.json();
  },

  async getAssessment(assessment_id: string): Promise<AssessmentDetail> {
    const res = await fetch(`${API_BASE}/assessments/${assessment_id}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch assessment');
    return res.json();
  },

  async getAssessmentGraph(assessment_id: string) {
    const res = await fetch(`${API_BASE}/assessments/${assessment_id}/graph`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch assessment graph');
    return res.json();
  },

  async generateReport(assessment_id: string) {
    const res = await fetch(`${API_BASE}/assessments/${assessment_id}/reports`, {
      method: 'POST',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to generate report');
    return res.json();
  },

  // Timeline
  async getTimeline() {
    const res = await fetch(`${API_BASE}/timeline`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch timeline');
    return res.json();
  },

  async createObservation(data: { title: string; notes?: string; severity: string; assessment_id?: string }) {
    const res = await fetch(`${API_BASE}/timeline`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('Failed to create observation');
    return res.json();
  },

  // Reports
  async listReports() {
    const res = await fetch(`${API_BASE}/reports`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to list reports');
    return res.json();
  },

  async getReport(report_id: string) {
    const res = await fetch(`${API_BASE}/reports/${report_id}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch report');
    return res.json();
  },

  // Rules
  async listRules() {
    const res = await fetch(`${API_BASE}/rules`);
    if (!res.ok) throw new Error('Failed to fetch rules');
    return res.json();
  }
};
